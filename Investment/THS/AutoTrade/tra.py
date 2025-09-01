import asyncio
import random
import datetime
import time
from datetime import time as dt_time

import pandas as pd
import uiautomator2 as u2

from Investment.THS.AutoTrade.pages.account_info import common_page
from Investment.THS.AutoTrade.pages.devices_init import initialize_device, is_device_connected
from Investment.THS.AutoTrade.pages.page_common import CommonPage
# 自定义模块
from Investment.THS.AutoTrade.scripts.portfolio_today.Combination_portfolio_today import Combination_main
from Investment.THS.AutoTrade.scripts.portfolio_today.Lhw_portfolio_today import Lhw_main
from Investment.THS.AutoTrade.scripts.portfolio_today.Robots_portfolio_today import Robot_main
from Investment.THS.AutoTrade.pages.page_guozhai import GuozhaiPage
from Investment.THS.AutoTrade.pages.page import THSPage
from Investment.THS.AutoTrade.scripts.data_process import read_operation_history, process_data_to_operate
# 导入新的策略处理模块
from Investment.THS.AutoTrade.scripts.holding.Strategy import StrategyHoldingProcessor
from Investment.THS.AutoTrade.scripts.holding.LhwHoldingProcessor import LhwHoldingProcessor
from Investment.THS.AutoTrade.scripts.holding.CombinationHoldingProcessor import CombinationHoldingProcessor
from Investment.THS.AutoTrade.scripts.trade_logic import TradeLogic
from Investment.THS.AutoTrade.utils.logger import setup_logger
from Investment.THS.AutoTrade.config.settings import (
    Strategy_portfolio_today_file,
    Combination_portfolio_today_file,
    OPERATION_HISTORY_FILE,
    MIN_DELAY,
    MAX_DELAY,
    MAX_RUN_TIME,
    Robot_portfolio_today_file, Account_holding_file, Lhw_portfolio_today_file,
)

# 导入你的20日监控模块
from Investment.THS.AutoTrade.scripts.monitor_20day import daily_check, check_morning_signals
from Investment.THS.AutoTrade.utils.notification import send_notification

# 设置日志
logger = setup_logger("trade_main.log")
trader = TradeLogic()

# 定义账户列表
ACCOUNTS = ["长城证券", "川财证券", "中泰证券"]

# 添加全局变量来跟踪是否已执行过信号检测
morning_signal_checked = False

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

async def execute_strategy_trades():
    """执行AI策略交易"""
    try:
        logger.info("🚀 开始执行AI策略交易...")
        processor = StrategyHoldingProcessor()
        success = processor.execute_strategy_trades()
        if success:
            logger.info("✅ AI策略交易执行完成")
            send_notification("AI策略交易执行完成")
        else:
            logger.error("❌ AI策略交易执行失败")
            send_notification("AI策略交易执行失败")
        return success
    except Exception as e:
        logger.error(f"❌ AI策略交易执行异常: {e}")
        send_notification(f"AI策略交易执行异常: {e}")
        return False

async def execute_lhw_trades():
    """执行量化王策略交易"""
    try:
        logger.info("🚀 开始执行量化王策略交易...")
        processor = LhwHoldingProcessor()
        success = processor.execute_lhw_trades()
        if success:
            logger.info("✅ 量化王策略交易执行完成")
            send_notification("量化王策略交易执行完成")
        else:
            logger.error("❌ 量化王策略交易执行失败")
            send_notification("量化王策略交易执行失败")
        return success
    except Exception as e:
        logger.error(f"❌ 量化王策略交易执行异常: {e}")
        send_notification(f"量化王策略交易执行异常: {e}")
        return False

async def execute_combination_trades():
    """执行组合策略交易"""
    try:
        logger.info("🚀 开始执行组合策略交易...")
        processor = CombinationHoldingProcessor()
        success = processor.execute_combination_trades()
        if success:
            logger.info("✅ 组合策略交易执行完成")
            send_notification("组合策略交易执行完成")
        else:
            logger.error("❌ 组合策略交易执行失败")
            send_notification("组合策略交易执行失败")
        return success
    except Exception as e:
        logger.error(f"❌ 组合策略交易执行异常: {e}")
        send_notification(f"组合策略交易执行异常: {e}")
        return False

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

    # 初始化国债逆回购状态
    guozhai_success = False
    strategy_diff_executed = False  # Strategy.py 的持仓差异 是否已执行
    robot_has_executed = False  # 策略/Robot任务执行标志
    combination_has_executed = False  # 组合任务执行标志
    lhw_has_executed = False  # 量化王任务执行标志

    # 标记是否已切换过账户
    account_switched_today = False

    # 国债逆回购状态跟踪 - 为每个账户分别跟踪
    guozhai_status = {account: False for account in ACCOUNTS}
    guozhai_retry_status = {account: False for account in ACCOUNTS}  # 重试状态

    while True:
        try:
            #  1.运行时间控制
            # 记录开始时间，用于最大运行时长控制
            start_time = datetime.datetime.now()
            now = datetime.datetime.now().time()
            # today = datetime.date.today()
            logger.info(f"开始时间： {start_time} 当前时间: {now}")

            # 检查是否超过最大运行时间
            if (datetime.datetime.now() - start_time) > datetime.timedelta(hours=MAX_RUN_TIME):
                logger.info(f"已达到最大运行时间 {MAX_RUN_TIME} 小时，退出程序")
                break

            # 检查是否超过每日结束时间
            if now >= dt_time(end_time_hour, end_time_minute):
                logger.info("当前时间超过 15:30，停止运行")
                break

            # 新增：检查是否在11:30到13:00之间，如果是则跳过本次循环
            if dt_time(11, 30) <= now < dt_time(13, 0):
                logger.info("当前时间在11:30到13:00之间，跳过本次循环")
                await asyncio.sleep(random.uniform(MIN_DELAY, MAX_DELAY))
                continue

            # 2. 检测设备是否断开
            if not is_device_connected(d):
                logger.warning("设备断开连接，尝试重新初始化...")
                d = await initialize_device()
                if not d:
                    logger.error("设备重连失败，等待下一轮检测")
                    await asyncio.sleep(random.uniform(MIN_DELAY, MAX_DELAY))
                    continue

            # 3. 开始任务
            logger.warning("开始任务")
            # 1). 执行早盘信号检查
            await check_morning_signals()

            # 2). 处理组合和策略文件
            # 初始化变量
            robot_success = False
            combination_success = False
            lhw_success = False

            robot_data_df = None
            combination_data_df = None
            lhw_data_df = None

            #  判断是否在策略任务时间窗口（9:30-9:35）
            if dt_time(9, 30) <= now <= dt_time(9, 35):
                if not robot_has_executed:  # 仅当未执行过时才触发
                    logger.warning("---------------------策略/Robot任务开始执行---------------------")
                    robot_result = await Robot_main()
                    if robot_result:
                        robot_success, robot_data_df = robot_result
                    else:
                        logger.warning("⚠️ 策略/Robot任务返回空值，默认视为无更新")
                        robot_success = False  # 避免未定义变量

                    logger.warning(f"策略/Robot是否有新增数据: {robot_success}\n"
                                f"---------------------策略/Robot任务执行结束---------------------")
                    robot_has_executed = True  # 执行后标记为已执行
                else:
                    logger.debug("本时间段内任务已执行，跳过重复执行")
            else:
                # 离开时间窗口后重置标志位，确保次日可重新执行
                if robot_has_executed:
                    robot_has_executed = False
                    logger.debug("离开任务时间窗口，重置执行标志")
                else:
                    logger.debug("尚未进入策略/Robot任务时间窗口，跳过执行")

            # 策略持仓差异任务（9:30-9:35）
            if dt_time(9, 30) <= now <= dt_time(9, 35) and not strategy_diff_executed:
                logger.warning("---------------------策略持仓差异分析开始---------------------")
                try:
                    # 执行新的AI策略交易
                    await execute_strategy_trades()
                except Exception as e:
                    logger.error(f"❌ 持仓差异分析过程中发生异常: {e}")

                logger.warning("---------------------策略持仓差异分析结束---------------------")
                strategy_diff_executed = True
            else:
                # 离开时间窗口后重置标志位，确保次日可重新执行
                if strategy_diff_executed:
                    strategy_diff_executed = False
                    logger.debug("离开任务时间窗口，重置执行标志")
                else:
                    logger.debug("尚未进入策略持仓差异分析时间窗口，跳过执行")

            # 判断是否在组合任务和自动化交易时间窗口（9:25-15:00）
            if dt_time(9, 25) <= now <= dt_time(15, 00):
                combination_executed = False
                lhw_executed = False

                if not combination_has_executed:
                    logger.warning("---------------------组合任务开始执行---------------------")
                    combination_result = await Combination_main()
                    if combination_result:
                        combination_success, combination_data_df = combination_result
                    else:
                        logger.warning("⚠️ 组合任务返回空值，默认视为无更新")
                    logger.warning(f"组合是否有新增数据: {combination_success}"
                                f"---------------------组合任务执行结束---------------------")
                    combination_has_executed = True
                    combination_executed = True
                else:
                    logger.debug("组合任务已执行，跳过重复执行")

                if not lhw_has_executed:
                    logger.warning("---------------------量化王任务开始执行---------------------")
                    lhw_result = await Lhw_main()
                    if lhw_result:
                        lhw_success, lhw_data_df = lhw_result
                    else:
                        logger.warning("⚠️ 量化王任务返回空值，默认视为无更新")
                    logger.warning(f"量化王是否有新增数据: {lhw_success}"
                                f"---------------------量化王任务执行结束---------------------")
                    lhw_has_executed = True
                    lhw_executed = True
                else:
                    logger.debug("量化王任务已执行，跳过重复执行")

                # 如果组合或量化王有新数据，执行相应的交易
                if (combination_executed and combination_success) or (lhw_executed and lhw_success):
                    logger.warning("---------------开始自动化操作---------------")
                    file_paths = []
                    if combination_success and combination_data_df is not None:
                        file_paths.append(Combination_portfolio_today_file)
                    if lhw_success and lhw_data_df is not None:
                        file_paths.append(Lhw_portfolio_today_file)

                    if file_paths:
                        process_data_to_operate(file_paths)
                    logger.warning("---------------自动化操作结束---------------")
                elif combination_executed or lhw_executed:
                    logger.info("有任务执行成功，但无新增交易数据，跳过交易处理")
                else:
                    logger.debug("无任务更新，跳过交易处理")
            else:
                # 离开时间窗口后重置标志位，确保次日可重新执行
                if combination_has_executed or lhw_has_executed:
                    combination_has_executed = False
                    lhw_has_executed = False
                    logger.debug("离开任务时间窗口，重置执行标志")
                else:
                    logger.debug("尚未进入组合任务和自动化交易时间窗口，跳过执行")

            # 国债逆回购操作（为每个账户执行一次）
            if dt_time(14, 56) <= now <= dt_time(15, 10):
                current_account = ACCOUNTS[current_account_index]
                logger.info(f"---------------------国债逆回购任务开始执行 (当前账户: {current_account})---------------------")

                try:
                    # 如果当前账户还未成功执行，或者执行失败且还未重试
                    if not guozhai_status[current_account] or (not guozhai_retry_status[current_account] and guozhai_status[current_account]):
                        guozhai = GuozhaiPage(d)
                        success, message = guozhai.guozhai_operation()

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

            # 随机等待，降低请求频率规律性
            delay = random.uniform(50, 70)
            logger.info(f"💤 等待 {delay:.2f} 秒后继续下一轮检测")
            await asyncio.sleep(delay)
        except Exception as e:
            logger.error(f"主循环中发生未预期的错误: {e}", exc_info=True)
            logger.info("程序将继续运行，等待下一轮检测")
            await asyncio.sleep(random.uniform(MIN_DELAY, MAX_DELAY))
            continue

if __name__ == '__main__':
    end_time_hour = 19
    end_time_minute = 30

    asyncio.run(main())
