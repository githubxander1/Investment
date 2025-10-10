# T0交易系统交易执行模块
import sys
import os
from datetime import datetime

# 添加项目根目录到路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# 复用AutoTrade的交易逻辑
try:
    from Investment.THS.AutoTrade.pages.trading.trade_logic import TradeLogic
    from Investment.THS.AutoTrade.pages.base.page_common import CommonPage
    AUTO_TRADE_AVAILABLE = True
except ImportError:
    AUTO_TRADE_AVAILABLE = False
    TradeLogic = None
    CommonPage = None

from config.settings import TRADE_QUANTITY
from utils.logger import setup_logger

logger = setup_logger('trade_executor')

class TradeExecutor:
    """交易执行器"""
    
    def __init__(self):
        # 这里可以初始化与交易相关的配置
        self.executed_signals = set()  # 记录已执行的信号
        self.account_name = "中泰证券"  # 默认使用中泰证券账户
        
        # 初始化交易逻辑（如果AutoTrade可用）
        if AUTO_TRADE_AVAILABLE:
            try:
                self.trade_logic = TradeLogic()
                self.common_page = CommonPage()
                logger.info("成功初始化AutoTrade交易逻辑")
            except Exception as e:
                logger.error(f"初始化AutoTrade交易逻辑失败: {e}")
                self.trade_logic = None
                self.common_page = None
        else:
            self.trade_logic = None
            self.common_page = None
            logger.warning("AutoTrade交易逻辑不可用，将使用模拟交易")
        
    def execute_buy(self, stock_code, indicator_name, price=None):
        """执行买入交易"""
        signal_key = f"{stock_code}_{indicator_name}_buy"
        
        if signal_key in self.executed_signals:
            logger.info(f"[{stock_code}] 买入信号 {signal_key} 已执行过，跳过")
            return False
            
        # 执行买入交易逻辑
        logger.info(f"[{stock_code}] 执行买入交易: 股票={stock_code}, 指标={indicator_name}, 数量={TRADE_QUANTITY}, 价格={price}")
        print(f"💰 [{stock_code}] 执行买入交易: 股票={stock_code}, 指标={indicator_name}, 数量={TRADE_QUANTITY}")
        
        # 如果有AutoTrade交易逻辑，则实际执行交易
        if self.trade_logic and self.common_page:
            try:
                # 切换到指定账户
                logger.info(f"[{stock_code}] 切换到账户: {self.account_name}")
                print(f"🔄 [{stock_code}] 切换到账户: {self.account_name}")
                self.common_page.change_account(self.account_name)
                
                # 执行买入操作
                success, info = self.trade_logic.operate_stock(
                    operation="买入",
                    stock_name=stock_code,
                    volume=TRADE_QUANTITY
                )
                
                if success:
                    logger.info(f"[{stock_code}] 买入交易成功: {stock_code} {TRADE_QUANTITY}股")
                    print(f"✅ [{stock_code}] 买入交易成功: {stock_code} {TRADE_QUANTITY}股")
                else:
                    logger.error(f"[{stock_code}] 买入交易失败: {info}")
                    print(f"❌ [{stock_code}] 买入交易失败: {info}")
            except Exception as e:
                logger.error(f"[{stock_code}] 执行买入交易时发生异常: {e}")
                print(f"❌ [{stock_code}] 执行买入交易时发生异常: {e}")
        else:
            # 模拟交易（用于测试）
            logger.info(f"[{stock_code}] 模拟买入交易: 股票={stock_code}, 指标={indicator_name}, 数量={TRADE_QUANTITY}, 价格={price}")
            print(f"🧪 [{stock_code}] 模拟买入交易: 股票={stock_code}, 指标={indicator_name}, 数量={TRADE_QUANTITY}")
        
        # 记录已执行的信号
        self.executed_signals.add(signal_key)
        
        return True
    
    def execute_sell(self, stock_code, indicator_name, price=None):
        """执行卖出交易"""
        signal_key = f"{stock_code}_{indicator_name}_sell"
        
        if signal_key in self.executed_signals:
            logger.info(f"[{stock_code}] 卖出信号 {signal_key} 已执行过，跳过")
            return False
            
        # 执行卖出交易逻辑
        logger.info(f"[{stock_code}] 执行卖出交易: 股票={stock_code}, 指标={indicator_name}, 数量={TRADE_QUANTITY}, 价格={price}")
        print(f"💰 [{stock_code}] 执行卖出交易: 股票={stock_code}, 指标={indicator_name}, 数量={TRADE_QUANTITY}")
        
        # 如果有AutoTrade交易逻辑，则实际执行交易
        if self.trade_logic and self.common_page:
            try:
                # 切换到指定账户
                logger.info(f"[{stock_code}] 切换到账户: {self.account_name}")
                print(f"🔄 [{stock_code}] 切换到账户: {self.account_name}")
                self.common_page.change_account(self.account_name)
                
                # 执行卖出操作
                success, info = self.trade_logic.operate_stock(
                    operation="卖出",
                    stock_name=stock_code,
                    volume=TRADE_QUANTITY
                )
                
                if success:
                    logger.info(f"[{stock_code}] 卖出交易成功: {stock_code} {TRADE_QUANTITY}股")
                    print(f"✅ [{stock_code}] 卖出交易成功: {stock_code} {TRADE_QUANTITY}股")
                else:
                    logger.error(f"[{stock_code}] 卖出交易失败: {info}")
                    print(f"❌ [{stock_code}] 卖出交易失败: {info}")
            except Exception as e:
                logger.error(f"[{stock_code}] 执行卖出交易时发生异常: {e}")
                print(f"❌ [{stock_code}] 执行卖出交易时发生异常: {e}")
        else:
            # 模拟交易（用于测试）
            logger.info(f"[{stock_code}] 模拟卖出交易: 股票={stock_code}, 指标={indicator_name}, 数量={TRADE_QUANTITY}, 价格={price}")
            print(f"🧪 [{stock_code}] 模拟卖出交易: 股票={stock_code}, 指标={indicator_name}, 数量={TRADE_QUANTITY}")
        
        # 记录已执行的信号
        self.executed_signals.add(signal_key)
        
        return True
    
    def reset_daily_signals(self):
        """重置每日信号记录（在每个交易日开始时调用）"""
        count = len(self.executed_signals)
        self.executed_signals.clear()
        logger.info(f"已重置每日信号记录，清除了 {count} 个已执行信号")