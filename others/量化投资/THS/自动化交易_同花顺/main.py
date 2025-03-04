# D:\Xander\PycharmProject\others\量化投资\THS\自动化交易_同花顺\main.py
import asyncio
import sys
import os
from datetime import time as dt_time, datetime
from typing import Dict, Tuple

# 路径初始化 ======================================================
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, '..', '..', '..'))

if project_root not in sys.path:
    sys.path.insert(0, project_root)

# 模块导入 ========================================================
from others.量化投资.THS.自动化交易_同花顺.scripts.etf和股票组合_今天调仓 import ETF_Combination_main, logger
from others.量化投资.THS.自动化交易_同花顺.scripts.策略_今天调仓 import strategy_main
from others.量化投资.THS.自动化交易_同花顺.utils.scheduler import Scheduler

# 调度器配置 ======================================================
SCHEDULE_CONFIG: Dict[str, Tuple[float, Tuple[int, int], Tuple[int, int]]] = {
    "strategy": (0.25, (9, 0), (9, 33)),
    "etf_combo": (1.0, (9, 0), (20, 30))
}

# 公共方法 ========================================================
def create_scheduler(name: str, config: tuple, callback) -> Scheduler:
    """统一创建调度器"""
    interval, start, end = config
    logger.info(f"初始化 {name} 调度器 | 间隔:{interval}min | 时段:{start[0]:02}:{start[1]:02}-{end[0]:02}:{end[1]:02}")

    return Scheduler(
        interval=interval,
        callback=callback,
        start_time=dt_time(*start),
        end_time=dt_time(*end)
    )

# 任务包装器 ======================================================
async def strategy_wrapper():
    """策略任务执行包装"""
    if not strategy_main:
        logger.error("策略模块加载失败: strategy_main 为 None")
        return

    logger.info("[策略任务] 开始执行...")
    try:
        await strategy_main()
        logger.info("[策略任务] 执行完成")
    except Exception as e:
        logger.error(f"[策略任务] 执行异常: {str(e)}", exc_info=True)

async def etf_combo_wrapper():
    """组合任务执行包装"""
    logger.info("[ETF组合] 开始执行...")
    try:
        await ETF_Combination_main()
        logger.info("[ETF组合] 执行完成")
    except Exception as e:
        logger.error(f"[ETF组合] 执行异常: {str(e)}", exc_info=True)

# 主程序 =========================================================
async def main():
    """调度器主程序"""
    try:
        # 初始化调度器
        schedulers = [
            create_scheduler(
                name="策略调度",
                config=SCHEDULE_CONFIG["strategy"],
                callback=strategy_wrapper
            ),
            create_scheduler(
                name="ETF组合调度",
                config=SCHEDULE_CONFIG["etf_combo"],
                callback=etf_combo_wrapper
            )
        ]

        # 启动所有调度任务
        await asyncio.gather(
            *(scheduler.start() for scheduler in schedulers)
        )

    except Exception as e:
        logger.critical(f"主程序异常终止: {str(e)}", exc_info=True)
        raise

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.warning("用户主动终止程序")
    except Exception as e:
        logger.error(f"程序启动失败: {str(e)}", exc_info=True)
