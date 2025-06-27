# import asyncio
#
# import uiautomator2 as u2
#
# from Investment.THS.AutoTrade.config.settings import (
#     Strategy_portfolio_today,
#     Combination_portfolio_today,
#     OPERATION_HISTORY_FILE
# )
# from Investment.THS.AutoTrade.pages.page_logic import THSPage
# from Investment.THS.AutoTrade.scripts.process_stocks_to_operate_data import process_excel_files
# from Investment.THS.AutoTrade.utils.file_monitor import get_file_hash, check_files_modified_by_hash
# from Investment.THS.AutoTrade.utils.logger import setup_logger
# import logging
# print(logging.getLogger().handlers)  # 查看当前 logger 是否绑定了 handlers
#
# # 初始化日志
# logger = setup_logger("自动化交易日志.log")
#
# # 文件路径列表
# file_paths = [
#     Strategy_portfolio_today,
#     Combination_portfolio_today,
# ]
# #
# async def connect_to_device():
#     """连接设备"""
#     try:
#         d = u2.connect()
#         logger.info(f"连接设备: {d.serial}")
#         return d
#     except Exception as e:
#         logger.error(f"连接设备失败: {e}", exc_info=True)
#         return None
#
#
# async def start_app(d,package_name="com.hexin.plat.android"):
#     """启动同花顺App"""
#     try:
#         # d = await connect_to_device()
#         d.app_start(package_name, wait=True)
#         logger.info(f"启动App成功: {package_name}")
#         return True
#     except Exception as e:
#         logger.error(f"启动app失败 {package_name}: {e}", exc_info=True)
#         return False
#
#
# async def initialize_device():
#     """初始化设备"""
#     d = await connect_to_device()
#     if not d:
#         logger.error("设备连接失败")
#         return None
#
#     if not await start_app(d):
#         logger.error("App启动失败")
#         return None
#
#     return d
#
# # from Investment.THS.AutoTrade.utils.event_bus import event_bus
# #
# # async def on_new_trades(data):
# #     logger.info("🔔 收到新交易事件，准备执行自动化交易")
# #     await auto_main()
# #
# # # 在模块加载时注册监听
# # event_bus.subscribe('new_trades_available', on_new_trades)
#
# # async def auto_main():
# #     logger.info("🚀 自动化交易程序开始运行")
# #
# #     file_paths = [Strategy_portfolio_today, Combination_portfolio_today]
# #     logger.info(f"📁 监控的文件路径: {file_paths}")
# #
# #     d = await initialize_device()
# #     if d is None:
# #         logger.error("❌ 设备初始化失败")
# #         return
# #
# #     ths_page = THSPage(d)
# #
# #     # 获取初始哈希值
# #     # last_hashes = {fp: get_file_hash(fp) for fp in file_paths}
# #
# #     while True:
# #         modified, new_hashes = check_files_modified_by_hash(file_paths, last_hashes)
# #         if modified:
# #             logger.info("🔔 检测到文件有更新，开始执行交易任务")
# #             process_excel_files(ths_page, file_paths)
# #             last_hashes = new_hashes  # 更新哈希
# #         else:
# #             logger.info("📄 文件未发生改变，跳过处理")
# #
# #         await asyncio.sleep(60)  # 每分钟检查一次
