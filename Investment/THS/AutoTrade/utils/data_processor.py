#data_processor.py
import pandas as pd

# from Investment.THS.AutoTrade.utils.common_config import EXPECTED_COLUMNS
from Investment.THS.AutoTrade.utils.logger import setup_logger
# logger = setup_logger('')


# from common_config import EXPECTED_COLUMNS

def normalize_time(time_str):
    """统一时间格式为 YYYY-MM-DD HH:MM"""
    if not time_str or time_str == 'N/A':
        return ''

    try:
        # 处理 float 类型（如 20250509.0）
        if isinstance(time_str, float) and not pd.isna(time_str):
            time_str = str(int(time_str))
        elif isinstance(time_str, str) and '.' in time_str:
            time_str = time_str.split('.')[0]  # 去掉小数点后内容

        time_str = " ".join(str(time_str).split())  # 清除多余空格

        # 处理纯数字日期（如 20250509）
        if len(time_str) == 8 and time_str.isdigit():
            return f"{time_str[:4]}-{time_str[4:6]}-{time_str[6:8]}"

        # 如果包含秒字段，去掉秒部分
        if len(time_str.split()) > 1:
            date_part, time_part = time_str.split(" ", 1)
            time_part = ":".join(time_part.split(":")[:2])  # 只取小时和分钟
            return f"{date_part} {time_part}"
        else:
            return time_str
    except Exception as e:
        print(f"时间标准化失败: {e}")
        return ''



def create_unique_id(df, time_col='时间', code_col='代码'):
    """为DataFrame添加唯一标识列"""
    df['_id'] = df[time_col].astype(str) + '_' + df[code_col].astype(str)
    return df

def get_new_records(current_df, history_df):
    """通过 _id 字段获取新增记录"""
    if current_df.empty:
        return pd.DataFrame()

    # # 标准化列名并补全缺失列
    # expected_columns = ['名称', '操作', '标的名称', '代码', '最新价', '新比例%', '市场', '时间']
    # for col in expected_columns:
    #     if col not in current_df.columns:
    #         current_df[col] = None
    #     if col not in history_df.columns:
    #         history_df[col] = None

    # 确保字段存在
    current_df['代码'] = current_df['代码'].astype(str).str.zfill(6)
    current_df['时间'] = current_df['时间'].apply(normalize_time)

    # 创建唯一标识
    current_df['_id'] = current_df['时间'].astype(str) + '_' + current_df['代码'] + '_' + current_df['新比例%'].astype(str)

    # 处理历史数据为空的情况
    if history_df.empty:
        return current_df.drop(columns=['_id'], errors='ignore')

    # 标准化历史数据
    history_df['代码'] = history_df['代码'].astype(str).str.zfill(6)
    history_df['时间'] = history_df['时间'].apply(normalize_time)
    history_df['_id'] = history_df['时间'].astype(str) + '_' + history_df['代码'] + '_' + current_df['新比例%'].astype(str)

    # 清洗异常 _id
    current_df = current_df[current_df['_id'].str.contains(r'^\d{4}-\d{2}-\d{2} \d{2}:\d{2}_\d{6}$', regex=True)]
    history_df = history_df[history_df['_id'].str.contains(r'^\d{4}-\d{2}-\d{2} \d{2}:\d{2}_\d{6}$', regex=True)]

    # 打印调试信息
    # print("清洗后当前记录 _id:", current_df['_id'].tolist())
    # print("清洗后历史记录 _id:", history_df['_id'].tolist())

    # 筛选新记录
    new_mask = ~current_df['_id'].isin(history_df['_id'])
    new_data = current_df[new_mask].copy()
    if not new_data.empty:
        new_data = standardize_dataframe(new_data)
        from Investment.THS.AutoTrade.scripts.auto_trade_on_ths import logger
        logger.info(f'新增记录：{new_data}')
    # print(f'新增记录：{new_data}')

    return new_data.drop(columns=['_id'], errors='ignore') if not new_data.empty else new_data


def standardize_dataframe(df):
    """标准化数据格式"""
    if not isinstance(df, pd.DataFrame):
        raise ValueError("输入必须是 pandas DataFrame")

    # 使用 .loc 避免 SettingWithCopyWarning
    df = df.copy()  # 创建副本以避免修改原始数据

    # if '代码' in df.columns:
        # 先转为字符串，确保 zfill 操作不会触发类型警告
        # df.loc[:, '代码'] = df['代码'].astype(str).str.zfill(6)

    if '时间' in df.columns:
        df.loc[:, '时间'] = df['时间'].astype(str).apply(normalize_time)
        df.loc[:, '时间'] = df['时间'].replace('nan', '').replace('', None)

    return df
