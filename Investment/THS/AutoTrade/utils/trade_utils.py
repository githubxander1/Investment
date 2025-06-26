# utils/trade_utils.py
import datetime

import pandas as pd


def mark_new_trades_as_scheduled(new_data, operation_history_file):
    """
    标记新交易为“已调度”，避免重复处理
    :param new_data: DataFrame 新增交易数据
    :param operation_history_file: 操作历史文件路径
    """
    from Investment.THS.AutoTrade.scripts.process_stocks_to_operate_data import read_operation_history, write_operation_history

    history_df = read_operation_history(operation_history_file)

    for index, row in new_data.iterrows():
        stock_name = row['标的名称'].strip()
        operation = row['操作'].strip()
        new_ratio = float(row['新比例%'])

        _id = f"{stock_name}_{operation}_{round(new_ratio, 2)}"
        if not history_df.empty and _id in history_df['_id'].values:
            print(f"✅ {stock_name} 已处理过，跳过")
            continue

        # 构造记录
        operate_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        record = pd.DataFrame([{
            '标的名称': stock_name,
            '操作': operation,
            '新比例%': new_ratio,
            '状态': '已调度',
            '信息': '等待执行',
            '时间': operate_time,
            '_id': _id
        }])

        write_operation_history(record, operation_history_file)
