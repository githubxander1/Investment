# Trade engine implementation for T0 trading system
import os
import sys
from datetime import datetime

# 添加项目根目录到路径
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.append(project_root)

from utils.logger import setup_logger
from monitor.trade_executor import TradeExecutor
from monitor.signal_detector import SignalDetector
from config.settings import DEFAULT_STOCK_POOL, MONITOR_INTERVAL

logger = setup_logger('trade_engine')


class TradeEngine:
    """
    交易引擎，负责协调信号检测和交易执行
    """
    
    def __init__(self, stock_pool=None):
        """
        初始化交易引擎
        
        参数:
        stock_pool: 股票池列表，如果为None则使用默认股票池
        """
        self.stock_pool = stock_pool if stock_pool else DEFAULT_STOCK_POOL
        self.detectors = {stock_code: SignalDetector(stock_code) 
                         for stock_code in self.stock_pool}
        self.executor = TradeExecutor()
        self.monitor_interval = MONITOR_INTERVAL
        
        logger.info(f"交易引擎初始化成功，股票池: {self.stock_pool}")
    
    def detect_signals(self, stock_code):
        """
        检测指定股票的交易信号
        
        参数:
        stock_code: 股票代码
        
        返回:
        list: 检测到的信号列表
        """
        try:
            detector = self.detectors.get(stock_code)
            if not detector:
                logger.error(f"股票{stock_code}没有对应的检测器")
                return []
            
            signals = detector.detect_signals()
            logger.info(f"股票{stock_code}检测到{len(signals)}个信号")
            return signals
            
        except Exception as e:
            logger.error(f"检测股票{stock_code}信号时出错: {e}")
            return []
    
    def process_signals(self, stock_code, signals):
        """
        处理检测到的信号
        
        参数:
        stock_code: 股票代码
        signals: 信号列表
        
        返回:
        dict: 处理结果
        """
        if not signals:
            return {"status": "no_signals", "message": "未检测到信号"}
        
        # 按指标类型分类信号
        signals_by_indicator = {}
        for signal in signals:
            indicator = signal.get('indicator', 'unknown')
            if indicator not in signals_by_indicator:
                signals_by_indicator[indicator] = []
            signals_by_indicator[indicator].append(signal)
        
        # 处理每种指标的信号
        processed_signals = []
        for indicator, indicator_signals in signals_by_indicator.items():
            # 按类型进一步分类
            buy_signals = [s for s in indicator_signals if s['type'] == '买入']
            sell_signals = [s for s in indicator_signals if s['type'] == '卖出']
            
            # 记录信号
            logger.info(f"[{stock_code}] {indicator}指标检测到 {len(buy_signals)} 个买入信号和 {len(sell_signals)} 个卖出信号")
            
            # 处理买入信号
            if buy_signals:
                # 取第一个买入信号执行
                first_buy = buy_signals[0]
                success = self.executor.execute_buy(
                    stock_code, 
                    indicator,
                    price=first_buy.get('price')
                )
                
                if success:
                    processed_signals.append({
                        'type': '买入',
                        'indicator': indicator,
                        'details': first_buy.get('details', ''),
                        'status': 'success'
                    })
            
            # 处理卖出信号
            if sell_signals:
                # 取第一个卖出信号执行
                first_sell = sell_signals[0]
                success = self.executor.execute_sell(
                    stock_code,
                    indicator,
                    price=first_sell.get('price')
                )
                
                if success:
                    processed_signals.append({
                        'type': '卖出',
                        'indicator': indicator,
                        'details': first_sell.get('details', ''),
                        'status': 'success'
                    })
        
        return {
            "status": "processed",
            "message": f"处理了{len(processed_signals)}个信号",
            "processed_signals": processed_signals
        }
    
    def run_monitoring(self):
        """
        运行监控，定期检测信号并处理
        """
        import time
        
        logger.info("开始运行交易监控")
        print("交易引擎监控已启动")
        print(f"监控股票池: {self.stock_pool}")
        print(f"监控间隔: {self.monitor_interval}秒")
        
        try:
            while True:
                current_time = datetime.now().time()
                
                # 检查是否在交易时间内
                is_trading_time = self._is_trading_time(current_time)
                
                if is_trading_time:
                    print(f"\n[{datetime.now().strftime('%H:%M:%S')}] 正在检测信号...")
                    
                    # 检测并处理每个股票的信号
                    for stock_code in self.stock_pool:
                        signals = self.detect_signals(stock_code)
                        if signals:
                            result = self.process_signals(stock_code, signals)
                            logger.info(f"股票{stock_code}信号处理结果: {result['message']}")
                else:
                    print(f"\n[{datetime.now().strftime('%H:%M:%S')}] 非交易时间，暂停监控")
                    
                # 等待下一次检测
                time.sleep(self.monitor_interval)
                
        except KeyboardInterrupt:
            logger.info("交易监控被用户中断")
            print("交易监控已停止")
        except Exception as e:
            logger.error(f"交易监控运行出错: {e}")
            print(f"交易监控运行出错: {e}")
    
    def _is_trading_time(self, current_time):
        """
        判断是否在交易时间内
        
        参数:
        current_time: 当前时间
        
        返回:
        bool: 是否在交易时间内
        """
        # 交易时间段：9:30-11:30 和 13:00-15:00
        morning_start = datetime.strptime('09:30', '%H:%M').time()
        morning_end = datetime.strptime('11:30', '%H:%M').time()
        afternoon_start = datetime.strptime('13:00', '%H:%M').time()
        afternoon_end = datetime.strptime('15:00', '%H:%M').time()
        
        morning_session = morning_start <= current_time <= morning_end
        afternoon_session = afternoon_start <= current_time <= afternoon_end
        
        return morning_session or afternoon_session


if __name__ == "__main__":
    # 测试交易引擎
    engine = TradeEngine()
    engine.run_monitoring()