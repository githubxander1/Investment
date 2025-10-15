# T0交易系统交易执行模块
import sys
import os
import logging
from datetime import datetime

# 添加项目根目录到路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# 使用ths_trade包装器进行交易
from Investment.T0.trading.ths_trade_wrapper import T0THSTradeWrapper

from Investment.T0.config.settings import TRADE_QUANTITY
from Investment.T0.utils.logger import setup_logger
from Investment.T0.utils.tools import is_trading_time
from Investment.T0.utils.signal_handler import SignalHandler

logger = setup_logger('trade_executor')

class TradeExecutor:
    """交易执行器 - 使用T0THSTradeWrapper实现"""
    
    def __init__(self):
        # 这里可以初始化与交易相关的配置
        self.executed_signals = set()  # 记录已执行的信号
        self.account_name = "中泰证券"
        self.signal_handler = SignalHandler()
        
        # 初始化ths_trade包装器
        try:
            self.trade_wrapper = T0THSTradeWrapper(account_name=self.account_name)
            self.trade_available = self.trade_wrapper.is_initialized()
            if self.trade_available:
                logger.info("成功初始化ths_trade交易包装器")
            else:
                logger.warning("ths_trade交易包装器初始化失败，将使用模拟交易")
        except Exception as e:
            logger.error(f"初始化ths_trade交易包装器异常: {e}")
            self.trade_wrapper = None
            self.trade_available = False
            logger.warning("ths_trade交易包装器不可用，将使用模拟交易")
        
    def execute_buy(self, stock_code, indicator_name, price=None, stock_name=None):
        """执行买入交易"""
        signal_key = f"{stock_code}_{indicator_name}_buy"
        
        if signal_key in self.executed_signals:
            logger.info(f"[{stock_code}] 买入信号 {signal_key} 已执行过，跳过")
            return False
        
        # 检查交易时间
        if not is_trading_time():
            logger.warning(f"[{stock_code}] 当前非交易时间，跳过买入交易: {stock_code} {stock_name or ''}")
            return False
            
        # 执行买入交易逻辑
        logger.info(f"[{stock_code}] 执行买入交易: 股票={stock_code}, 指标={indicator_name}, 数量={TRADE_QUANTITY}, 价格={price}")
        print(f"💰 [{stock_code}] 执行买入交易: 股票={stock_code}, 指标={indicator_name}, 数量={TRADE_QUANTITY}")
        
        # 如果有ths_trade包装器，则实际执行交易
        if self.trade_available and self.trade_wrapper:
            try:
                # 执行买入操作
                result = self.trade_wrapper.buy_stock(
                    stock_code=stock_code,
                    stock_name=stock_name or stock_code,
                    quantity=TRADE_QUANTITY,
                    price=price
                )
                
                if result.get("success", False):
                    order_id = result.get("order_id", "N/A")
                    logger.info(f"[{stock_code}] 买入交易成功: {stock_code} {TRADE_QUANTITY}股，合同编号: {order_id}")
                    print(f"✅ [{stock_code}] 买入交易成功: {stock_code} {TRADE_QUANTITY}股")
                    
                    # 记录交易信号
                    signal_data = {
                        "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "stock_code": stock_code,
                        "stock_name": stock_name or "",
                        "operation": "buy",
                        "volume": TRADE_QUANTITY,
                        "price": price or "市价",
                        "result": "success",
                        "contract_no": order_id
                    }
                    self.signal_handler.save_signal(signal_data)
                else:
                    error_msg = result.get("msg", "Unknown error")
                    logger.error(f"[{stock_code}] 买入交易失败: {error_msg}")
                    print(f"❌ [{stock_code}] 买入交易失败: {error_msg}")
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
    
    def execute_sell(self, stock_code, indicator_name, price=None, stock_name=None):
        """执行卖出交易"""
        signal_key = f"{stock_code}_{indicator_name}_sell"
        
        if signal_key in self.executed_signals:
            logger.info(f"[{stock_code}] 卖出信号 {signal_key} 已执行过，跳过")
            return False
        
        # 检查交易时间
        if not is_trading_time():
            logger.warning(f"[{stock_code}] 当前非交易时间，跳过卖出交易: {stock_code} {stock_name or ''}")
            return False
            
        # 执行卖出交易逻辑
        logger.info(f"[{stock_code}] 执行卖出交易: 股票={stock_code}, 指标={indicator_name}, 数量={TRADE_QUANTITY}, 价格={price}")
        print(f"💰 [{stock_code}] 执行卖出交易: 股票={stock_code}, 指标={indicator_name}, 数量={TRADE_QUANTITY}")
        
        # 如果有ths_trade包装器，则实际执行交易
        if self.trade_available and self.trade_wrapper:
            try:
                # 执行卖出操作
                result = self.trade_wrapper.sell_stock(
                    stock_code=stock_code,
                    stock_name=stock_name or stock_code,
                    quantity=TRADE_QUANTITY,
                    price=price
                )
                
                if result.get("success", False):
                    order_id = result.get("order_id", "N/A")
                    logger.info(f"[{stock_code}] 卖出交易成功: {stock_code} {TRADE_QUANTITY}股，合同编号: {order_id}")
                    print(f"✅ [{stock_code}] 卖出交易成功: {stock_code} {TRADE_QUANTITY}股")
                    
                    # 记录交易信号
                    signal_data = {
                        "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "stock_code": stock_code,
                        "stock_name": stock_name or "",
                        "operation": "sell",
                        "volume": TRADE_QUANTITY,
                        "price": price or "市价",
                        "result": "success",
                        "contract_no": order_id
                    }
                    self.signal_handler.save_signal(signal_data)
                else:
                    error_msg = result.get("msg", "Unknown error")
                    logger.error(f"[{stock_code}] 卖出交易失败: {error_msg}")
                    print(f"❌ [{stock_code}] 卖出交易失败: {error_msg}")
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
    
    def close(self):
        """关闭交易执行器"""
        try:
            # 这里不需要关闭特定资源，因为ths_trade适配器会自行处理
            logger.info("交易执行器已关闭")
        except Exception as e:
            logger.error(f"关闭交易执行器异常: {str(e)}")
    
    def execute_trade(self, trade_data: dict) -> bool:
        """
        执行交易的统一入口
        
        Args:
            trade_data: 交易数据字典，包含：
                - stock_code: 股票代码
                - indicator_name: 指标名称
                - operation: 'buy'或'sell'
                - price: 交易价格
                - stock_name: 股票名称（可选）
                
        Returns:
            bool: 交易是否成功执行
        """
        try:
            stock_code = trade_data.get("stock_code")
            indicator_name = trade_data.get("indicator_name")
            operation = trade_data.get("operation", "buy")
            price = trade_data.get("price")
            stock_name = trade_data.get("stock_name")
            
            if not stock_code or not indicator_name:
                logger.error("无效的交易数据：缺少股票代码或指标名称")
                return False
            
            # 根据操作类型执行交易
            if operation.lower() == "buy":
                return self.execute_buy(stock_code, indicator_name, price, stock_name)
            elif operation.lower() == "sell":
                return self.execute_sell(stock_code, indicator_name, price, stock_name)
            else:
                logger.error(f"不支持的操作类型: {operation}")
                return False
                
        except Exception as e:
            logger.error(f"执行交易异常: {str(e)}")
            return False