# scheduler.py
import asyncio
from datetime import datetime, time as dt_time, timedelta

from others.量化投资.THS.自动化交易_同花顺.config.settings import SCHEDULER_LOG_FILE
from others.量化投资.THS.自动化交易_同花顺.utils.logger import setup_logger

logger = setup_logger(SCHEDULER_LOG_FILE)

class Scheduler:
    def __init__(self, interval, callback, start_time=None, end_time=None):
        self.interval = interval  # 间隔时间，单位为分钟
        self.callback = callback
        self.start_time = start_time if start_time is not None else dt_time.min
        self.end_time = end_time if end_time is not None else dt_time.max
        self.is_trading_day = lambda: True
        self._done_event = asyncio.Event()

    def is_weekend(self):
        """检查今天是否为周末"""
        today = datetime.now().weekday()
        return today >= 5  # 5 表示星期六，6 表示星期日

    async def job(self):
        if self.is_trading_day() and not self.is_weekend():
            try:
                await self.callback()
                next_run_time = await self.get_next_run_time()  # 使用 await 调用异步方法
                if next_run_time:
                    countdown = (next_run_time - datetime.now()).seconds
                    logger.info(f"下一次任务将在 {countdown} 秒后 {next_run_time} 执行")
                else:
                    logger.warning("无法确定下一次任务的时间")
            except Exception as e:
                logger.error(f"任务执行失败: {e}", exc_info=True)
        else:
            logger.info("今天不是交易日或为周末，跳过任务执行")

    async def start(self):
        # schedule.every(self.interval).minutes.do(lambda: asyncio.create_task(self.job()))# 如果是秒要去掉

        logger.info("定时任务已启动")
        while True:
            current_time = datetime.now().time()
            if current_time > dt_time(15, 0):  # 检查当前时间是否超过下午三点
                logger.info("当前时间超过下午三点，停止任务执行")
                self._done_event.set()
                break
            if self.start_time <= current_time <= self.end_time:
                await self.job()
                await asyncio.sleep(self.interval * 60)  # 将分钟转换为秒
            else:
                logger.info(f"当前时间为{current_time},不在任务执行窗口内，等待...")
                await asyncio.sleep(60)  # 等待一分钟再检查

    async def get_next_run_time(self):
        now = datetime.now()
        next_run = now + timedelta(minutes=self.interval)  # 如果是秒就改为timedelta(seconds=self.interval)
        if next_run.time() > self.end_time:
            return None
        return next_run

    async def wait_until_done(self):
        await self._done_event.wait()

    # def is_trading_day(self, date):
    #     xshg = mcal.get_calendar('XSHG')  # 获取上海证券交易所的交易日历
    #     schedule = xshg.schedule(start_date=date, end_date=date)
    #     return not schedule.empty
