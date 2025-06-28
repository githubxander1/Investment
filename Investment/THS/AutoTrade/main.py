import asyncio
import datetime
from datetime import time as dt_time
import os
import logging
import sys
import uiautomator2 as u2
from Investment.THS.AutoTrade.scripts.Combination_portfolio_today import Combination_main
from Investment.THS.AutoTrade.scripts.Strategy_portfolio_today import Strategy_main
from Investment.THS.AutoTrade.pages.page_logic import THSPage
from Investment.THS.AutoTrade.scripts.process_stocks_to_operate_data import process_excel_files
from Investment.THS.AutoTrade.utils.file_monitor import get_file_hash, check_files_modified_by_hash
from Investment.THS.AutoTrade.utils.logger import setup_logger
from Investment.THS.AutoTrade.utils.scheduler import TradeScheduler
from Investment.THS.AutoTrade.config.settings import (
    Strategy_portfolio_today,
    Combination_portfolio_today,
    OPERATION_HISTORY_FILE
)
from Investment.THS.AutoTrade.utils.tradeScheduler import TradeScheduler

# 设置日志
logger = setup_logger("trade_scheduler.log")

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
    """主程序：启动两个定时任务"""
    logger.info("⏰ 调度器已启动，等待执行时间窗口...")

    d = await initialize_device()
    if not d:
        logger.error("❌ 设备初始化失败")
        return

    ths_page = THSPage(d)

    # 策略文件调度器（9:30-15:00）
    strategy_scheduler = TradeScheduler(
        interval=1,
        callback=lambda: asyncio.run(Strategy_main()),
        start_time=dt_time(9, 30),
        end_time=dt_time(19, 0)
    )

    # 组合文件调度器（9:30-15:33）
    combination_scheduler = TradeScheduler(
        interval=1,
        callback=lambda: asyncio.run(Combination_main()),
        start_time=dt_time(9, 30),
        end_time=dt_time(19, 33)
    )

    # 启动交易处理循环
    while True:
        try:
            # 执行策略数据获取
            strategy_success, strategy_data = await Strategy_main()
            logger.info(f"策略数据获取结果: {strategy_success}")

            # 执行组合数据获取
            combination_success, combination_data = await Combination_main()
            logger.info(f"组合数据获取结果: {combination_success}")

            # 如果有任何一个数据获取成功，则执行交易处理
            if strategy_success or combination_success:
                file_paths = [Strategy_portfolio_today, Combination_portfolio_today]
                process_excel_files(ths_page, file_paths, OPERATION_HISTORY_FILE)

        except Exception as e:
            logger.error(f"主循环执行错误: {e}", exc_info=True)

        # 每隔1分钟执行一次
        await asyncio.sleep(60)

if __name__ == '__main__':
    asyncio.run(main())
