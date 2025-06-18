# 数据处理.py
import os
from datetime import datetime
import pandas as pd

from Investment.THS.AutoTrade.config.settings import trade_operations_log_file
from Investment.THS.AutoTrade.utils.logger import setup_logger
# from Investment.THS.AutoTrade.utils.notification import send_notification
# from Investment.THS.AutoTrade.pages.ths_page import THSPage

logger = setup_logger(trade_operations_log_file)

def ensure_valid_excel_file(file_path):
    if not os.path.exists(file_path):
        return

    try:
        with pd.ExcelFile(file_path, engine='openpyxl') as f:
            if not f.sheet_names:
                logger.warning(f"{file_path} 是空文件，正在重建")
                os.remove(file_path)
                pd.DataFrame().to_excel(file_path, index=False)
    except Exception as e:
        logger.warning(f"{file_path} 文件损坏，正在重建: {e}")
        os.remove(file_path)
        pd.DataFrame().to_excel(file_path, index=False)

def read_operation_history(file_path):
    today = datetime.now().strftime('%Y%m%d')
    if os.path.exists(file_path):
        try:
            with pd.ExcelFile(file_path, engine='openpyxl') as f:
                if today in f.sheet_names:
                    df = pd.read_excel(f, sheet_name=today)
                    df.drop_duplicates(subset=['标的名称', '操作', '时间'], inplace=True)
                    return df
        except Exception as e:
            logger.error(f"读取操作记录失败: {e}")
    return pd.DataFrame(columns=['标的名称', '操作', '状态', '信息', '时间'])


def write_operation_history(file_path, new_df):
    today = datetime.now().strftime('%Y-%m-%d')
    mode = 'a' if os.path.exists(file_path) else 'w'
    excel_writer_kwargs = {
        'engine': 'openpyxl'
    }

    # 如果是追加模式且文件存在，检查是否有可见工作表
    if mode == 'a':
        try:
            with pd.ExcelFile(file_path, engine='openpyxl') as f:
                pass  # 确保可以打开文件
        except ValueError as e:
            if "Excel file format cannot be determined" in str(e):
                logger.warning(f"{file_path} 格式无法识别，尝试创建新文件")
                mode = 'w'  # 强制改为写入模式
                os.remove(file_path)  # 删除无效文件
                excel_writer_kwargs['mode'] = 'w'

    if mode == 'a':
        excel_writer_kwargs.update({
            'mode': 'a',
            'if_sheet_exists': 'replace'
        })
    else:
        excel_writer_kwargs['mode'] = 'w'

    try:
        with pd.ExcelWriter(file_path, **excel_writer_kwargs) as writer:
            if mode == 'a' and today in pd.ExcelFile(file_path).sheet_names:
                old_df = pd.read_excel(file_path, sheet_name=today)
                updated_df = pd.concat([old_df, new_df], ignore_index=True).drop_duplicates(
                    subset=['标的名称', '操作', '时间'])
            else:
                updated_df = new_df

            updated_df.to_excel(writer, sheet_name=today, index=False)
            logger.info("写入操作历史完成")

    except IndexError as ie:
        if "At least one sheet must be visible" in str(ie):
            logger.warning(f"{file_path} 中没有可见的工作表，尝试重新创建文件...")
            if os.path.exists(file_path):
                os.remove(file_path)
            with pd.ExcelWriter(file_path, engine='openpyxl') as writer:
                new_df.to_excel(writer, sheet_name=today, index=False)
            logger.info("成功重建操作记录文件并写入数据")
        else:
            logger.error(f"写入 Excel 失败: {str(ie)}", exc_info=True)

    except Exception as e:
        logger.error(f"写入操作记录失败: {e}", exc_info=True)


def process_excel_files(ths_page, file_paths, operation_history_file, holding_stock_file):
    for file_path in file_paths:
        logger.info(f"检测到文件更新，即将进行操作的文件路径: {file_path}")
        if not os.path.exists(file_path):
            logger.warning(f"文件不存在: {file_path}")
            continue

        try:
            # 读取要处理的文件
            df = pd.read_csv(file_path)
            for index, row in df.iterrows():
                stock_name = row['标的名称']
                operation = row['操作']
                time = row['时间']
                price = row['最新价']
                new_ratio = float(row['新比例%'])
                # logger.info(f"要处理的信息:  {operation} {stock_name} {new_ratio}")
                logger.info(f"要处理的信息:  {operation} {stock_name} 价格:{price} 比例:{new_ratio}")

                # 检查是否已执行过该操作
                history_df = read_operation_history(operation_history_file)
                if not history_df.empty:
                    exists = history_df[
                        (history_df['标的名称'] == stock_name) &
                        (history_df['操作'] == operation) &
                        (history_df['新比例%'] == new_ratio)
                    ]
                    if not exists.empty:
                        logger.info(f"{stock_name} 已操作过，跳过")
                        continue

                # 执行买卖操作
                logger.info(f"开始操作: {operation} {stock_name}")
                if operation == '买入':
                    status, info = ths_page.buy_stock(stock_name)
                elif operation == '卖出':
                    status, info = ths_page.sell_stock(stock_name, new_ratio=new_ratio)
                else:
                    logger.warning(f"不支持的操作: {operation}")
                    continue

                # 写入操作记录
                operate_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                new_record = pd.DataFrame([{
                    '标的名称': stock_name,
                    '操作': operation,
                    '新比例%': new_ratio,
                    '状态': status,
                    '信息': info,
                    '时间': operate_time
                }])
                ensure_valid_excel_file(file_path)
                write_operation_history(operation_history_file, new_record)
                logger.info(f"{operation} {stock_name} 流程结束，操作已记录")

        except Exception as e:
            logger.error(f"处理文件 {file_path} 失败: {e}", exc_info=True)
