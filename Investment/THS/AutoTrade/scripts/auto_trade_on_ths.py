import uiautomator2 as u2

from Investment.THS.AutoTrade.config.settings import (
    Strategy_portfolio_today,
    Combination_portfolio_today,
    OPERATION_HISTORY_FILE
)
from Investment.THS.AutoTrade.pages.page_logic import THSPage
from Investment.THS.AutoTrade.scripts.process_stocks_to_operate_data import process_excel_files
from Investment.THS.AutoTrade.utils.logger import setup_logger

# 初始化日志
logger = setup_logger("自动化交易日志")

# 文件路径列表
file_paths = [
    Strategy_portfolio_today,
    Combination_portfolio_today,
]
#
async def connect_to_device():
    """连接设备"""
    try:
        d = u2.connect()
        logger.info(f"连接设备: {d.serial}")
        return d
    except Exception as e:
        logger.error(f"连接设备失败: {e}", exc_info=True)
        return None


async def start_app(d,package_name="com.hexin.plat.android"):
    """启动同花顺App"""
    try:
        # d = await connect_to_device()
        d.app_start(package_name, wait=True)
        logger.info(f"启动App成功: {package_name}")
        return True
    except Exception as e:
        logger.error(f"启动app失败 {package_name}: {e}", exc_info=True)
        return False


async def initialize_device():
    """初始化设备"""
    d = await connect_to_device()
    if not d:
        logger.error("设备连接失败")
        return None

    if not await start_app(d):
        logger.error("App启动失败")
        return None

    return d


async def auto_main():
    """
    检测策略/组合文件是否更新 → 若有变化 → 启动自动化操作
    """
    logger.info("自动化交易程序开始运行")

    # 获取设备实例
    d = await initialize_device()
    if not d:
        raise Exception("设备初始化失败，无法继续执行")

    ths_page = THSPage(d)

    # 执行交易逻辑
    process_excel_files(
        ths_page=ths_page,
        file_paths=file_paths,
        operation_history_file=OPERATION_HISTORY_FILE,
        holding_stock_file=""
    )
    logger.info("文件处理完成")

# if __name__ == '__main__':
#     try:
#         # 初始化文件路径和最后修改时间
#         file_paths = [
#             Strategy_portfolio_today,
#             Combination_portfolio_today
#         ]
#         operation_history_file = OPERATION_HISTORY_FILE
#         last_modification_times = get_file_modification_times(operation_history_file)
#
#         # 主循环，保持程序运行
#         stop_time = datetime.time(18, 00)  # 设置停止时间为18:00
#         while True:
#             now = datetime.datetime.now().time()
#
#             # 检查是否达到停止时间
#             if now.hour >= stop_time.hour and now.minute >= stop_time.minute:
#                 logger.info("到达停止时间，自动化交易程序结束运行")
#                 break
#
#             # 检查标志文件是否存在
#             if not os.path.exists(OPRATION_RECORD_DONE_FILE):
#                 logger.warning("标志文件不存在，跳过本次执行")
#                 time.sleep(30)
#                 continue
#
#             # 执行主逻辑
#             asyncio.run(auto_main())
#             time.sleep(30)  # 每分钟检查一次
#
#     except KeyboardInterrupt:
#         logger.info("程序被手动终止")
#     finally:
#         logger.info("程序结束运行")
