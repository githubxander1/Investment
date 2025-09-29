# T0交易系统交易执行模块
import sys
import os

# 添加项目根目录到路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.settings import TRADE_QUANTITY
from utils.logger import setup_logger

logger = setup_logger('trade_executor')

class TradeExecutor:
    """交易执行器"""
    
    def __init__(self):
        # 这里可以初始化与交易相关的配置
        self.executed_signals = set()  # 记录已执行的信号
        
    def execute_buy(self, stock_code, indicator_name, price=None):
        """执行买入交易"""
        signal_key = f"{stock_code}_{indicator_name}_buy"
        
        if signal_key in self.executed_signals:
            logger.info(f"买入信号 {signal_key} 已执行过，跳过")
            return False
            
        # 执行买入交易逻辑（示例）
        logger.info(f"执行买入交易: 股票={stock_code}, 指标={indicator_name}, 数量={TRADE_QUANTITY}, 价格={price}")
        
        # 这里应该集成实际的交易接口
        # 例如调用券商API或自动化交易系统
        
        # 记录已执行的信号
        self.executed_signals.add(signal_key)
        
        return True
    
    def execute_sell(self, stock_code, indicator_name, price=None):
        """执行卖出交易"""
        signal_key = f"{stock_code}_{indicator_name}_sell"
        
        if signal_key in self.executed_signals:
            logger.info(f"卖出信号 {signal_key} 已执行过，跳过")
            return False
            
        # 执行卖出交易逻辑（示例）
        logger.info(f"执行卖出交易: 股票={stock_code}, 指标={indicator_name}, 数量={TRADE_QUANTITY}, 价格={price}")
        
        # 这里应该集成实际的交易接口
        # 例如调用券商API或自动化交易系统
        
        # 记录已执行的信号
        self.executed_signals.add(signal_key)
        
        return True
    
    def reset_daily_signals(self):
        """重置每日信号记录（在每个交易日开始时调用）"""
        self.executed_signals.clear()
        logger.info("已重置每日信号记录")