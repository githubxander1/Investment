import os
import sys
import pandas as pd
from datetime import datetime
import time

# 添加项目根目录到路径
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.append(project_root)

# 导入各个模块
from indicators import tdx_indicators
from visualization import plotting
from utils import tools, data_handler


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
        # 600900长江电力，601088中国神华
        self.stock_pool = stock_pool if stock_pool else ['600900','601088']
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
            
            # 获取股票分时数据
            df = data_handler.get_stock_intraday_data(stock_code)
            
            # 验证数据
            if not data_handler.validate_data(df):
                print(f"股票{stock_code}数据无效")
                return None
            
            # 数据预处理
            df = data_handler.preprocess_data(df)
            
            # 检查是否有NaN值
            if df.isnull().values.any():
                print("数据包含NaN值，进行填充处理")
                df = df.fillna(method='ffill').fillna(method='bfill')
            
            # 计算前一日收盘价
            prev_close = data_handler.get_previous_close(stock_code, current_date)
            
            # 计算技术指标
            df = tdx_indicators.calculate_tdx_indicators(df, prev_close)
            
            # 生成交易信号
            signals = tdx_indicators.generate_trading_signals(df)
            
            # 保存结果
            result = {
                'stock_code': stock_code,
                'data': df,
                'prev_close': float(prev_close),
                'signals': signals
            }
            self.results[stock_code] = result
            
            # 保存图表（如果启用）
            if self.save_charts:
                plotting.plot_stock_with_signals(df, stock_code, signals, self.output_dir)
            
            # 检查是否有新的买入信号
            if signals['buy_signals']:
                # 获取最新的买入信号
                latest_buy_signal = max(signals['buy_signals'], key=lambda x: pd.to_datetime(x['time']))
                signal_time_str = latest_buy_signal['time'].strftime('%Y-%m-%d %H:%M:%S')
                latest_time = df['时间'].max()
                
                # 如果信号是最近5分钟内的，发送通知
                signal_time = pd.to_datetime(latest_buy_signal['time'])
                latest_time = pd.to_datetime(latest_time)
                time_diff = (latest_time - signal_time).total_seconds()
                if time_diff < 300 and time_diff >= 0:
                    try:
                        tools.notify_signal('buy', stock_code, latest_buy_signal['price'], signal_time_str)
                    except Exception as e:
                        print(f"发送买入信号通知失败: {e}")
            
            # 检查是否有新的卖出信号
            if signals['sell_signals']:
                # 获取最新的卖出信号
                latest_sell_signal = max(signals['sell_signals'], key=lambda x: pd.to_datetime(x['time']))
                signal_time_str = latest_sell_signal['time'].strftime('%Y-%m-%d %H:%M:%S')
                
                # 如果信号是最近5分钟内的，发送通知
                signal_time = pd.to_datetime(latest_sell_signal['time'])
                latest_time = pd.to_datetime(latest_time)
                time_diff = (latest_time - signal_time).total_seconds()
                if time_diff < 300 and time_diff >= 0:
                    try:
                        tools.notify_signal('sell', stock_code, latest_sell_signal['price'], signal_time_str)
                    except Exception as e:
                        print(f"发送卖出信号通知失败: {e}")
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
                if not tools.is_trading_time():
                    print("非交易时间，等待交易时间开始...")
                    tools.wait_until_trading_time()
                    continue
                
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
                    # 确保数据类型正确
                    latest_price = float(latest_price)
                    prev_close = float(prev_close)
                    change_percent = tools.calculate_percentage_change(latest_price, prev_close)
                    
                    print(f"股票: {stock_code}, 最新价: {latest_price:.2f}, 涨跌幅: {change_percent:.2f}%")
                    print(f"  买入信号: {buy_count}, 卖出信号: {sell_count}")
                    
                    # 如果有最近的信号，显示
                    if signals['buy_signals']:
                        latest_buy = max(signals['buy_signals'], key=lambda x: pd.to_datetime(x['time']))
                        print(f"  最近买入信号: {latest_buy['time'].strftime('%H:%M:%S')}, 价格: {latest_buy['price']:.2f}, 类型: {latest_buy['type']}")
                    
                    if signals['sell_signals']:
                        latest_sell = max(signals['sell_signals'], key=lambda x: pd.to_datetime(x['time']))
                        print(f"  最近卖出信号: {latest_sell['time'].strftime('%H:%M:%S')}, 价格: {latest_sell['price']:.2f}, 类型: {latest_sell['type']}")
        
        print("======================\n")


if __name__ == '__main__':
    # 创建并运行T0策略
    strategy = T0Strategy(
        stock_pool=['600900', '601088'],  # 长江电力、中国神华
        refresh_interval=60,
        save_charts=True,
        notification_enabled=True
    )
    strategy.run()
# T0交易系统入口
import sys
import os

# 添加项目根目录到路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def show_help():
    """显示帮助信息"""
    help_text = """
T0交易系统使用说明:

命令行参数:
  gui [股票代码...]      启动图形界面监控
  monitor [股票代码...]  启动命令行监控
  run [股票代码...]      启动实际交易监控
  help                  显示此帮助信息

示例:
  python main.py gui              # 启动图形界面监控默认股票
  python main.py gui 601088       # 以图形界面监控指定股票
  python main.py monitor          # 启动命令行监控默认股票
  python main.py monitor 601088 600900  # 监控多个指定股票
  python main.py run              # 启动实际交易监控默认股票
  python main.py run 601088       # 启动实际交易监控指定股票

默认监控股票: 601088 (中国神华)
"""
    print(help_text)

def main():
    """主函数"""
    if len(sys.argv) < 2:
        show_help()
        return
    
    mode = sys.argv[1]
    stock_codes = sys.argv[2:] if len(sys.argv) > 2 else None
    
    if mode == "gui":
        # 启动图形界面
        from monitor.gui import main as gui_main
        gui_main(stock_codes)
    elif mode == "monitor":
        # 启动命令行监控（测试模式）
        from monitor.main import main as monitor_main
        # 添加测试参数
        sys.argv = [sys.argv[0], '--test'] + (stock_codes if stock_codes else [])
        monitor_main()
    elif mode == "run":
        # 启动实际交易监控
        from run_t0_system import main as run_main
        # 重构参数
        sys.argv = [sys.argv[0]] + (stock_codes if stock_codes else [])
        run_main()
    elif mode in ["-h", "--help", "help"]:
        show_help()
    else:
        print("未知的命令参数")
        show_help()

if __name__ == "__main__":
    main()
