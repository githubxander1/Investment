#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
账户信息管理模块
提供账户信息查询、持仓管理等功能
"""

import os
import sys
import time
import pandas as pd
from typing import Optional, Dict, List, Any

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

# 使用统一的日志记录器
from utils.logger import setup_logger
from utils.common_utils import load_stock_name_map, format_stock_code, ensure_directory
from pages.trading.ths_trade_wrapper import trade_wrapper

logger = setup_logger('account_info.log')


class AccountInfo:
    """
    账户信息管理类
    用于管理账户信息、获取持仓、资金等数据
    """
    
    def __init__(self, account_name: str):
        """
        初始化账户信息管理类
        
        Args:
            account_name: 账户名称
        """
        self.account_name = account_name
        self.trade_api = trade_wrapper
        self.stock_name_map = load_stock_name_map()
        
        # 确保数据目录存在
        self.position_data_dir = 'data/xml/position'
        self.holding_data_dir = 'data/holding'
        ensure_directory(self.position_data_dir)
        ensure_directory(self.holding_data_dir)
        
        # 初始化时切换到指定账户
        self._switch_to_account()
    
    def _switch_to_account(self) -> bool:
        """
        切换到指定账户
        
        Returns:
            bool: 是否切换成功
        """
        return self.trade_api.switch_account(self.account_name)
    
    def verify_account_switch(self) -> bool:
        """
        验证账户是否正确切换
        
        Returns:
            bool: 是否验证通过
        """
        current_account = self.trade_api.get_current_account()
        if current_account != self.account_name:
            logger.warning(f"账户验证失败，当前: {current_account}，预期: {self.account_name}")
            # 尝试重新切换
            return self._switch_to_account()
        return True
    
    def get_buying_power(self) -> float:
        """
        获取可用资金
        
        Returns:
            float: 可用资金金额
        """
        try:
            # 验证账户切换
            if not self.verify_account_switch():
                raise Exception("账户切换失败")
            
            # 直接从交易API获取可用资金
            buying_power = self.trade_api.get_buying_power()
            logger.info(f"账户 {self.account_name} 可用资金: {buying_power}")
            return buying_power
        except Exception as e:
            logger.error(f"获取可用资金失败: {e}")
            return 0.0
    
    def get_stock_available(self, stock_code: str) -> int:
        """
        获取股票可用数量
        
        Args:
            stock_code: 股票代码
            
        Returns:
            int: 可用数量
        """
        try:
            # 验证账户切换
            if not self.verify_account_switch():
                raise Exception("账户切换失败")
            
            # 从交易API获取可用数量
            available = self.trade_api.get_stock_available(stock_code)
            logger.info(f"账户 {self.account_name} 股票 {stock_code} 可用数量: {available}")
            return available
        except Exception as e:
            logger.error(f"获取股票可用数量失败: {e}")
            return 0
    
    def get_account_summary_info(self) -> Dict[str, float]:
        """
        获取账户汇总信息
        
        Returns:
            Dict: 包含总资产、可用资金等信息的字典
        """
        try:
            # 验证账户切换
            if not self.verify_account_switch():
                raise Exception("账户切换失败")
            
            # 从交易API获取资金信息
            balance = self.trade_api.get_balance()
            
            # 构建汇总信息
            summary = {
                '总资产': balance.get('total_assets', 0.0),
                '总市值': balance.get('market_value', 0.0),
                '可用资金': balance.get('available', 0.0),
                '可取资金': balance.get('withdrawable', 0.0),
                '当日盈亏': balance.get('today_profit', 0.0),
                '总盈亏': balance.get('total_profit', 0.0)
            }
            
            logger.info(f"获取账户 {self.account_name} 汇总信息成功")
            return summary
        except Exception as e:
            logger.error(f"获取账户汇总信息失败: {e}")
            return {
                '总资产': 0.0,
                '总市值': 0.0,
                '可用资金': 0.0,
                '可取资金': 0.0,
                '当日盈亏': 0.0,
                '总盈亏': 0.0
            }
    
    def get_account_summary_info_from_file(self, file_path: Optional[str] = None) -> Dict[str, float]:
        """
        从文件读取账户汇总信息（保持接口兼容）
        
        Args:
            file_path: 文件路径（可选）
            
        Returns:
            Dict: 账户汇总信息
        """
        # 为了保持接口兼容，实际还是从API获取
        # 如果文件存在，可以考虑从文件读取作为备份
        logger.info("从文件读取账户汇总信息（保持接口兼容）")
        return self.get_account_summary_info()
    
    def extract_stock_info(self, position_df: pd.DataFrame) -> List[Dict[str, Any]]:
        """
        提取股票信息列表
        
        Args:
            position_df: 持仓数据表格
            
        Returns:
            List[Dict]: 股票信息列表
        """
        stock_info_list = []
        
        if not position_df.empty:
            for _, row in position_df.iterrows():
                stock_info = {
                    'stock_code': format_stock_code(str(row.get('stock_code', ''))),
                    'stock_name': row.get('stock_name', ''),
                    'position': int(row.get('position', 0)),
                    'available': int(row.get('available', 0)),
                    'price': float(row.get('price', 0.0)),
                    'market_value': float(row.get('market_value', 0.0)),
                    'cost_price': float(row.get('cost_price', 0.0)),
                    'profit': float(row.get('profit', 0.0)),
                    'profit_rate': float(row.get('profit_rate', 0.0))
                }
                stock_info_list.append(stock_info)
        
        return stock_info_list
    
    def update_holding_info_for_account(self) -> tuple[Optional[pd.DataFrame], Optional[pd.DataFrame]]:
        """
        更新指定账户的持仓信息
        
        Returns:
            tuple: (账户汇总信息DataFrame, 持仓信息DataFrame)
        """
        try:
            # 验证账户切换
            if not self.verify_account_switch():
                raise Exception("账户切换失败")
            
            logger.info(f"开始更新账户 {self.account_name} 的持仓信息")
            
            # 获取持仓数据
            position_df = self.trade_api.get_position()
            
            # 如果没有持仓，返回空DataFrame
            if position_df.empty:
                logger.info(f"账户 {self.account_name} 无持仓")
                return pd.DataFrame(), pd.DataFrame()
            
            # 提取股票信息
            stock_info_list = self.extract_stock_info(position_df)
            
            # 创建持仓DataFrame
            holding_df = pd.DataFrame(stock_info_list)
            
            # 计算持仓占比
            total_value = holding_df['market_value'].sum()
            if total_value > 0:
                holding_df['占比'] = holding_df['market_value'] / total_value * 100
                holding_df['占比'] = holding_df['占比'].apply(lambda x: f"{x:.2f}%")
            
            # 保存持仓信息到Excel
            holding_file = os.path.join(self.holding_data_dir, f"{self.account_name}_holding.xlsx")
            holding_df.to_excel(holding_file, index=False)
            logger.info(f"持仓信息已保存到: {holding_file}")
            # 打印账户持仓详情
            if not holding_df.empty:
                logger.info(f"账户 {self.account_name} 持仓详情:\n{holding_df.to_string()}")
            
            # 获取账户汇总信息
            account_summary = self.get_account_summary_info()
            
            # 返回账户汇总信息和持仓信息
            summary_df = pd.DataFrame([account_summary])
            return summary_df, holding_df
        
        except Exception as e:
            logger.error(f"更新持仓信息失败: {e}")
            return None, None
    
    def update_holding_info_all(self, account_list: Optional[List[str]] = None) -> Dict[str, pd.DataFrame]:
        """
        更新所有账户的持仓信息
        
        Args:
            account_list: 账户列表，如果为None则更新所有账户
            
        Returns:
            Dict: 各账户的持仓数据字典
        """
        result_dict = {}
        
        # 如果没有指定账户列表，使用当前账户
        if not account_list:
            account_list = [self.account_name]
        
        for account_name in account_list:
            try:
                # 切换到指定账户
                temp_account = AccountInfo(account_name)
                # 更新持仓信息
                holding_df = temp_account.update_holding_info_for_account()
                if holding_df is not None:
                    result_dict[account_name] = holding_df
            except Exception as e:
                logger.error(f"更新账户 {account_name} 持仓信息失败: {e}")
        
        # 汇总所有账户持仓到一个文件
        self._update_account_summary(result_dict)
        
        return result_dict
    
    def _update_account_summary(self, holding_dict: Dict[str, pd.DataFrame]) -> None:
        """
        更新账户汇总信息
        
        Args:
            holding_dict: 各账户的持仓数据字典
        """
        try:
            summary_list = []
            
            # 汇总每个账户的信息
            for account_name, holding_df in holding_dict.items():
                account_info = AccountInfo(account_name)
                account_summary = account_info.get_account_summary_info()
                
                # 计算持仓数量
                stock_count = len(holding_df)
                
                summary_info = {
                    '账户名称': account_name,
                    '总资产': account_summary.get('总资产', 0.0),
                    '总市值': account_summary.get('总市值', 0.0),
                    '可用资金': account_summary.get('可用资金', 0.0),
                    '持仓数量': stock_count,
                    '当日盈亏': account_summary.get('当日盈亏', 0.0),
                    '总盈亏': account_summary.get('总盈亏', 0.0)
                }
                
                summary_list.append(summary_info)
            
            # 保存汇总信息
            if summary_list:
                summary_df = pd.DataFrame(summary_list)
                summary_file = os.path.join(self.holding_data_dir, "account_summary.xlsx")
                summary_df.to_excel(summary_file, index=False)
                logger.info(f"账户汇总信息已保存到: {summary_file}")
        
        except Exception as e:
            logger.error(f"更新账户汇总信息失败: {e}")


# 测试代码
if __name__ == "__main__":
    # 请替换为实际的账户名称
    test_account = "川财证券"
    
    try:
        account_info = AccountInfo(test_account)
        
        # 获取可用资金
        buying_power = account_info.get_buying_power()
        print(f"可用资金: {buying_power}")
        
        # 获取账户汇总信息
        summary = account_info.get_account_summary_info()
        print("账户汇总信息:")
        for key, value in summary.items():
            print(f"{key}: {value}")
        
        # 更新持仓信息
        holding_df = account_info.update_holding_info_for_account()
        if holding_df is not None and not holding_df.empty:
            print("持仓信息:")
            print(holding_df)
    
    except Exception as e:
        print(f"测试失败: {e}")