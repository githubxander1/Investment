# trade_main.py
import asyncio
import logging
import os
import sys
import signal
from datetime import datetime, time as dt_time

from Investment.THS.AutoTrade.scripts.Strategy_portfolio_today import Strategy_main
from Investment.THS.AutoTrade.scripts.Combination_portfolio_today import Combination_main
from Investment.THS.AutoTrade.scripts.auto_trade_on_ths import auto_main
from Investment.THS.AutoTrade.scripts.process_stocks_to_operate_data import process_excel_files
from Investment.THS.AutoTrade.utils import data_processor

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

from Investment.THS.AutoTrade.utils.logger import setup_logger
from Investment.THS.AutoTrade.config.settings import THS_AUTO_TRADE_LOG_FILE, Strategy_portfolio_today, \
    Combination_portfolio_today, OPERATION_HISTORY_FILE
from Investment.THS.AutoTrade.utils.scheduler import Scheduler

logger = setup_logger(THS_AUTO_TRADE_LOG_FILE)
# STOP_FLAG = False


# def handle_signal(sig, frame):
#     global STOP_FLAG
#     logger.warning("收到终止信号，准备退出...")
#     STOP_FLAG = True


async def run_strategy_tasks():
    strategy_updated = await Strategy_main()
    combo_updated = await Combination_main()
    return strategy_updated or combo_updated


# 当前文件名，用于生成日志文件
current_file_name = os.path.splitext(os.path.basename(__file__))[0]
logger_name = setup_logger(f"{current_file_name}.log")

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
    print(f"🔧 初始化 {name} 调度器 | 间隔:{interval}min | 时间段:{start[0]:02}:{start[1]:02}-{end[0]:02}:{end[1]:02}")

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
        result, new_data = await Strategy_main()
        logger.info("[策略] 执行完成")
        # 对比历史操作和新增数据，找出未执行过的数据
        process_excel_files(ths_page=None, file_paths=[Strategy_portfolio_today],operation_history_file=OPERATION_HISTORY_FILE)
        return result
    except Exception as e:
        logger.error(f"[策略任务] 执行异常: {e}", exc_info=True)
        return False


async def combination_wrapper():
    """组合任务执行包装"""
    try:
        logger.info("[组合] 开始执行...")
        result = await Combination_main()
        logger.info("[组合] 执行完成")
        return result
    except Exception as e:
        logger.error(f"[组合任务] 执行异常: {e}", exc_info=True)
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
    global STOP_FLAG
    signal.signal(signal.SIGINT, handle_signal)
    signal.signal(signal.SIGTERM, handle_signal)

    try:
        # 初始化调度器
        portfolio_tasks = [
            create_scheduler("策略调度", SCHEDULE_CONFIG["strategy"], strategy_wrapper),
            create_scheduler("组合调度", SCHEDULE_CONFIG["etf_combo"], combination_wrapper),
        ]

        auto_trade_tasks = [
            create_scheduler("自动化交易", SCHEDULE_CONFIG["automation"], automation_wrapper),
        ]

        while not STOP_FLAG:
            now = datetime.now().time()

            if now >= dt_time(19, 0):
                logger.info("⏰ 到达下午3点，停止所有任务")
                break

            elif dt_time(9, 25) <= now <= dt_time(19, 33):
                logger.info("⏰ 当前为策略调度时间段")
                await asyncio.gather(*(scheduler.start() for scheduler in portfolio_tasks[:1]))

            # 9:30 - 15:00 运行组合和自动化交易
            elif dt_time(9, 30) <= now <= dt_time(19, 0):
                logger.info("⏰ 当前为组合+自动化交易时间段")

                # 并行运行策略和组合任务
                strategy_task = asyncio.create_task(strategy_wrapper())
                combo_task = asyncio.create_task(combination_wrapper())

                # 等待结果
                strategy_updated = await strategy_task
                combo_updated = await combo_task

                # 如果有新增数据，启动自动化交易
                if strategy_updated or combo_updated:
                    logger.info("🔔 检测到新增数据，准备启动自动化交易")
                    task = asyncio.create_task(auto_main())
                    try:
                        await asyncio.wait_for(task, timeout=60)
                    except asyncio.TimeoutError:
                        logger.warning("⏳ 自动化交易任务超时，正在取消...")
                        task.cancel()
                        try:
                            await task
                        except asyncio.CancelledError:
                            pass

            else:
                logger.info("💤 当前不在交易时间段，休眠60秒")
                await asyncio.sleep(60)

            await asyncio.sleep(60)

        logger.info("✅ 主程序已安全退出")

    except KeyboardInterrupt:
        logger.warning("🛑 用户手动终止程序")
    except Exception as e:
        logger.critical(f"💥 主程序异常终止: {str(e)}", exc_info=True)
    finally:
        logger.info("🔚 程序结束运行")


if __name__ == '__main__':
    try:
        print('\n---------------------------------------------------------------------------')
        asyncio.run(main())

        now_time = datetime.now()
        if now_time.hour == 15 and now_time.minute >= 30:
            logger.info("🧹 当前时间是下午3点，开始清理今日持仓记录文件")
            from Investment.THS.AutoTrade.utils.excel_handler import clear_csv
            clear_csv(Strategy_portfolio_today)
            clear_csv(Combination_portfolio_today)

    except KeyboardInterrupt:
        logger.warning("🛑 用户主动终止程序")
    except Exception as e:
        logger.critical(f"❌ 致命错误: {e}", exc_info=True)
