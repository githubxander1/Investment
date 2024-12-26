import datetime
import logging
import os
import sys
import time
import pandas as pd
import uiautomator2 as u2
from others.量化投资.THS.自动化交易_同花顺.整合.config.settings import (
    THS_AUTO_TRADE_LOG_FILE,
    OPERATION_HISTORY_FILE,
    DATA_DIR,
    OPRATION_RECORD_DONE_FILE, trade_operations_log_file, STRATEGY_TODAY_ADJUSTMENT_FILE, COMBINATION_TODAY_ADJUSTMENT_FILE
)
from others.量化投资.THS.自动化交易_同花顺.整合.pages.ths_page2 import THSPage
from others.量化投资.THS.自动化交易_同花顺.整合.utils.ths_logger import setup_logger
from others.量化投资.THS.自动化交易_同花顺.整合.utils.file_monitor_utils import FileMonitor
from others.量化投资.THS.自动化交易_同花顺.整合.utils.trade_operations import process_excel_files, read_operation_history, write_operation_history

logger = setup_logger(THS_AUTO_TRADE_LOG_FILE)

def connect_to_device():
    try:
        d = u2.connect()
        logger.info(f"连接设备: {d.serial}")
        return d
    except Exception as e:
        logger.error(f"连接设备失败: {e}", exc_info=True)
        return None

def start_app(d, package_name):
    try:
        d.app_start(package_name, wait=True)
        logger.info(f"启动app: {package_name}")
        return True
    except Exception as e:
        logger.error(f"启动app失败 {package_name}: {e}", exc_info=True)
        return False

def initialize_device():
    d = connect_to_device()
    if d is None:
        logger.error("连接设备失败，退出程序")
        return None
    if not start_app(d, 'com.hexin.plat.android'):
        logger.error("启动APP失败，退出程序")
        return None
    return d

def wait_for_flag_file(flag_file):
    while not os.path.exists(flag_file):
        logger.info("等待调仓操作记录完成的标志文件...")
        time.sleep(10)
    if os.path.exists(flag_file):
        logger.info("检测到标志文件，今日调仓操作已记录完成，开始自动化交易...")
        os.remove(flag_file)
        logger.info("标志文件已删除")

def get_file_modification_times(file_paths):
    return {file_path: os.path.getmtime(file_path) for file_path in file_paths if os.path.exists(file_path)}

def check_files_modified(file_paths, last_modification_times):
    current_modification_times = get_file_modification_times(file_paths)
    for file_path in file_paths:
        if file_path not in last_modification_times or last_modification_times[file_path] != current_modification_times[file_path]:
            return True
    return False

def main(file_paths, last_modification_times):
    logger.info("自动化交易程序开始运行")

    # 等待组合调仓完成的标志文件
    flag_file = OPRATION_RECORD_DONE_FILE
    wait_for_flag_file(flag_file)

    # 初始化设备和页面对象
    d = initialize_device()
    if d is None:
        logger.error("初始化设备失败，退出程序")
        sys.exit(1)
    ths_page = THSPage(d)

    # # 检查文件是否有更新
    # if check_files_modified(file_paths, last_modification_times):
    #     operation_history_file = OPERATION_HISTORY_FILE
    process_excel_files(ths_page, file_paths, operation_history_file)
    #     logger.info("文件处理完成")
    #     last_modification_times.update(get_file_modification_times(file_paths))
    # else:
    #     logger.info("文件没有更新，跳过处理")

if __name__ == '__main__':
    try:
        # 初始化文件路径和最后修改时间
        file_paths = [
            STRATEGY_TODAY_ADJUSTMENT_FILE,
            COMBINATION_TODAY_ADJUSTMENT_FILE
        ]
        operation_history_file = OPERATION_HISTORY_FILE
        last_modification_times = get_file_modification_times(operation_history_file)

        # 主循环，保持程序运行
        stop_time = datetime.time(19, 00)  # 设置停止时间为15:00
        while True:
            now = datetime.datetime.now().time()

            # 检查是否达到停止时间
            if now.hour >= stop_time.hour and now.minute >= stop_time.minute:
                logger.info("到达停止时间，自动化交易程序结束运行")
                break

            # 执行主逻辑
            main(file_paths, last_modification_times)
            time.sleep(30)  # 每分钟检查一次

    except KeyboardInterrupt:
        logger.info("程序被手动终止")
    finally:
        logger.info("程序结束运行")
