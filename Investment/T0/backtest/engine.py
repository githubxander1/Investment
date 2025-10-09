import pandas as pd
import numpy as np
from datetime import datetime
from typing import List, Dict, Tuple
import matplotlib.pyplot as plt
import os
from .models import Signal, SignalType, Trade, Position, BacktestResult
from .config import RESULTS_DIR
from .strategies import (
    detect_resistance_support_signals,
    detect_extended_signals,
    detect_volume_price_signals_func
)
from .data_loader import get_prev_close
from indicators.extended_indicators import get_prev_close as get_prev_close_extended

class BacktestEngine:
    """T0回测引擎"""
    
    def __init__(self, initial_capital: float = 100000, trade_amount: int = 100, 
                 commission_rate: float = 0.0003, slippage: float = 0.001):
        """
        初始化回测引擎
        
        Args:
            initial_capital: 初始资金
            trade_amount: 每次交易数量
            commission_rate: 手续费率
            slippage: 滑点
        """
        self.initial_capital = initial_capital
        self.trade_amount = trade_amount
        self.commission_rate = commission_rate
        self.slippage = slippage
        self.results = []
    
    def run_backtest(self, symbol: str, indicator: str, data: pd.DataFrame, 
                     start_date: str, end_date: str) -> BacktestResult:
        """
        运行单个股票的回测
        
        Args:
            symbol: 股票代码
            indicator: 指标类型 ('resistance_support', 'extended', 'volume_price')
            data: 分时数据
            start_date: 开始日期
            end_date: 结束日期
            
        Returns:
            BacktestResult: 回测结果
        """
        # 获取前收盘价
        prev_close = get_prev_close(symbol, start_date)
        if prev_close is None:
            prev_close = data['开盘'].iloc[0] if not data.empty else 0
        
        # 根据指标类型检测信号
        if indicator == 'resistance_support':
            signals = detect_resistance_support_signals(data, prev_close)
        elif indicator == 'extended':
            # 获取日线数据用于扩展指标
            _, daily_data = get_prev_close_extended(symbol, start_date)
            signals = detect_extended_signals(data, prev_close, daily_data)
        elif indicator == 'volume_price':
            signals = detect_volume_price_signals_func(data, prev_close)
        else:
            raise ValueError(f"不支持的指标类型: {indicator}")
        
        # 执行交易
        trades, final_capital = self._execute_trades(data, signals)
        
        # 计算回测指标
        total_return, win_rate, max_drawdown, sharpe_ratio = self._calculate_metrics(trades, data)
        
        result = BacktestResult(
            symbol=symbol,
            indicator=indicator,
            initial_capital=self.initial_capital,
            final_capital=final_capital,
            total_return=total_return,
            total_trades=len(trades),
            win_rate=win_rate,
            max_drawdown=max_drawdown,
            sharpe_ratio=sharpe_ratio,
            trades=trades,
            signals=signals
        )
        
        self.results.append(result)
        return result
    
    def _execute_trades(self, data: pd.DataFrame, signals: List[Signal]) -> Tuple[List[Trade], float]:
        """
        执行交易
        
        Args:
            data: 分时数据
            signals: 信号列表
            
        Returns:
            Tuple[List[Trade], float]: 交易列表和最终资金
        """
        capital = self.initial_capital
        position = Position(quantity=0, avg_price=0, entry_time=None)
        trades = []
        
        # 按时间排序信号
        signals = sorted(signals, key=lambda x: x.timestamp)
        
        for signal in signals:
            if signal.timestamp not in data.index:
                continue
                
            price = data.loc[signal.timestamp, '收盘']
            if pd.isna(price):
                continue
                
            # 考虑滑点
            adjusted_price = price * (1 + self.slippage) if signal.signal_type == SignalType.BUY else price * (1 - self.slippage)
            
            if signal.signal_type == SignalType.BUY:
                # 买入
                cost = adjusted_price * self.trade_amount
                commission = cost * self.commission_rate
                total_cost = cost + commission
                
                if capital >= total_cost:
                    # 更新持仓
                    total_quantity = position.quantity + self.trade_amount
                    position.avg_price = (position.quantity * position.avg_price + cost) / total_quantity if total_quantity > 0 else adjusted_price
                    position.quantity = total_quantity
                    position.entry_time = signal.timestamp
                    
                    # 记录交易
                    trades.append(Trade(
                        timestamp=signal.timestamp,
                        trade_type=SignalType.BUY,
                        price=adjusted_price,
                        quantity=self.trade_amount,
                        commission=commission,
                        indicator=signal.indicator
                    ))
                    
                    # 更新资金
                    capital -= total_cost
                    
            elif signal.signal_type == SignalType.SELL and position.quantity > 0:
                # 卖出
                revenue = adjusted_price * min(self.trade_amount, position.quantity)
                commission = revenue * self.commission_rate
                total_revenue = revenue - commission
                
                # 记录交易
                trades.append(Trade(
                    timestamp=signal.timestamp,
                    trade_type=SignalType.SELL,
                    price=adjusted_price,
                    quantity=min(self.trade_amount, position.quantity),
                    commission=commission,
                    indicator=signal.indicator
                ))
                
                # 更新持仓
                position.quantity -= min(self.trade_amount, position.quantity)
                if position.quantity == 0:
                    position.avg_price = 0
                    position.entry_time = None
                
                # 更新资金
                capital += total_revenue
        
        return trades, capital
    
    def _calculate_metrics(self, trades: List[Trade], data: pd.DataFrame) -> Tuple[float, float, float, float]:
        """
        计算回测指标
        
        Args:
            trades: 交易列表
            data: 分时数据
            
        Returns:
            Tuple[float, float, float, float]: 总收益率、胜率、最大回撤、夏普比率
        """
        if len(trades) == 0:
            return 0.0, 0.0, 0.0, 0.0
        
        # 计算总收益率
        total_return = 0.0
        winning_trades = 0
        
        # 计算每笔交易的收益
        for i in range(0, len(trades), 2):
            if i + 1 < len(trades) and trades[i].trade_type == SignalType.BUY and trades[i+1].trade_type == SignalType.SELL:
                buy_trade = trades[i]
                sell_trade = trades[i+1]
                
                profit = (sell_trade.price - buy_trade.price) * buy_trade.quantity - buy_trade.commission - sell_trade.commission
                total_return += profit
                
                if profit > 0:
                    winning_trades += 1
        
        # 计算胜率
        win_rate = winning_trades / (len(trades) // 2) if len(trades) >= 2 else 0.0
        
        # 简化的最大回撤和夏普比率计算
        max_drawdown = 0.0
        sharpe_ratio = 0.0
        
        return total_return, win_rate, max_drawdown, sharpe_ratio
    
    def save_results(self, filename: str = None):
        """
        保存回测结果
        
        Args:
            filename: 文件名
        """
        if not filename:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"backtest_results_{timestamp}.csv"
        
        filepath = os.path.join(RESULTS_DIR, filename)
        
        # 准备结果数据
        results_data = []
        for result in self.results:
            results_data.append({
                'symbol': result.symbol,
                'indicator': result.indicator,
                'initial_capital': result.initial_capital,
                'final_capital': result.final_capital,
                'profit': result.profit,
                'profit_rate': result.profit_rate,
                'total_trades': result.total_trades,
                'win_rate': result.win_rate,
                'max_drawdown': result.max_drawdown,
                'sharpe_ratio': result.sharpe_ratio
            })
        
        # 保存为CSV
        df = pd.DataFrame(results_data)
        df.to_csv(filepath, index=False, encoding='utf-8-sig')
        
        print(f"回测结果已保存到: {filepath}")
    
    def plot_results(self):
        """
        绘制回测结果图表
        """
        if not self.results:
            print("没有回测结果可绘制")
            return
        
        # 创建图表
        fig, axes = plt.subplots(2, 2, figsize=(15, 10))
        fig.suptitle('T0回测结果分析', fontsize=16)
        
        # 按指标分组结果
        indicator_results = {}
        for result in self.results:
            if result.indicator not in indicator_results:
                indicator_results[result.indicator] = []
            indicator_results[result.indicator].append(result)
        
        # 1. 各指标收益率对比
        indicators = list(indicator_results.keys())
        profits = [np.mean([r.profit_rate for r in indicator_results[ind]]) for ind in indicators]
        
        axes[0, 0].bar(indicators, profits)
        axes[0, 0].set_title('各指标平均收益率 (%)')
        axes[0, 0].set_ylabel('收益率 (%)')
        
        # 2. 各指标胜率对比
        win_rates = [np.mean([r.win_rate for r in indicator_results[ind]]) for ind in indicators]
        
        axes[0, 1].bar(indicators, win_rates)
        axes[0, 1].set_title('各指标平均胜率')
        axes[0, 1].set_ylabel('胜率')
        
        # 3. 各股票收益对比
        symbols = list(set([r.symbol for r in self.results]))
        symbol_profits = []
        for symbol in symbols:
            symbol_results = [r for r in self.results if r.symbol == symbol]
            avg_profit = np.mean([r.profit_rate for r in symbol_results])
            symbol_profits.append(avg_profit)
        
        axes[1, 0].bar(symbols, symbol_profits)
        axes[1, 0].set_title('各股票平均收益率 (%)')
        axes[1, 0].set_ylabel('收益率 (%)')
        axes[1, 0].tick_params(axis='x', rotation=45)
        
        # 4. 交易次数分布
        total_trades = [len(result.trades) for result in self.results]
        axes[1, 1].hist(total_trades, bins=10)
        axes[1, 1].set_title('交易次数分布')
        axes[1, 1].set_xlabel('交易次数')
        axes[1, 1].set_ylabel('频次')
        
        plt.tight_layout()
        plt.savefig(os.path.join(RESULTS_DIR, 'backtest_analysis.png'), dpi=300, bbox_inches='tight')
        plt.close()
        
        print("回测分析图表已保存到:", os.path.join(RESULTS_DIR, 'backtest_analysis.png'))