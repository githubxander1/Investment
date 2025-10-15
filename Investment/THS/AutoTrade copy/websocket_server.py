import asyncio
import websockets
import json
import datetime
import random
import logging
from datetime import time as dt_time
from threading import Thread
import functools

from Investment.THS.AutoTrade.pages.account_info import common_page
from Investment.THS.AutoTrade.pages.devices_init import initialize_device, is_device_connected
from Investment.THS.AutoTrade.pages.page_guozhai import GuozhaiPage
from Investment.THS.AutoTrade.pages.page import THSPage
from Investment.THS.AutoTrade.scripts.data_process import read_operation_history, process_data_to_operate
from Investment.THS.AutoTrade.scripts.portfolio_today.Strategy import operate_result
from Investment.THS.AutoTrade.scripts.trade_logic import TradeLogic
from Investment.THS.AutoTrade.utils.logger import setup_logger
from Investment.THS.AutoTrade.config.settings import (
    Strategy_portfolio_today_file,
    Combination_portfolio_today_file,
    OPERATION_HISTORY_FILE,
    MIN_DELAY,
    MAX_DELAY,
    MAX_RUN_TIME,
    Robot_portfolio_today_file, Account_holding_file, Lhw_portfolio_today_file,
)

# 导入策略模块
from Investment.THS.AutoTrade.scripts.portfolio_today.Combination_portfolio_today import Combination_main
from Investment.THS.AutoTrade.scripts.portfolio_today.Lhw_portfolio_today import Lhw_main
from Investment.THS.AutoTrade.scripts.portfolio_today.Robots_portfolio_today import Robot_main

# 导入20日监控模块
from Investment.THS.AutoTrade.scripts.monitor_20day import daily_check, check_morning_signals
from Investment.THS.AutoTrade.utils.notification import send_notification

# 设置日志
logger = setup_logger("websocket_server.log")
trader = TradeLogic()

# WebSocket连接存储
connected_clients = set()

# 定义账户列表
ACCOUNTS = ["长城证券", "川财证券", "中泰证券"]

# 添加全局变量来跟踪是否已执行过信号检测
morning_signal_checked = False

def is_trading_day(date: datetime.date) -> bool:
    """
    判断是否为中国股市的交易日
    :param date: 日期
    :return: 是否是交易日
    """
    # 忽略周六周日
    if date.weekday() >= 5:  # 5=Saturday, 6=Sunday
        return False

    # 可以在此添加节假日列表进行排除
    holidays = [
        (1, 1),     # 元旦
        (2, 10),    # 春节
        (4, 5),     # 清明
        (5, 1),     # 劳动节
        (6, 22),    # 端午
        (9, 30),    # 国庆
    ]

    return not ((date.month, date.day) in holidays)

async def switch_to_next_account(d, current_account_index):
    """
    切换到下一个账户
    :param d: uiautomator2设备对象
    :param current_account_index: 当前账户索引
    :return: 下一个账户索引
    """
    next_account_index = (current_account_index + 1) % len(ACCOUNTS)
    account_name = ACCOUNTS[next_account_index]

    try:
        guozhai = GuozhaiPage(d)
        if guozhai.guozhai_change_account(account_name):
            logger.info(f"✅ 成功切换到账户: {account_name}")
            send_notification(f"账户已切换至: {account_name}")
        else:
            logger.warning(f"❌ 切换账户失败: {account_name}")
    except Exception as e:
        logger.error(f"切换账户时发生异常: {e}")
        # 即使切换失败也返回下一个索引，避免程序卡死在当前账户
        logger.info("将继续尝试下一个账户")

    return next_account_index

async def check_morning_signals_async():
    """异步检查早盘信号"""
    global morning_signal_checked

    now = datetime.datetime.now()
    current_time = now.time()

    # 检查是否是交易日
    if not is_trading_day(now.date()):
        logger.info("今天是非交易日，跳过信号检查")
        return

    # 检查是否在信号检查时间窗口内（9:25-9:35）
    if dt_time(9, 25) <= current_time <= dt_time(9, 28):
        logger.info("开始执行早盘信号检查...")
        # 检查是否已经执行过今天的信号检查
        if not morning_signal_checked:
            logger.info("开始执行早盘信号检查...")

            try:
                stocks_code = read_operation_history(Account_holding_file)
                # 定义要监控的股票（从配置或其他地方获取）
                MONITORED_STOCKS = {
                    "601728": "中国电信",
                    "601398": "工商银行",
                    "600900": "长江电力"
                }

                # 定义要监控的ETF
                MONITORED_ETFS = {
                    "508011": "嘉实物美消费REIT",
                    "508005": "华夏首创奥莱REIT",
                    "511380": "可转债ETF",
                    "511580": "国债证金债ETF",
                    "518850": "黄金ETF华夏",
                    "510300": "沪深300ETF",
                }

                # 执行股票信号检查（使用5日均线）
                stock_signals_found, stock_signals = daily_check("stock", MONITORED_STOCKS, ma_window=20)

                # 执行ETF信号检查（使用20日均线）
                etf_signals_found, etf_signals = daily_check("etf", MONITORED_ETFS, ma_window=20)

                # 如果有任何信号，发送汇总通知
                if stock_signals_found or etf_signals_found:
                    all_signals = stock_signals + etf_signals
                    summary_msg = "📈📉 早盘信号提醒 📈📉\n" + "\n".join(all_signals)
                    logger.info("早盘信号检查完成，发现信号")
                    # 发送给所有连接的客户端
                    await broadcast_message({
                        "type": "morning_signals",
                        "data": all_signals,
                        "timestamp": datetime.datetime.now().isoformat()
                    })
                else:
                    logger.info("早盘信号检查完成，未发现明显信号")

                # 标记今天已执行信号检查
                morning_signal_checked = True
                logger.info("早盘信号检查完成")

            except Exception as e:
                logger.error(f"执行早盘信号检查时发生异常: {e}")
    else:
        # 如果过了信号检查时间窗口，重置标记以便第二天使用
        if current_time > dt_time(9, 35):
            morning_signal_checked = False

async def execute_trading_tasks(d):
    """执行交易任务"""
    now = datetime.datetime.now().time()
    logger.info(f"执行交易任务，当前时间: {now}")
    
    # 发送任务开始通知
    await broadcast_message({
        "type": "task_status",
        "status": "started",
        "message": "开始执行交易任务",
        "timestamp": datetime.datetime.now().isoformat()
    })

    try:
        # 1). 执行早盘信号检查
        await check_morning_signals_async()

        # 2). 处理组合和策略文件
        # 初始化变量
        robot_success = False
        strategy_success = False
        combination_success = False
        lhw_success = False

        robot_data_df = None
        strategy_data_df = None
        combination_data_df = None
        lhw_data_df = None

        #  判断是否在策略任务时间窗口（9:30-9:33）
        robot_has_executed = False
        if dt_time(9, 30) <= now <= dt_time(9, 35):
            if not robot_has_executed:  # 仅当未执行过时才触发
                logger.warning("---------------------策略/Robot任务开始执行---------------------")
                robot_result = await Robot_main()
                if robot_result:
                    robot_success, robot_data_df = robot_result
                else:
                    logger.warning("⚠️ 策略/Robot任务返回空值，默认视为无更新")
                    robot_success = False  # 避免未定义变量

                logger.warning(f"策略/Robot是否有新增数据: {robot_success}\n"
                            f"---------------------策略/Robot任务执行结束---------------------")
                
                # 发送策略执行结果
                await broadcast_message({
                    "type": "strategy_result",
                    "strategy": "robot",
                    "success": robot_success,
                    "timestamp": datetime.datetime.now().isoformat()
                })
                
                robot_has_executed = True  # 执行后标记为已执行
            else:
                logger.debug("本时间段内任务已执行，跳过重复执行")
        else:
            # 离开时间窗口后重置标志位，确保次日可重新执行
            if robot_has_executed:
                robot_has_executed = False
                logger.debug("离开任务时间窗口，重置执行标志")
            else:
                logger.debug("尚未进入策略/Robot任务时间窗口，跳过执行")

        # 策略持仓差异任务（9:32-9:35）
        strategy_diff_executed = False
        if dt_time(9, 30) <= now <= dt_time(9, 35) and not strategy_diff_executed:
            logger.warning("---------------------策略持仓差异分析开始---------------------")
            try:
                operate_result()
                await broadcast_message({
                    "type": "strategy_analysis",
                    "status": "completed",
                    "message": "策略持仓差异分析完成",
                    "timestamp": datetime.datetime.now().isoformat()
                })

            except Exception as e:
                logger.error(f"❌ 持仓差异分析过程中发生异常: {e}")
                await broadcast_message({
                    "type": "strategy_analysis",
                    "status": "error",
                    "message": f"策略持仓差异分析异常: {str(e)}",
                    "timestamp": datetime.datetime.now().isoformat()
                })

            logger.warning("---------------------策略持仓差异分析结束---------------------")
            strategy_diff_executed = True
        else:
            # 离开时间窗口后重置标志位，确保次日可重新执行
            if strategy_diff_executed:
                strategy_diff_executed = False
                logger.debug("离开任务时间窗口，重置执行标志")
            else:
                logger.debug("尚未进入策略/Robot任务时间窗口，跳过执行")

        # 判断是否在组合任务和自动化交易时间窗口（9:25-15:00）
        if dt_time(9, 25) <= now <= dt_time(15, 00):
            logger.warning("---------------------组合任务开始执行---------------------")
            combination_result = await Combination_main()
            lhw_result = await Lhw_main()
            if combination_result:
                combination_success, combination_data_df = combination_result
                lhw_success, lhw_data_df = lhw_result
            else:
                logger.warning("⚠️ 组合任务返回空值，默认视为无更新")
            logger.warning(f"组合是否有新增数据: {combination_success}"
                           f"---------------------组合任务执行结束---------------------")
            
            # 发送组合执行结果
            await broadcast_message({
                "type": "portfolio_result",
                "combination_success": combination_success,
                "lhw_success": lhw_success,
                "timestamp": datetime.datetime.now().isoformat()
            })
        else:
            logger.debug("尚未进入组合任务和自动化交易时间窗口，跳过执行")

        logger.warning("---------------开始自动化操作---------------")
        # 如果有任何一个数据获取成功且有新数据，则执行交易处理
        if (strategy_success and strategy_data_df is not None) or \
           (combination_success and combination_data_df is not None) or \
           (robot_success and robot_data_df is not None) or \
           (lhw_success and lhw_data_df is not None):
            file_paths = [Combination_portfolio_today_file, Robot_portfolio_today_file, Lhw_portfolio_today_file]
            process_data_to_operate(file_paths)
            await broadcast_message({
                "type": "trade_processing",
                "status": "completed",
                "message": "交易处理完成",
                "timestamp": datetime.datetime.now().isoformat()
            })
        elif strategy_success or combination_success or robot_success or lhw_success:
            logger.info("有任务执行成功，但无新增交易数据，跳过交易处理")
            await broadcast_message({
                "type": "trade_processing",
                "status": "no_new_data",
                "message": "有任务执行成功，但无新增交易数据，跳过交易处理",
                "timestamp": datetime.datetime.now().isoformat()
            })
        else:
            logger.debug("无任务更新，跳过交易处理")
            await broadcast_message({
                "type": "trade_processing",
                "status": "no_updates",
                "message": "无任务更新，跳过交易处理",
                "timestamp": datetime.datetime.now().isoformat()
            })
        logger.warning("---------------自动化操作结束---------------")

        # 发送任务完成通知
        await broadcast_message({
            "type": "task_status",
            "status": "completed",
            "message": "交易任务执行完成",
            "timestamp": datetime.datetime.now().isoformat()
        })

    except Exception as e:
        logger.error(f"执行交易任务时发生异常: {e}")
        await broadcast_message({
            "type": "task_status",
            "status": "error",
            "message": f"执行交易任务时发生异常: {str(e)}",
            "timestamp": datetime.datetime.now().isoformat()
        })

async def broadcast_message(message):
    """广播消息给所有连接的客户端"""
    if connected_clients:
        # 确保消息是JSON可序列化的
        if not isinstance(message, (dict, list)):
            message = {"message": str(message)}
            
        message_json = json.dumps(message, ensure_ascii=False)
        # 创建一个任务列表来发送消息
        tasks = []
        for client in connected_clients.copy():  # 使用副本以防在迭代时发生变化
            try:
                tasks.append(client.send(message_json))
            except websockets.exceptions.ConnectionClosed:
                # 如果连接已关闭，从集合中移除
                connected_clients.remove(client)
        
        # 并发发送所有消息
        if tasks:
            await asyncio.gather(*tasks, return_exceptions=True)

async def handle_client_commands(websocket, path):
    """处理客户端命令"""
    # 将新客户端添加到连接集合
    connected_clients.add(websocket)
    logger.info(f"新客户端连接: {websocket.remote_address}")
    
    try:
        # 发送欢迎消息
        await websocket.send(json.dumps({
            "type": "welcome",
            "message": "已连接到AutoTrade WebSocket服务器",
            "timestamp": datetime.datetime.now().isoformat()
        }))
        
        # 监听客户端消息
        async for message in websocket:
            try:
                data = json.loads(message)
                command = data.get("command")
                
                if command == "execute_tasks":
                    # 执行交易任务
                    logger.info("收到执行任务命令")
                    await websocket.send(json.dumps({
                        "type": "command_response",
                        "command": "execute_tasks",
                        "status": "started",
                        "message": "开始执行交易任务",
                        "timestamp": datetime.datetime.now().isoformat()
                    }))
                    
                    # 初始化设备
                    d = await initialize_device()
                    if not d:
                        error_msg = "设备初始化失败"
                        logger.error(error_msg)
                        await websocket.send(json.dumps({
                            "type": "command_response",
                            "command": "execute_tasks",
                            "status": "error",
                            "message": error_msg,
                            "timestamp": datetime.datetime.now().isoformat()
                        }))
                        continue
                    
                    # 执行交易任务
                    await execute_trading_tasks(d)
                    
                    await websocket.send(json.dumps({
                        "type": "command_response",
                        "command": "execute_tasks",
                        "status": "completed",
                        "message": "交易任务执行完成",
                        "timestamp": datetime.datetime.now().isoformat()
                    }))
                    
                elif command == "get_status":
                    # 获取系统状态
                    now = datetime.datetime.now()
                    status = {
                        "type": "system_status",
                        "time": now.isoformat(),
                        "is_trading_day": is_trading_day(now.date()),
                        "connected_clients": len(connected_clients),
                        "morning_signal_checked": morning_signal_checked
                    }
                    await websocket.send(json.dumps(status, ensure_ascii=False))
                    
                else:
                    # 未知命令
                    await websocket.send(json.dumps({
                        "type": "error",
                        "message": f"未知命令: {command}",
                        "timestamp": datetime.datetime.now().isoformat()
                    }))
                    
            except json.JSONDecodeError:
                await websocket.send(json.dumps({
                    "type": "error",
                    "message": "无效的JSON格式",
                    "timestamp": datetime.datetime.now().isoformat()
                }))
            except Exception as e:
                logger.error(f"处理客户端消息时发生错误: {e}")
                await websocket.send(json.dumps({
                    "type": "error",
                    "message": f"处理消息时发生错误: {str(e)}",
                    "timestamp": datetime.datetime.now().isoformat()
                }))
                
    except websockets.exceptions.ConnectionClosed:
        logger.info(f"客户端断开连接: {websocket.remote_address}")
    except Exception as e:
        logger.error(f"处理客户端连接时发生错误: {e}")
    finally:
        # 确保在连接关闭时从集合中移除客户端
        connected_clients.discard(websocket)

async def periodic_task_scheduler():
    """定期任务调度器"""
    logger.info("启动定期任务调度器")
    
    # 初始化设备
    d = await initialize_device()
    if not d:
        logger.error("设备初始化失败")
        return

    while True:
        try:
            now = datetime.datetime.now().time()
            
            # 在特定时间自动执行任务
            if dt_time(9, 25) <= now <= dt_time(9, 35) or \
               dt_time(11, 30) <= now <= dt_time(11, 35) or \
               dt_time(14, 50) <= now <= dt_time(15, 10):
                
                logger.info("定时任务触发")
                await broadcast_message({
                    "type": "scheduled_task",
                    "message": "定时任务触发",
                    "time": datetime.datetime.now().isoformat()
                })
                
                # 执行交易任务
                await execute_trading_tasks(d)
                
                # 等待一段时间避免重复触发
                await asyncio.sleep(600)  # 等待10分钟
                
            # 每分钟检查一次
            await asyncio.sleep(60)
            
        except Exception as e:
            logger.error(f"定期任务调度器发生错误: {e}")
            await asyncio.sleep(60)

async def start_websocket_server():
    """启动WebSocket服务器"""
    # 启动定期任务调度器
    scheduler_task = asyncio.create_task(periodic_task_scheduler())
    
    # 启动WebSocket服务器
    server = await websockets.serve(handle_client_commands, "localhost", 8765)
    logger.info("WebSocket服务器已启动，监听端口 8765")
    
    await broadcast_message({
        "type": "server_status",
        "status": "started",
        "message": "WebSocket服务器已启动",
        "timestamp": datetime.datetime.now().isoformat()
    })
    
    # 等待服务器完成
    await server.wait_closed()
    # 取消调度器任务
    scheduler_task.cancel()

if __name__ == "__main__":
    asyncio.run(start_websocket_server())