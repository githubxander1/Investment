import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime
import os

class BacktestEngine:
    """通用回测引擎"""
    
    def __init__(self, stock_code, start_date, end_date, initial_capital=100000):
        self.stock_code = stock_code
        self.start_date = start_date
        self.end_date = end_date
        self.initial_capital = initial_capital
        self.capital = initial_capital
        self.position = 0
        self.trades = []
        self.data = None
        self.backtest_log = []  # 用于保存详细回测记录
        self.daily_log = []     # 用于保存每日详细记录
    
    def load_data(self, data):
        """
        加载数据
        
        Parameters:
        data (pd.DataFrame): 股票数据
        """
        self.data = data.copy()
        print(f"数据加载成功，共{len(self.data)}条记录")
    
    def calculate_indicators(self):
        """
        计算技术指标，需要在子类中实现
        """
        raise NotImplementedError("需要在子类中实现calculate_indicators方法")
    
    def calculate_signals(self):
        """
        计算买卖信号，需要在子类中实现
        """
        raise NotImplementedError("需要在子类中实现calculate_signals方法")
    
    def run_backtest(self):
        """执行回测"""
        if self.data is None:
            print("请先加载数据")
            return False
        
        df = self.data.copy()
        
        # 重置回测参数
        self.capital = self.initial_capital
        self.position = 0
        self.trades = []
        self.backtest_log = []
        self.daily_log = []
        
        # 记录回测开始信息
        self.backtest_log.append({
            'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'type': '回测开始',
            'stock_code': self.stock_code,
            'start_date': self.start_date,
            'end_date': self.end_date,
            'initial_capital': self.initial_capital
        })
        
        print("开始回测...")
        print(f"初始资金: {self.initial_capital}")
        print("交易记录:")
        print("日期\t\t类型\t价格\t数量\t金额\t持仓\t资金")
        
        # 执行回测逻辑
        for i in range(len(df)):
            date = df['date'].iloc[i] if 'date' in df.columns else df.index[i]
            close_price = df['close'].iloc[i]
            
            # 保存每日详细记录
            daily_info = {
                'date': date.strftime('%Y-%m-%d') if hasattr(date, 'strftime') else str(date),
                'close': close_price,
                'position': self.position,
                'capital': self.capital,
                'total_value': self.capital + self.position * close_price
            }
            
            # 如果有OHLC数据，也保存
            if 'open' in df.columns:
                daily_info['open'] = df['open'].iloc[i]
            if 'high' in df.columns:
                daily_info['high'] = df['high'].iloc[i]
            if 'low' in df.columns:
                daily_info['low'] = df['low'].iloc[i]
            if 'volume' in df.columns:
                daily_info['volume'] = df['volume'].iloc[i]
            
            # 计算日收益率
            if i > 0 and len(self.daily_log) > 0:
                prev_value = self.daily_log[-1]['total_value']
                if prev_value > 0:
                    daily_info['daily_return'] = (daily_info['total_value'] - prev_value) / prev_value * 100
                else:
                    daily_info['daily_return'] = 0
            else:
                daily_info['daily_return'] = 0
            
            self.daily_log.append(daily_info)
            
            # 检查买入信号（如果有的话）
            buy_signal = df['买入信号'].iloc[i] if '买入信号' in df.columns else 0
            if buy_signal == 1 and self.position == 0:
                # 计算可以买入的数量（整百股）
                quantity = int(self.capital // close_price) // 100 * 100
                if quantity >= 100:  # 至少买入100股
                    cost = quantity * close_price
                    self.position += quantity
                    self.capital -= cost
                    
                    self.trades.append({
                        'date': date,
                        'type': '买入',
                        'price': close_price,
                        'quantity': quantity,
                        'amount': cost,
                        'position': self.position,
                        'capital': self.capital
                    })
                    
                    # 保存到详细日志
                    self.backtest_log.append({
                        'date': date.strftime('%Y-%m-%d') if hasattr(date, 'strftime') else str(date),
                        'type': '买入',
                        'price': close_price,
                        'quantity': quantity,
                        'amount': cost,
                        'position': self.position,
                        'capital': self.capital
                    })
                    
                    print(f"{date.strftime('%Y-%m-%d') if hasattr(date, 'strftime') else str(date)}\t买入\t{close_price:.2f}\t{quantity}\t{cost:.2f}\t{self.position}\t{self.capital:.2f}")
            
            # 检查卖出信号（如果有的话）
            sell_signal = df['卖出信号'].iloc[i] if '卖出信号' in df.columns else 0
            if sell_signal == 1 and self.position > 0:
                # 卖出全部持仓
                revenue = self.position * close_price
                self.capital += revenue
                
                self.trades.append({
                    'date': date,
                    'type': '卖出',
                    'price': close_price,
                    'quantity': self.position,
                    'amount': revenue,
                    'position': 0,
                    'capital': self.capital
                })
                
                # 保存到详细日志
                self.backtest_log.append({
                    'date': date.strftime('%Y-%m-%d') if hasattr(date, 'strftime') else str(date),
                    'type': '卖出',
                    'price': close_price,
                    'quantity': self.position,
                    'amount': revenue,
                    'position': 0,
                    'capital': self.capital
                })
                
                print(f"{date.strftime('%Y-%m-%d') if hasattr(date, 'strftime') else str(date)}\t卖出\t{close_price:.2f}\t{self.position}\t{revenue:.2f}\t0\t{self.capital:.2f}")
                self.position = 0
        
        # 回测结束时，如果还有持仓，强制卖出
        if self.position > 0:
            last_date = df['date'].iloc[-1] if 'date' in df.columns else df.index[-1]
            last_price = df['close'].iloc[-1]
            revenue = self.position * last_price
            self.capital += revenue
            
            self.trades.append({
                'date': last_date,
                'type': '强制卖出',
                'price': last_price,
                'quantity': self.position,
                'amount': revenue,
                'position': 0,
                'capital': self.capital
            })
            
            # 保存到详细日志
            self.backtest_log.append({
                'date': last_date.strftime('%Y-%m-%d') if hasattr(last_date, 'strftime') else str(last_date),
                'type': '强制卖出',
                'price': last_price,
                'quantity': self.position,
                'amount': revenue,
                'position': 0,
                'capital': self.capital
            })
            
            print(f"{last_date.strftime('%Y-%m-%d') if hasattr(last_date, 'strftime') else str(last_date)}\t强制卖出\t{last_price:.2f}\t{self.position}\t{revenue:.2f}\t0\t{self.capital:.2f}")
            self.position = 0
        
        # 计算回测结果
        total_return = (self.capital - self.initial_capital) / self.initial_capital * 100
        
        # 保存回测结果到日志
        self.backtest_log.append({
            'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'type': '回测结果',
            'final_capital': self.capital,
            'total_return': total_return,
            'trade_count': len(self.trades),
            'win_rate': 0
        })
        
        print("\n回测结果:")
        print(f"最终资金: {self.capital:.2f}")
        print(f"总收益率: {total_return:.2f}%")
        print(f"交易次数: {len(self.trades)}")
        
        # 计算胜率
        winning_trades = 0
        if len(self.trades) >= 2:
            for i in range(0, len(self.trades), 2):
                if i + 1 < len(self.trades):  # 确保有对应的卖出交易
                    buy_price = self.trades[i]['price']
                    sell_price = self.trades[i + 1]['price']
                    if sell_price > buy_price:
                        winning_trades += 1
            
            win_rate = winning_trades / (len(self.trades) / 2) * 100
            print(f"胜率: {win_rate:.2f}%")
            # 更新胜率到回测日志
            self.backtest_log[-1]['win_rate'] = win_rate
        
        return True
    
    def plot_results(self, title_suffix="", save_dir=None):
        """绘制回测结果图表"""
        if self.data is None or len(self.trades) == 0:
            print("没有足够的数据来绘制图表")
            return False
        
        df = self.data.copy()
        
        try:
            # 创建图形和子图
            fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(15, 10), gridspec_kw={'height_ratios': [3, 1]})
            fig.subplots_adjust(hspace=0.3)
            
            # 子图1: 价格图和买卖信号
            ax1.plot(df['date'] if 'date' in df.columns else df.index, df['close'], 'b-', label='收盘价')
            
            # 如果有OHLC数据，绘制蜡烛图
            if all(col in df.columns for col in ['open', 'high', 'low', 'close']):
                # 绘制蜡烛图的简化版本
                for i in range(0, len(df), 5):  # 每5天绘制一个蜡烛图以避免过于密集
                    if i < len(df):
                        date = df['date'].iloc[i] if 'date' in df.columns else df.index[i]
                        open_price = df['open'].iloc[i]
                        close_price = df['close'].iloc[i]
                        high_price = df['high'].iloc[i]
                        low_price = df['low'].iloc[i]
                        
                        # 根据涨跌设置颜色
                        color = 'red' if close_price >= open_price else 'green'
                        
                        # 绘制影线
                        ax1.plot([date, date], [low_price, high_price], color='black', linewidth=1)
                        
                        # 绘制实体
                        ax1.bar(date, abs(close_price - open_price), 
                                bottom=min(open_price, close_price), 
                                width=0.6, color=color, alpha=0.7)
            
            # 标记买卖点
            if '买入信号' in df.columns:
                buy_signals = df[df['买入信号'] == 1]
                if len(buy_signals) > 0:
                    buy_dates = [buy_signals['date'].iloc[i] if 'date' in buy_signals.columns else buy_signals.index[i] 
                                for i in range(len(buy_signals))]
                    ax1.scatter(buy_dates, buy_signals['close'], marker='^', color='red', s=100, label='买入信号')
            
            if '卖出信号' in df.columns:
                sell_signals = df[df['卖出信号'] == 1]
                if len(sell_signals) > 0:
                    sell_dates = [sell_signals['date'].iloc[i] if 'date' in sell_signals.columns else sell_signals.index[i] 
                                 for i in range(len(sell_signals))]
                    ax1.scatter(sell_dates, sell_signals['close'], marker='v', color='green', s=100, label='卖出信号')
            
            # 标记实际交易点
            for trade in self.trades:
                if trade['type'] == '买入':
                    ax1.scatter(trade['date'], trade['price'], color='red', marker='^', s=150)
                elif trade['type'] in ['卖出', '强制卖出']:
                    ax1.scatter(trade['date'], trade['price'], color='green', marker='v', s=150)
            
            ax1.set_title(f'{self.stock_code} 回测结果 {title_suffix}')
            ax1.set_ylabel('价格')
            ax1.legend()
            ax1.grid(True)
            
            # 子图2: 资金曲线
            ax2 = plt.subplot(2, 1, 2)
            
            # 计算每日资金曲线
            dates = [record['date'] for record in self.daily_log]
            total_values = [record['total_value'] for record in self.daily_log]
            
            ax2.plot(dates, total_values, label='总资产', color='blue')
            ax2.axhline(y=self.initial_capital, color='gray', linestyle='--', label=f'初始资金: {self.initial_capital}')
            
            ax2.set_title('资金曲线')
            ax2.set_xlabel('日期')
            ax2.set_ylabel('资金')
            ax2.legend()
            ax2.grid(True)
            
            # 设置日期格式
            for ax in [ax1, ax2]:
                ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
                ax.xaxis.set_major_locator(mdates.MonthLocator())
                plt.setp(ax.xaxis.get_majorticklabels(), rotation=45)
            
            plt.tight_layout()
            
            # 确保保存目录存在
            if save_dir is None:
                # 使用默认路径，但也考虑Indicators目录
                save_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '回测')
            os.makedirs(save_dir, exist_ok=True)
            
            # 保存图表
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f'回测结果_{self.stock_code}_{timestamp}.png'
            filepath = os.path.join(save_dir, filename)
            plt.savefig(filepath, dpi=300)
            print(f"图表已生成并保存为'{filename}'到'{save_dir}'")
            
            plt.close(fig)  # 关闭图表以释放内存
            return True
        except Exception as e:
            print(f"绘制图表时出错: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    def save_backtest_log(self, prefix="回测记录"):
        """保存详细回测记录到CSV文件"""
        if not self.backtest_log and not self.daily_log:
            print("没有回测记录可保存")
            return
        
        try:
            # 确保保存目录存在
            save_dir = "e:/git_documents/Investment/Investment/Indicators/回测记录"
            os.makedirs(save_dir, exist_ok=True)
            
            # 生成时间戳
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            
            # 保存交易记录（主要事件）
            if self.backtest_log:
                log_df = pd.DataFrame(self.backtest_log)
                filename = f"{prefix}_{self.stock_code}_{timestamp}.csv"
                filepath = f"{save_dir}/{filename}"
                
                # 保存到CSV文件
                log_df.to_csv(filepath, index=False, encoding='utf-8-sig')
                print(f"详细回测记录已保存到: {filepath}")
            
            # 保存每日详细记录（包含所有指标和资金变化）
            if self.daily_log:
                daily_df = pd.DataFrame(self.daily_log)
                filename = f"{prefix}_每日记录_{self.stock_code}_{timestamp}.csv"
                filepath = f"{save_dir}/{filename}"
                
                # 保存到CSV文件
                daily_df.to_csv(filepath, index=False, encoding='utf-8-sig')
                print(f"每日详细回测记录已保存到: {filepath}")
        except Exception as e:
            print(f"保存回测记录时出错: {e}")

# 便捷函数
def run_backtest(backtester_class, stock_code, start_date, end_date, initial_capital=100000, **kwargs):
    """
    运行回测的便捷函数
    
    Parameters:
    backtester_class: 回测类
    stock_code (str): 股票代码
    start_date (str): 开始日期，格式'YYYYMMDD'
    end_date (str): 结束日期，格式'YYYYMMDD'
    initial_capital (float): 初始资金
    **kwargs: 传递给回测类的其他参数
    
    Returns:
    backtester: 回测实例
    """
    try:
        from utils.data_manager import get_stock_data
        
        # 创建回测实例
        backtester = backtester_class(
            stock_code=stock_code,
            start_date=start_date,
            end_date=end_date,
            initial_capital=initial_capital,
            **kwargs
        )
        
        # 获取数据
        data = get_stock_data(stock_code, start_date, end_date)
        if data is not None:
            backtester.load_data(data)
            backtester.calculate_indicators()
            backtester.calculate_signals()
            backtester.run_backtest()
            backtester.plot_results()
            backtester.save_backtest_log()
        else:
            print(f"无法获取{stock_code}的数据")
        
        return backtester
    except Exception as e:
        print(f"运行回测时出错: {e}")
        import traceback
        traceback.print_exc()
        return None