# main.py
import asyncio
from datetime import time as dt_time, datetime
import sys
import os

# 获取当前文件所在的目录
current_dir = os.path.dirname(os.path.abspath(__file__))
print("当前文件所在目录:", current_dir)

# 获取项目根目录（假设项目根目录为 'others' 目录）
project_root = os.path.abspath(os.path.join(current_dir, '..', '..', '..'))
print("项目根目录:", project_root)

# 将项目根目录添加到系统路径
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# 确认项目根目录已正确添加到 sys.path
print("sys.path:", sys.path)

# 使用绝对路径导入模块
from others.量化投资.THS.自动化交易_同花顺.scripts.etf和股票组合_今天调仓 import ETF_Combination_main, logger
from others.量化投资.THS.自动化交易_同花顺.scripts.策略_今天调仓 import strategy_main
from others.量化投资.THS.自动化交易_同花顺.utils.scheduler import Scheduler

async def strategy_main_wrapper():
    """策略任务的包装函数，执行策略逻辑"""
    logger.info("当前时间介于9:30 9:33，执行策略 today_trade")
    if strategy_main is None:
        logger.error("strategy_main 为 None")
    else:
        await strategy_main()

async def ETF_Combination_main_wrapper():
    """组合任务的包装函数，执行ETF和股票组合逻辑"""
    logger.info("当前时间介于9:30 15:30，执行etf和股票组合")
    await ETF_Combination_main()

async def main():
    """主函数，调度策略和组合任务"""
    try:
        # 检查是否为周末
        # if datetime.now().weekday() >= 5:
        #     logger.info("今天是周末，停止程序")
        #     return

        # 检查当前时间是否在任务执行窗口内
        current_time = datetime.now().time()
        # if not (dt_time(9, 30) <= current_time <= dt_time(20, 30)):
        #     logger.info("当前时间不在任务执行窗口内，停止程序")
        #     return

        # 调度器1：9:30 到 9:33 每0.25分钟执行一次策略
        scheduler_strategy = Scheduler(
            interval=0.25,  # 0.25分钟 = 15秒
            callback=strategy_main_wrapper,
            start_time=dt_time(9, 00),
            end_time=dt_time(9, 33)
        )
        asyncio.create_task(scheduler_strategy.start())
        logger.info("策略调度器已启动")

        # 调度器2：9:30 到 15:30 每1分钟执行一次组合
        scheduler_etf = Scheduler(
            interval=1,  # 1分钟 = 60秒
            callback=ETF_Combination_main_wrapper,
            start_time=dt_time(9, 00),
            end_time=dt_time(20, 30)
        )
        asyncio.create_task(scheduler_etf.start())
        logger.info("组合调度器已启动")

        # 调度器3：9:30 到 15:00 每2分钟执行一次自动化交易
        # scheduler_auto = Scheduler(interval=2,  # 2分钟 = 120秒
        #                            callback=auto_main_wrapper,
        #                            start_time=dt_time(9, 30),
        #                            end_time=dt_time(15, 0))
        # asyncio.create_task(scheduler_auto.start())
        # logger.info("自动化交易调度器已启动")

        # while True:
        # current_time = datetime.now().time()
        #     if current_time > dt_time(20, 0):  # 检查当前时间是否超过下午三点
        #         logger.info("当前时间超过下午三点，停止任务执行")
        #         self._done_event.set()
        #         break
        #     if self.start_time <= current_time <= self.end_time:
        # 运行事件循环
        await asyncio.gather(
            # scheduler_strategy.wait_until_done(),
            # scheduler_etf.wait_until_done(),
            scheduler_strategy.start(),
            scheduler_etf.start(),
        )

        # 所有调度任务完成后，更新账户持仓信息
        # logger.info("所有调度任务已完成，开始更新账户持仓信息")
        # update_holding_info()
        # logger.info("账户持仓信息更新完成")

    except Exception as e:
        logger.error(f"调度器启动失败: {e}", exc_info=True)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception as e:
        logger.error(f"事件循环启动失败: {e}", exc_info=True)
