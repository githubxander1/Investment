# scheduler.py
import schedule
import time
from datetime import datetime, time as dt_time, timedelta

from others.量化投资.THS.自动化交易_同花顺.ths_logger import setup_logger
from others.量化投资.THS.自动化交易_同花顺.整合.config.settings import SCHEDULER_LOG_FILE
from others.量化投资.THS.自动化交易_同花顺.整合.utils.notification import send_notification
# import pandas_market_calendars as mcal

logger = setup_logger(SCHEDULER_LOG_FILE)

class Scheduler:
    def __init__(self, interval, callback, start_time=None, end_time=None):
        self.interval = interval
        self.callback = callback
        self.start_time = start_time if start_time is not None else dt_time.min
        self.end_time = end_time if end_time is not None else dt_time.max

    def job(self):
        try:
            self.callback()
            next_run_time = self.get_next_run_time()
            # logger.info(f'{next_run_time}')
            if next_run_time:
                countdown = (next_run_time - datetime.now()).seconds
                logger.info(f"下一次任务将在 {countdown} 秒后 {next_run_time} 执行")
            else:
                logger.warning("无法确定下一次任务的时间")
            # 添加更多调试信息
            # logger.debug(f"当前时间: {datetime.now()}")
            # logger.debug(f"下次运行时间: {next_run_time}")
        except Exception as e:
            logger.error(f"任务执行失败: {e}", exc_info=True)

    def start(self):
        schedule.every(self.interval).minutes.do(self.job)
        logger.info("定时任务已启动")
        while True:
            current_time = datetime.now().time()
            # logger.debug(f"当前时间: {current_time}")  # 添加调试信息
            if self.start_time <= current_time <= self.end_time:
                schedule.run_pending()
                time.sleep(1)
            else:
                if self.start_time <= current_time:
                    logger.info(f"当前时间为{current_time},定时任务结束")
                    send_notification("定时任务结束")
                    break
                else:
                    logger.info("当前时间不在任务执行窗口内，等待...")
                    time.sleep(60)  # 等待一分钟再检查

    def get_next_run_time(self):
        now = datetime.now()
        next_run = now + timedelta(minutes=self.interval)
        if next_run.time() > self.end_time:
            return None
        return next_run

    # def is_trading_day(self, date):
    #     xshg = mcal.get_calendar('XSHG')  # 获取上海证券交易所的交易日历
    #     schedule = xshg.schedule(start_date=date, end_date=date)
    #     return not schedule.empty
