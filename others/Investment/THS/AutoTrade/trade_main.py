# D:\Xander\PycharmProject\z_others\Investment\THS\AutoTrade\trade_main.py
import asyncio
import sys
import os
import datetime
from datetime import time as dt_time
# from plogger import plogger
from typing import Dict, Tuple


from pathlib import Path
sys.path.append(Path(__file__).parent.as_posix())
sys.path.append(Path(__file__).parent.parent.as_posix())
sys.path.append(Path(__file__).parent.parent.parent.as_posix())
# logger(sys.path)

from THS.AutoTrade.config.settings import \
    Strategy_portfolio_today, Combination_portfolio_today
from THS.AutoTrade.utils.excel_handler import clear_csv

# 模块导入 ========================================================
from THS.AutoTrade.scripts.组合.Combination_portfolio_today import Combination_main
from THS.AutoTrade.scripts.策略.strategy_portfolio_today import strategy_main
from THS.AutoTrade.utils.scheduler import Scheduler
from THS.AutoTrade.utils.logger import setup_logger
from THS.AutoTrade.scripts.自动化交易 import auto_main

# 路径初始化 ======================================================
current_dir = os.path.dirname(os.path.abspath(__file__))
# logger(f"当前目录: {current_dir}")
project_root = os.path.abspath(os.path.join(current_dir, '..', '..', '..', '..'))
# logger(f"项目根目录: {project_root}")

if project_root not in sys.path:
    sys.path.insert(0, project_root)
    # logger(f"已将项目根目录添加到 sys.path: {project_root}")
else:
    print(f"项目根目录已在 sys.path 中: {project_root}")

logger = setup_logger(f"{__file__}.log")

# 调度器配置 ======================================================
SCHEDULE_CONFIG: Dict[str, Tuple[float, Tuple[int, int], Tuple[int, int]]] = {
    "strategy": (1, (9, 29), (9, 33)),
    "etf_combo": (1, (9, 15), (15, 00)),
    "automation": (1, (9, 15), (15, 00))
}

# 公共方法 ========================================================
def create_scheduler(name: str, config: tuple, callback) -> Scheduler:
    """统一创建调度器"""
    interval, start, end = config
    print(f"初始化 {name} 调度器 | 间隔:{interval}min | 时段:{start[0]:02}:{start[1]:02}-{end[0]:02}:{end[1]:02}")

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
        logger.warning("策略模块加载失败: strategy_main 为 None")
        return

    logger.info("[策略任务] 开始执行...")
    try:
        await strategy_main()
        next_run = datetime.datetime.now() + datetime.timedelta(seconds=60)
        logger.info(f"\n[策略组合] 执行完成，下一次执行时间: {next_run.strftime('%Y-%m-%d %H:%M:%S')}")
        print("--------------------------------------------------------------")
    except Exception as e:
        logger.warning(f"[策略任务] 执行异常: {e}")

async def combination_wrapper():
    """组合任务执行包装"""
    logger("\n[组合] 开始执行...")
    try:
        await Combination_main()
        next_run = datetime.datetime.now() + datetime.timedelta(seconds=60)
        logger(f"\n[组合] 执行完成，下一次执行时间: {next_run.strftime('%Y-%m-%d %H:%M:%S')}")
        print("----------------------------------------------------")
    except Exception as e:
        logger(f"[组合] 执行异常: {e}")

async def automation_wrapper():
    """自动化交易执行包装"""
    logger("\n[自动化交易] 开始执行...")
    try:
        await auto_main()
        logger("[自动化交易] 执行完成")
    except Exception as e:
        logger(f"[自动化交易] 执行异常: {e}")

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
                name="组合调度",
                config=SCHEDULE_CONFIG["etf_combo"],
                callback=combination_wrapper
            ),
            create_scheduler(
                name='自动化交易',
                config=SCHEDULE_CONFIG['automation'],
                callback=automation_wrapper
            )
        ]

        # 启动所有调度任务
        await asyncio.gather(
            *(scheduler.start() for scheduler in schedulers)
        )

    except Exception as e:
        logger.error(f"主程序异常终止: {str(e)}", exc_info=True)
        raise

if __name__ == "__main__":
    try:
        # 清空上一次的数据
        print('\n---------------------------------------------------------------------------')
        asyncio.run(main())
        now_time = datetime.datetime.now()
        print(now_time)
        # now_time = datetime.datetime.now()
        if now_time.hour == 15 and now_time.minute >= 30:
            logger("当前时间是下午3点，程序将自动退出。")
            # clear_sheet(Combination_portfolio_today, '所有今天调仓')  # 清空昨天的数据
            # clear_sheet(Strategy_portfolio_today, '策略今天调仓')  # 清空昨天的数据
            clear_csv(Strategy_portfolio_today)
            clear_csv(Combination_portfolio_today)

            sys.exit(0)
    except KeyboardInterrupt:
        logger.warning("用户主动终止程序")
    except Exception as e:
        logger.warning(f"程序启动失败: {str(e)}", exc_info=True)
