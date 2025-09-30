# T0交易系统主监控程序
import time
import sys
import os
from datetime import datetime, date

# 添加项目根目录到路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Investment.T0.config.settings import DEFAULT_STOCK_POOL, MONITOR_INTERVAL
from Investment.T0.monitor.signal_detector import SignalDetector
from Investment.T0.monitor.trade_executor import TradeExecutor
from Investment.T0.utils.logger import setup_logger
from Investment.T0.utils import tools
from Investment.THS.AutoTrade.utils.notification import send_notification
NOTIFICATION_AVAILABLE = True

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
            
        # 按指标类型分组信号
        buy_signals = [s for s in signals if s['type'] == '买入']
        sell_signals = [s for s in signals if s['type'] == '卖出']
        
        # 打印所有检测到的信号
        print(f"\n📊 检测到 {len(signals)} 个信号:")
        for signal in signals:
            print(f"  - 指标: {signal['indicator']}, 类型: {signal['type']}, 详情: {signal['details']}")
        
        # 只处理最先发出的买入和卖出信号
        processed_signals = []
        
        # 处理买入信号（如果有的话）
        if buy_signals:
            first_buy_signal = buy_signals[0]  # 取第一个买入信号
            indicator = first_buy_signal['indicator']
            details = first_buy_signal['details']
            stock_code = self.stock_pool[0]
            
            signal_key = f"{indicator}_买入"
            processed_signals.append(signal_key)
            
            # 发送通知
            title = f"T0交易信号 - {stock_code}"
            content = f"指标: {indicator}\n类型: 买入\n详情: {details}\n时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
            try:
                send_notification(content)  # 注意：这里只传一个参数
                logger.info(f"已发送通知: {title}")
            except Exception as e:
                logger.error(f"发送通知失败: {e}")
            
            # 执行交易
            try:
                self.executor.execute_buy(stock_code, indicator)
                logger.info(f"已执行买入交易: {stock_code} - {indicator}")
                print(f"✅ 已执行买入交易: {stock_code} - {indicator}")
            except Exception as e:
                logger.error(f"执行买入交易失败: {e}")
                print(f"❌ 执行买入交易失败: {e}")
        
        # 处理卖出信号（如果有的话）
        if sell_signals:
            first_sell_signal = sell_signals[0]  # 取第一个卖出信号
            indicator = first_sell_signal['indicator']
            details = first_sell_signal['details']
            stock_code = self.stock_pool[0]
            
            signal_key = f"{indicator}_卖出"
            processed_signals.append(signal_key)
            
            # 发送通知
            title = f"T0交易信号 - {stock_code}"
            content = f"指标: {indicator}\n类型: 卖出\n详情: {details}\n时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
            try:
                send_notification(content)  # 注意：这里只传一个参数
                logger.info(f"已发送通知: {title}")
            except Exception as e:
                logger.error(f"发送通知失败: {e}")
            
            # 执行交易
            try:
                self.executor.execute_sell(stock_code, indicator)
                logger.info(f"已执行卖出交易: {stock_code} - {indicator}")
                print(f"✅ 已执行卖出交易: {stock_code} - {indicator}")
            except Exception as e:
                logger.error(f"执行卖出交易失败: {e}")
                print(f"❌ 执行卖出交易失败: {e}")
    
    def run(self):
        """运行主监控循环"""
        logger.info(f"开始监控T0交易信号，股票池: {self.stock_pool}")
        
        while True:
            # 检查是否为交易时间
            if not tools.is_trading_time():
                print("当前非交易时间，等待交易时间开始...")
                logger.info("当前非交易时间，等待交易时间开始...")
                tools.wait_until_trading_time()
                continue
            
            # 检查并重置每日信号
            self.check_and_reset_daily_signals()
            
            # 检查每个股票的信号
            for stock_code in self.stock_pool:
                if stock_code != self.detector.stock_code:
                    self.detector = SignalDetector(stock_code)
                
                try:
                    signals = self.detector.detect_all_signals()
                    if signals:
                        logger.info(f"检测到 {len(signals)} 个新信号")
                        self.process_signals(signals)
                    else:
                        logger.debug(f"未检测到新信号: {stock_code}")
                        print(f"未检测到 {stock_code} 的新信号")
                except Exception as e:
                    logger.error(f"检测信号时出错: {e}")
                    print(f"❌ 检测信号时出错: {e}")
            
            # 等待下次检测
            print(f"等待 {MONITOR_INTERVAL} 秒后进行下一次检测...")
            time.sleep(MONITOR_INTERVAL)
            
            # 检查是否已收盘
            if tools.is_market_closed():
                print("今日交易已结束，等待下一个交易日...")
                logger.info("今日交易已结束，等待下一个交易日...")
                tools.wait_until_trading_time()
    
    def run_once(self):
        """运行一次检测（用于测试）"""
        logger.info(f"开始单次检测T0交易信号，股票池: {self.stock_pool}")
        logger.info("移除交易时间限制，直接运行一次信号检测...")
        
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
                else:
                    logger.debug(f"未检测到新信号: {stock_code}")
                    print("❌ 未检测到任何新信号")
            except Exception as e:
                logger.error(f"检测信号时出错: {e}")
                print(f"❌ 检测信号时出错: {e}")
        
        print("\n=== T0交易系统测试完成 ===")


def main(stock_pool=None):
    """主函数"""
    # 检查是否有测试参数
    if len(sys.argv) > 1 and sys.argv[1] == '--test':
        monitor = T0Monitor(stock_pool)
        monitor.run_once()
    else:
        monitor = T0Monitor(stock_pool)
        monitor.run()

if __name__ == "__main__":
    # 可以通过命令行参数指定股票代码
    stock_pool = sys.argv[1:] if len(sys.argv) > 1 else None
    # 如果第一个参数是--test，则移除它
    if stock_pool and stock_pool[0] == '--test':
        stock_pool = stock_pool[1:] if len(stock_pool) > 1 else None
    main(stock_pool)