# T0交易系统主监控程序
import os
import sys
import time
import logging
from datetime import datetime, time as dt_time, timedelta

# 添加项目根目录到路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Investment.T0.monitor.signal_detector import SignalDetector
# 注释掉自动交易执行器的导入
# from Investment.T0.monitor.trade_executor import TradeExecutor

# 导入价格成交量偏离指标分析函数
from Investment.T0.indicators.price_volume_deviation import analyze_strategy, indicator_main
from Investment.T0.utils.notification import send_notification

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    filename='t0_trading.log'
)
logger = logging.getLogger('T0Monitor')

class T0Monitor:
    """T0交易监控器"""
    
    def __init__(self, stock_codes=None):
        # 默认监控中信证券和海康威视
        if stock_codes is None:
            self.stock_codes = ['600030', '002415']  # 中信证券和海康威视
        else:
            self.stock_codes = stock_codes
            
        # 为每只股票创建信号检测器
        self.signal_detectors = {}
        for stock_code in self.stock_codes:
            self.signal_detectors[stock_code] = SignalDetector(stock_code)
            
        # 注释掉交易执行器的创建
        # 创建交易执行器
        # self.executor = TradeExecutor()
        
        # 初始化每日重置标记
        self.reset_daily_flag = True
        self.last_trading_date = None
        
        # 初始化信号队列（按重要性排序）
        self.signal_queue = []
        
        # 买入和卖出信号分别存储，用于实现先卖后买原则
        self.buy_signals = []
        self.sell_signals = []
        
        # 当日已执行的交易记录
        self.executed_trades = []
        
        # 用于跟踪已发送的通知，避免重复发送
        self.sent_notifications = set()
        
    # def is_trading_time(self):
    #     """判断是否为交易时间"""
    #     now = datetime.now()
    #     # 判断是否为工作日（周一到周五）
    #     if now.weekday() >= 5:
    #         return False
    #
    #     # 判断是否在交易时间段内
    #     current_time = now.time()
    #     morning_trading = dt_time(9, 30) <= current_time <= dt_time(11, 30)
    #     afternoon_trading = dt_time(13, 0) <= current_time <= dt_time(15, 0)
    #
    #     return morning_trading or afternoon_trading
    
    def reset_daily_state(self):
        """重置每日状态"""
        now = datetime.now()
        current_date = now.date()
        
        # 如果日期变更，重置状态
        if self.last_trading_date != current_date:
            self.reset_daily_flag = True
            self.last_trading_date = current_date
        
        # 执行每日重置
        if self.reset_daily_flag:
            logger.info(f"执行每日重置，日期: {current_date}")
            
            # 清空信号队列和已执行交易记录
            self.signal_queue.clear()
            logger.info("清空信号队列")
            self.buy_signals.clear()
            logger.info("清空买入信号队列")
            self.sell_signals.clear()
            logger.info("清空卖出信号队列")
            self.executed_trades.clear()
            logger.info("清空已执行交易记录")
            
            # 重置信号检测器的状态
            for stock_code, detector in self.signal_detectors.items():
                if hasattr(detector, 'prev_signals'):
                    # 重置综合T+0策略的持仓状态
                    if 'comprehensive_t0' in detector.prev_signals:
                        detector.prev_signals['comprehensive_t0']['has_open_position'] = False
                    logger.info(f"重置股票 {stock_code} 的信号检测器状态")
                    
            # 清空已发送通知记录
            self.sent_notifications.clear()
            logger.info("清空已发送通知记录")
            
            self.reset_daily_flag = False
            logger.info("完成每日重置")
    
    def process_signals(self):
        """处理检测到的信号"""
        # 清空现有信号队列
        self.buy_signals.clear()
        self.sell_signals.clear()

        # 每30秒重新获取数据并检测信号
        indicator_main()

        # 按时间戳排序
        self.buy_signals.sort(key=lambda x: x['timestamp'])
        self.sell_signals.sort(key=lambda x: x['timestamp'])
        
        # 按照先卖后买原则构建最终信号队列
        self.signal_queue = self.sell_signals + self.buy_signals
        
        # 发送信号通知（注释掉自动交易执行）
        for signal in self.signal_queue:
            self._send_notification_for_signal(signal)
    
    def _send_notification_for_signal(self, signal):
        """为信号发送通知"""
        stock_code = signal['stock_code']
        signal_type = signal['type']
        indicator = signal['indicator']
        details = signal['details']
        
        try:
            # 构建通知消息
            notification_msg = f"股票代码: {stock_code}\n"
            notification_msg += f"信号类型: {signal_type}\n"
            notification_msg += f"指标来源: {indicator}\n"
            notification_msg += f"详细信息: {details}\n"
            notification_msg += f"时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
            
            # 发送通知
            self._send_notification(notification_msg)
            
        except Exception as e:
            logger.error(f"发送信号通知时出错: {e}", exc_info=True)
    
    def _send_notification(self, message):
        """发送通知"""
        try:
            # 首先打印到控制台
            print("=" * 50)
            print("交易信号通知")
            print("=" * 50)
            print(message)
            print("=" * 50)
            
            # 记录到日志
            logger.info(f"发送通知: {message}")
            
            # 使用统一的通知函数发送通知
            send_notification(message)
                
        except Exception as e:
            logger.error(f"发送通知时出错: {e}")
    
    def run_monitor(self):
        """运行监控器"""
        logger.info(f"启动T0交易监控器，监控股票: {', '.join(self.stock_codes)}")
        
        try:
            while True:
                # 重置每日状态
                self.reset_daily_state()
                
                # 处理信号（每30秒执行一次）
                logger.info("处理信号...")
                self.process_signals()
                
                # 交易时间内，每30秒检查一次信号
                time.sleep(30)
                
        except KeyboardInterrupt:
            logger.info("监控器被用户中断")
        except Exception as e:
            logger.error(f"监控器运行出错: {e}", exc_info=True)
        finally:
            self.close()
    
    def run_once(self):
        """单次运行模式，用于测试"""
        logger.info(f"单次运行模式，检查股票: {', '.join(self.stock_codes)}")
        
        try:
            # 重置每日状态
            self.reset_daily_state()
            
            # 处理信号
            self.process_signals()
            
            logger.info("单次运行完成")
        except Exception as e:
            logger.error(f"单次运行出错: {e}", exc_info=True)
    
    def close(self):
        """关闭监控器，释放资源"""
        logger.info("关闭T0交易监控器")
        
        # 释放资源
        # 注释掉交易执行器的关闭
        # if hasattr(self, 'executor'):
        #     try:
        #         self.executor.close()
        #     except:
        #         pass

def main():
    """主函数"""
    import argparse
    
    # 解析命令行参数
    parser = argparse.ArgumentParser(description='T0交易系统主监控程序')
    parser.add_argument('--stocks', nargs='+', help='要监控的股票代码列表，默认监控中信证券(600030)和海康威视(002415)')
    parser.add_argument('--test', action='store_true', help='测试模式，仅运行一次')
    
    args = parser.parse_args()
    
    # 创建监控器实例
    if args.stocks:
        monitor = T0Monitor(args.stocks)
    else:
        # 默认监控中信证券和海康威视
        monitor = T0Monitor(['600030', '002415'])
    
    # 运行监控器
    if args.test:
        monitor.run_once()
    else:
        monitor.run_monitor()

if __name__ == '__main__':
    main()