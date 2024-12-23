import logging
import os
import time
import pandas as pd
from pprint import pprint

import uiautomator2 as u2
from others.量化投资.THS.自动化交易_同花顺.ths_logger import setup_logger
from others.量化投资.THS.自动化交易_同花顺.ths_page import THSPage

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
        d.app_start(package_name,wait=True)
        logger.info(f"启动app: {package_name}")
    except Exception as e:
        logger.error(f"启动app失败 {package_name}: {e}", exc_info=True)

def load_operation_history():
    if os.path.exists(OPERATION_HISTORY_FILE):
        return pd.read_csv(OPERATION_HISTORY_FILE)
    return pd.DataFrame(columns=['stock_name', 'operation'])

def save_operation_history(operation_history_df):
    operation_history_df.to_csv(OPERATION_HISTORY_FILE, index=False)

def process_excel_files(d, ths_page, file_paths, operation_history_df):
    datas = []
    for file_path in file_paths:
        print(f"要操作的文件路径: {file_path}")
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
                        if success:
                            datas.append({'stock_name': stock_name, 'operation': operation})
                            logger.info(f'卖出 {stock_name} 流程结束')
                        else:
                            logger.error(f'卖出 {stock_name} 失败')
                    elif operation == 'BUY':
                        success = ths_page.buy_stock(stock_name, 200)
                        if success:
                            datas.append({'stock_name': stock_name, 'operation': operation})
                            logger.info(f'买入 {stock_name} 流程结束')
                        else:
                            logger.error(f'买入 {stock_name} 失败')
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

def main():
    d = connect_to_device()
    if d is None:
        return

    start_app(d, 'com.hexin.plat.android')
    time.sleep(10)

    ths_page = THSPage(d)

    # 假设Excel文件在同目录下的data文件夹中
    file_paths = [
        r'D:\1document\1test\PycharmProject_gitee\others\量化投资\THS\自动化交易_同花顺\保存的数据\策略今天调仓.xlsx',
        r'D:\1document\1test\PycharmProject_gitee\others\量化投资\THS\自动化交易_同花顺\保存的数据\组合今天调仓.xlsx'
    ]

    # 加载操作历史
    operation_history_df = load_operation_history()

    process_excel_files(d, ths_page, file_paths, operation_history_df)

    # 打印设备信息
    device_info = d.info
    logger.info(f"设备信息: {device_info}", exc_info=True)

    # 在程序结束前调用
    logging.shutdown()

if __name__ == "__main__":
    logger = setup_logger(r'D:\1document\1test\PycharmProject_gitee\others\量化投资\THS\自动化交易_同花顺\保存的数据\ths_auto_trade_log.txt')

    # 记录操作历史的文件路径
    OPERATION_HISTORY_FILE = r'D:\1document\1test\PycharmProject_gitee\others\量化投资\THS\自动化交易_同花顺\保存的数据\operation_history.csv'

    main()
