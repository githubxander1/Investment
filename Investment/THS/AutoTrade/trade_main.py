# trade_main.py

import asyncio
import os
import random
import datetime
import time
from datetime import time as dt_time

import pandas as pd
import uiautomator2 as u2
from sympy.physics.units import volume

# 自定义模块
from Investment.THS.AutoTrade.scripts.portfolio_today.Combination_portfolio_today import Combination_main
from Investment.THS.AutoTrade.scripts.portfolio_today.Lhw_portfolio_today import Lhw_main
from Investment.THS.AutoTrade.scripts.portfolio_today.Robots_portfolio_today import Robot_main
from Investment.THS.AutoTrade.scripts.portfolio_today.Strategy_portfolio_today import Strategy_main
from Investment.THS.AutoTrade.pages.page_guozhai import GuozhaiPage
from Investment.THS.AutoTrade.pages.page import THSPage
from Investment.THS.AutoTrade.scripts.data_process import process_excel_files, read_operation_history, \
    write_operation_history
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
from Investment.THS.AutoTrade.scripts.monitor_20day import daily_check
from Investment.THS.AutoTrade.utils.notification import send_notification

# 设置日志
logger = setup_logger("trade_main.log")
trader = TradeLogic()

# 定义账户列表
ACCOUNTS = ["长城证券", "川财证券", "中泰证券"]

async def connect_to_device():
    """连接设备"""
    try:
        d = u2.connect()
        logger.info(f"连接设备: {d.serial}")
        return d
    except Exception as e:
        logger.error(f"连接设备失败: {e}", exc_info=True)
        return None

async def start_app(d, package_name="com.hexin.plat.android"):
    """启动同花顺App"""
    try:
        d.app_start(package_name, wait=True)
        logger.info(f"启动App成功: {package_name}")
        return True
    except Exception as e:
        logger.error(f"启动app失败 {package_name}: {e}", exc_info=True)
        return False

async def initialize_device():
    """初始化设备"""
    d = await connect_to_device()
    if not d:
        logger.error("设备连接失败")
        return None

    if not await start_app(d):
        logger.error("App启动失败")
        return None

    return d

def is_device_connected(d):
    """简单心跳检测设备是否还在线"""
    try:
        return d.info['screenOn']
    except:
        return False


# 添加全局变量来跟踪是否已执行过信号检测
morning_signal_checked = False


async def check_morning_signals():
    """检查早盘信号"""
    global morning_signal_checked

    now = datetime.datetime.now()
    current_time = now.time()

    # 检查是否是交易日
    if not is_trading_day(now.date()):
        logger.info("今天是非交易日，跳过信号检查")
        return

    # 检查是否在信号检查时间窗口内（9:25-9:35）
    if dt_time(9, 25) <= current_time <= dt_time(9, 28):
        logger.info("开始执行早盘信号检查...")
        # 检查是否已经执行过今天的信号检查
        if not morning_signal_checked:
            logger.info("开始执行早盘信号检查...")

            try:
                stocks_code = read_operation_history(Account_holding_file)
                # 定义要监控的股票（从配置或其他地方获取）
                MONITORED_STOCKS = {
                    "601728": "中国电信",
                    "601398": "工商银行",
                    "600900": "长江电力"
                }

                # 定义要监控的ETF
                MONITORED_ETFS = {
                    "508011": "嘉实物美消费REIT",
                    "508005": "华夏首创奥莱REIT",
                    "511380": "可转债ETF",
                    "511580": "国债证金债ETF",
                    "518850": "黄金ETF华夏",
                    "510300": "沪深300ETF",
                    # "510050": "上证50ETF",
                    # "510500": "中证500ETF",
                }

                # 执行股票信号检查（使用5日均线）
                stock_signals_found, stock_signals = daily_check("stock", MONITORED_STOCKS, ma_window=20)

                # 执行ETF信号检查（使用20日均线）
                etf_signals_found, etf_signals = daily_check("etf", MONITORED_ETFS, ma_window=20)

                # 如果有任何信号，发送汇总通知
                if stock_signals_found or etf_signals_found:
                    all_signals = stock_signals + etf_signals
                    summary_msg = "📈📉 早盘信号提醒 📈📉\n" + "\n".join(all_signals)
                    logger.info("早盘信号检查完成，发现信号")
                else:
                    logger.info("早盘信号检查完成，未发现明显信号")

                # 标记今天已执行信号检查
                morning_signal_checked = True
                logger.info("早盘信号检查完成")

            except Exception as e:
                logger.error(f"执行早盘信号检查时发生异常: {e}")
    else:
        # 如果过了信号检查时间窗口，重置标记以便第二天使用
        if current_time > dt_time(9, 35):
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
    strategy1_executed = False  # Strategy_portfolio_today 是否已执行
    strategy2_executed = False  # Strategy.py 的持仓差异 是否已执行

    # 记录开始时间，用于最大运行时长控制
    start_time = datetime.datetime.now()

    # 1. 提前读取历史记录
    history_df = read_operation_history(OPERATION_HISTORY_FILE)

    # 标记是否已切换过账户
    account_switched_today = False

    # 国债逆回购状态跟踪 - 为每个账户分别跟踪
    guozhai_status = {account: False for account in ACCOUNTS}
    guozhai_retry_status = {account: False for account in ACCOUNTS}  # 重试状态

    while True:
        try:
            now = datetime.datetime.now().time()

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

            # 检测设备是否断开
            if not is_device_connected(d):
                logger.warning("设备断开连接，尝试重新初始化...")
                d = await initialize_device()
                if not d:
                    logger.error("设备重连失败，等待下一轮检测")
                    await asyncio.sleep(random.uniform(MIN_DELAY, MAX_DELAY))
                    continue

            # 更新页面对象引用
            ths_page = THSPage(d)

            # 执行早盘信号检查
            await check_morning_signals()

            # 2. 处理组合和策略文件
            # 初始化变量
            robot_success = False
            strategy_success = False
            combination_success = False
            lhw_success = False

            strategy_data = None
            combination_data = None

            # 获取当前日期
            today = datetime.date.today()
            current_time = now

            # {策略}任务时间窗口（9:32-9:35）
            if dt_time(9, 32) <= current_time <= dt_time(9, 35) and not strategy1_executed:
                logger.info("---------------------策略任务开始执行---------------------")
                strategy_result = await Strategy_main()
                if strategy_result:
                    strategy_success, strategy_data = strategy_result
                else:
                    logger.warning("⚠️ 策略任务返回空值，默认视为无更新")
                logger.info(f"策略是否有新增数据: {strategy_success}\n---------------------策略任务执行结束---------------------")
                strategy1_executed = True

            # 策略持仓差异任务（9:32-9:35）
            if dt_time(9, 32) <= current_time <= dt_time(9, 35) and not strategy2_executed:
                logger.info("---------------------策略持仓差异分析开始---------------------")
                try:
                    from Investment.THS.AutoTrade.scripts.portfolio_today.Strategy import get_difference_holding
                    diff_result = get_difference_holding()
                    if diff_result:
                        to_buy = diff_result.get('to_buy')
                        to_sell = diff_result.get('to_sell')

                        if not to_buy.empty or not to_sell.empty:
                            logger.info(f"发现持仓差异，准备执行交易操作：买入 {len(to_buy)} 只，卖出 {len(to_sell)} 只")

                            # 合并买入/卖出数据
                            combined_df = pd.concat([
                                to_buy[['标的名称', '操作']],
                                to_sell[['标的名称', '操作']]
                            ], ignore_index=True)

                            # 遍历每一行，执行交易
                            for index, row in combined_df.iterrows():
                                stock_name = row['标的名称']
                                operation = row['操作']

                                logger.info(f"🛠️ 要处理: {operation} {stock_name}")

                                # 特殊处理：卖出时全仓卖出
                                if operation == "卖出":
                                    new_ratio = 0.0
                                else:
                                    new_ratio = None  # 买入时无需新比例

                                # 调用交易逻辑
                                status, info = trader.operate_stock(
                                    operation=operation,
                                    stock_name=stock_name,
                                    volume=200 if operation == "买入" else None,
                                    new_ratio=new_ratio
                                )

                                # 检查交易是否成功执行
                                if status is None:
                                    logger.error(f"❌ {operation} {stock_name} 交易执行失败: {info}")
                                    continue

                                # 构造记录
                                # operate_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                                operate_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                                record = pd.DataFrame([{
                                    '标的名称': stock_name,
                                    '操作': operation,
                                    '新比例%': new_ratio,
                                    '状态': status,
                                    '信息': info,
                                    '时间': operate_time
                                }])

                                # 写入历史
                                write_operation_history(record)
                                logger.info(f"{operation} {stock_name} 流程结束，操作已记录")

                        else:
                            logger.info("✅ 当前无持仓差异，无需执行交易")
                    else:
                        logger.warning("⚠️ 持仓差异分析返回空值，默认视为无更新")

                except Exception as e:
                    logger.error(f"❌ 持仓差异分析过程中发生异常: {e}")

                logger.info("---------------------策略持仓差异分析结束---------------------")
                strategy2_executed = True

            # 国债逆回购操作（为每个账户执行一次）
            if dt_time(14, 56) <= now <= dt_time(16, 25):
                current_account = ACCOUNTS[current_account_index]
                logger.info(f"---------------------国债逆回购任务开始执行 (当前账户: {current_account})---------------------")

                try:
                    # 切换到当前账户
                    # guozhai_page = GuozhaiPage(d)
                    # if not guozhai_page.guozhai_change_account(current_account):
                    #     logger.warning(f"切换到账户 {current_account} 失败")
                    #     # 尝试切换到下一个账户
                    #     current_account_index = switch_to_next_account(d, current_account_index)
                    #     await asyncio.sleep(2)
                    #     # 继续执行下一个账户而不是等待下一轮
                    #     continue

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
                        # 切换到下一个账户
                        current_account_index = switch_to_next_account(d, current_account_index)
                        continue

                except Exception as e:
                    logger.error(f"国债逆回购操作过程中发生错误: {e}", exc_info=True)
                    logger.info("将继续执行下一个账户的操作")
                    current_account_index = switch_to_next_account(d, current_account_index)
                    # 即使出错也继续执行下一个账户
                    continue
    # else:
    #     logger.debug("尚未进入国债逆回购时间窗口，跳过执行")

            # # 每日账户切换（在收盘后执行一次）
            # if not account_switched_today and dt_time(15, 1) <= now <= dt_time(15, 5):
            #     current_account_index = switch_to_next_account(d, current_account_index)
            #     account_switched_today = True
            #     logger.info("每日账户切换完成")

            # 重置每日账户切换标记和国债逆回购状态
            if dt_time(0, 0) <= now <= dt_time(1, 0):
                if account_switched_today:
                    account_switched_today = False
                    logger.info("重置每日账户切换标记")

                # 重置国债逆回购状态（新的一天）
                guozhai_status = {account: False for account in ACCOUNTS}
                guozhai_retry_status = {account: False for account in ACCOUNTS}
                logger.info("重置国债逆回购状态")

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
    # config/settings.py

    # 时间窗口设置
    # STRATEGY_WINDOW_START = dt_time(9, 30)
    # STRATEGY_WINDOW_END = dt_time(9, 35)
    # REPO_TIME_START = dt_time(14, 59)
    # REPO_TIME_END = dt_time(15, 1)
    #
    # # 文件路径
    # # Strategy_portfolio_today_file = "path/to/strategy.xlsx"
    # # Combination_portfolio_today_file = "path/to/combination.xlsx"
    # # OPERATION_HISTORY_FILE = "path/to/history.json"
    #
    # # 延迟范围（秒）
    # MIN_DELAY = 50
    # MAX_DELAY = 70
    #
    # # 最大运行时间（小时）
    # MAX_RUN_TIME = 8
    end_time_hour = 15
    end_time_minute = 30

    asyncio.run(main())
