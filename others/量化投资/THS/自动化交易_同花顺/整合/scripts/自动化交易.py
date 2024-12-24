import datetime
import logging
import os
import threading
import time
import pandas as pd
import uiautomator2 as u2
from others.量化投资.THS.自动化交易_同花顺.整合.config.settings import (
    THS_AUTO_TRADE_LOG_FILE_MAIN,
    OPERATION_HISTORY_FILE,
    SUCCESSFUL_OPERATIONS_FILE,
    DATA_DIR,
    WATCHED_FOLDER,
    OPRATION_RECORD_DONE_FILE
)
from others.量化投资.THS.自动化交易_同花顺.整合.pages.ths_page import THSPage
from others.量化投资.THS.自动化交易_同花顺.整合.utils.ths_logger import setup_logger
from others.量化投资.THS.自动化交易_同花顺.整合.utils.file_monitor_utils import start_file_monitor
from others.量化投资.THS.自动化交易_同花顺.整合.utils.trade_operations import process_excel_files

logger = setup_logger(THS_AUTO_TRADE_LOG_FILE_MAIN)

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
def load_file(file_path, columns):
    if not os.path.exists(file_path):
        logger.info(f"文件 {file_path} 不存在，创建一个新的空 DataFrame")
        return os.makedirs(os.path.dirname(file_path), exist_ok=True)

    try:
        df = pd.read_csv(file_path)
        if df.empty:
            logger.info(f"文件 {file_path} 为空，返回一个新的空 DataFrame")
            return pd.DataFrame(columns=columns)
        return df
    except pd.errors.EmptyDataError:
        logger.info(f"文件 {file_path} 为空，返回一个新的空 DataFrame")
        return pd.DataFrame(columns=columns)
    except Exception as e:
        logger.error(f"读取文件 {file_path} 时出错: {e}")
        raise
def load_operation_data():
    operation_history_df = load_file(OPERATION_HISTORY_FILE, ['stock_name', 'operation', 'status'])
    logger.info(f'加载操作历史: \n{operation_history_df}')
    successful_operations_df = load_file(SUCCESSFUL_OPERATIONS_FILE, ['stock_name', 'operation', 'status'])
    logger.info(f'加载成功操作记录: \n{successful_operations_df}')
    return operation_history_df, successful_operations_df
def wait_for_flag_file(flag_file):
    while not os.path.exists(flag_file):
        logger.info("等待调仓操作记录完成的标志文件...")
        time.sleep(10)
    logger.info("检测到文件改动，今日调仓操作已记录完成，等待一分钟后开始自动化交易...")
    time.sleep(20)
    os.remove(flag_file)
    logger.info("标志文件已删除")


def main():
    global processed_files

    # 等待组合调仓完成的标志文件
    flag_file = OPRATION_RECORD_DONE_FILE
    wait_for_flag_file(flag_file)

    # 初始化设备
    d = initialize_device()
    if d is None:
        return

    time.sleep(10)

    ths_page = THSPage(d)


    # 加载操作数据
    operation_history_df, successful_operations_df = load_operation_data()

    # 假设Excel文件在同目录下的data文件夹中
    file_paths = [
        os.path.join(DATA_DIR, '策略今天调仓.xlsx'),
        os.path.join(DATA_DIR, '组合今天调仓.xlsx')
    ]
    # 定义处理文件的函数
    def process_files(file_paths):
        nonlocal operation_history_df, successful_operations_df
        operation_history_df, successful_operations_df = process_excel_files(d, THSPage,file_paths, operation_history_df, successful_operations_df)

    # 启动文件监控
    start_file_monitor(file_paths, process_files)

    # 主循环，保持程序运行
    try:
        while True:
            current_time = datetime.datetime.now().time()
            if current_time >= datetime.time(19,0):
                logger.info("当前时间已超过15点，程序将退出")
                break
            time.sleep(60)  # 每分钟检查一次
    except KeyboardInterrupt:
        logger.info("程序被手动终止")
    finally:
        logger.info("程序运行结束")
        logging.shutdown()

if __name__ == "__main__":
    main()
