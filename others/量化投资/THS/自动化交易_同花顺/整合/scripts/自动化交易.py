# scripts/自动化交易.py
import logging
import os
import threading
import time
import pandas as pd
import uiautomator2 as u2
from others.量化投资.THS.自动化交易_同花顺.整合.config.settings import THS_AUTO_TRADE_LOG_FILE_MAIN, OPERATION_HISTORY_FILE, DATA_DIR, \
    WATCHED_FOLDER, SUCCESSFUL_OPERATIONS_FILE
from others.量化投资.THS.自动化交易_同花顺.整合.pages.ths_page import THSPage
from others.量化投资.THS.自动化交易_同花顺.整合.utils.file_monitor import FileMonitor
from others.量化投资.THS.自动化交易_同花顺.整合.utils.notification import send_notification
from others.量化投资.THS.自动化交易_同花顺.整合.utils.scheduler import Scheduler
from others.量化投资.THS.自动化交易_同花顺.整合.utils.ths_logger import setup_logger

logger = setup_logger(THS_AUTO_TRADE_LOG_FILE_MAIN)

def connect_to_device():
    try:
        d = u2.connect()
        logger.info(f"连接设备: {d.serial}")
        return d
    except Exception as e:
        logger.error(f"连接设备失败: {e}", exc_info=True)
        return None

def start_app(d, package_name):
    try:
        d.app_start(package_name, wait=True)
        logger.info(f"启动app: {package_name}")
    except Exception as e:
        logger.error(f"启动app失败 {package_name}: {e}", exc_info=True)

def load_operation_history():
    if not os.path.exists(OPERATION_HISTORY_FILE):
        logger.info(f"文件 {OPERATION_HISTORY_FILE} 不存在，创建一个新的空 DataFrame")
        return pd.DataFrame(columns=['stock_name', 'operation', 'status'])

    try:
        df = pd.read_csv(OPERATION_HISTORY_FILE)
        if df.empty:
            logger.info(f"文件 {OPERATION_HISTORY_FILE} 为空，返回一个新的空 DataFrame")
            return pd.DataFrame(columns=['stock_name', 'operation', 'status'])
        return df
    except pd.errors.EmptyDataError:
        logger.info(f"文件 {OPERATION_HISTORY_FILE} 为空，返回一个新的空 DataFrame")
        return pd.DataFrame(columns=['stock_name', 'operation', 'status'])
    except Exception as e:
        logger.error(f"读取文件 {OPERATION_HISTORY_FILE} 时出错: {e}")
        raise

def load_successful_operations():
    if not os.path.exists(SUCCESSFUL_OPERATIONS_FILE):
        logger.info(f"文件 {SUCCESSFUL_OPERATIONS_FILE} 不存在，创建一个新的空 DataFrame")
        return pd.DataFrame(columns=['stock_name', 'operation', 'status'])

    try:
        df = pd.read_csv(SUCCESSFUL_OPERATIONS_FILE)
        if df.empty:
            logger.info(f"文件 {SUCCESSFUL_OPERATIONS_FILE} 为空，返回一个新的空 DataFrame")
            return pd.DataFrame(columns=['stock_name', 'operation', 'status'])
        return df
    except pd.errors.EmptyDataError:
        logger.info(f"文件 {SUCCESSFUL_OPERATIONS_FILE} 为空，返回一个新的空 DataFrame")
        return pd.DataFrame(columns=['stock_name', 'operation', 'status'])
    except Exception as e:
        logger.error(f"读取文件 {SUCCESSFUL_OPERATIONS_FILE} 时出错: {e}")
        raise

def save_operation_history(operation_history_df):
    operation_history_df.to_csv(OPERATION_HISTORY_FILE, index=False)

def save_successful_operations(successful_operations_df):
    successful_operations_df.to_csv(SUCCESSFUL_OPERATIONS_FILE, index=False)

def process_excel_files(d, ths_page, file_paths, operation_history_df, successful_operations_df):
    datas = []
    successful_datas = []
    for file_path in file_paths:
        logger.info(f"要操作的文件路径: {file_path}")
        if not os.path.exists(file_path):
            logger.warning(f"文件不存在: {file_path}")
            continue
        try:
            df = pd.read_excel(file_path)
            for index, row in df.iterrows():
                stock_name = row['股票名称']
                operation = row['操作']
                if operation_history_df[(operation_history_df['stock_name'] == stock_name) & (operation_history_df['operation'] == operation)].empty:
                    if operation == 'SALE':
                        success = ths_page.sell_stock(stock_name, '200')
                        send_notification(f"卖出 {stock_name} {'成功' if success else '失败'}")
                        datas.append({'stock_name': stock_name, 'operation': operation, 'status': 'success' if success else 'failure'})
                        if success:
                            successful_datas.append({'stock_name': stock_name, 'operation': operation, 'status': 'success'})
                            logger.info(f'卖出 {stock_name} 流程结束, 操作已记录')
                        else:
                            logger.error(f'卖出 {stock_name} 失败, 操作已记录')
                    elif operation == 'BUY':
                        success = ths_page.buy_stock(stock_name, 200)
                        send_notification(f"买入 {stock_name} {'成功' if success else '失败'}")
                        datas.append({'stock_name': stock_name, 'operation': operation, 'status': 'success' if success else 'failure'})
                        if success:
                            successful_datas.append({'stock_name': stock_name, 'operation': operation, 'status': 'success'})
                            logger.info(f'买入 {stock_name} 流程结束, 操作已记录')
                        else:
                            logger.error(f'买入 {stock_name} 失败, 操作已记录')
                    else:
                        logger.warning(f"未知操作类型: {operation} 对于股票: {stock_name}")
                else:
                    logger.info(f"股票 {stock_name} 的操作 {operation} 已经执行过，跳过")
        except Exception as e:
            logger.error(f"处理文件 {file_path} 失败: {e}", exc_info=True)
        # 更新操作历史
        if datas:
            operation_history_df = pd.concat([operation_history_df, pd.DataFrame(datas)], ignore_index=True)
            datas = []
            save_operation_history(operation_history_df)
        # 更新成功操作记录
        if successful_datas:
            successful_operations_df = pd.concat([successful_operations_df, pd.DataFrame(successful_datas)], ignore_index=True)
            successful_datas = []
            save_successful_operations(successful_operations_df)
    return operation_history_df, successful_operations_df

def main():
    d = connect_to_device()
    if d is None:
        return

    start_app(d, 'com.hexin.plat.android')
    # 打印设备信息
    device_info = d.info
    logger.info(f"设备信息: {device_info}")

    time.sleep(10)

    ths_page = THSPage(d)

    # 假设Excel文件在同目录下的data文件夹中
    file_paths = [
        os.path.join(DATA_DIR, '策略今天调仓.xlsx'),
        os.path.join(DATA_DIR, '组合今天调仓.xlsx')
    ]

    # 加载操作历史
    operation_history_df = load_operation_history()
    logger.info(f'加载操作历史: {operation_history_df}')

    # 加载成功操作记录
    successful_operations_df = load_successful_operations()
    logger.info(f'加载成功操作记录: {successful_operations_df}')

    # 文件监控回调函数
    def file_monitor_callback():
        nonlocal operation_history_df, successful_operations_df
        logger.info(f"文件监控触发，开始处理文件: {file_paths}")
        operation_history_df, successful_operations_df = process_excel_files(d, ths_page, file_paths, operation_history_df, successful_operations_df)
        logger.info(f'文件监控回调函数执行完毕，更新后的操作历史: {operation_history_df}')
        logger.info(f'文件监控回调函数执行完毕，更新后的成功操作记录: {successful_operations_df}')

    file_monitor = FileMonitor(WATCHED_FOLDER, file_monitor_callback)
    logger.info(f"文件监控已启动，监控目录: {WATCHED_FOLDER}")
    file_monitor_thread = threading.Thread(target=file_monitor.start)
    file_monitor_thread.start()
    logger.info(f"文件监控线程已启动")

    # 定时任务回调函数
    def scheduler_callback():
        nonlocal operation_history_df, successful_operations_df
        logger.info(f"定时任务触发，开始处理文件: {file_paths}")
        operation_history_df, successful_operations_df = process_excel_files(d, ths_page, file_paths, operation_history_df, successful_operations_df)
        logger.info(f'定时任务回调函数执行完毕，更新后的操作历史: {operation_history_df}')
        logger.info(f'定时任务回调函数执行完毕，更新后的成功操作记录: {successful_operations_df}')

    # scheduler = Scheduler(180, scheduler_callback)
    # scheduler_thread = threading.Thread(target=scheduler.start)
    # scheduler_thread.start()
    # logger.info(f"定时任务线程已启动，间隔: {180} 秒")

    logger.info('程序运行结束')
    # 在程序结束前调用
    logging.shutdown()

if __name__ == "__main__":
    main()
