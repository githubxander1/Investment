import os
import pandas as pd
from others.量化投资.THS.自动化交易_同花顺.整合.utils.notification import send_notification
from others.量化投资.THS.自动化交易_同花顺.整合.config.settings import OPERATION_HISTORY_FILE, SUCCESSFUL_OPERATIONS_FILE, \
    trade_operations
from others.量化投资.THS.自动化交易_同花顺.整合.utils.ths_logger import setup_logger

logger = setup_logger(trade_operations)

def process_excel_files(d,ths_page, file_paths, operation_history_df, successful_operations_df):
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
                logger.info(f"处理股票: {stock_name}, 操作: {operation}")
                if operation_history_df[(operation_history_df['stock_name'] == stock_name) & (operation_history_df['operation'] == operation)].empty:
                    success = ths_page.sell_stock(stock_name, '200') if operation == 'SALE' else ths_page.buy_stock(stock_name, 200)
                    status = 'success' if success else 'failure'
                    send_notification(f"{operation} {stock_name} {'成功' if success else '失败'}")
                    datas.append({'stock_name': stock_name, 'operation': operation, 'status': status})
                    if success:
                        successful_datas.append({'stock_name': stock_name, 'operation': operation, 'status': 'success'})
                        logger.info(f'{operation} {stock_name} 流程结束, 操作已记录')
                    else:
                        logger.error(f'{operation} {stock_name} 失败, 操作已记录')
                else:
                    logger.info(f"股票 {stock_name} 的操作 {operation} 已经执行过，跳过")
        except Exception as e:
            logger.error(f"处理文件 {file_path} 失败: {e}", exc_info=True)

        # 更新操作历史
        if datas:
            operation_history_df = pd.concat([operation_history_df, pd.DataFrame(datas)], ignore_index=True)
            datas = []
            save_file(operation_history_df, OPERATION_HISTORY_FILE)

        # 更新成功操作记录
        if successful_datas:
            successful_operations_df = pd.concat([successful_operations_df, pd.DataFrame(successful_datas)], ignore_index=True)
            successful_datas = []
            save_file(successful_operations_df, SUCCESSFUL_OPERATIONS_FILE)

    return operation_history_df, successful_operations_df

def save_file(df, file_path):
    df.to_csv(file_path, index=False)
    logger.info(f"已保存文件: {file_path}")
