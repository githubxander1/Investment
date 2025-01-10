# 数据处理.py
import os
from datetime import datetime

import pandas as pd

from others.量化投资.THS.自动化交易_同花顺.config.settings import trade_operations_log_file
from others.量化投资.THS.自动化交易_同花顺.utils.logger import setup_logger
from others.量化投资.THS.自动化交易_同花顺.utils.notification import send_notification

logger = setup_logger(trade_operations_log_file)

# 文件操作模块
# def get_daily_log_file():
#     today = datetime.now().strftime('%Y%m%d')
#     return os.path.join(os.path.dirname(OPERATION_HISTORY_FILE), f'交易记录_{today}.xlsx')

def read_operation_history(file_path):
    today = datetime.now().strftime('%Y%m%d')
    if os.path.exists(file_path):
        try:
            with pd.ExcelFile(file_path, engine='openpyxl') as operation_history_xlsx:
                if today in operation_history_xlsx.sheet_names:
                    operation_history_df = pd.read_excel(operation_history_xlsx, sheet_name=today)
                    # 去重处理
                    operation_history_df.drop_duplicates(subset=['股票名称', '操作', '时间'], inplace=True)
                    logger.info(f"读取去重后的操作历史文件")#\n{operation_history_df}
                else:
                    operation_history_df = pd.DataFrame(columns=['股票名称', '操作', '状态', '信息', '时间'])
        except Exception as e:
            logger.error(f"读取操作历史文件失败: {e}", exc_info=True)
            operation_history_df = pd.DataFrame(columns=['股票名称', '操作', '状态', '信息', '时间'])
    else:
        operation_history_df = pd.DataFrame(columns=['股票名称', '操作', '状态', '信息', '时间'])

    return operation_history_df

def write_operation_history(file_path, new_operation_history_df):
    today = datetime.now().strftime('%Y%m%d')

    if not os.path.exists(file_path):
        # 文件不存在时创建一个新的Excel文件，并添加一个以今日日期为名称的工作表
        with pd.ExcelWriter(file_path, engine='openpyxl') as writer:
            new_operation_history_df.to_excel(writer, sheet_name=today, index=False)
            logger.info(f"操作历史文件不存在，创建新的Excel文件: {file_path}")
    else:
        # 文件存在时读取现有文件
        with pd.ExcelFile(file_path, engine='openpyxl') as operation_history_xlsx:
            if today in operation_history_xlsx.sheet_names:
                # 如果今天的工作表存在，读取现有数据并追加新数据
                existing_df = pd.read_excel(operation_history_xlsx, sheet_name=today)
                updated_df = pd.concat([existing_df, new_operation_history_df], ignore_index=True)
                logger.info(f"追加新的操作记录: \n{new_operation_history_df}")
            else:
                # 如果今天的工作表不存在，使用新数据创建新的工作表
                updated_df = new_operation_history_df
                logger.info(f"今天的工作表不存在，创建新的操作记录: \n{updated_df}")

        # 写回文件
        with pd.ExcelWriter(file_path, engine='openpyxl', mode='a', if_sheet_exists='replace') as writer:
            updated_df.to_excel(writer, sheet_name=today, index=False)

def process_excel_files(ths_page, file_paths, operation_history_file):
    for file_path in file_paths:
        logger.info(f"检测到文件更新，即将进行操作的文件路径: {file_path}")
        if not os.path.exists(file_path):
            logger.warning(f"文件不存在: {file_path}")
            continue
        try:
            df = pd.read_excel(file_path)
            for index, row in df.iterrows():
                stock_name = row['股票名称']
                operation = row['操作']
                time = row['时间']
                logger.info(f"要处理的信息: {stock_name}, 操作: {operation}")

                # 读取最新的操作历史记录
                operation_history_df = read_operation_history(operation_history_file)

                # 检查股票名称和操作是否已经存在于操作历史中
                if not operation_history_df.empty:
                    existing_operations = operation_history_df[(operation_history_df['股票名称'] == stock_name) & (operation_history_df['时间'] == time)]
                    if not existing_operations.empty:
                        logger.info(f"{stock_name} 和操作 {operation} 已经操作过，跳过")
                        continue

                volume = 100
                status, info = ths_page.sell_stock(stock_name, '200') if operation == 'SALE' else ths_page.buy_stock(stock_name, volume)
                logger.info(f"{operation} {stock_name} {'成功' if status else '失败'} {info}")
                send_notification(f"{operation} {stock_name} {info}")
                logger.info(f"发送通知成功")

                # 写入操作历史
                operate_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                new_operation_history = pd.DataFrame([{
                    '股票名称': stock_name,
                    '操作': operation,
                    '状态': status,
                    '信息': info,
                    '时间': operate_time
                }])

                # 写回操作历史文件
                write_operation_history(operation_history_file, new_operation_history)
                logger.info(f"写入操作历史文件成功")

                logger.info(f'{operation} {stock_name} 流程结束, 操作已记录')
            logger.info(f'文件处理完成 {file_path} \n')
        except Exception as e:
            logger.error(f"处理文件 {file_path} 失败: {e}", exc_info=True)
