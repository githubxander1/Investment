"""
详细日志版回测脚本 - 用于分析交易过程
"""

import pandas as pd
import akshare as ak
import sys
import os
from datetime import datetime, timedelta

# 添加项目根目录到路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from backtest.data_loader import load_stock_data, get_prev_close
from backtest.strategies import (
    detect_resistance_support_signals,
    detect_extended_signals,
    detect_volume_price_signals_func
)
from backtest.engine import BacktestEngine
from backtest.models import SignalType
from config.settings import DEFAULT_STOCK_POOL

def detailed_backtest_single_stock(symbol='000333', start_date='20250901', end_date='20250930'):
    """
    详细日志版回测 - 单个股票
    
    Args:
        symbol: 股票代码
        start_date: 开始日期 (YYYYMMDD)
        end_date: 结束日期 (YYYYMMDD)
    """
    print(f"开始详细回测股票: {symbol}")
    print(f"回测期间: {start_date} 到 {end_date}")
    print("=" * 60)
    
    # 1. 加载数据
    print("1. 加载数据...")
    data = load_stock_data(symbol, start_date, end_date)
    if data.empty:
        print("❌ 无法加载数据")
        return
    
    print(f"✅ 成功加载 {len(data)} 条数据")
    print(f"   数据时间范围: {data.index.min()} 到 {data.index.max()}")
    
    # 2. 获取前收盘价
    print("2. 获取前收盘价...")
    prev_close = get_prev_close(symbol, start_date)
    if prev_close is None:
        prev_close = data['开盘'].iloc[0] if not data.empty else 0
        print(f"⚠️ 无法获取前收盘价，使用开盘价替代: {prev_close:.2f}")
    else:
        print(f"✅ 前收盘价: {prev_close:.2f}")
    
    # 3. 测试各个指标
    indicators = ['resistance_support', 'extended', 'volume_price']
    
    for indicator in indicators:
        print(f"\n3.{indicators.index(indicator)+1}. 详细测试 {indicator} 指标...")
        print("-" * 40)
        
        # 检测信号
        try:
            if indicator == 'resistance_support':
                signals = detect_resistance_support_signals(data, prev_close)
            elif indicator == 'extended':
                # 获取日线数据用于扩展指标
                from indicators.extended_indicators import get_prev_close as get_prev_close_extended
                _, daily_data = get_prev_close_extended(symbol, start_date)
                signals = detect_extended_signals(data, prev_close, daily_data)
            elif indicator == 'volume_price':
                signals = detect_volume_price_signals_func(data, prev_close)
            
            print(f"检测到 {len(signals)} 个信号:")
            if signals:
                buy_signals = [s for s in signals if s.signal_type == SignalType.BUY]
                sell_signals = [s for s in signals if s.signal_type == SignalType.SELL]
                print(f"  买入信号: {len(buy_signals)} 个")
                print(f"  卖出信号: {len(sell_signals)} 个")
                
                # 显示前几个信号
                for i, signal in enumerate(signals[:5]):  # 只显示前5个
                    print(f"  信号 {i+1}: {signal.signal_type.value} at {signal.timestamp.strftime('%Y-%m-%d %H:%M')} (价格: {signal.price:.2f})")
                
                if len(signals) > 5:
                    print(f"  ... 还有 {len(signals) - 5} 个信号")
            else:
                print("  未检测到任何信号")
                
        except Exception as e:
            print(f"  ❌ 检测 {indicator} 指标信号时出错: {e}")
            import traceback
            traceback.print_exc()
            continue
        
        # 执行回测
        try:
            engine = BacktestEngine()
            result = engine.run_backtest(symbol, indicator, data, start_date, end_date)
            
            print(f"\n回测结果:")
            print(f"  初始资金: {result.initial_capital:.2f}")
            print(f"  最终资金: {result.final_capital:.2f}")
            print(f"  收益: {result.profit:.2f} ({result.profit_rate:.2f}%)")
            print(f"  交易次数: {result.total_trades}")
            print(f"  胜率: {result.win_rate:.2f}")
            
            # 显示前几笔交易
            if result.trades:
                print(f"\n前 {min(3, len(result.trades))} 笔交易:")
                for i, trade in enumerate(result.trades[:3]):
                    print(f"  交易 {i+1}: {trade.trade_type.value} at {trade.timestamp.strftime('%Y-%m-%d %H:%M')} "
                          f"(价格: {trade.price:.2f}, 数量: {trade.quantity}, 手续费: {trade.commission:.2f})")
            else:
                print("  未执行任何交易")
                
        except Exception as e:
            print(f"  ❌ 执行 {indicator} 指标回测时出错: {e}")
            import traceback
            traceback.print_exc()
    
    print("\n详细回测完成!")

if __name__ == "__main__":
    # 测试默认股票池中的第一个股票
    stock_code = DEFAULT_STOCK_POOL[0] if DEFAULT_STOCK_POOL else '000333'
    detailed_backtest_single_stock(stock_code, '20250901', '20250930')