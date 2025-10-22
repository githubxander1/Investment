import asyncio
import random
import datetime
from datetime import time as dt_time
import threading

from Investment.THS.AutoTrade.pages.trading import TradeLogic, NationalDebtPage
from Investment.THS.AutoTrade.pages.devices import DeviceManager
from Investment.THS.AutoTrade.scripts.processor.CombinationHoldingProcessor_glm import CombinationHoldingProcessor
from Investment.THS.AutoTrade.scripts.monitor_20day import check_morning_signals
from Investment.THS.AutoTrade.utils.notification import send_notification
from Investment.THS.AutoTrade.utils.logger import setup_logger
from Investment.THS.AutoTrade.config.settings import (
    MIN_DELAY,
    MAX_DELAY,
    MAX_RUN_TIME)

# 设置日志
logger = setup_logger("trade_main.log")
trader = TradeLogic()
device_manager = DeviceManager()

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

# 添加线程锁以确保线程安全
auto_trade_lock = threading.Lock()

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
    # 注意：这里的日期需要根据具体年份调整，特别是国庆节等可能变动的假期
    current_year = date.year
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
        guozhai = NationalDebtPage(d)
        if guozhai.common_page.change_account(account_name):
            logger.info(f"✅ 成功切换到账户: {account_name}")
            send_notification(f"账户已切换至: {account_name}")
        else:
            logger.warning(f"❌ 切换账户失败: {account_name}")
    except Exception as e:
        logger.error(f"切换账户时发生异常: {e}")
        # 即使切换失败也返回下一个索引，避免程序卡死在当前账户
        logger.info("将继续尝试下一个账户")

    return next_account_index


async def execute_guozhai_trades(d):
    """执行国债逆回购交易"""
    try:
        logger.info("🚀 开始执行国债逆回购交易...")
        guozhai_page = NationalDebtPage(d)
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
    d = device_manager.initialize_device()
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

    # 检查线程锁是否可用
    if not auto_trade_lock.acquire(blocking=False):
        logger.warning("AutoTrade系统正在运行中，无法重复启动")
        return
    
    try:
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
                if not device_manager.is_device_connected(d):
                    logger.warning("设备断开连接，尝试重新初始化...")
                    d = await device_manager.initialize_device()
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
                    combination_processor.operate_strategy_with_account()
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
    finally:
        # 释放线程锁
        auto_trade_lock.release()

if __name__ == '__main__':
    end_time_hour = 15
    end_time_minute = 30

    asyncio.run(main())