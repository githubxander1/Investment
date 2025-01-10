# file_monitor.py
import os

from others.量化投资.THS.自动化交易_同花顺.ths_logger import setup_logger
from others.量化投资.THS.自动化交易_同花顺.整合.config.settings import file_monitor_file
from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer

logger = setup_logger(file_monitor_file)

class FileMonitor:
    def __init__(self, watched_files, callback):
        self.watched_files = watched_files
        self.callback = callback
        self.observer = Observer()
        self.running = False

    def on_modified(self, event):
        if not event.is_directory and event.src_path in self.watched_files and self.running:
            self.callback()
            # 不再立即停止监控，保持监控以便处理后续文件改动
            # self.stop()  # 处理完文件后停止监控

    def start(self):
        event_handler = FileSystemEventHandler()
        event_handler.on_modified = self.on_modified
        self.observer.schedule(event_handler, os.path.dirname(self.watched_files[0]), recursive=False)
        self.observer.start()
        self.running = True
        logger.info("文件监控已启动")

    def stop(self):
        self.running = False
        self.observer.stop()
        self.observer.join()
        logger.info("文件监控已停止")
