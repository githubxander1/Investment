# main.py
import asyncio
from datetime import time as dt_time

from others.量化投资.THS.自动化交易_同花顺.scripts.策略_今天调仓 import strategy_main
from others.量化投资.THS.自动化交易_同花顺.scripts.组合_今天调仓 import combination_main
from others.量化投资.THS.自动化交易_同花顺.scripts.自动化交易 import auto_main
from others.量化投资.THS.自动化交易_同花顺.utils.scheduler import Scheduler, logger


async def strategy_main_wrapper():
    logger.info("当前时间介于9:29 9:33，执行策略 today_trade")
    if strategy_main is None:
        logger.error("strategy_main 为 None")
    else:
        await strategy_main()

async def combination_main_wrapper():
    logger.info("当前时间介于9:25 15:00，执行组合 today_trade")
    await combination_main()

async def auto_main_wrapper():
    logger.info("当前时间介于9:25 15:00，执行组合 today_trade")
    await auto_main()

# async def main():
#     try:
#         current_time = datetime.datetime.now().time()
#
#         if dt_time(9, 29) <= current_time < dt_time(9, 33):
#             await strategy_main_wrapper()
#         elif dt_time(9, 25) <= current_time < dt_time(15, 0):
#             await combination_main_wrapper()
#         else:
#             print("不在执行时间段内")
#     except Exception as e:
#         logger.error(f"主函数执行失败: {e}", exc_info=True)

async def main():
    try:
        # 调度器1：9:29 到 9:33 每0.25分钟执行一次策略
        scheduler_strategy = Scheduler(interval=0.25,  # 0.25分钟
                                       callback=strategy_main_wrapper,
                                       start_time=dt_time(9, 29),
                                       end_time=dt_time(9, 33))
        asyncio.create_task(scheduler_strategy.start())
        logger.info("策略调度器已启动")

        # 调度器2：9:25 到 15:00 每1分钟执行一次组合
        scheduler_combination = Scheduler(interval=1,  # 1分钟 = 60秒
                                          callback=combination_main_wrapper,
                                          start_time=dt_time(9, 25),
                                          end_time=dt_time(15, 00))
        asyncio.create_task(scheduler_combination.start())
        logger.info("组合调度器已启动")

        # 调度器3：9:30 到 15:00 每2分钟执行一次自动化交易
        # scheduler_auto = Scheduler(interval=2,  # 120秒
        #                            callback=auto_main_wrapper,
        #                            start_time=dt_time(9, 30),
        #                            end_time=dt_time(15, 0))
        # asyncio.create_task(scheduler_auto.start())
        # logger.info("自动化交易调度器已启动")

        # 运行事件循环
        await asyncio.gather(
            scheduler_strategy.wait_until_done(),
            scheduler_combination.wait_until_done(),
            # scheduler_auto.wait_until_done(),
        )

    except Exception as e:
        logger.error(f"调度器启动失败: {e}", exc_info=True)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception as e:
        logger.error(f"事件循环启动失败: {e}", exc_info=True)
