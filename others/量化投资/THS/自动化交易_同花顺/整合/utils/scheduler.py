# scheduler.py
import schedule
import time

class Scheduler:
    def __init__(self, interval, callback):
        self.interval = interval
        self.callback = callback

    def job(self):
        self.callback()

    def start(self):
        schedule.every(self.interval).minutes.do(self.job)
        while True:
            schedule.run_pending()
            time.sleep(1)
