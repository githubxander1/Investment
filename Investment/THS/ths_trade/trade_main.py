#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
交易主程序模块
提供账户轮询、交易执行等核心功能
"""

import os
import time
import datetime
from typing import Optional, Dict, List, Any
import pandas as pd

# 使用统一的日志记录器
from Investment.THS.ths_trade.utils.logger import setup_logger
from Investment.THS.ths_trade.utils.notification import send_notification
from Investment.THS.ths_trade.utils.common_utils import is_trading_time, ensure_directory
from Investment.THS.ths_trade.pages.base.page_common import CommonPage
from Investment.THS.ths_trade.pages.account.account_info import AccountInfo
from Investment.THS.ths_trade.pages.trading.trade_logic import TradeLogic

logger = setup_logger('trade_main.log')

# 账户列表配置
ACCOUNTS = [
    "川财证券",
    # 可以添加更多账户
]

# 账户策略映射
ACCOUNT_STRATEGY_MAP = {
    "川财证券": ["逻辑为王"],
    # 其他账户的策略映射
}


def is_trading_day() -> bool:
    """
    判断当前是否为交易日
    
    Returns:
        bool: 是否为交易日
    """
    now = datetime.datetime.now()
    
    # 检查是否为周末
    if now.weekday() >= 5:
        logger.info(f"今天是周末，非交易日: {now.strftime('%Y-%m-%d')}")
        return False
    
    # TODO: 可以添加节假日判断逻辑
    # 目前简化处理，只判断是否为工作日
    logger.info(f"今天是交易日: {now.strftime('%Y-%m-%d')}")
    return True


def switch_to_next_account(common_page: CommonPage, 
                          current_account: Optional[str] = None) -> Optional[str]:
    """
    切换到下一个账户
    
    Args:
        common_page: 通用页面操作对象
        current_account: 当前账户
        
    Returns:
        Optional[str]: 切换后的账户名称
    """
    try:
        # 使用通用页面的切换账户方法
        next_account = common_page.switch_to_next_account(ACCOUNTS, current_account)
        
        if next_account:
            logger.info(f"成功切换到账户: {next_account}")
            # 切换账户后，等待一小段时间
            time.sleep(1)
        
        return next_account
        
    except Exception as e:
        logger.error(f"切换账户失败: {e}")
        return None


def execute_guozhai_trades(account_name: str) -> bool:
    """
    执行国债逆回购交易
    
    Args:
        account_name: 账户名称
        
    Returns:
        bool: 是否执行成功
    """
    try:
        logger.info(f"开始执行国债逆回购交易: {account_name}")
        
        # 这里简化处理，实际应该有具体的国债逆回购交易逻辑
        # 例如：检查可用资金，执行204001、131810等国债逆回购品种的交易
        
        # 创建交易逻辑对象
        trade_logic = TradeLogic(account_name)
        
        # 获取可用资金
        account_info = AccountInfo(account_name)
        buying_power = account_info.get_buying_power()
        
        if buying_power < 1000:
            logger.info(f"可用资金不足，无法执行国债逆回购: {buying_power}")
            return True  # 资金不足不算失败
        
        # 示例：执行204001（1天期国债逆回购）
        # 这里使用简化的逻辑，实际应该根据市场利率等因素决定
        guozhai_code = "204001"
        price = 1.5  # 假设价格
        volume = int(buying_power / 1000) * 10  # 国债逆回购以10张为单位，每张100元
        
        if volume >= 10:
            logger.info(f"执行国债逆回购: {guozhai_code}，价格: {price}，数量: {volume}")
            result = trade_logic.buy_stock_with_logic(
                stock_code=guozhai_code,
                price=price,
                volume=volume,
                stock_name="国债逆回购204001"
            )
            
            if result.get('success', False):
                logger.info("国债逆回购交易成功")
                return True
            else:
                logger.error(f"国债逆回购交易失败: {result.get('message', '未知错误')}")
                return False
        
        return True
        
    except Exception as e:
        logger.error(f"执行国债逆回购交易失败: {e}")
        return False


def update_all_account_holdings() -> Dict[str, pd.DataFrame]:
    """
    更新所有账户的持仓信息
    
    Returns:
        Dict[str, pd.DataFrame]: 各账户的持仓数据
    """
    logger.info("开始更新所有账户持仓信息")
    result_dict = {}
    
    for account_name in ACCOUNTS:
        try:
            logger.info(f"更新账户持仓: {account_name}")
            account_info = AccountInfo(account_name)
            holding_df = account_info.update_holding_info_for_account()
            if holding_df is not None:
                result_dict[account_name] = holding_df
        except Exception as e:
            logger.error(f"更新账户 {account_name} 持仓失败: {e}")
    
    # 如果有多个账户，更新汇总信息
    if len(result_dict) > 1:
        account_info = AccountInfo(ACCOUNTS[0])
        account_info._update_account_summary(result_dict)
    
    logger.info(f"更新账户持仓完成，成功更新 {len(result_dict)} 个账户")
    return result_dict


def execute_trading_for_account(account_name: str, strategies: List[str]) -> bool:
    """
    为指定账户执行交易策略
    
    Args:
        account_name: 账户名称
        strategies: 策略列表
        
    Returns:
        bool: 是否执行成功
    """
    try:
        logger.info(f"开始为账户执行交易策略: {account_name}，策略: {strategies}")
        
        # 创建交易逻辑对象
        trade_logic = TradeLogic(account_name)
        
        # TODO: 实现具体的策略执行逻辑
        # 这里可以根据不同的策略名称执行不同的交易逻辑
        
        # 示例：遍历策略列表
        for strategy in strategies:
            logger.info(f"执行策略: {strategy}")
            # 这里可以调用对应的策略处理器
            # 例如：根据策略读取交易信号，执行买入卖出操作
        
        logger.info(f"账户 {account_name} 的策略执行完成")
        return True
        
    except Exception as e:
        logger.error(f"执行交易策略失败: {e}")
        return False


def main_trading_loop() -> None:
    """
    主交易循环
    """
    logger.info("启动交易主程序")
    
    # 确保数据目录存在
    ensure_directory('data')
    ensure_directory('logs')
    
    # 创建通用页面操作对象
    common_page = CommonPage()
    
    # 初始账户
    current_account = None
    
    try:
        # 首先检查是否为交易日
        if not is_trading_day():
            logger.info("今天非交易日，程序退出")
            return
        
        # 更新所有账户持仓信息
        update_all_account_holdings()
        
        # 主循环
        while True:
            # 检查是否为交易时间
            if not is_trading_time():
                logger.info("当前非交易时间，等待...")
                time.sleep(60)  # 每分钟检查一次
                continue
            
            # 切换到下一个账户
            current_account = switch_to_next_account(common_page, current_account)
            
            if current_account:
                # 获取该账户的策略
                strategies = ACCOUNT_STRATEGY_MAP.get(current_account, [])
                
                if strategies:
                    # 执行交易策略
                    execute_trading_for_account(current_account, strategies)
                
                # 检查是否需要执行国债逆回购（可以在收盘前执行）
                now = datetime.datetime.now()
                close_time = now.replace(hour=14, minute=50, second=0, microsecond=0)
                
                if now >= close_time:
                    execute_guozhai_trades(current_account)
            
            # 每个账户操作间隔
            time.sleep(10)
            
    except KeyboardInterrupt:
        logger.info("接收到中断信号，程序退出")
    except Exception as e:
        logger.error(f"主交易循环异常: {e}")
        # 发送异常通知
        send_notification(f"交易程序异常: {e}", "交易异常", "system")
    finally:
        logger.info("交易程序退出")


def batch_account_update() -> None:
    """
    批量更新账户信息
    """
    logger.info("开始批量更新账户信息")
    
    try:
        # 更新所有账户持仓
        result_dict = update_all_account_holdings()
        
        # 发送完成通知
        success_count = len(result_dict)
        total_count = len(ACCOUNTS)
        message = f"账户信息更新完成，成功: {success_count}/{total_count}"
        logger.info(message)
        send_notification(message, "账户更新完成")
        
    except Exception as e:
        logger.error(f"批量更新账户信息失败: {e}")
        send_notification(f"账户更新失败: {e}", "账户更新异常")


# 主程序入口
if __name__ == "__main__":
    logger.info("=====================================")
    logger.info("交易主程序启动")
    logger.info(f"启动时间: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    logger.info("=====================================")
    
    try:
        # 这里可以根据命令行参数决定执行模式
        # 例如：main_trading_loop() 或者 batch_account_update()
        
        # 默认执行批量更新账户信息
        batch_account_update()
        
    except Exception as e:
        logger.error(f"程序执行失败: {e}")
    finally:
        logger.info("=====================================")
        logger.info("交易主程序结束")
        logger.info(f"结束时间: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        logger.info("=====================================")