# D:\Xander\PycharmProject\others\Investment\THS\AutoTrade\utils\scheduler.py
import asyncio
from datetime import datetime, time as dt_time, timedelta
from pprint import pprint

import pandas_market_calendars as mcal

from others.Investment.THS.AutoTrade.config import settings
from others.Investment.THS.AutoTrade.config.settings import SCHEDULER_LOG_FILE
from others.Investment.THS.AutoTrade.utils.logger import setup_logger

logger = setup_logger(SCHEDULER_LOG_FILE)

# 调度器类 ======================================================
class Scheduler:
    def __init__(
        self,
        interval: float,
        callback,
        start_time: dt_time = dt_time(9, 0),   # 默认开始时间改为9点
        end_time: dt_time = dt_time(15, 0)     # 默认结束时间改为15点
    ):
        """
        :param interval: 执行间隔（分钟）
        :param callback: 异步回调函数
        :param start_time: 每日开始时间（强制设为9点）
        :param end_time: 每日结束时间（强制设为15点）
        """
        self.interval = interval
        self.callback = callback
        self.start_time = start_time
        self.end_time = end_time
        self._shutdown = asyncio.Event()

    def _within_time_window(self) -> bool:
        """严格限定在9:00-15:00之间"""
        now = datetime.now().time()
        return self.start_time <= now <= self.end_time

    async def _execute_task(self):
        """简化版任务执行"""
        try:
            await self.callback()
        except Exception as e:
            logger.error(f"任务执行异常: {str(e)}", exc_info=True)

    # async def _calculate_next_run(self) -> datetime:
    #     """计算下一次运行时间"""
    #     now = datetime.now()
    #     start_datetime = datetime(now.year, now.month, now.day, self.start_time.hour, self.start_time.minute, self.start_time.second)
    #
    #     # 如果当前时间已经过了开始时间，则从下一个间隔开始计算
    #     if now.time() > self.start_time:
    #         start_datetime += timedelta(minutes=self.interval)
    #
    #     # 确保下一次运行时间在调度时段内
    #     while start_datetime.time() < self.start_time or start_datetime.time() > self.end_time:
    #         start_datetime += timedelta(minutes=self.interval)
    #
    #     return start_datetime

    async def start(self):
        """启动调度器核心逻辑"""
        pprint(f"调度器启动 | 时间窗口: {self.start_time.strftime('%H:%M')}-{self.end_time.strftime('%H:%M')}")

        while not self._shutdown.is_set():
            if self._within_time_window():
                # next_run = await self._calculate_next_run()
                # print(f"下一次运行时间: {next_run.strftime('%Y-%m-%d %H:%M:%S')}")
                await self._execute_task()

            # 动态计算休眠时间
            now = datetime.now()
            next_run = now + timedelta(minutes=self.interval)
            sleep_seconds = min(
                (datetime.combine(now.date(), self.end_time) - now).total_seconds(),
                (next_run - now).total_seconds()
            )

            await asyncio.sleep(max(sleep_seconds, 60))  # 保证最小休眠60秒

    async def stop(self):
        """优雅停止调度器"""
        self._shutdown.set()
        pprint("调度器已停止")
