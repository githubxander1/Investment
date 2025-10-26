import os
import sys
import time
import schedule
import threading
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple, Any
import pandas as pd

# 添加项目根目录到系统路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# 导入指标接口模块
try:
    from core.indicator_interface import get_indicator_manager, IndicatorProtocol
    INDICATORS_AVAILABLE = True
except ImportError as e:
    print(f"导入指标接口模块失败: {e}")
    INDICATORS_AVAILABLE = False

class AutoTrader:
    def __init__(self, config: Dict[str, Any]):
        """
        自动交易系统初始化
        
        Args:
            config: 交易配置参数
        """
        self.config = config
        self.stock_codes = config.get('stock_codes', ['000333'])
        self.indicator_type = config.get('indicator_type', 'resistance_support')  # 可选: resistance_support, volume_price, extended
        self.trading_enabled = config.get('trading_enabled', False)  # 控制是否实际执行交易
        self.check_interval = config.get('check_interval', 60)  # 检查间隔（秒）
        self.is_running = False
        self.trade_log = []
        self.scheduler_thread = None
        
        # 交易状态跟踪
        self.position = {code: 0 for code in self.stock_codes}  # 股票持仓
        self.trade_history = {code: [] for code in self.stock_codes}  # 交易历史
        
        # 初始化指标管理器
        self.indicator_manager = None
        if INDICATORS_AVAILABLE:
            self.indicator_manager = get_indicator_manager()
            self.set_indicator(self.indicator_type)
        
        print(f"自动交易系统初始化完成 - 指标类型: {self.indicator_type}, 监控股票: {self.stock_codes}")
    
    def set_indicator(self, indicator_type: str) -> bool:
        """
        设置使用的指标类型
        
        Args:
            indicator_type: 指标类型
        
        Returns:
            是否设置成功
        """
        if self.indicator_manager:
            success = self.indicator_manager.set_indicator(indicator_type)
            if success:
                self.indicator_type = indicator_type
                print(f"已切换到指标: {self.indicator_manager.current_indicator.get_name()}")
            return success
        return False
    
    def start(self):
        """启动自动交易系统"""
        if not INDICATORS_AVAILABLE:
            print("错误: 指标模块不可用，无法启动自动交易系统")
            return
        
        self.is_running = True
        print(f"自动交易系统启动 - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        # 设置交易时段定时任务
        self._setup_trading_schedule()
        
        # 启动定时任务线程
        self.scheduler_thread = threading.Thread(target=self._run_scheduler)
        self.scheduler_thread.daemon = True
        self.scheduler_thread.start()
        
        print("定时任务已启动，将在交易时段内自动监控市场")
    
    def stop(self):
        """停止自动交易系统"""
        self.is_running = False
        print(f"自动交易系统停止 - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        # 打印交易摘要
        self._print_trade_summary()
    
    def _setup_trading_schedule(self):
        """设置交易时段的定时任务"""
        # 上午交易时段: 9:30-11:30
        schedule.every().monday.at("09:30").do(self._start_morning_trading)
        schedule.every().tuesday.at("09:30").do(self._start_morning_trading)
        schedule.every().wednesday.at("09:30").do(self._start_morning_trading)
        schedule.every().thursday.at("09:30").do(self._start_morning_trading)
        schedule.every().friday.at("09:30").do(self._start_morning_trading)
        
        schedule.every().monday.at("11:30").do(self._end_morning_trading)
        schedule.every().tuesday.at("11:30").do(self._end_morning_trading)
        schedule.every().wednesday.at("11:30").do(self._end_morning_trading)
        schedule.every().thursday.at("11:30").do(self._end_morning_trading)
        schedule.every().friday.at("11:30").do(self._end_morning_trading)
        
        # 下午交易时段: 13:00-15:00
        schedule.every().monday.at("13:00").do(self._start_afternoon_trading)
        schedule.every().tuesday.at("13:00").do(self._start_afternoon_trading)
        schedule.every().wednesday.at("13:00").do(self._start_afternoon_trading)
        schedule.every().thursday.at("13:00").do(self._start_afternoon_trading)
        schedule.every().friday.at("13:00").do(self._start_afternoon_trading)
        
        schedule.every().monday.at("15:00").do(self._end_afternoon_trading)
        schedule.every().tuesday.at("15:00").do(self._end_afternoon_trading)
        schedule.every().wednesday.at("15:00").do(self._end_afternoon_trading)
        schedule.every().thursday.at("15:00").do(self._end_afternoon_trading)
        schedule.every().friday.at("15:00").do(self._end_afternoon_trading)
    
    def _run_scheduler(self):
        """运行定时任务的线程函数"""
        while self.is_running:
            schedule.run_pending()
            time.sleep(1)
    
    def _start_morning_trading(self):
        """开始上午交易时段"""
        print(f"=== 上午交易时段开始 - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ===")
        self._monitor_market()
    
    def _end_morning_trading(self):
        """结束上午交易时段"""
        print(f"=== 上午交易时段结束 - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ===")
    
    def _start_afternoon_trading(self):
        """开始下午交易时段"""
        print(f"=== 下午交易时段开始 - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ===")
        self._monitor_market()
    
    def _end_afternoon_trading(self):
        """结束下午交易时段"""
        print(f"=== 下午交易时段结束 - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ===")
        # 可选：在收盘前清理持仓
        if self.config.get('close_positions_at_end', False):
            self._close_all_positions()
    
    def _monitor_market(self):
        """监控市场并生成交易信号"""
        # 在实际交易时段内，创建一个监控线程
        monitor_thread = threading.Thread(target=self._continuous_monitoring)
        monitor_thread.daemon = True
        monitor_thread.start()
    
    def _continuous_monitoring(self):
        """持续监控市场，直到交易时段结束"""
        now = datetime.now()
        
        # 确定当前交易时段的结束时间
        if 9 <= now.hour < 12:
            end_time = now.replace(hour=11, minute=30, second=0, microsecond=0)
        elif 13 <= now.hour < 15:
            end_time = now.replace(hour=15, minute=0, second=0, microsecond=0)
        else:
            return  # 不在交易时段
        
        print(f"开始持续监控市场，将在 {end_time.strftime('%H:%M:%S')} 结束")
        
        while self.is_running and datetime.now() < end_time:
            # 分析每只股票
            for stock_code in self.stock_codes:
                try:
                    self._analyze_stock(stock_code)
                except Exception as e:
                    print(f"分析股票 {stock_code} 时出错: {e}")
            
            # 等待下一次检查
            time.sleep(self.check_interval)
    
    def _analyze_stock(self, stock_code: str):
        """分析单只股票并生成交易信号"""
        today = datetime.now().strftime('%Y-%m-%d')
        
        print(f"分析股票: {stock_code}, 日期: {today}")
        
        # 使用指标管理器进行统一分析
        if self.indicator_manager and self.indicator_manager.current_indicator:
            try:
                df = self.indicator_manager.analyze(stock_code, today)
                if df is not None:
                    signals = self.indicator_manager.detect_signals(df)
                    self._process_signals(stock_code, signals, df)
                    
                    # 绘制并保存图表
                    chart_path = self.indicator_manager.plot(stock_code, today)
                    if chart_path:
                        print(f"图表已保存至: {chart_path}")
            except Exception as e:
                print(f"使用指标管理器分析股票 {stock_code} 时出错: {e}")
    
    def _process_signals(self, stock_code: str, signals: Dict[str, List], df: pd.DataFrame):
        """处理交易信号"""
        current_time = datetime.now()
        # 尝试多种可能的价格列名
        if 'close' in df.columns:
            current_price = df['close'].iloc[-1] if not df.empty else 0
        elif '收盘' in df.columns:
            current_price = df['收盘'].iloc[-1] if not df.empty else 0
        elif 'price' in df.columns:
            current_price = df['price'].iloc[-1] if not df.empty else 0
        elif '价格' in df.columns:
            current_price = df['价格'].iloc[-1] if not df.empty else 0
        else:
            current_price = 0
        
        # 处理买入信号
        if signals.get('buy_signals') and len(signals['buy_signals']) > 0:
            latest_buy = signals['buy_signals'][-1]
            # 检查信号是否足够新（例如：5分钟内）
            time_diff = (current_time - latest_buy).total_seconds()
            if time_diff <= 300 and self.position[stock_code] == 0:  # 无持仓时买入
                self._execute_buy(stock_code, current_price)
        
        # 处理卖出信号
        if signals.get('sell_signals') and len(signals['sell_signals']) > 0:
            latest_sell = signals['sell_signals'][-1]
            # 检查信号是否足够新
            time_diff = (current_time - latest_sell).total_seconds()
            if time_diff <= 300 and self.position[stock_code] > 0:  # 有持仓时卖出
                self._execute_sell(stock_code, current_price)
    

    
    def _execute_buy(self, stock_code: str, price: float):
        """执行买入操作"""
        trade_time = datetime.now()
        quantity = self.config.get('trade_quantity', 100)  # 默认买入100股
        
        trade_info = {
            'time': trade_time,
            'type': 'BUY',
            'code': stock_code,
            'price': price,
            'quantity': quantity,
            'amount': price * quantity
        }
        
        print(f"[{trade_time.strftime('%H:%M:%S')}] 买入信号: {stock_code} @ {price:.2f}, 数量: {quantity}")
        
        if self.trading_enabled:
            # 这里应该调用实际的交易API
            # 示例：self.trade_api.buy(stock_code, quantity, price)
            self.position[stock_code] += quantity
            self.trade_history[stock_code].append(trade_info)
            self.trade_log.append(trade_info)
            print(f"✅ 买入执行成功: {stock_code}, 持仓: {self.position[stock_code]}")
        else:
            print("⚠️ 模拟交易模式，未实际执行买入")
    
    def _execute_sell(self, stock_code: str, price: float):
        """执行卖出操作"""
        trade_time = datetime.now()
        quantity = self.position[stock_code]  # 卖出全部持仓
        
        trade_info = {
            'time': trade_time,
            'type': 'SELL',
            'code': stock_code,
            'price': price,
            'quantity': quantity,
            'amount': price * quantity
        }
        
        print(f"[{trade_time.strftime('%H:%M:%S')}] 卖出信号: {stock_code} @ {price:.2f}, 数量: {quantity}")
        
        if self.trading_enabled and quantity > 0:
            # 这里应该调用实际的交易API
            # 示例：self.trade_api.sell(stock_code, quantity, price)
            self.position[stock_code] = 0
            self.trade_history[stock_code].append(trade_info)
            self.trade_log.append(trade_info)
            print(f"✅ 卖出执行成功: {stock_code}, 持仓: {self.position[stock_code]}")
        else:
            print("⚠️ 模拟交易模式，未实际执行卖出")
    
    def _close_all_positions(self):
        """平仓所有持仓"""
        print("开始平仓所有持仓...")
        for stock_code, quantity in self.position.items():
            if quantity > 0:
                # 这里需要获取最新价格
                # 简化处理，使用模拟价格
                current_price = 0  # 实际应该从市场获取
                print(f"收盘前平仓: {stock_code}, 数量: {quantity}")
                if self.trading_enabled:
                    self.position[stock_code] = 0
        print("平仓操作完成")
    
    def _print_trade_summary(self):
        """打印交易摘要"""
        print("\n=== 交易摘要 ===")
        print(f"总交易次数: {len(self.trade_log)}")
        
        for stock_code, history in self.trade_history.items():
            if history:
                print(f"\n股票: {stock_code}")
                print(f"交易次数: {len(history)}")
                print("交易记录:")
                for trade in history:
                    print(f"  {trade['time'].strftime('%Y-%m-%d %H:%M:%S')} | {trade['type']} | {trade['price']:.2f} | {trade['quantity']} | {trade['amount']:.2f}")
        
        print("\n当前持仓:")
        for stock_code, quantity in self.position.items():
            if quantity > 0:
                print(f"  {stock_code}: {quantity}股")

# 示例配置
DEFAULT_CONFIG = {
    'stock_codes': ['000333'],  # 监控的股票代码列表
    'indicator_type': 'resistance_support',  # 使用的指标类型
    'trading_enabled': False,  # 是否启用实际交易
    'check_interval': 60,  # 检查间隔（秒）
    'trade_quantity': 100,  # 每次交易数量
    'close_positions_at_end': True  # 是否在收盘前平仓
}

if __name__ == "__main__":
    # 示例运行
    trader = AutoTrader(DEFAULT_CONFIG)
    trader.start()
    
    try:
        # 保持程序运行
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n接收到停止信号")
    finally:
        trader.stop()