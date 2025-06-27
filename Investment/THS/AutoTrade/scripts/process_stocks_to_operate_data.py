# process_stocks_to_operate_data.py
import os
import time
from datetime import datetime

import pandas
import pandas as pd

from Investment.THS.AutoTrade.config.settings import trade_operations_log_file, OPERATION_HISTORY_FILE
from Investment.THS.AutoTrade.utils.excel_handler import read_portfolio_record_history
from Investment.THS.AutoTrade.utils.logger import setup_logger
from Investment.THS.AutoTrade.utils.file_utils import get_file_hash, check_files_modified

logger = setup_logger(trade_operations_log_file)

def write_operation_history(df):
    """将操作记录写入Excel文件，按日期作为sheet名"""
    today = datetime.now().strftime('%Y%m%d')

    try:
        file_exists = os.path.exists(OPERATION_HISTORY_FILE)

        with pd.ExcelWriter(OPERATION_HISTORY_FILE, mode='a', engine='openpyxl') as writer:
            if today in writer.book.sheetnames:
                old_df = pd.read_excel(writer.book, sheet_name=today)
                combined_df = pd.concat([old_df, df], ignore_index=True)
            else:
                combined_df = df

            # 去重
            combined_df.drop_duplicates(subset=['标的名称', '操作', '新比例%'], keep='last', inplace=True)

            combined_df.to_excel(writer, sheet_name=today, index=False)
            logger.info(f"✅ 成功写入操作记录到 {today} 表")
    except Exception as e:
        logger.error(f"❌ 写入操作记录失败: {e}")


def read_operation_history(history_file):
    """读取当日操作历史"""
    today = datetime.now().strftime('%Y%m%d')
    if not os.path.exists(history_file):
        return pd.DataFrame(columns=['标的名称', '操作', '新比例%'])

    try:
        with pd.ExcelFile(history_file, engine='openpyxl') as f:
            if today in f.sheet_names:
                df = pd.read_excel(f, sheet_name=today)
                df['标的名称'] = df['标的名称'].astype(str).str.strip()
                df['操作'] = df['操作'].astype(str).str.strip()
                df['新比例%'] = df['新比例%'].astype(float).round(2)
                df['_id'] = df.apply(lambda x: f"{x['标的名称']}_{x['操作']}_{x['新比例%']}", axis=1)
                return df
    except Exception as e:
        logger.warning(f"读取操作历史失败，可能文件被占用或损坏: {e}")
    return pd.DataFrame(columns=['标的名称', '操作', '新比例%'])


def process_excel_files(ths_page, file_paths, operation_history_file, holding_stock_file):
    for file_path in file_paths:
        logger.info(f"🔄 检测到文件更新，即将处理: {file_path}")

        # 检查文件是否存在且非空
        if not os.path.exists(file_path) or os.path.getsize(file_path) == 0:
            logger.warning(f"⚠️ 文件不存在或为空: {file_path}")
            continue

        try:
            # 读取要处理的文件
            df = read_portfolio_record_history(file_path)
            history_df = read_operation_history(history_file=operation_history_file)
            if df.empty:
                logger.warning(f"文件 {file_path} 为空，跳过处理")
                continue

            for index, row in df.iterrows():
                stock_name = row['标的名称'].strip()
                operation = row['操作'].strip()
                new_ratio = float(row['新比例%'])

                logger.info(f"🛠️ 要处理: {operation} {stock_name} 比例:{new_ratio}")

                # 判断是否已执行
                exists = history_df[
                    (history_df['标的名称'] == stock_name) &
                    (history_df['操作'] == operation) &
                    (history_df['新比例%'] == round(new_ratio, 2))
                ]
                if not exists.empty:
                    logger.info(f"✅ 已处理过: {stock_name}")
                    continue

                # new_to_operate = [~(exists['标的名称'] == stock_name) & (exists['操作'] == operation) & (exists['新比例%'] == round(new_ratio, 2))]
                # return new_to_operate
                # 执行交易逻辑
                logger.info(f"🚀 开始交易: {operation} {stock_name}")
                status, info = ths_page.operate_stock(operation, stock_name, volume=None)

                # 构造记录
                operate_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                record = pd.DataFrame([{
                    '标的名称': stock_name,
                    '操作': operation,
                    '新比例%': new_ratio,
                    '状态': status,
                    '信息': info,
                    '时间': operate_time
                }])

                # 写入历史
                write_operation_history(record)
                logger.info(f"{operation} {stock_name} 流程结束，操作已记录")

        except pandas.errors.EmptyDataError:
            logger.error(f"处理文件 {file_path} 失败: 文件为空或格式错误")
        except Exception as e:
            logger.error(f"处理文件 {file_path} 失败: {e}", exc_info=True)
