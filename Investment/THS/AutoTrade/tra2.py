import asyncio
import random
import datetime
import time
from datetime import time as dt_time

import pandas as pd
import uiautomator2 as u2

from Investment.THS.AutoTrade.pages.account_info import common_page, AccountInfo
from Investment.THS.AutoTrade.pages.devices_init import initialize_device, is_device_connected
from Investment.THS.AutoTrade.pages.page_common import CommonPage
from Investment.THS.AutoTrade.scripts.holding.Combination_holding_all import get_portfolio_holding_data_all
from Investment.THS.AutoTrade.scripts.holding.CommonHoldingProcessor import CommonHoldingProcessor
from Investment.THS.AutoTrade.scripts.monitor_20day import check_morning_signals
# 自定义模块
from Investment.THS.AutoTrade.scripts.portfolio_today.Combination_portfolio_today import Combination_main
from Investment.THS.AutoTrade.pages.page_guozhai import GuozhaiPage
from Investment.THS.AutoTrade.pages.page import THSPage
from Investment.THS.AutoTrade.scripts.data_process import read_operation_history, process_data_to_operate
# 导入新的策略处理模块
from Investment.THS.AutoTrade.scripts.holding.CombinationHoldingProcessor import CombinationHoldingProcessor
from Investment.THS.AutoTrade.scripts.trade_logic import TradeLogic
from Investment.THS.AutoTrade.utils.logger import setup_logger
from Investment.THS.AutoTrade.config.settings import (
    Combination_portfolio_today_file,
    OPERATION_HISTORY_FILE,
    MIN_DELAY,
    MAX_DELAY,
    MAX_RUN_TIME,
    Account_holding_file, Combination_holding_file, Strategy_holding_file, Trade_history)

# 导入你的20日监控模块
# from Investment.THS.AutoTrade.scripts.monitor_20day import daily_check, check_morning_signals
from Investment.THS.AutoTrade.utils.notification import send_notification

# 设置日志
logger = setup_logger("trade_main.log")
trader = TradeLogic()

# 定义账户列表 - 只保留中山证券和中泰证券
ACCOUNTS = ["中山证券", "中泰证券"]

# 账户与策略映射关系
ACCOUNT_STRATEGY_MAP = {
    "中山证券": "逻辑为王"
    # "中泰证券": "一枝梨花"
}

# 添加全局变量来跟踪是否已执行过信号检测
morning_signal_checked = False

# 添加全局变量来跟踪是否需要更新账户数据
account_update_needed = True

def is_trading_day(date: datetime.date) -> bool:
    """
    判断是否为中国股市的交易日
    :param date: 日期
    :return: 是否是交易日
    """
    # 忽略周六周日
    if date.weekday() >= 5:  # 5=Saturday, 6=Sunday
        return False

    # 可以在此添加节假日列表进行排除
    holidays = [
        (1, 1),     # 元旦
        (2, 10),    # 春节
        (4, 5),     # 清明
        (5, 1),     # 劳动节
        (6, 22),    # 端午
        (9, 30),    # 国庆
    ]

    return not ((date.month, date.day) in holidays)

def switch_to_next_account(d, current_account_index):
    """
    切换到下一个账户
    :param d: uiautomator2设备对象
    :param current_account_index: 当前账户索引
    :return: 下一个账户索引
    """
    next_account_index = (current_account_index + 1) % len(ACCOUNTS)
    account_name = ACCOUNTS[next_account_index]

    try:
        guozhai = GuozhaiPage(d)
        if guozhai.guozhai_change_account(account_name):
            logger.info(f"✅ 成功切换到账户: {account_name}")
            send_notification(f"账户已切换至: {account_name}")
        else:
            logger.warning(f"❌ 切换账户失败: {account_name}")
    except Exception as e:
        logger.error(f"切换账户时发生异常: {e}")
        # 即使切换失败也返回下一个索引，避免程序卡死在当前账户
        logger.info("将继续尝试下一个账户")

    return next_account_index

# async def execute_combination_trades():
#     """执行组合交易"""
#     try:
#         logger.info("🚀 开始执行组合交易...")
#
#         # 更新策略持仓数据
#         strategy_df = get_portfolio_holding_data_all()
#         logger.info(f"✅ 策略持仓数据已更新\n{strategy_df}")
#
#         # 首先更新账户数据，只更新ACCOUNT_STRATEGY_MAP中的账户
#         global account_update_needed
#         if account_update_needed:
#             logger.info("🔄 开始更新账户数据...")
#             account_info = AccountInfo()
#             update_success = True
#
#             # 只更新需要的账户
#             for account_name in ACCOUNT_STRATEGY_MAP.keys():
#                 logger.info(f"正在更新账户 {account_name} 的数据...")
#                 account_update_success = account_info.update_holding_info_for_account(account_name)
#                 if not account_update_success:
#                     logger.warning(f"⚠️ 账户 {account_name} 数据更新失败")
#                     update_success = False
#
#             if update_success:
#                 logger.info("✅ 所需账户数据更新完成")
#                 # 重置更新标志
#                 account_update_needed = False
#             else:
#                 logger.warning("⚠️ 部分账户数据更新失败，将继续使用现有数据执行交易")
#         else:
#             logger.info("🔄 账户数据无需更新，使用上一轮数据")
#
#         # account_file = r"D:\Xander\Inverstment\Investment\THS\AutoTrade\data\position\Account_position.xlsx"
#         strategy_file = Strategy_holding_file
#         # trade_file = r"D:\Xander\Inverstment\Investment\THS\AutoTrade\data\portfolio\trade_operations.xlsx"
#         trade_file = Trade_history
#
#         # account_file = r"D:\Xander\Inverstment\Investment\THS\AutoTrade\data\position\Account_position.xlsx"
#         # 设置pandas显示选项，确保所有列都能完整显示
#         pd.set_option('display.max_columns', None)
#         pd.set_option('display.width', None)
#         pd.set_option('display.max_colwidth', None)
#
#         # 预先收集所有账户和策略的数据
#         logger.info("🔍 预先收集所有账户和策略的数据...")
#         processor_data = {}
#         for account_name, strategy_name in ACCOUNT_STRATEGY_MAP.items():
#             logger.info(f"🔄 收集账户 {account_name} 和策略 {strategy_name} 的数据")
#             processor = CommonHoldingProcessor()
#             diff = processor.extract_different_holding(
#                 Account_holding_file,
#                 account_name,
#                 Combination_holding_file,
#                 strategy_name
#             )
#             filtered_result = processor.filter_executed_operations(diff, account_name)
#             processor_data[account_name] = {
#                 'processor': processor,
#                 'diff': diff,
#                 'filtered_result': filtered_result,
#                 'strategy_name': strategy_name
#             }
#
#         # 为每个账户执行对应的策略
#         execution_results = {}
#         for account_name, data in processor_data.items():
#             strategy_name = data['strategy_name']
#             logger.info(f"🔄 处理账户 {account_name} 对应的策略 {strategy_name}")
#
#             try:
#                 # 执行策略
#                 processor = data['processor']
#                 to_sell = data['filtered_result'].get('to_sell', pd.DataFrame())
#                 to_buy = data['filtered_result'].get('to_buy', pd.DataFrame())
#
#                 # 只保留市场为沪深A股的
#                 if not to_sell.empty and '市场' in to_sell.columns:
#                     to_sell = to_sell[to_sell['市场'] == '沪深A股']
#                 if not to_buy.empty and '市场' in to_buy.columns:
#                     to_buy = to_buy[to_buy['市场'] == '沪深A股']
#
#                 # 标记是否执行了任何交易操作
#                 any_trade_executed = False
#
#                 # 遍历每一项卖出操作，执行交易
#                 for idx, op in to_sell.iterrows():
#                     stock_name = op['股票名称'] if '股票名称' in op else op['股票名称']
#                     operation = op['操作']
#                     # 安全获取可能不存在的字段
#                     new_ratio = op.get('新比例%', None)  # 对于卖出操作，获取策略中的目标比例
#
#                     # 计算交易数量：对于卖出操作，使用策略中的目标比例
#                     volume = processor.calculate_trade_volume(Account_holding_file, account_name, strategy_file, strategy_name, stock_name, new_ratio, operation)
#                     logger.info(f"🛠️ 卖出 {stock_name}，目标比例:{new_ratio}，交易数量:{volume}")
#
#                     logger.info(f"🛠️ 开始处理: {operation} {stock_name} 目标比例:{new_ratio} 策略:{strategy_name} 账户:{account_name}")
#
#                     # 切换到对应账户
#                     processor.common_page.change_account(account_name)
#                     logger.info(f"✅ 已切换到账户: {account_name}")
#
#                     # 调用交易逻辑
#                     status, info = processor.trader.operate_stock(operation, stock_name, volume)
#
#                     # 检查交易是否成功执行
#                     if status is None:
#                         logger.error(f"❌ {operation} {stock_name} 交易执行失败: {info}")
#                         continue
#
#                     # 标记已执行交易
#                     any_trade_executed = True
#                     # 标记下次需要更新账户数据
#                     account_update_needed = True
#
#                 # 遍历每一项买入操作，执行交易
#                 for idx, op in to_buy.iterrows():
#                     stock_name = op['股票名称'] if '股票名称' in op else op['股票名称']
#                     operation = op['操作']
#                     # 安全获取可能不存在的字段
#                     new_ratio = op.get('新比例%', None)  # 对于买入操作，获取策略中的目标比例
#
#                     # 计算交易数量：对于买入操作，使用策略中的目标比例
#                     volume = processor.calculate_trade_volume(Account_holding_file, account_name, strategy_file, strategy_name, stock_name, new_ratio, operation)
#                     logger.info(f"🛠️ 买入 {stock_name}，目标比例:{new_ratio}，交易数量:{volume}")
#
#                     logger.info(f"🛠️ 开始处理: {operation} {stock_name} 目标比例:{new_ratio} 策略:{strategy_name} 账户:{account_name}")
#
#                     # 切换到对应账户
#                     processor.common_page.change_account(account_name)
#                     logger.info(f"✅ 已切换到账户: {account_name}")
#
#                     # 调用交易逻辑
#                     status, info = processor.trader.operate_stock(operation, stock_name, volume)
#
#                     # 检查交易是否成功执行
#                     if status is None:
#                         logger.error(f"❌ {operation} {stock_name} 交易执行失败: {info}")
#                         continue
#
#                     # 标记已执行交易
#                     any_trade_executed = True
#                     # 标记下次需要更新账户数据
#                     account_update_needed = True
#
#                 execution_results[account_name] = True
#                 logger.info(f"✅ 账户 {account_name} 对应的策略 {strategy_name} 执行完成")
#                 send_notification(f"✅ 账户 {account_name} 对应的策略 {strategy_name} 执行完成")
#             except Exception as e:
#                 execution_results[account_name] = False
#                 logger.error(f"❌ 账户 {account_name} 对应的策略 {strategy_name} 执行失败: {e}")
#                 send_notification(f"❌ 账户 {account_name} 对应的策略 {strategy_name} 执行失败: {e}")
#
#         # 检查执行结果
#         all_success = all(execution_results.values())
#         if all_success:
#             logger.info("🎉 所有组合交易执行完成")
#         else:
#             failed_accounts = [acc for acc, success in execution_results.items() if not success]
#             logger.error(f"❌ 以下账户交易执行失败: {failed_accounts}")
#
#         return all_success
#     except Exception as e:
#         logger.error(f"❌ 组合交易执行异常: {e}")
#         send_notification(f"组合交易执行异常: {e}")
#         return False

async def execute_guozhai_trades(d):
    """执行国债逆回购交易"""
    try:
        logger.info("🚀 开始执行国债逆回购交易...")
        guozhai_page = GuozhaiPage(d)
        success, message = guozhai_page.guozhai_operation()
        if success:
            logger.info("✅ 国债逆回购交易执行完成")
            send_notification(f"国债逆回购交易执行完成: {message}")
        else:
            logger.error(f"❌ 国债逆回购交易执行失败: {message}")
            send_notification(f"国债逆回购交易执行失败: {message}")
        return success, message
    except Exception as e:
        logger.error(f"❌ 国债逆回购交易执行异常: {e}")
        send_notification(f"国债逆回购交易执行异常: {e}")
        return False, str(e)

# 在 main 函数的 while 循环中添加信号检查调用
async def main():
    """主程序：控制任务执行的时间窗口"""

    logger.info("⏰ 调度器已启动，等待执行时间窗口...")

    # 初始化设备
    d = await initialize_device()
    if not d:
        logger.error("❌ 设备初始化失败")
        return

    # 初始化账户索引
    current_account_index = 0

    # 初始化任务执行标志
    portfolio_updates_executed = False  # 组合和策略更新是否已执行
    guozhai_executed = False  # 国债逆回购是否已执行

    # 国债逆回购状态跟踪 - 为每个账户分别跟踪
    guozhai_status = {account: False for account in ACCOUNTS}
    guozhai_retry_status = {account: False for account in ACCOUNTS}  # 重试状态

    while True:
        try:
            #  1.运行时间控制
            # 记录开始时间，用于最大运行时长控制
            start_time = datetime.datetime.now()
            now = datetime.datetime.now().time()
            logger.info(f"开始时间： {start_time} 当前时间: {now}")

            # 检查是否超过最大运行时间
            if (datetime.datetime.now() - start_time) > datetime.timedelta(hours=MAX_RUN_TIME):
                logger.info(f"已达到最大运行时间 {MAX_RUN_TIME} 小时，退出程序")
                break

            # 检查是否超过每日结束时间
            if now >= dt_time(end_time_hour, end_time_minute):
                logger.info("当前时间超过设定结束时间，停止运行")
                break

            # 检查是否在11:30到13:00之间，如果是则跳过本次循环
            if dt_time(11, 30) <= now < dt_time(13, 0):
                logger.info("当前时间在11:30到13:00之间，跳过本次循环")
                await asyncio.sleep(random.uniform(MIN_DELAY, MAX_DELAY))
                continue

            # 检测设备是否断开
            if not is_device_connected(d):
                logger.warning("设备断开连接，尝试重新初始化...")
                d = await initialize_device()
                if not d:
                    logger.error("设备重连失败，等待下一轮检测")
                    await asyncio.sleep(random.uniform(MIN_DELAY, MAX_DELAY))
                    continue

            # 开始任务
            logger.warning("开始任务")

            # 1. 执行早盘信号检查
            global morning_signal_checked
            await check_morning_signals()

            # 2. 组合更新任务（9:25-15:00）
            if dt_time(9, 25) <= now <= dt_time(end_time_hour, 0):
                # if not portfolio_updates_executed:
                logger.warning("---------------------组合更新任务开始---------------------")
                combination_processor = CombinationHoldingProcessor()
                combination_processor.execute_combination_trades()
                logger.warning("---------------------组合更新任务结束---------------------")
                # portfolio_updates_executed = True
                # else:
                #     logger.debug("组合和策略更新任务已执行，跳过重复执行")
            else:
                logger.info("尚未进入组合更新任务时间窗口，跳过执行")
            # pass
            # 停止运行

            # 离开时间窗口后重置标志位
            # if portfolio_updates_executed:
            #     portfolio_updates_executed = False
            #     logger.debug("离开组合和策略更新时间窗口，重置执行标志")

            # 3. 国债逆回购操作（14:56-15:10）
            if dt_time(14, 56) <= now <= dt_time(15, 10):
                if not guozhai_executed:
                    current_account = ACCOUNTS[current_account_index]
                    logger.info(f"---------------------国债逆回购任务开始执行 (当前账户: {current_account})---------------------")

                    try:
                        # 如果当前账户还未成功执行，或者执行失败且还未重试
                        if not guozhai_status[current_account] or (not guozhai_retry_status[current_account] and guozhai_status[current_account]):
                            success, message = await execute_guozhai_trades(d)

                            if success:
                                logger.info(f"国债逆回购成功 (账户: {current_account})")
                                guozhai_status[current_account] = True
                                send_notification(f"国债逆回购任务完成 (账户: {current_account}): {message}")

                                # 成功后立即切换到下一个账户并继续执行
                                logger.info(
                                    f"---------------------国债逆回购任务执行结束 (账户: {current_account})---------------------")
                                current_account_index = switch_to_next_account(d, current_account_index)
                                # 不等待，立即继续执行下一个账户
                                continue
                            else:
                                logger.info(f"国债逆回购失败 (账户: {current_account}): {message}")
                                # 标记需要下一轮重试
                                if not guozhai_status[current_account]:
                                    guozhai_status[current_account] = True  # 标记已尝试
                                    guozhai_retry_status[current_account] = False  # 需要重试
                                else:
                                    guozhai_retry_status[current_account] = True  # 已重试过

                            logger.info(f"---------------------国债逆回购任务执行结束 (账户: {current_account})---------------------")

                            # 切换到下一个账户
                            current_account_index = switch_to_next_account(d, current_account_index)
                            # 继续执行下一个账户
                            continue
                        else:
                            logger.debug(f"账户 {current_account} 已完成国债逆回购任务，跳过执行")
                            # 检查是否所有账户都已完成国债逆回购任务
                            all_accounts_done = all(guozhai_status[account] for account in ACCOUNTS)
                            if all_accounts_done:
                                logger.info("所有账户国债逆回购任务已完成，跳过后续账户切换")
                                guozhai_executed = True  # 标记国债逆回购任务完成
                            else:
                                # 只有在还有账户未完成时才切换到下一个账户
                                current_account_index = switch_to_next_account(d, current_account_index)
                            continue

                    except Exception as e:
                        logger.error(f"国债逆回购操作过程中发生错误: {e}", exc_info=True)
                        logger.info("将继续执行下一个账户的操作")
                        current_account_index = switch_to_next_account(d, current_account_index)
                        # 即使出错也继续执行下一个账户
                        continue
                else:
                    logger.debug("国债逆回购任务已执行，跳过重复执行")
            else:
                logger.info("尚未进入国债逆回购任务时间窗口，跳过执行")
                # 离开时间窗口后重置标志位
                if guozhai_executed:
                    guozhai_executed = False
                    guozhai_status = {account: False for account in ACCOUNTS}  # 重置账户状态
                    guozhai_retry_status = {account: False for account in ACCOUNTS}  # 重置重试状态
                    logger.debug("离开国债逆回购时间窗口，重置执行标志")

            # 随机等待，降低请求频率规律性
            delay = random.uniform(MIN_DELAY, MAX_DELAY)
            logger.info(f"💤 等待 {delay:.2f} 秒后继续下一轮检测")
            await asyncio.sleep(delay)

        except Exception as e:
            logger.error(f"主循环中发生未预期的错误: {e}", exc_info=True)
            logger.info("程序将继续运行，等待下一轮检测")
            await asyncio.sleep(random.uniform(MIN_DELAY, MAX_DELAY))
            continue

if __name__ == '__main__':
    end_time_hour = 15
    end_time_minute = 30

    asyncio.run(main())