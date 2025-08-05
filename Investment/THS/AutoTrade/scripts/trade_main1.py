# 在 trade_main.py 中添加Socket监控相关代码

import asyncio
import datetime

import websockets
import threading

import asyncio
import random
import datetime
from datetime import time as dt_time

import uiautomator2 as u2

# 自定义模块
from Investment.THS.AutoTrade.scripts.portfolio_today.Combination_portfolio_today import Combination_main
from Investment.THS.AutoTrade.scripts.portfolio_today.Robots_portfolio_today import Robot_main
from Investment.THS.AutoTrade.scripts.portfolio_today.Strategy_portfolio_today import Strategy_main
from Investment.THS.AutoTrade.pages.page_guozhai import GuozhaiPage
from Investment.THS.AutoTrade.pages.page import THSPage
from Investment.THS.AutoTrade.scripts.data_process import process_excel_files, read_operation_history
from Investment.THS.AutoTrade.scripts.trade_logic import TradeLogic
from Investment.THS.AutoTrade.utils.logger import setup_logger
from Investment.THS.AutoTrade.config.settings import (
    Strategy_portfolio_today_file,
    Combination_portfolio_today_file,
    OPERATION_HISTORY_FILE,
    MIN_DELAY,
    MAX_DELAY,
    MAX_RUN_TIME,
    Robot_portfolio_today_file, Account_holding_file,
)

# 导入你的20日监控模块
from Investment.THS.AutoTrade.scripts.monitor_20day import daily_check
from Investment.THS.AutoTrade.utils.notification import send_notification
from Investment.THS.AutoTrade.config.settings import OPERATION_HISTORY_FILE, MAX_RUN_TIME
from Investment.THS.AutoTrade.scripts.data_process import read_operation_history
from Investment.THS.AutoTrade.trade_main import initialize_device, is_device_connected, check_morning_signals, trader
from Investment.THS.AutoTrade.utils.logger import setup_logger
# 添加全局变量
socket_monitor_thread = None
socket_monitor_server = None

logger = setup_logger(__name__)

end_time_hour = 15
end_time_minute = 00
# Socket监控类
class SocketMonitor:
    def __init__(self):
        self.clients = set()
        self.is_running = False

    async def register(self, websocket):
        self.clients.add(websocket)
        try:
            await websocket.wait_closed()
        finally:
            self.clients.remove(websocket)

    async def broadcast(self, message):
        if self.clients:
            await asyncio.gather(
                *[client.send(message) for client in self.clients],
                return_exceptions=True
            )

# 创建Socket监控实例
socket_monitor = SocketMonitor()

async def websocket_handler(websocket, path):
    await socket_monitor.register(websocket)

def start_socket_monitor():
    """启动Socket监控服务器"""
    global socket_monitor_server

    async def serve():
        server = await websockets.serve(websocket_handler, "localhost", 8765)
        socket_monitor_server = server
        await server.wait_closed()

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(serve())

async def start_socket_monitor_async():
    """异步启动Socket监控"""
    server = await websockets.serve(websocket_handler, "localhost", 8765)
    logger.info("Socket监控服务器已启动: ws://localhost:8765")
    return server

# 修改 main 函数
async def main():
    """主程序：控制任务执行的时间窗口"""
    from Investment.THS.AutoTrade.utils import logger
    logger.info("⏰ 调度器已启动，等待执行时间窗口...")

    # 启动Socket监控服务器
    socket_server = await start_socket_monitor_async()

    # 初始化设备
    d = await initialize_device()
    if not d:
        logger.error("❌ 设备初始化失败")
        return

    # ths_page = THSPage(d)

    # 初始化国债逆回购状态
    guozhai_success = False

    # 记录开始时间，用于最大运行时长控制
    start_time = datetime.datetime.now()

    # 1. 提前读取历史记录
    history_df = read_operation_history(OPERATION_HISTORY_FILE)

    while True:
        now = datetime.datetime.now().time()

        # 检查是否超过最大运行时间
        if (datetime.datetime.now() - start_time) > datetime.timedelta(hours=MAX_RUN_TIME):
            logger.info(f"已达到最大运行时间 {MAX_RUN_TIME} 小时，退出程序")
            break

        # 检查是否超过每日结束时间
        if now >= dt_time(end_time_hour, end_time_minute):
            logger.info("当前时间超过 15:30，停止运行")
            break

        # 新增：检查是否在11:30到13:00之间，如果是则跳过本次循环
        if dt_time(11, 30) <= now < dt_time(13, 0):
            logger.info("当前时间在11:30到13:00之间，跳过本次循环")
            await asyncio.sleep(random.uniform(MIN_DELAY, MAX_DELAY))
            continue

        # 检测设备是否断开
        if not is_device_connected(d):
            logger.warning("设备断开连接，尝试重新初始化...")
            d = await initialize_device()
            if not d:
                logger.error("设备重连失败，等待下一轮检测")
                await asyncio.sleep(random.uniform(MIN_DELAY, MAX_DELAY))
                continue

        # 更新页面对象引用
        ths_page = THSPage(d)

        # 执行早盘信号检查
        await check_morning_signals()

        # 2. 处理组合和策略文件
        # 初始化变量
        robot_success = False
        strategy_success = False
        combination_success = False

        strategy_data = None
        combination_data = None

        # 判断是否在策略任务时间窗口（9:30-9:33）
        now = datetime.datetime.now().time()
        if dt_time(9, 31) <= now <= dt_time(9, 35):
            logger.info("---------------------策略/Robot任务开始执行---------------------")
            strategy_result = await Strategy_main()
            robot_result = await Robot_main()
            if strategy_result or robot_result:
                strategy_success, strategy_data = strategy_result
                robot_success, robot_data = robot_result
            else:
                logger.warning("⚠️ 策略/Robot任务返回空值，默认视为无更新")
            logger.info(f"策略/Robot是否有新增数据: {strategy_success}\n---------------------策略/Robot任务执行结束---------------------")
        else:
            logger.debug("尚未进入策略/Robot任务时间窗口，跳过执行")

        # 判断是否在组合任务和自动化交易时间窗口（9:25-15:00）
        if dt_time(9, 25) <= now <= dt_time(end_time_hour, end_time_minute):
            logger.info("---------------------组合任务开始执行---------------------")
            combination_result = await Combination_main()
            if combination_result:
                combination_success, combination_data = combination_result
            else:
                logger.warning("⚠️ 组合任务返回空值，默认视为无更新")
            logger.info(f"组合是否有新增数据: {combination_success}\n---------------------组合任务执行结束---------------------")

            # 如果有任何一个数据获取成功，则执行交易处理
            if strategy_success or combination_success or robot_success:
                file_paths = [Strategy_portfolio_today_file, Combination_portfolio_today_file, Robot_portfolio_today_file]
                process_excel_files(trader, file_paths, OPERATION_HISTORY_FILE, history_df=history_df)

        else:
            logger.debug("尚未进入组合任务和自动化交易时间窗口，跳过执行")

        # 国债逆回购操作（只执行一次）
        if not guozhai_success and dt_time(14,56) <= now <= dt_time(end_time_hour,end_time_minute):
            logger.info("---------------------国债逆回购任务开始执行---------------------")
            guozhai = GuozhaiPage(d)
            success, message = guozhai.guozhai_operation()
            if success:
                logger.info("国债逆回购成功")
                guozhai_success = True  # 标记国债逆回购任务已执行
            else:
                logger.info(f"国债逆回购失败: {message}")
            logger.info("---------------------国债逆回购任务执行结束---------------------")

        else:
            logger.debug("尚未进入国债逆回购时间窗口，跳过执行")

        # 随机等待，降低请求频率规律性
        delay = random.uniform(50, 70)
        logger.info(f"💤 等待 {delay:.2f} 秒后继续下一轮检测")
        await asyncio.sleep(delay)

    # 关闭Socket服务器
    socket_server.close()
    await socket_server.wait_closed()