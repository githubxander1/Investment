#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
同花顺交易包装器模块
用于封装ths_trade库的功能，提供统一的交易接口
"""

import os
import time
from typing import Optional, Dict, List, Any
import pandas as pd

# 使用统一的日志记录器
from Investment.THS.ths_trade.utils.logger import setup_logger
from Investment.THS.ths_trade.utils.common_utils import retry, get_full_stock_code

logger = setup_logger('ths_trade.log')


class THSTradeWrapper:
    """
    同花顺交易包装器
    封装ths_trade库的功能，提供统一的交易接口
    """
    
    def __init__(self):
        """
        初始化交易包装器
        优先使用增强版适配器
        """
        self.trade_api = None
        self.current_account = None
        self.accounts = []
        self._init_trade_api()
    
    @retry(max_retries=3, delay=2)
    def _init_trade_api(self):
        """
        初始化交易API
        优先尝试导入和使用增强版适配器
        """
        try:
            # 优先使用增强版适配器
            from Investment.THS.ths_trade.applications.adapter.enhanced_ths_trade_adapter import EnhancedTHSTradeAdapter
            self.trade_api = EnhancedTHSTradeAdapter()
            logger.info("成功初始化增强版交易适配器")
        except ImportError:
            logger.warning("无法导入增强版适配器，尝试使用基础适配器")
            try:
                from Investment.THS.ths_trade.applications.adapter.ths_trade_adapter import THSTradeAdapter
                self.trade_api = THSTradeAdapter()
                logger.info("成功初始化基础交易适配器")
            except ImportError as e:
                logger.error(f"初始化交易适配器失败: {e}")
                raise ImportError("无法初始化交易适配器")
        
        # 加载账户列表
        self._load_accounts()
    
    def _load_accounts(self):
        """
        加载可用的账户列表
        """
        try:
            # 从配置中获取账户列表
            self.accounts = self.trade_api.get_account_list()
            logger.info(f"成功加载账户列表，共 {len(self.accounts)} 个账户")
        except Exception as e:
            logger.error(f"加载账户列表失败: {e}")
            self.accounts = []
    
    def switch_account(self, account_name: str, force_reinit: bool = False) -> bool:
        """
        切换账户
        
        Args:
            account_name: 账户名称
            force_reinit: 是否强制重新初始化（适用于账户认证过期等情况）
            
        Returns:
            bool: 是否切换成功
        """
        try:
            # 如果强制重新初始化，先销毁当前实例
            if force_reinit:
                logger.info(f"强制重新初始化账户: {account_name}")
                self._init_trade_api()
            
            # 检查账户是否在列表中
            account_exists = any(acc['account_name'] == account_name for acc in self.accounts)
            if not account_exists:
                logger.error(f"账户不存在: {account_name}")
                return False
            
            # 执行账户切换
            success = self.trade_api.switch_account(account_name)
            if success:
                self.current_account = account_name
                logger.info(f"成功切换到账户: {account_name}")
            else:
                logger.error(f"切换账户失败: {account_name}")
            
            return success
        except Exception as e:
            logger.error(f"切换账户异常: {e}")
            return False
    
    def get_current_account(self) -> Optional[str]:
        """
        获取当前账户名称
        
        Returns:
            str: 当前账户名称，未设置时返回None
        """
        return self.current_account
    
    def get_account_list(self) -> List[Dict[str, str]]:
        """
        获取所有可用账户列表
        
        Returns:
            List[Dict]: 账户列表，每个元素包含账户信息
        """
        return self.accounts
    
    @retry(max_retries=3, delay=1)
    def get_position(self) -> pd.DataFrame:
        """
        获取持仓信息
        
        Returns:
            pd.DataFrame: 持仓信息表格
        """
        try:
            positions = self.trade_api.get_position()
            if positions:
                df = pd.DataFrame(positions)
                logger.info(f"成功获取持仓信息，共 {len(df)} 条记录")
                return df
            else:
                # 返回空的DataFrame
                return pd.DataFrame(columns=['stock_code', 'stock_name', 'position', 'available', 'price', 'market_value'])
        except Exception as e:
            logger.error(f"获取持仓失败: {e}")
            raise
    
    @retry(max_retries=3, delay=1)
    def get_balance(self) -> Dict[str, float]:
        """
        获取资金信息
        
        Returns:
            Dict: 资金信息字典
        """
        try:
            balance = self.trade_api.get_balance()
            logger.info(f"成功获取资金信息")
            return balance
        except Exception as e:
            logger.error(f"获取资金失败: {e}")
            raise
    
    @retry(max_retries=3, delay=1)
    def get_buying_power(self) -> float:
        """
        获取可用资金
        
        Returns:
            float: 可用资金金额
        """
        balance = self.get_balance()
        return balance.get('available', 0.0)
    
    @retry(max_retries=3, delay=1)
    def get_stock_available(self, stock_code: str) -> int:
        """
        获取股票可用数量
        
        Args:
            stock_code: 股票代码
            
        Returns:
            int: 可用数量
        """
        positions = self.get_position()
        if not positions.empty:
            # 转换为带市场前缀的代码进行匹配
            full_code = get_full_stock_code(stock_code)
            stock_positions = positions[positions['stock_code'].str.contains(stock_code)]
            if not stock_positions.empty:
                return int(stock_positions.iloc[0].get('available', 0))
        return 0
    
    @retry(max_retries=3, delay=2)
    def buy_stock(self, stock_code: str, price: float, volume: int) -> Dict[str, Any]:
        """
        买入股票
        
        Args:
            stock_code: 股票代码
            price: 买入价格
            volume: 买入数量
            
        Returns:
            Dict: 交易结果
        """
        try:
            result = self.trade_api.buy(stock_code, price, volume)
            logger.info(f"买入股票: {stock_code}, 价格: {price}, 数量: {volume}, 结果: {result}")
            return result
        except Exception as e:
            logger.error(f"买入股票失败: {e}")
            raise
    
    @retry(max_retries=3, delay=2)
    def sell_stock(self, stock_code: str, price: float, volume: int) -> Dict[str, Any]:
        """
        卖出股票
        
        Args:
            stock_code: 股票代码
            price: 卖出价格
            volume: 卖出数量
            
        Returns:
            Dict: 交易结果
        """
        try:
            result = self.trade_api.sell(stock_code, price, volume)
            logger.info(f"卖出股票: {stock_code}, 价格: {price}, 数量: {volume}, 结果: {result}")
            return result
        except Exception as e:
            logger.error(f"卖出股票失败: {e}")
            raise
    
    @retry(max_retries=3, delay=1)
    def get_orders(self, status: str = 'all') -> pd.DataFrame:
        """
        获取委托信息
        
        Args:
            status: 委托状态，可选值: 'all', 'pending', 'filled', 'cancelled'
            
        Returns:
            pd.DataFrame: 委托信息表格
        """
        try:
            orders = self.trade_api.get_orders(status)
            if orders:
                df = pd.DataFrame(orders)
                logger.info(f"成功获取委托信息，共 {len(df)} 条记录")
                return df
            else:
                return pd.DataFrame(columns=['order_no', 'stock_code', 'stock_name', 'direction', 'price', 'volume', 'status'])
        except Exception as e:
            logger.error(f"获取委托失败: {e}")
            raise
    
    @retry(max_retries=3, delay=1)
    def get_trades(self, start_date: Optional[str] = None, end_date: Optional[str] = None) -> pd.DataFrame:
        """
        获取成交信息
        
        Args:
            start_date: 开始日期 (YYYY-MM-DD)
            end_date: 结束日期 (YYYY-MM-DD)
            
        Returns:
            pd.DataFrame: 成交信息表格
        """
        try:
            trades = self.trade_api.get_trades(start_date, end_date)
            if trades:
                df = pd.DataFrame(trades)
                logger.info(f"成功获取成交信息，共 {len(df)} 条记录")
                return df
            else:
                return pd.DataFrame(columns=['trade_no', 'stock_code', 'stock_name', 'direction', 'price', 'volume', 'trade_time'])
        except Exception as e:
            logger.error(f"获取成交失败: {e}")
            raise


# 创建全局实例
trade_wrapper = THSTradeWrapper()