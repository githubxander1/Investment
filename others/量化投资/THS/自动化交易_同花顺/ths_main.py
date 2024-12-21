import os
import time
from pprint import pprint

import uiautomator2 as u2
import pandas as pd
from others.量化投资.THS.自动化交易_同花顺.ths_logger import logger
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
        d.app_start(package_name)
        logger.info(f"启动app: {package_name}")
    except Exception as e:
        logger.error(f"启动app失败 {package_name}: {e}", exc_info=True)

def process_excel_files(d, ths_page, file_paths):
    datas = []
    for file_path in file_paths:
        print(f"检查文件路径: {file_path}")
        if not os.path.exists(file_path):
            logger.warning(f"文件不存在: {file_path}")
            continue
        try:
            df = pd.read_excel(file_path)
            for index, row in df.iterrows():
                stock_name = row['股票名称']
                operation = row['操作']
                datas.append({'stock_name': stock_name, 'operation': operation})
                if operation == 'SALE':
                    ths_page.sell_stock(stock_name, '200')
                    logger.info(f'卖出{stock_name}流程结束', exc_info=True)
                elif operation == 'BUY':
                    ths_page.buy_stock(stock_name, 200)
                    logger.info(f'买入{stock_name}流程结束', exc_info=True)
                else:
                    logger.warning(f"未知操作类型: {operation} 对于股票: {stock_name}")
        except Exception as e:
            logger.error(f"处理文件 {file_path} 失败: {e}", exc_info=True)
        # pprint(datas)
        df = pd.DataFrame(datas)
        print(df)
        datas = []
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

    process_excel_files(d, ths_page, file_paths)

    # 打印设备信息
    device_info = d.info
    logger.info(f"设备信息: {device_info}", exc_info=True)

if __name__ == "__main__":
    main()
