# file_monitor.py
import time
import threading
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

from others.量化投资.THS.自动化交易_同花顺.ths_logger import setup_logger
from others.量化投资.THS.自动化交易_同花顺.整合.config.settings import file_monitor_file
#
logger = setup_logger(file_monitor_file)

class FileMonitor:
    def __init__(self, watched_folder, callback):
        self.watched_folder = watched_folder
        self.callback = callback
        self.observer = Observer()

    def on_modified(self, event):
        if not event.is_directory:
            self.callback()

    def start(self):
        event_handler = FileSystemEventHandler()
        event_handler.on_modified = self.on_modified
        self.observer.schedule(event_handler, self.watched_folder, recursive=False)
        self.observer.start()
        logger.info("文件监控已启动")
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            self.observer.stop()
            logger.info("文件监控已停止")
        self.observer.join()
        logger.info("文件监控线程已退出")
