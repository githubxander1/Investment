import os
import sys
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import time

# from Investment.T0_NewSystem.src.visualization import plotting

# 添加项目根目录到路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# 导入各个模块
from Investment.T0_NewSystem.src.indicators import tdx_indicators
from Investment.T0_NewSystem.src.data import data_handler
from Investment.T0_NewSystem.src.visualization import plotting
from Investment.T0_NewSystem.src.utils import tools


class T0Strategy:
    """
    T0交易策略主类
    """
    
    def __init__(self, stock_pool=None, refresh_interval=60, save_charts=True, notification_enabled=True):
        """
        初始化T0策略
        
        参数:
        stock_pool: 股票池列表，如果为None则使用默认股票池
        refresh_interval: 数据刷新间隔（秒）
        save_charts: 是否保存图表
        notification_enabled: 是否启用通知
        """
        # 设置股票池
        self.stock_pool = stock_pool if stock_pool else ['600000', '000001', '601318', '000858', '600519']
        
        # 设置参数
        self.refresh_interval = refresh_interval
        self.save_charts = save_charts
        self.notification_enabled = notification_enabled
        
        # 初始化结果记录
        self.results = {}
        
        # 设置中文字体
        plotting.set_chinese_font()
        
        # 创建输出目录
        self.output_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'output')
        tools.create_directory(self.output_dir)
        
        print(f"T0策略初始化成功，股票池: {self.stock_pool}")
    
    def analyze_stock(self, stock_code):
        """
        分析单只股票
        
        参数:
        stock_code: 股票代码
        
        返回:
        dict: 分析结果
        """
        try:
            print(f"分析股票: {stock_code}")
            
            # 获取当前日期
            current_date = tools.get_current_date_str()
            
            # 尝试从缓存获取数据
            df = data_handler.get_cached_data(stock_code, current_date)
            
            # 如果缓存中没有数据，从API获取
            if df is None or df.empty:
                df = data_handler.get_stock_intraday_data(stock_code)
                
                # 验证数据
                if not data_handler.validate_data(df):
                    print(f"股票{stock_code}数据无效")
                    return None
                
                # 处理交易时间段
                df = data_handler.process_time_period(df)
                
                # 填充缺失数据
                df = data_handler.fill_missing_data(df)
                
                # 保存到缓存
                data_handler.save_data_to_cache(df, stock_code, current_date)
            
            # 获取前一日收盘价
            prev_close = data_handler.get_prev_close(stock_code)
            if prev_close is None:
                print(f"无法获取股票{stock_code}的前一日收盘价")
                return None
            
            # 计算通达信指标
            df = tdx_indicators.calculate_tdx_indicators(df, prev_close)
            
            # 计算其他指标
            df = tdx_indicators.calculate_rsi(df)
            df = tdx_indicators.calculate_macd(df)
            df = tdx_indicators.calculate_bollinger_bands(df)
            
            # 检查交易信号
            signals = self._check_signals(df)
            
            # 生成图表
            if self.save_charts:
                chart_path = self._generate_charts(df, stock_code, prev_close)
            else:
                chart_path = None
            
            # 记录结果
            result = {
                'stock_code': stock_code,
                'data': df,
                'prev_close': prev_close,
                'signals': signals,
                'chart_path': chart_path,
                'timestamp': tools.get_current_time_str()
            }
            
            self.results[stock_code] = result
            
            # 发送信号通知
            if self.notification_enabled:
                self._send_signal_notifications(stock_code, df, signals)
            
            return result
            
        except Exception as e:
            print(f"分析股票{stock_code}失败: {e}")
            return None
    
    def _check_signals(self, df):
        """
        检查交易信号
        
        参数:
        df: 包含股票数据和指标的DataFrame
        
        返回:
        dict: 信号字典
        """
        signals = {
            'buy_signals': [],
            'sell_signals': [],
            'other_signals': []
        }
        
        # 检查买入信号
        if 'longcross_support' in df.columns:
            buy_signals = df[df['longcross_support']]
            for _, row in buy_signals.iterrows():
                signals['buy_signals'].append({
                    'time': row['时间'],
                    'price': row['收盘'],
                    'type': 'longcross_support'
                })
        
        # 检查RSI买入信号
        if 'RSI_买入信号' in df.columns:
            rsi_buy_signals = df[df['RSI_买入信号']]
            for _, row in rsi_buy_signals.iterrows():
                signals['buy_signals'].append({
                    'time': row['时间'],
                    'price': row['收盘'],
                    'type': 'RSI_buy'
                })
        
        # 检查MACD买入信号
        if 'MACD_买入信号' in df.columns:
            macd_buy_signals = df[df['MACD_买入信号']]
            for _, row in macd_buy_signals.iterrows():
                signals['buy_signals'].append({
                    'time': row['时间'],
                    'price': row['收盘'],
                    'type': 'MACD_buy'
                })
        
        # 检查布林带买入信号
        if '布林买入信号' in df.columns:
            boll_buy_signals = df[df['布林买入信号']]
            for _, row in boll_buy_signals.iterrows():
                signals['buy_signals'].append({
                    'time': row['时间'],
                    'price': row['收盘'],
                    'type': 'Bollinger_buy'
                })
        
        # 检查卖出信号
        if 'longcross_resistance' in df.columns:
            sell_signals = df[df['longcross_resistance']]
            for _, row in sell_signals.iterrows():
                signals['sell_signals'].append({
                    'time': row['时间'],
                    'price': row['收盘'],
                    'type': 'longcross_resistance'
                })
        
        # 检查RSI卖出信号
        if 'RSI_卖出信号' in df.columns:
            rsi_sell_signals = df[df['RSI_卖出信号']]
            for _, row in rsi_sell_signals.iterrows():
                signals['sell_signals'].append({
                    'time': row['时间'],
                    'price': row['收盘'],
                    'type': 'RSI_sell'
                })
        
        # 检查MACD卖出信号
        if 'MACD_卖出信号' in df.columns:
            macd_sell_signals = df[df['MACD_卖出信号']]
            for _, row in macd_sell_signals.iterrows():
                signals['sell_signals'].append({
                    'time': row['时间'],
                    'price': row['收盘'],
                    'type': 'MACD_sell'
                })
        
        # 检查布林带卖出信号
        if '布林卖出信号' in df.columns:
            boll_sell_signals = df[df['布林卖出信号']]
            for _, row in boll_sell_signals.iterrows():
                signals['sell_signals'].append({
                    'time': row['时间'],
                    'price': row['收盘'],
                    'type': 'Bollinger_sell'
                })
        
        # 检查其他信号
        if 'cross_support' in df.columns:
            cross_signals = df[df['cross_support']]
            for _, row in cross_signals.iterrows():
                signals['other_signals'].append({
                    'time': row['时间'],
                    'price': row['收盘'],
                    'type': 'cross_support'
                })
        
        return signals
    
    def _generate_charts(self, df, stock_code, prev_close):
        """
        生成图表
        
        参数:
        df: 包含股票数据和指标的DataFrame
        stock_code: 股票代码
        prev_close: 前一日收盘价
        
        返回:
        str: 图表保存路径
        """
        try:
            # 创建股票特定的输出目录
            stock_output_dir = os.path.join(self.output_dir, stock_code)
            tools.create_directory(stock_output_dir)
            
            # 生成带信号的分时图
            timestamp = tools.get_current_time_str('%Y%m%d_%H%M%S')
            chart_path = os.path.join(stock_output_dir, f'{stock_code}_signals_{timestamp}.png')
            
            # 绘制图表
            title = f'{stock_code} 分时图与交易信号'
            fig = plotting.plot_with_signals(df, prev_close, title=title, save_path=chart_path)
            
            # 关闭图表以释放资源
            if fig:
                import matplotlib.pyplot as plt
                plt.close(fig)
            
            # 生成其他图表
            # 量价关系图
            volume_price_path = os.path.join(stock_output_dir, f'{stock_code}_volume_price_{timestamp}.png')
            plotting.plot_volume_price(df, title=f'{stock_code} 量价关系图', save_path=volume_price_path)
            
            # RSI指标图
            if 'RSI' in df.columns:
                rsi_path = os.path.join(stock_output_dir, f'{stock_code}_rsi_{timestamp}.png')
                plotting.plot_rsi(df, title=f'{stock_code} RSI指标图', save_path=rsi_path)
            
            return chart_path
            
        except Exception as e:
            print(f"生成图表失败: {e}")
            return None
    
    def _send_signal_notifications(self, stock_code, df, signals):
        """
        发送信号通知
        
        参数:
        stock_code: 股票代码
        df: 包含股票数据和指标的DataFrame
        signals: 信号字典
        """
        try:
            # 获取最新的价格和时间
            latest_data = df.iloc[-1] if not df.empty else None
            if latest_data is None:
                return
            
            latest_price = latest_data['收盘']
            latest_time = latest_data['时间'].strftime('%Y-%m-%d %H:%M:%S')
            
            # 检查是否有新的买入信号
            if signals['buy_signals']:
                # 获取最新的买入信号
                latest_buy_signal = max(signals['buy_signals'], key=lambda x: x['time'])
                signal_time_str = latest_buy_signal['time'].strftime('%Y-%m-%d %H:%M:%S')
                
                # 如果信号是最近5分钟内的，发送通知
                signal_time = pd.to_datetime(signal_time_str)
                if (pd.to_datetime(latest_time) - signal_time).total_seconds() < 300:
                    tools.notify_signal(stock_code, 'buy', latest_buy_signal['price'], signal_time_str)
            
            # 检查是否有新的卖出信号
            if signals['sell_signals']:
                # 获取最新的卖出信号
                latest_sell_signal = max(signals['sell_signals'], key=lambda x: x['time'])
                signal_time_str = latest_sell_signal['time'].strftime('%Y-%m-%d %H:%M:%S')
                
                # 如果信号是最近5分钟内的，发送通知
                signal_time = pd.to_datetime(signal_time_str)
                if (pd.to_datetime(latest_time) - signal_time).total_seconds() < 300:
                    tools.notify_signal(stock_code, 'sell', latest_sell_signal['price'], signal_time_str)
            
        except Exception as e:
            print(f"发送信号通知失败: {e}")
    
    def run(self):
        """
        运行T0策略
        """
        print(f"开始运行T0策略，股票池: {self.stock_pool}")
        
        try:
            while True:
                # 检查是否为交易时间
                # if not tools.is_trading_time():
                #     print("非交易时间，等待交易时间开始...")
                #     tools.wait_until_trading_time()
                #     continue
                
                # 分析每只股票
                for stock_code in self.stock_pool:
                    self.analyze_stock(stock_code)
                
                # 显示结果摘要
                self._display_results_summary()
                
                # 等待下一次刷新
                print(f"等待 {self.refresh_interval} 秒后刷新数据...")
                time.sleep(self.refresh_interval)
                
                # 检查是否已收盘
                if tools.is_market_closed():
                    print("今日交易已结束，等待下一个交易日...")
                    tools.wait_until_trading_time()
        
        except KeyboardInterrupt:
            print("用户中断策略运行")
        except Exception as e:
            print(f"策略运行出错: {e}")
        finally:
            print("T0策略运行结束")
    
    def _display_results_summary(self):
        """
        显示结果摘要
        """
        print("\n=== 策略运行结果摘要 ===")
        print(f"时间: {tools.get_current_time_str()}")
        
        for stock_code, result in self.results.items():
            if result and 'signals' in result:
                signals = result['signals']
                buy_count = len(signals['buy_signals'])
                sell_count = len(signals['sell_signals'])
                
                # 获取最新价格
                if 'data' in result and not result['data'].empty:
                    latest_price = result['data'].iloc[-1]['收盘']
                    prev_close = result['prev_close']
                    change_percent = tools.calculate_percentage_change(latest_price, prev_close)
                    
                    print(f"股票: {stock_code}, 最新价: {latest_price:.2f}, 涨跌幅: {change_percent:.2f}%")
                    print(f"  买入信号: {buy_count}, 卖出信号: {sell_count}")
                    
                    # 如果有最近的信号，显示
                    if signals['buy_signals']:
                        latest_buy = max(signals['buy_signals'], key=lambda x: x['time'])
                        print(f"  最近买入信号: {latest_buy['time'].strftime('%H:%M:%S')}, 价格: {latest_buy['price']:.2f}, 类型: {latest_buy['type']}")
                    if signals['sell_signals']:
                        latest_sell = max(signals['sell_signals'], key=lambda x: x['time'])
                        print(f"  最近卖出信号: {latest_sell['time'].strftime('%H:%M:%S')}, 价格: {latest_sell['price']:.2f}, 类型: {latest_sell['type']}")
        
        print("======================\n")


if __name__ == '__main__':
    # 创建并运行T0策略
    strategy = T0Strategy(
        stock_pool=['600000', '000001', '601318', '000858', '600519'],
        refresh_interval=60,
        save_charts=True,
        notification_enabled=True
    )
    strategy.run()