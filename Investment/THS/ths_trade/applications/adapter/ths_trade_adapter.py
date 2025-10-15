#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
同花顺交易适配器
为AutoTrade和T0项目提供统一的交易接口
"""

import sys
import os
import logging
from datetime import datetime

# 添加项目根目录到路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

# 导入ths_trade核心模块
try:
    from applications.trade.Exec_Auto_Trade import exec_run
    from applications.trade.server.THS_Trader_Server import THSTraderServer
    import applications.API_Config as API_Config
    THS_TRADE_AVAILABLE = True
except ImportError as e:
    logging.error(f"导入ths_trade模块失败: {e}")
    THS_TRADE_AVAILABLE = False

# 设置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('ths_trade_adapter')


class THSTradeAdapter:
    """
    同花顺交易适配器类，提供简洁统一的交易接口
    """
    
    def __init__(self, exe_path=None, account_name=None):
        """
        初始化适配器
        
        Args:
            exe_path: 同花顺交易软件路径，默认使用API_Config中的配置
            account_name: 账户名称，用于日志记录
        """
        self.exe_path = exe_path or (API_Config.cfg['exe_path'] if THS_TRADE_AVAILABLE else None)
        self.account_name = account_name or "默认账户"
        self.ths_trader = None
        self.initialized = False
        
        # 初始化交易客户端
        if THS_TRADE_AVAILABLE:
            try:
                self.ths_trader = THSTraderServer(exe_path=self.exe_path)
                self.initialized = True
                logger.info(f"✅ 同花顺交易客户端初始化成功 - 账户: {self.account_name}")
            except Exception as e:
                logger.error(f"❌ 同花顺交易客户端初始化失败: {e}")
                self.initialized = False
        else:
            logger.error("❌ ths_trade模块不可用")
    
    def _check_initialized(self):
        """检查客户端是否初始化成功"""
        if not self.initialized or not self.ths_trader:
            logger.error("❌ 交易客户端未初始化成功")
            return False
        return True
    
    def buy_stock(self, stock_code, stock_name, amount, strategy_no="default"):
        """
        买入股票
        
        Args:
            stock_code: 股票代码
            stock_name: 股票名称
            amount: 买入数量
            strategy_no: 策略编号
            
        Returns:
            dict: 交易结果
        """
        if not self._check_initialized():
            return {"success": False, "msg": "交易客户端未初始化成功"}
        
        try:
            logger.info(f"📈 [{self.account_name}] 执行买入: {stock_name}({stock_code}) - 数量: {amount}")
            
            # 构建交易请求
            request_item = {
                "operate": "buy",
                "stock_no": stock_code,
                "stock_name": stock_name,
                "amount": amount,
                "strategy_no": strategy_no,
                "key": f"{datetime.now().strftime('%Y%m%d%H%M%S')}_buy_{stock_code}"
            }
            
            # 执行交易
            result = exec_run(request_item)
            
            # 处理结果
            if result and result.get("success"):
                logger.info(f"✅ [{self.account_name}] 买入成功 - 合同号: {result.get('entrust_no')}")
                return {
                    "success": True,
                    "entrust_no": result.get('entrust_no'),
                    "msg": "买入成功"
                }
            else:
                error_msg = result.get("msg", "买入失败") if result else "买入失败"
                logger.error(f"❌ [{self.account_name}] 买入失败: {error_msg}")
                return {
                    "success": False,
                    "msg": error_msg
                }
                
        except Exception as e:
            logger.error(f"❌ [{self.account_name}] 买入异常: {str(e)}", exc_info=True)
            return {"success": False, "msg": f"买入异常: {str(e)}"}
    
    def sell_stock(self, stock_code, stock_name, amount, strategy_no="default"):
        """
        卖出股票
        
        Args:
            stock_code: 股票代码
            stock_name: 股票名称
            amount: 卖出数量
            strategy_no: 策略编号
            
        Returns:
            dict: 交易结果
        """
        if not self._check_initialized():
            return {"success": False, "msg": "交易客户端未初始化成功"}
        
        try:
            logger.info(f"📉 [{self.account_name}] 执行卖出: {stock_name}({stock_code}) - 数量: {amount}")
            
            # 构建交易请求
            request_item = {
                "operate": "sell",
                "stock_no": stock_code,
                "stock_name": stock_name,
                "amount": amount,
                "strategy_no": strategy_no,
                "key": f"{datetime.now().strftime('%Y%m%d%H%M%S')}_sell_{stock_code}"
            }
            
            # 执行交易
            result = exec_run(request_item)
            
            # 处理结果
            if result and result.get("success"):
                logger.info(f"✅ [{self.account_name}] 卖出成功 - 合同号: {result.get('entrust_no')}")
                return {
                    "success": True,
                    "entrust_no": result.get('entrust_no'),
                    "msg": "卖出成功"
                }
            else:
                error_msg = result.get("msg", "卖出失败") if result else "卖出失败"
                logger.error(f"❌ [{self.account_name}] 卖出失败: {error_msg}")
                return {
                    "success": False,
                    "msg": error_msg
                }
                
        except Exception as e:
            logger.error(f"❌ [{self.account_name}] 卖出异常: {str(e)}", exc_info=True)
            return {"success": False, "msg": f"卖出异常: {str(e)}"}
    
    def get_position(self):
        """
        获取持仓信息
        
        Returns:
            pd.DataFrame or None: 持仓数据
        """
        if not self._check_initialized():
            return None
        
        try:
            logger.info(f"📊 [{self.account_name}] 获取持仓信息")
            request_item = {"operate": "get_position"}
            position_data = exec_run(request_item)
            logger.info(f"✅ [{self.account_name}] 持仓数据获取成功 - 股票数量: {len(position_data) if position_data is not None else 0}")
            return position_data
        except Exception as e:
            logger.error(f"❌ [{self.account_name}] 获取持仓异常: {str(e)}", exc_info=True)
            return None
    
    def get_balance(self):
        """
        获取资金情况
        
        Returns:
            pd.DataFrame or None: 资金数据
        """
        if not self._check_initialized():
            return None
        
        try:
            logger.info(f"💰 [{self.account_name}] 获取资金情况")
            request_item = {"operate": "get_balance"}
            balance_data = exec_run(request_item)
            logger.info("✅ 资金数据获取成功")
            return balance_data
        except Exception as e:
            logger.error(f"❌ 获取资金异常: {str(e)}", exc_info=True)
            return None
    
    def get_today_trades(self):
        """
        获取当日成交
        
        Returns:
            pd.DataFrame or None: 当日成交数据
        """
        if not self._check_initialized():
            return None
        
        try:
            logger.info(f"📋 [{self.account_name}] 获取当日成交")
            request_item = {"operate": "get_today_trades"}
            trades_data = exec_run(request_item)
            logger.info(f"✅ 当日成交数据获取成功 - 成交笔数: {len(trades_data) if trades_data is not None else 0}")
            return trades_data
        except Exception as e:
            logger.error(f"❌ 获取当日成交异常: {str(e)}", exc_info=True)
            return None
    
    def get_today_entrusts(self):
        """
        获取当日委托
        
        Returns:
            pd.DataFrame or None: 当日委托数据
        """
        if not self._check_initialized():
            return None
        
        try:
            logger.info(f"📝 [{self.account_name}] 获取当日委托")
            request_item = {"operate": "get_today_entrusts"}
            entrusts_data = exec_run(request_item)
            logger.info(f"✅ 当日委托数据获取成功 - 委托笔数: {len(entrusts_data) if entrusts_data is not None else 0}")
            return entrusts_data
        except Exception as e:
            logger.error(f"❌ 获取当日委托异常: {str(e)}", exc_info=True)
            return None


# 创建一个全局实例，方便导入使用
try:
    ths_adapter = THSTradeAdapter()
except:
    ths_adapter = None


if __name__ == "__main__":
    """测试适配器功能"""
    # 初始化适配器
    adapter = THSTradeAdapter(account_name="测试账户")
    
    # 测试获取持仓
    if adapter.initialized:
        print("\n=== 测试获取持仓 ===")
        position = adapter.get_position()
        if position is not None:
            print(f"持仓股票数量: {len(position)}")
            print(position.head())
        
        print("\n=== 测试获取资金 ===")
        balance = adapter.get_balance()
        if balance is not None:
            print(balance)
    else:
        print("适配器初始化失败，无法进行测试")