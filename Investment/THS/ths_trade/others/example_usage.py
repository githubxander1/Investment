#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
同花顺交易功能使用示例
演示如何使用ths_trade的核心功能
"""

import os
import time
from Investment.THS.ths_trade.utils.logger import setup_logger
from Investment.THS.ths_trade.pages.base.page_common import CommonPage
from Investment.THS.ths_trade.pages.account.account_info import AccountInfo
from Investment.THS.ths_trade.pages.trading.trade_logic import TradeLogic
from Investment.THS.ths_trade.pages.trading.ths_trade_wrapper import trade_wrapper

logger = setup_logger('example_usage.log')


def example_account_operations():
    """
    账户操作示例
    """
    logger.info("=== 账户操作示例 ===")
    
    # 创建通用页面操作对象
    common_page = CommonPage()
    
    # 获取账户列表
    accounts = common_page.get_account_list()
    logger.info(f"可用账户数量: {len(accounts)}")
    
    for account in accounts:
        account_name = account.get('account_name')
        logger.info(f"账户: {account_name}")
    
    # 如果有账户，演示账户切换和信息查询
    if accounts:
        test_account = accounts[0]['account_name']
        
        # 切换账户
        success = common_page.change_account(test_account)
        logger.info(f"切换到账户 {test_account}: {'成功' if success else '失败'}")
        
        # 创建账户信息对象
        account_info = AccountInfo(test_account)
        
        # 获取可用资金
        buying_power = account_info.get_buying_power()
        logger.info(f"可用资金: {buying_power}")
        
        # 获取账户汇总信息
        summary = account_info.get_account_summary_info()
        logger.info("账户汇总信息:")
        for key, value in summary.items():
            logger.info(f"  {key}: {value}")
        
        # 更新持仓信息
        holding_df = account_info.update_holding_info_for_account()
        if holding_df is not None and not holding_df.empty:
            logger.info(f"持仓数量: {len(holding_df)}")
            logger.info("持仓明细:")
            for _, row in holding_df.iterrows():
                logger.info(f"  {row['stock_code']} {row['stock_name']}: {row['position']}股")


def example_trading_operations():
    """
    交易操作示例（仅演示，不执行实际交易）
    """
    logger.info("=== 交易操作示例 ===")
    
    # 获取账户列表
    common_page = CommonPage()
    accounts = common_page.get_account_list()
    
    if not accounts:
        logger.error("没有可用账户，无法演示交易操作")
        return
    
    test_account = accounts[0]['account_name']
    
    # 创建交易逻辑对象
    trade_logic = TradeLogic(test_account)
    
    # 示例：计算买入数量
    stock_code = "000001"  # 平安银行
    test_price = 12.5
    volume, amount = trade_logic.calculate_buy_volume(stock_code, test_price, 0.1)  # 使用10%资金
    logger.info(f"测试买入计算: 股票={stock_code}, 价格={test_price}, 可用资金10%可买数量={volume}股, 金额={amount}元")
    
    # 示例：计算卖出数量
    volume = trade_logic.calculate_sell_volume(stock_code, 0.5)  # 卖出50%
    logger.info(f"测试卖出计算: 股票={stock_code}, 卖出50%可卖数量={volume}股")
    
    # 注意：以下代码仅为演示，实际执行交易需要取消注释
    # logger.info("演示买入操作（已注释）")
    # result = trade_logic.buy_stock_with_logic(
    #     stock_code=stock_code,
    #     price=test_price,
    #     volume=100,
    #     stock_name="平安银行"
    # )
    # logger.info(f"买入结果: {result}")


def example_batch_holding_update():
    """
    批量更新持仓示例
    """
    logger.info("=== 批量更新持仓示例 ===")
    
    # 获取账户列表
    common_page = CommonPage()
    accounts = common_page.get_account_list()
    
    if not accounts:
        logger.error("没有可用账户，无法演示批量更新")
        return
    
    # 批量更新所有账户的持仓
    first_account = accounts[0]['account_name']
    account_info = AccountInfo(first_account)
    
    # 构建账户名称列表
    account_names = [acc['account_name'] for acc in accounts]
    
    # 批量更新
    result_dict = account_info.update_holding_info_all(account_names)
    
    logger.info(f"批量更新完成，成功更新 {len(result_dict)} 个账户")
    
    # 检查汇总文件是否生成
    summary_file = os.path.join('data', 'holding', 'account_summary.xlsx')
    if os.path.exists(summary_file):
        logger.info(f"账户汇总文件已生成: {summary_file}")


def example_direct_api_usage():
    """
    直接使用交易API示例
    """
    logger.info("=== 直接使用交易API示例 ===")
    
    # 使用全局交易包装器实例
    global_trade_api = trade_wrapper
    
    # 获取账户列表
    accounts = global_trade_api.get_account_list()
    logger.info(f"通过API获取账户数量: {len(accounts)}")
    
    if accounts:
        test_account = accounts[0]['account_name']
        
        # 切换账户
        success = global_trade_api.switch_account(test_account)
        logger.info(f"API切换账户: {'成功' if success else '失败'}")
        
        # 获取持仓信息
        try:
            positions = global_trade_api.get_position()
            logger.info(f"API获取持仓数量: {len(positions) if positions is not None else 0}")
        except Exception as e:
            logger.error(f"获取持仓失败: {e}")
        
        # 获取资金信息
        try:
            balance = global_trade_api.get_balance()
            logger.info(f"API获取资金: 总资产={balance.get('total_assets', 0)}")
        except Exception as e:
            logger.error(f"获取资金失败: {e}")


def main():
    """
    主函数
    """
    logger.info("同花顺交易功能使用示例开始")
    
    try:
        # 执行各个示例
        example_account_operations()
        print("-" * 50)
        
        example_trading_operations()
        print("-" * 50)
        
        example_batch_holding_update()
        print("-" * 50)
        
        example_direct_api_usage()
        
    except Exception as e:
        logger.error(f"示例执行失败: {e}")
    finally:
        logger.info("同花顺交易功能使用示例结束")


if __name__ == "__main__":
    main()