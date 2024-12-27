import logging
import os
import threading
from others.量化投资.THS.自动化交易_同花顺.整合.utils.file_monitor import FileMonitor
from others.量化投资.THS.自动化交易_同花顺.整合.config.settings import WATCHED_FOLDER, file_monitor_file
from others.量化投资.THS.自动化交易_同花顺.整合.utils.ths_logger import setup_logger

logger = setup_logger(file_monitor_file)
lock = threading.Lock()
processed_files = False

def file_monitor_callback(file_paths, process_files_func):
    global processed_files
    with lock:
        if processed_files:
            logger.info("文件已处理过，不再重复处理")
            return

        logger.info(f"文件监控触发，开始处理文件: {file_paths}")
        process_files_func(file_paths)
        processed_files = True  # 标记文件已处理

def start_file_monitor(file_paths, process_files_func):
    def callback():
        file_monitor_callback(file_paths, process_files_func)

    file_monitor = FileMonitor(WATCHED_FOLDER, callback)
    logger.info(f"文件监控已启动，监控目录: {WATCHED_FOLDER}")
    file_monitor_thread = threading.Thread(target=file_monitor.start)
    file_monitor_thread.start()
    logger.info(f"文件监控线程已启动")
    return file_monitor_thread
