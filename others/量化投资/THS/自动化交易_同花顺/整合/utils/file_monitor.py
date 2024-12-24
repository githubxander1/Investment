# file_monitor.py
import time
import threading
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

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
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            self.observer.stop()
        self.observer.join()
