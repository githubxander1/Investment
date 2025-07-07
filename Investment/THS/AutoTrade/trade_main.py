# trade_main.py

import asyncio
import datetime
from datetime import time as dt_time
import uiautomator2 as u2
from Investment.THS.AutoTrade.scripts.Combination_portfolio_today import Combination_main
from Investment.THS.AutoTrade.scripts.Strategy_portfolio_today import Strategy_main
# from Investment.THS.AutoTrade.pages.page_guozhai import guozhai_operation  # 导入国债逆回购操作
from Investment.THS.AutoTrade.pages.page_logic import THSPage
from Investment.THS.AutoTrade.scripts.data_process import process_excel_files
from Investment.THS.AutoTrade.utils.logger import setup_logger
from Investment.THS.AutoTrade.config.settings import (
    Strategy_portfolio_today,
    Combination_portfolio_today,
    OPERATION_HISTORY_FILE
)

# 设置日志
logger = setup_logger("trade_main.log")

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

async def main():
    """主程序：控制任务执行的时间窗口"""
    logger.info("⏰ 调度器已启动，等待执行时间窗口...")

    d = await initialize_device()
    if not d:
        logger.error("❌ 设备初始化失败")
        return

    ths_page = THSPage(d)

    # 国债逆回购任务只执行一次
    guozhai_success = False
    while True:
        now = datetime.datetime.now().time()

        # 如果当前时间超过 15:30，停止运行
        if now >= dt_time(15, 30):
            logger.info("当前时间超过 15:30，停止运行")
            break

        # 初始化变量，防止 UnboundLocalError
        strategy_success = False
        strategy_data = None
        combination_success = False
        combination_data = None

        # 判断是否在策略任务时间窗口（9:30-9:33）
        if dt_time(9, 30) <= now <= dt_time(9, 33):
            logger.info("---------------------策略任务开始执行---------------------")
            strategy_result = await Strategy_main()
            if strategy_result:
                strategy_success, strategy_data = strategy_result
            else:
                logger.warning("⚠️ 策略任务返回空值，默认视为无更新")
            logger.info(f"策略是否有新增数据: {strategy_success}\n---------------------策略任务执行结束---------------------")

        # 判断是否在组合任务和自动化交易时间窗口（9:15-15:00）
        if dt_time(9, 25) <= now <= dt_time(14, 55):
            logger.info("---------------------组合任务开始执行---------------------")
            combination_result = await Combination_main()
            if combination_result:
                combination_success, combination_data = combination_result
            else:
                logger.warning("⚠️ 组合任务返回空值，默认视为无更新")
            logger.info(f"组合是否有新增数据: {combination_success}\n---------------------组合任务执行结束---------------------")

            # 如果有任何一个数据获取成功，则执行交易处理
            if strategy_success or combination_success:
                file_paths = [Strategy_portfolio_today, Combination_portfolio_today]
                process_excel_files(ths_page, file_paths, OPERATION_HISTORY_FILE)

        # 每隔1分钟执行一次
        await asyncio.sleep(60)

        # 在组合任务结束后执行国债逆回购操作（只执行一次）
        if not guozhai_success and dt_time(14, 56) <= now <= dt_time(15, 30):
            logger.info("---------------------国债逆回购任务开始执行---------------------")
            # ths = THSPage(d)
            success, message = ths_page.guozhai_operation()
            if success:
                logger.info("国债逆回购成功")
                guozhai_success = True  # 标记国债逆回购任务已执行
            else:
                logger.info(f"国债逆回购失败: {message}")
            logger.info("---------------------国债逆回购任务执行结束---------------------")

        elif not guozhai_success:
            logger.info("当前时间不在国债逆回购任务执行窗口内 (14:56-15:30)，跳过 国债逆回购 任务执行")



if __name__ == '__main__':
    asyncio.run(main())
