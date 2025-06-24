# trade_main.py
import asyncio
import sys
import os
import datetime
from datetime import time as dt_time

from pathlib import Path

from Investment.THS.AutoTrade.utils.file_monitor import get_file_hash, check_files_modified_by_hash

# 添加项目根目录到系统路径
sys.path.append(Path(__file__).parent.as_posix())
sys.path.append(Path(__file__).parent.parent.as_posix())
sys.path.append(Path(__file__).parent.parent.parent.as_posix())

# 导入配置和工具
from Investment.THS.AutoTrade.config.settings import Strategy_portfolio_today, Combination_portfolio_today, \
    OPERATION_HISTORY_FILE
from Investment.THS.AutoTrade.scripts.Combination_portfolio_today import Combination_main
from Investment.THS.AutoTrade.scripts.Strategy_portfolio_today import Strategy_main
from Investment.THS.AutoTrade.utils.scheduler import Scheduler
from Investment.THS.AutoTrade.utils.logger import setup_logger
from Investment.THS.AutoTrade.scripts.auto_trade_on_ths import auto_main

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

#当前文件名，去掉后缀
current_file_name = os.path.splitext(os.path.basename(__file__))[0]
logger = setup_logger(f"{current_file_name}.log")

# 调度器配置
SCHEDULE_CONFIG: dict[str, tuple[float, tuple[int, int], tuple[int, int]]] = {
    "strategy": (1, (9, 29), (23, 33)),
    "etf_combo": (1, (9, 15), (23, 00)),
    "automation": (1, (9, 15), (23, 10))
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
    try:
        logger.info("[策略] 开始执行...")
        result = await Strategy_main()
        logger.info("[策略] 执行完成")
        return result
    except Exception as e:
        logger.warning(f"[策略任务] 执行异常: {e}")
        return False


async def combination_wrapper():
    """组合任务执行包装"""
    try:
        logger.info("[组合] 开始执行...")
        result = await Combination_main()
        logger.info("[组合] 执行完成")
        return result
    except Exception as e:
        logger.error(f"[组合] 执行异常: {e}")
        return False


async def automation_wrapper():
    """自动化交易执行包装"""
    try:
        logger.info("[自动化交易] 开始执行...")
        await auto_main()
        logger.info("[自动化交易] 执行完成")
    except Exception as e:
        logger.warning(f"[自动化交易] 执行异常: {e}")

# 主程序 =========================================================
async def main():
    """主程序：持续监听文件变化并调度任务"""
    try:
        # 初始化调度器
        portfolio_tasks = [
            create_scheduler("策略调度", SCHEDULE_CONFIG["strategy"], strategy_wrapper),
            create_scheduler("组合调度", SCHEDULE_CONFIG["etf_combo"], combination_wrapper),
        ]

        auto_trade_tasks = [
            create_scheduler("自动化交易", SCHEDULE_CONFIG["automation"], automation_wrapper),
        ]

        # 获取初始文件哈希
        file_paths = [Strategy_portfolio_today, Combination_portfolio_today]
        last_hashes = [get_file_hash(fp) for fp in file_paths]
        last_mod_times = {fp: os.path.getmtime(fp) for fp in file_paths}
        logger.info(f"初始文件hash值: {last_hashes}")

        while True:
            now = datetime.datetime.now().time()

            # 判断当前时间是否在交易时间段内
            # if not (dt_time(9, 0) <= now <= dt_time(15, 0)):
            #     logger.info("当前不在交易时间段内，暂停监听...")
            #     if dt_time(9, 30) <= now <= dt_time(15, 0):
            #         logger.info("下午3点已到，程序将自动退出。")
            #         break
            #     await asyncio.sleep(60)
            #     continue

            # 只在 9:30 - 9:33 执行策略调度
            if dt_time(9, 25) <= now <= dt_time(17, 00):
                # await asyncio.gather(*(s.start() for s in portfolio[:1]))  # 只运行策略调度
            # elif dt_time(9, 30) <= now <= dt_time(23, 33):
                # 其他时间运行组合调度和自动化交易
                # await asyncio.gather(
                #     *(s.start() for s in portfolio),
                    # *(s.start() for s in portfolio[1:]),
                    # *(s.start() for s in auto_trade[1:])
                # )
                # 启动策略和组合任务（并行）
                # strategy_task = asyncio.create_task(strategy_wrapper())
                combo_task = asyncio.create_task(combination_wrapper())
                # strategy_updated = await Strategy_main()
                # combo_updated = await Combination_main()

                # 获取返回值
                # strategy_updated = await strategy_task
                combo_updated = await combo_task

                # 如果有新数据，启动自动化交易
                # if strategy_updated or combo_updated:
                if combo_updated:
                    logger.info("检测到策略或组合更新，准备启动自动化交易")
                    await asyncio.gather(*(s.start() for s in auto_trade_tasks))

                # # 检查文件是否有变更（作为备用触发机制）
                # modified, new_hashes = check_files_modified_by_hash(file_paths, last_hashes)
                # if modified:
                #     logger.warning('[文件更新] 检测到文件有更新，开始执行交易任务')
                #     await asyncio.gather(*(s.start() for s in auto_trade_tasks))
                #     last_hashes = new_hashes
                # else:
                #     logger.info("[文件监控] 文件未发生改变，跳过处理")

                await asyncio.sleep(60)  # 每分钟检查一次

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
            logger.info("当前时间是下午3点，程序将自动退出。")
            from Investment.THS.AutoTrade.utils.excel_handler import clear_csv
            clear_csv(Strategy_portfolio_today)
            clear_csv(Combination_portfolio_today)
            sys.exit(0)

    except KeyboardInterrupt:
        logger.warning("用户主动终止程序")
    except Exception as e:
        logger.warning(f"程序启动失败: {str(e)}", exc_info=True)
