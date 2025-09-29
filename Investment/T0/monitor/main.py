# T0交易系统主监控程序
import time
import sys
import os
from datetime import datetime, date

# 添加项目根目录到路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.settings import DEFAULT_STOCK_POOL, MONITOR_INTERVAL
from monitor.signal_detector import SignalDetector
from monitor.trade_executor import TradeExecutor
from utils.logger import setup_logger
# 复用AutoTrade的通知机制
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '..', 'THS', 'AutoTrade'))
try:
    from utils.notification import send_notification
    NOTIFICATION_AVAILABLE = True
except ImportError:
    def send_notification(title, content):
        print(f"[通知] {title}: {content}")
    NOTIFICATION_AVAILABLE = False

logger = setup_logger('t0_main')

class T0Monitor:
    """T0主监控程序"""
    
    def __init__(self, stock_pool=None):
        self.stock_pool = stock_pool if stock_pool else DEFAULT_STOCK_POOL
        self.detector = SignalDetector(self.stock_pool[0])  # 暂时只监控第一个股票
        self.executor = TradeExecutor()
        self.last_trade_date = None
        
    def check_and_reset_daily_signals(self):
        """检查并重置每日信号"""
        current_date = date.today()
        if self.last_trade_date != current_date:
            self.executor.reset_daily_signals()
            self.detector.prev_signals = {
                'resistance_support': {'buy': False, 'sell': False},
                'extended': {'buy': False, 'sell': False},
                'volume_price': {'buy': False, 'sell': False}
            }
            self.last_trade_date = current_date
            logger.info(f"开始新交易日: {current_date}")
    
    def process_signals(self, signals):
        """处理检测到的信号"""
        if not signals:
            return
            
        for signal in signals:
            indicator = signal['indicator']
            signal_type = signal['type']
            details = signal['details']
            stock_code = self.stock_pool[0]
            
            # 发送通知
            title = f"T0交易信号 - {stock_code}"
            content = f"指标: {indicator}\n类型: {signal_type}\n详情: {details}\n时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
            try:
                send_notification(title, content)
                logger.info(f"已发送通知: {title}")
            except Exception as e:
                logger.error(f"发送通知失败: {e}")
            
            # 执行交易
            if signal_type == '买入':
                try:
                    self.executor.execute_buy(stock_code, indicator)
                    logger.info(f"已执行买入交易: {stock_code} - {indicator}")
                except Exception as e:
                    logger.error(f"执行买入交易失败: {e}")
            elif signal_type == '卖出':
                try:
                    self.executor.execute_sell(stock_code, indicator)
                    logger.info(f"已执行卖出交易: {stock_code} - {indicator}")
                except Exception as e:
                    logger.error(f"执行卖出交易失败: {e}")
    
    def run(self):
        """运行主监控循环"""
        logger.info(f"开始监控T0交易信号，股票池: {self.stock_pool}")
        logger.info("等待交易时间开始...")
        
        # 为了测试，我们移除时间限制
        print("=== T0交易系统测试模式 ===")
        print("移除交易时间限制，直接运行一次信号检测...")
        
        # 检查并重置每日信号
        self.check_and_reset_daily_signals()
        
        # 检查每个股票的信号（只运行一次用于测试）
        for stock_code in self.stock_pool:
            if stock_code != self.detector.stock_code:
                self.detector = SignalDetector(stock_code)
            
            try:
                signals = self.detector.detect_all_signals()
                if signals:
                    logger.info(f"检测到 {len(signals)} 个新信号")
                    self.process_signals(signals)
                    print(f"\n✅ 检测到 {len(signals)} 个信号:")
                    for signal in signals:
                        print(f"  - 指标: {signal['indicator']}, 类型: {signal['type']}, 详情: {signal['details']}")
                else:
                    logger.debug(f"未检测到新信号: {stock_code}")
                    print("❌ 未检测到任何新信号")
            except Exception as e:
                logger.error(f"检测信号时出错: {e}")
                print(f"❌ 检测信号时出错: {e}")
        
        print("\n=== T0交易系统测试完成 ===")

def main(stock_pool=None):
    """主函数"""
    monitor = T0Monitor(stock_pool)
    monitor.run()

if __name__ == "__main__":
    # 可以通过命令行参数指定股票代码
    stock_pool = sys.argv[1:] if len(sys.argv) > 1 else None
    main(stock_pool)