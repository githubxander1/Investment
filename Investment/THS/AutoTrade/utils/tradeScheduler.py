# 优化后的 TradeScheduler 类
from datetime import time as dt_time, datetime, timedelta
import asyncio
from Investment.THS.AutoTrade.utils.logger import setup_logger

logger = setup_logger("scheduler.log")

class TradeScheduler:
    def __init__(
        self,
        interval: float,
        callback,
        start_time: dt_time = dt_time(9, 0),
        end_time: dt_time = dt_time(15, 0)
    ):
        """
        :param interval: 执行间隔（分钟）
        :param callback: 异步回调函数
        :param start_time: 每日开始时间
        :param end_time: 每日结束时间
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
    def _is_trading_day(self):
        """判断是否为中国股市交易日"""
        today = datetime.now().date()

        # 简单实现：排除周末
        if today.weekday() >= 5:  # 5=Saturday, 6=Sunday
            return False

        # TODO: 可以添加具体节假日判断逻辑
        # 这里可以对接交易所API或使用本地节假日数据

        return True
def _is_trading_day(self):
    """判断是否为中国股市交易日"""
    today = datetime.now().date()

    # 简单实现：排除周末
    if today.weekday() >= 5:  # 5=Saturday, 6=Sunday
        return False

    # TODO: 可以添加具体节假日判断逻辑
    # 这里可以对接交易所API或使用本地节假日数据

    return True


    async def _execute_task(self):
        """简化版任务执行"""
        try:
            await self.callback()
        except Exception as e:
            logger.error(f"任务执行异常: {str(e)}", exc_info=True)

    async def start(self):
        """启动调度器核心逻辑"""
        logger.info(f"调度器启动 | 时间窗口: {self.start_time.strftime('%H:%M')}-{self.end_time.strftime('%H:%M')}")

        while not self._shutdown.is_set():
            if self._within_time_window():
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
        logger.info("调度器已停止")
