#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
同花顺交易包装器
为AutoTrade项目提供基于ths_trade的交易功能
"""

import sys
import os
import logging
from typing import Tuple, Optional

# 添加项目根目录到路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))

# 设置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('ths_trade_wrapper')

# 尝试导入新的适配器
try:
    from Investment.THS.ths_trade.applications.adapter.ths_trade_adapter import THSTradeAdapter
    THS_ADAPTER_AVAILABLE = True
except ImportError as e:
    logger.error(f"导入THS适配器失败: {e}")
    THS_ADAPTER_AVAILABLE = False


class THSTradeWrapper:
    """
    为AutoTrade项目提供的同花顺交易包装器
    与原有的Android模拟器交易方式兼容，但使用ths_trade进行实际交易
    """
    
    def __init__(self, account_name: str = "默认账户"):
        """
        初始化交易包装器
        
        Args:
            account_name: 账户名称
        """
        self.account_name = account_name
        self.adapter = None
        self.initialized = False
        
        # 初始化适配器
        if THS_ADAPTER_AVAILABLE:
            try:
                self.adapter = THSTradeAdapter(account_name=account_name)
                self.initialized = self.adapter.initialized
                if self.initialized:
                    logger.info(f"✅ THS交易包装器初始化成功 - 账户: {account_name}")
                else:
                    logger.error(f"❌ THS交易包装器初始化失败 - 账户: {account_name}")
            except Exception as e:
                logger.error(f"❌ THS交易包装器初始化异常: {e}")
                self.initialized = False
        else:
            logger.error("❌ THS适配器不可用")
    
    def operate_stock(self, operation: str, stock_name: str, volume: int,
                     new_ratio: Optional[float] = None, stock_code: Optional[str] = None) -> Tuple[bool, str]:
        """
        操作股票（买入/卖出）
        
        Args:
            operation: 操作类型，"买入"或"卖出"
            stock_name: 股票名称
            volume: 交易数量
            new_ratio: 新比例（仅卖出时使用）
            stock_code: 股票代码（可选，如果提供会更准确）
            
        Returns:
            Tuple[bool, str]: (是否成功, 信息)
        """
        if not self.initialized or not self.adapter:
            return False, "交易包装器未初始化成功"
        
        # 如果没有提供股票代码，尝试从股票名称中提取
        if not stock_code:
            # 这里可以添加从股票名称提取代码的逻辑，暂时使用名称作为代码
            stock_code = stock_name
            logger.warning(f"未提供股票代码，使用股票名称作为代码: {stock_name}")
        
        try:
            # 执行交易
            if operation == "买入":
                result = self.adapter.buy_stock(
                    stock_code=stock_code,
                    stock_name=stock_name,
                    amount=volume,
                    strategy_no="AutoTrade"
                )
            elif operation == "卖出":
                result = self.adapter.sell_stock(
                    stock_code=stock_code,
                    stock_name=stock_name,
                    amount=volume,
                    strategy_no="AutoTrade"
                )
            else:
                return False, f"不支持的操作类型: {operation}"
            
            # 处理结果
            if result["success"]:
                return True, result.get("msg", "操作成功")
            else:
                return False, result.get("msg", "操作失败")
                
        except Exception as e:
            logger.error(f"❌ 股票操作异常: {str(e)}", exc_info=True)
            return False, f"操作异常: {str(e)}"
    
    def get_account_position(self) -> Optional[object]:
        """
        获取账户持仓
        
        Returns:
            Optional[DataFrame]: 持仓数据
        """
        if not self.initialized or not self.adapter:
            logger.error("交易包装器未初始化成功")
            return None
        
        try:
            return self.adapter.get_position()
        except Exception as e:
            logger.error(f"❌ 获取持仓异常: {str(e)}", exc_info=True)
            return None
    
    def get_account_balance(self) -> Optional[object]:
        """
        获取账户资金
        
        Returns:
            Optional[DataFrame]: 资金数据
        """
        if not self.initialized or not self.adapter:
            logger.error("交易包装器未初始化成功")
            return None
        
        try:
            return self.adapter.get_balance()
        except Exception as e:
            logger.error(f"❌ 获取资金异常: {str(e)}", exc_info=True)
            return None
    
    def get_today_trades(self) -> Optional[object]:
        """
        获取今日成交
        
        Returns:
            Optional[DataFrame]: 成交数据
        """
        if not self.initialized or not self.adapter:
            return None
        
        try:
            return self.adapter.get_today_trades()
        except Exception as e:
            logger.error(f"❌ 获取今日成交异常: {str(e)}", exc_info=True)
            return None
    
    def get_today_entrusts(self) -> Optional[object]:
        """
        获取今日委托
        
        Returns:
            Optional[DataFrame]: 委托数据
        """
        if not self.initialized or not self.adapter:
            return None
        
        try:
            return self.adapter.get_today_entrusts()
        except Exception as e:
            logger.error(f"❌ 获取今日委托异常: {str(e)}", exc_info=True)
            return None


if __name__ == "__main__":
    """测试交易包装器"""
    # 初始化包装器
    wrapper = THSTradeWrapper(account_name="测试账户")
    
    # 测试获取持仓
    if wrapper.initialized:
        print("\n=== 测试获取持仓 ===")
        position = wrapper.get_account_position()
        if position is not None:
            print(f"持仓股票数量: {len(position)}")
            print(position.head())
        
        # 注意：实际交易操作请谨慎执行
        # success, info = wrapper.operate_stock("买入", "中国平安", 100, "601318")
        # print(f"买入结果: {success}, 信息: {info}")
    else:
        print("交易包装器初始化失败，无法进行测试")