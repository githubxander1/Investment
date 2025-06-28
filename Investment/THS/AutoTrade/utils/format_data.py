#format_data.py
import pandas as pd

# from Investment.THS.AutoTrade.utils.common_config import EXPECTED_COLUMNS
from Investment.THS.AutoTrade.utils.logger import setup_logger
logger = setup_logger('data_process.log')


# from common_config import EXPECTED_COLUMNS
def determine_market(stock_code):
    """根据股票代码判断市场"""
    if stock_code.startswith(('60', '00')):
        return '沪深A股'
    elif stock_code.startswith('688'):
        return '科创板'
    elif stock_code.startswith('30'):
        return '创业板'
    elif stock_code.startswith(('4', '8')):
        return '北交所'
    else:
        return '其他'

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



def create_unique_id(df):
    df['代码'] = df['代码'].astype(str).str.zfill(6)
    df['新比例%'] = df['新比例%'].round(2).map(lambda x: f"{x:.2f}")
    df['_id'] = df['时间'].astype(str) + '_' + df['代码'] + '_' + df['新比例%']
    return df


def get_new_records(current_df, history_df):
    """通过 _id 字段获取新增记录"""
    if current_df.empty:
        return pd.DataFrame()

    # 标准化列并创建唯一标识符
    current_df['代码'] = current_df['代码'].astype(str).str.zfill(6)
    current_df['时间'] = current_df['时间'].apply(normalize_time)

    # 保留浮点数，并统一保留两位小数用于生成 _id
    current_df['新比例%'] = current_df['新比例%'].round(2).astype(float)
    current_df['_id'] = (
        current_df['时间'].astype(str) + '_' +
        current_df['代码'] + '_' +
        current_df['新比例%'].map(lambda x: f"{x:.2f}")
    )

    # 处理历史数据为空的情况
    if history_df.empty:
        return current_df.drop(columns=['_id'], errors='ignore')

    # 同样处理历史数据
    history_df['代码'] = history_df['代码'].astype(str).str.zfill(6)
    history_df['时间'] = history_df['时间'].apply(normalize_time)
    history_df['新比例%'] = history_df['新比例%'].round(2).astype(float)
    history_df['_id'] = (
        history_df['时间'].astype(str) + '_' +
        history_df['代码'] + '_' +
        history_df['新比例%'].map(lambda x: f"{x:.2f}")
    )

    # 找出新增记录
    new_mask = ~current_df['_id'].isin(history_df['_id'])
    new_data = current_df[new_mask].copy()

    # logger.info(f'新增记录：{new_data}')
    return new_data.drop(columns=['_id'], errors='ignore') if not new_data.empty else new_data



def standardize_dataframe(df):
    """标准化数据格式"""
    if not isinstance(df, pd.DataFrame):
        raise ValueError("输入必须是 pandas DataFrame")

    # 使用 .loc 避免 SettingWithCopyWarning
    df = df.copy()  # 创建副本以避免修改原始数据

    # if '代码' in df.columns:
    #     df.loc[:, '代码'] = df['代码'].astype(str).str.zfill(6)

    if '时间' in df.columns:
        df.loc[:, '时间'] = df['时间'].astype(str).apply(normalize_time)
        df.loc[:, '时间'] = df['时间'].replace('nan', '').replace('', None)

    return df
