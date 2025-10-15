#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
通用页面操作模块
提供页面切换、账户切换等通用功能
"""

import time
from typing import Optional, Dict, List, Any

# 使用统一的日志记录器
from Investment.THS.ths_trade.utils.logger import setup_logger
from Investment.THS.ths_trade.pages.trading.ths_trade_wrapper import trade_wrapper

logger = setup_logger('page_common.log')


class CommonPage:
    """
    通用页面操作类
    提供页面切换、账户切换等通用功能
    """
    
    def __init__(self):
        """
        初始化通用页面操作类
        """
        self.trade_api = trade_wrapper
        self.current_account = None
    
    def switch_to_next_account(self, accounts: List[str], current_account: Optional[str] = None) -> Optional[str]:
        """
        切换到下一个账户
        
        Args:
            accounts: 账户列表
            current_account: 当前账户名称
            
        Returns:
            Optional[str]: 切换后的账户名称
        """
        try:
            if not accounts:
                logger.error("账户列表为空")
                return None
            
            # 如果未指定当前账户，使用第一个账户
            if not current_account:
                next_account = accounts[0]
            else:
                # 查找当前账户在列表中的索引
                try:
                    current_index = accounts.index(current_account)
                    # 切换到下一个账户，如果是最后一个则切换到第一个
                    next_index = (current_index + 1) % len(accounts)
                    next_account = accounts[next_index]
                except ValueError:
                    logger.warning(f"当前账户不在列表中: {current_account}")
                    next_account = accounts[0]
            
            # 执行账户切换
            success = self.change_account(next_account)
            if success:
                self.current_account = next_account
                logger.info(f"成功切换到下一个账户: {next_account}")
                return next_account
            else:
                logger.error(f"切换账户失败: {next_account}")
                return None
                
        except Exception as e:
            logger.error(f"切换到下一个账户失败: {e}")
            return None
    
    def change_account(self, account_name: str, force_reinit: bool = False) -> bool:
        """
        切换账户
        
        Args:
            account_name: 账户名称
            force_reinit: 是否强制重新初始化
            
        Returns:
            bool: 是否切换成功
        """
        try:
            logger.info(f"开始切换账户: {account_name}，强制重新初始化: {force_reinit}")
            
            # 使用交易API切换账户
            success = self.trade_api.switch_account(account_name, force_reinit)
            
            if success:
                self.current_account = account_name
                logger.info(f"账户切换成功: {account_name}")
            else:
                logger.error(f"账户切换失败: {account_name}")
            
            return success
            
        except Exception as e:
            logger.error(f"切换账户异常: {e}")
            return False
    
    def get_account_list(self) -> List[Dict[str, str]]:
        """
        获取账户列表
        
        Returns:
            List[Dict]: 账户列表
        """
        try:
            accounts = self.trade_api.get_account_list()
            logger.info(f"成功获取账户列表，共 {len(accounts)} 个账户")
            return accounts
        except Exception as e:
            logger.error(f"获取账户列表失败: {e}")
            return []
    
    def is_account_valid(self, account_name: str) -> bool:
        """
        验证账户是否有效
        
        Args:
            account_name: 账户名称
            
        Returns:
            bool: 账户是否有效
        """
        try:
            accounts = self.get_account_list()
            return any(acc['account_name'] == account_name for acc in accounts)
        except Exception as e:
            logger.error(f"验证账户有效性失败: {e}")
            return False
    
    def switch_to_trade_page(self) -> bool:
        """
        切换到交易页面（保持接口兼容）
        
        Returns:
            bool: 是否切换成功
        """
        # 在基于API的实现中，这个方法只需要返回True
        logger.info("切换到交易页面（API模式）")
        return True
    
    def switch_to_account_page(self) -> bool:
        """
        切换到账户页面（保持接口兼容）
        
        Returns:
            bool: 是否切换成功
        """
        # 在基于API的实现中，这个方法只需要返回True
        logger.info("切换到账户页面（API模式）")
        return True
    
    def wait_for_page_load(self, timeout: int = 5) -> bool:
        """
        等待页面加载完成（保持接口兼容）
        
        Args:
            timeout: 超时时间（秒）
            
        Returns:
            bool: 是否加载完成
        """
        # 在基于API的实现中，这个方法只需要短暂等待后返回True
        time.sleep(0.5)
        logger.info("页面加载完成（API模式）")
        return True
    
    def safe_click(self, element_selector: str, max_retries: int = 3) -> bool:
        """
        安全点击操作（保持接口兼容）
        
        Args:
            element_selector: 元素选择器
            max_retries: 最大重试次数
            
        Returns:
            bool: 是否点击成功
        """
        # 在基于API的实现中，这个方法只需要返回True
        logger.info(f"安全点击元素: {element_selector}（API模式）")
        return True
    
    def is_page_active(self, page_name: str) -> bool:
        """
        检查页面是否处于活动状态（保持接口兼容）
        
        Args:
            page_name: 页面名称
            
        Returns:
            bool: 页面是否活动
        """
        # 在基于API的实现中，我们假设所有页面都是活动的
        logger.info(f"检查页面活动状态: {page_name}（API模式）")
        return True


# 测试代码
if __name__ == "__main__":
    try:
        common_page = CommonPage()
        
        # 获取账户列表
        accounts = common_page.get_account_list()
        print(f"可用账户数量: {len(accounts)}")
        for account in accounts:
            print(f"账户名称: {account.get('account_name')}")
        
        # 测试切换账户（如果有账户的话）
        if accounts:
            test_account = accounts[0]['account_name']
            success = common_page.change_account(test_account)
            print(f"切换到账户 {test_account}: {'成功' if success else '失败'}")
        
    except Exception as e:
        print(f"测试失败: {e}")