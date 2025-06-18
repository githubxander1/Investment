# 自动化交易.py
import asyncio
import datetime
import os
import sys
import time
import uiautomator2 as u2

from Investment.THS.AutoTrade.config.settings import (
    OPRATION_RECORD_DONE_FILE,
    Strategy_portfolio_today, Combination_portfolio_today,
    OPERATION_HISTORY_FILE
)
from Investment.THS.AutoTrade.pages.ths_page2 import THSPage
from Investment.THS.AutoTrade.scripts.数据处理 import process_excel_files
from Investment.THS.AutoTrade.utils.logger import setup_logger

logger = setup_logger("自动化交易日志")


async def connect_to_device():
    """连接设备"""
    try:
        d = u2.connect()
        #打印当前屏幕的结构树
        # print("当前屏幕结构树:\n")
        # pprint(d.dump_hierarchy())
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


async def wait_for_flag_file(flag_file):
    """等待调仓记录完成标志文件出现并删除它"""
    while not os.path.exists(flag_file):
        logger.info("等待调仓操作记录完成...")
        await asyncio.sleep(15)

    if os.path.exists(flag_file):
        logger.info("检测到标志文件，开始自动化交易")
        os.remove(flag_file)
        logger.info("标志文件已删除")


def get_file_modification_times(file_paths):
    import os
    import time

    for path in file_paths:
        with open(path, 'a'):
            os.utime(path, None)  # 更新文件时间戳
        # print(f"刷新文件时间戳: {path}")

    times = {
        file_path: os.path.getmtime(file_path)
        for file_path in file_paths
        if os.path.exists(file_path)
    }
    # print("文件最后修改时间:", {k: datetime.datetime.fromtimestamp(v).strftime('%Y-%m-%d %H:%M:%S') for k, v in times.items()})
    return times



def check_files_modified(file_paths, last_modification_times):
    current_modification_times = get_file_modification_times(file_paths)
    # print("当前修改时间:", current_modification_times)
    # print("上次修改时间:", last_modification_times)

    for file_path in file_paths:
        if not os.path.exists(file_path):
            continue

        current_time = current_modification_times[file_path]
        last_time = last_modification_times.get(file_path, 0)

        if abs(current_time - last_time) > 1:  # 容忍1秒误差
            print(f"[变动] 检测到文件变动: {file_path}")
            return True
    return False



async def auto_main():
    logger.info("自动化交易程序开始运行")

    file_paths = [
        Strategy_portfolio_today,
        Combination_portfolio_today,
    ]
    print("监控的文件路径:", file_paths)

    operation_history_file = OPERATION_HISTORY_FILE
    flag_file = OPRATION_RECORD_DONE_FILE

    # 获取初始文件修改时间
    last_modification_times = get_file_modification_times(file_paths)

    # 等待标志文件
    await wait_for_flag_file(flag_file)

    # 初始化设备
    d = await initialize_device()
    if d is None:
        logger.error("设备初始化失败，退出程序")
        return

    ths_page = THSPage(d)

    # 检查文件是否更新
    if check_files_modified(file_paths, last_modification_times):
        logger.info("检测到文件有更新，开始执行交易任务")
        process_excel_files(
            ths_page=ths_page,
            file_paths=file_paths,
            operation_history_file=operation_history_file,
            holding_stock_file=""
        )
        logger.info("文件处理完成")
        last_modification_times.update(get_file_modification_times(file_paths))
    else:
        logger.info("未检测到文件更新，跳过处理")


if __name__ == '__main__':
    try:
        # 初始化文件路径和最后修改时间
        file_paths = [
            Strategy_portfolio_today,
            Combination_portfolio_today,
        ]
        last_modification_times = get_file_modification_times(file_paths)

        # 设置停止时间
        stop_time = datetime.time(23, 0)

        while True:
            now = datetime.datetime.now().time()

            if now.hour >= stop_time.hour and now.minute >= stop_time.minute:
                logger.info("到达停止时间，程序结束运行")
                break

            # 执行主逻辑
            asyncio.run(auto_main())
            logger.info("等待下一轮执行... (30秒后)")
            time.sleep(30)  # 每30秒检查一次

    except KeyboardInterrupt:
        logger.info("用户手动终止程序")
    finally:
        logger.info("程序运行结束")
