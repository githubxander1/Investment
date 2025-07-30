# trade_main.py

import asyncio
import random
import datetime
from datetime import time as dt_time

import uiautomator2 as u2

# 自定义模块
from Investment.THS.AutoTrade.scripts.portfolio_today.Combination_portfolio_today import Combination_main
from Investment.THS.AutoTrade.scripts.portfolio_today.Robots_portfolio_today import Robot_main
from Investment.THS.AutoTrade.scripts.portfolio_today.Strategy_portfolio_today import Strategy_main
from Investment.THS.AutoTrade.pages.page_guozhai import GuozhaiPage
from Investment.THS.AutoTrade.pages.page import THSPage
from Investment.THS.AutoTrade.scripts.data_process import process_excel_files, read_operation_history
from Investment.THS.AutoTrade.scripts.trade_logic import TradeLogic
from Investment.THS.AutoTrade.utils.logger import setup_logger
from Investment.THS.AutoTrade.config.settings import (
    Strategy_portfolio_today_file,
    Combination_portfolio_today_file,
    OPERATION_HISTORY_FILE,
    MIN_DELAY,
    MAX_DELAY,
    MAX_RUN_TIME,
    Robot_portfolio_today_file, Account_holding_file,
)

# 导入你的20日监控模块
from Investment.THS.AutoTrade.scripts.monitor_20day import daily_check
from Investment.THS.AutoTrade.utils.notification import send_notification

# 设置日志
logger = setup_logger("trade_main.log")
trader = TradeLogic()
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

    # 检查是否在信号检查时间窗口内（9:30-9:35）
    # if dt_time(9, 30) <= current_time <= dt_time(9, 35):
    #定时在九点二十五执行
    if  current_time == dt_time(9, 25):
        logger.info("开始执行早盘信号检查...")
        # 检查是否已经执行过今天的信号检查
        if not morning_signal_checked:
            logger.info("开始执行早盘信号检查...")

            try:
                stocks_code = read_operation_history(Account_holding_file)
                # 定义要监控的股票（从配置或其他地方获取）
                MONITORED_STOCKS = {
                    "600858": "银座股份",
                    "603978": "深圳新星",
                    "603278": "大业股份",
                    "603018": "华社集团",
                    # 可添加更多股票
                }

                # 定义要监控的ETF
                MONITORED_ETFS = {
                    "508011": "嘉实物美消费REIT",
                    "508005": "华夏首创奥莱REIT",
                    "511380": "可转债ETF",
                    "511580": "国债证金债ETF",
                    "518850": "黄金ETF华夏",
                    "510050": "中证500ETF",
                    "510300": "沪深300ETF",
                    "510500": "中证500ETF",
                }

                # 执行股票信号检查（使用5日均线）
                stock_signals_found, stock_signals = daily_check("stock", MONITORED_STOCKS, ma_window=20)

                # 执行ETF信号检查（使用20日均线）
                etf_signals_found, etf_signals = daily_check("etf", MONITORED_ETFS, ma_window=20)

                # 如果有任何信号，发送汇总通知
                if stock_signals_found or etf_signals_found:
                    all_signals = stock_signals + etf_signals
                    summary_msg = "📈📉 早盘信号提醒 📈📉\n" + "\n".join(all_signals)
                    send_notification(summary_msg)
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

# 在 main 函数的 while 循环中添加信号检查调用
async def main():
    """主程序：控制任务执行的时间窗口"""

    logger.info("⏰ 调度器已启动，等待执行时间窗口...")

    # 初始化设备
    d = await initialize_device()
    if not d:
        logger.error("❌ 设备初始化失败")
        return

    # ths_page = THSPage(d)

    # 初始化国债逆回购状态
    guozhai_success = False

    # 记录开始时间，用于最大运行时长控制
    start_time = datetime.datetime.now()

    # 1. 提前读取历史记录
    history_df = read_operation_history(OPERATION_HISTORY_FILE)

    while True:
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

        strategy_data = None
        combination_data = None

        # 判断是否在策略任务时间窗口（9:30-9:33）
        # 改成到了九点三十一就执行一次
        #判断当前时间，如果到了九点三十一就执行一次
        now = datetime.datetime.now().time()
        # if dt_time(9, 31) == now:



        if dt_time(9, 31) <= now <= dt_time(9, 35):
        # if dt_time(9, 31):
            # holding_success, ai_datas = Ai_strategy_main()
            #
            # to_sell = ai_datas.get("to_sell")
            # to_buy = ai_datas.get("to_buy")
            #
            # if not to_sell.empty or not to_buy.empty:
            #     # 将 to_sell 和 to_buy 合并为一个 DataFrame
            #     to_sell['操作'] = '卖出'
            #     to_buy['操作'] = '买入'
            #
            #     combined_df = pd.concat([to_sell[['标的名称', '操作']], to_buy[['标的名称', '操作']]],
            #                             ignore_index=True)
            #     combined_df['新比例%'] = None  # 可根据需要设置默认值
            #
            #     # 写入临时文件
            #     combined_df.to_excel(ai_strategy_diff_file_path, index=False)
            #     logger.warning(f"发现持仓差异，准备执行模拟账户交易操作：买\n{to_buy}，卖\n{to_sell}")

            #     # 初始化设备
            #     d = await initialize_device()
            #     if not d:
            #         logger.error("❌ 设备初始化失败，跳过模拟账户操作")
            #     else:
            #         # ths_page = THSPage(d)
            #
            #         # 切换到模拟账户
            #         common_page.change_account("模拟练习区")
            #         logger.info("✅ 已切换至模拟账户")
            #
            #         # 构造临时文件用于 process_excel_files
            #         from tempfile import NamedTemporaryFile
            #         import pandas as pd
            #
            #         temp_file_path = os.path.join(DATA_DIR, "temp_strategy_diff.xlsx")
            #
            #         # 将 to_sell 和 to_buy 合并为一个 DataFrame
            #         to_sell['操作'] = '卖出'
            #         to_buy['操作'] = '买入'
            #
            #         combined_df = pd.concat([to_sell[['标的名称', '操作']], to_buy[['标的名称', '操作']]],
            #                                 ignore_index=True)
            #         combined_df['新比例%'] = None  # 可根据需要设置默认值
            #
            #         # 写入临时文件
            #         combined_df.to_excel(temp_file_path, index=False)
            #
            #         # 执行交易
            #         process_excel_files(
            #             ths_page=trader,
            #             file_paths=[temp_file_path],
            #             operation_history_file=OPERATION_HISTORY_FILE
            #         )
            #
            #         logger.info("✅ 模拟账户持仓差异处理完成")
            # else:
            #     logger.info("✅ 当前无持仓差异，无需执行模拟账户操作")


            logger.info("---------------------策略/Robot任务开始执行---------------------")
            strategy_result = await Strategy_main()
            robot_result = await Robot_main()
            if strategy_result or robot_result:
                strategy_success, strategy_data = strategy_result
                robot_success, robot_data = robot_result
            else:
                logger.warning("⚠️ 策略/Robot任务返回空值，默认视为无更新")
            logger.info(f"策略/Robot是否有新增数据: {strategy_success}\n---------------------策略/Robot任务执行结束---------------------")
        else:
            logger.debug("尚未进入策略/Robot任务时间窗口，跳过执行")
        # 判断是否在组合任务和自动化交易时间窗口（9:25-15:00）
        if dt_time(9, 25) <= now <= dt_time(end_time_hour, end_time_minute):
            logger.info("---------------------组合任务开始执行---------------------")
            combination_result = await Combination_main()
            if combination_result:
                combination_success, combination_data = combination_result
            else:
                logger.warning("⚠️ 组合任务返回空值，默认视为无更新")
            logger.info(f"组合是否有新增数据: {combination_success}\n---------------------组合任务执行结束---------------------")

            # 如果有任何一个数据获取成功，则执行交易处理
            # if strategy_success or combination_success or holding_success:
                # file_paths = [Strategy_portfolio_today_file, Combination_portfolio_today_file, ai_strategy_diff_file_path]
            if strategy_success or combination_success or robot_success:
                file_paths = [Strategy_portfolio_today_file, Combination_portfolio_today_file, Robot_portfolio_today_file]
                process_excel_files(trader, file_paths, OPERATION_HISTORY_FILE, history_df=history_df)

        else:
            logger.debug("尚未进入组合任务和自动化交易时间窗口，跳过执行")
        # # 国债逆回购操作（只执行一次）
        if not guozhai_success and dt_time(14,56) <= now <= dt_time(end_time_hour,end_time_minute):
            logger.info("---------------------国债逆回购任务开始执行---------------------")
            guozhai = GuozhaiPage(d)
            success, message = guozhai.guozhai_operation()
            if success:
                logger.info("国债逆回购成功")
                guozhai_success = True  # 标记国债逆回购任务已执行
            else:
                logger.info(f"国债逆回购失败: {message}")
            logger.info("---------------------国债逆回购任务执行结束---------------------")

        else:# not guozhai_success and now < dt_time(14, 59):
            logger.debug("尚未进入国债逆回购时间窗口，跳过执行")

        # 随机等待，降低请求频率规律性
        delay = random.uniform(50, 70)
        logger.info(f"💤 等待 {delay:.2f} 秒后继续下一轮检测")
        await asyncio.sleep(delay)

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
    end_time_minute = 00

    asyncio.run(main())
