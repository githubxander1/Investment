#format_data.py
import pandas as pd
from dateutil.utils import today

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

from datetime import datetime

def normalize_time(time_str):
    """统一时间格式为 YYYY-MM-DD HH:MM"""
    if not time_str or time_str == 'N/A':
        return ''

    try:
        # 新增：处理字符串类型的时间戳
        if isinstance(time_str, str) and time_str.isdigit() and len(time_str) == 13:
            timestamp = int(time_str) / 1000  # 毫秒转秒
            dt = datetime.fromtimestamp(timestamp)
            return dt.strftime('%Y-%m-%d %H:%M')

        # 新增：处理 ISO 格式时间（如 2025-07-09 10:03）
        if isinstance(time_str, str) and '-' in time_str and ':' in time_str:
            parts = time_str.split()
            if len(parts) >= 2:
                date_part = parts[0]
                time_part = parts[1].split('.')[0]  # 去除毫秒
                time_part = ":".join(time_part.split(":")[:2])  # 只取小时和分钟
                return f"{date_part} {time_part}"

        # 新增：处理时间戳（如 1751419860000）
        if isinstance(time_str, (int, float)) and str(time_str).isdigit():
            timestamp = int(time_str) / 1000  # 毫秒转秒
            dt = datetime.fromtimestamp(timestamp)
            return dt.strftime("%Y-%m-%d %H:%M")

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

    #         date_part, time_part = time_str.split(" ", 1)
    #         time_part = ":".join(time_part.split(":")[:2])  # 只取小时和分钟
    #         return f"{date_part} {time_part}"
    #     else:
    #         return time_str
    # except Exception as e:
    #     print(f"时间标准化失败: {e}")
    #     return ''




# def create_unique_id(df):
#     df['代码'] = df['代码'].astype(str).str.zfill(6)
#     df['新比例%'] = df['新比例%'].round(2).map(lambda x: f"{x:.2f}")
#     df['_id'] = df['时间'].astype(str) + '_' + df['代码'] + '_' + df['新比例%']
#     return df

# def validate_dataframe(df, required_columns=None):
#     """验证并清理DataFrame"""
#     if required_columns is None:
#         required_columns = ['名称', '操作', '标的名称', '代码', '时间']
#
#         # 确保字段存在并填充默认值
#     for col in required_columns:
#         if col not in df.columns:
#             df[col] = 0.0 if col in ['新比例%', '最新价'] else ''
#
#     df = df.fillna({
#     col: '' if col in ['名称', '操作', '标的名称', '代码', '市场', '时间'] else 0.0
#     for col in required_columns
# })
#
#
#     # 确保所有必需列存在
#     for col in required_columns:
#         if col not in df.columns:
#             df[col] = ''
#
#     # 标准化代码列
#     if '代码' in df.columns:
#         df['代码'] = df['代码'].astype(str).str.zfill(6)
#
#     # 标准化时间列
#     if '时间' in df.columns:
#         df['时间'] = df['时间'].astype(str).apply(normalize_time)
#
#     # 标准化数值列
#     numeric_cols = ['新比例%', '最新价']
#     for col in numeric_cols:
#         if col in df.columns:
#             df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0.0).round(2)
#
#     # 标准化字符串列
#     str_cols = ['名称', '操作', '标的名称', '市场']
#     for col in str_cols:
#         if col in df.columns:
#             df[col] = df[col].astype(str).str.strip()
#
#     return df[required_columns]

def get_new_records(current_df, history_df):
    """通过 _id 字段获取新增记录"""
    if current_df.empty:
        return pd.DataFrame()

    # 处理历史数据为空的情况
    if history_df.empty:
        return current_df.drop(columns=['_id'], errors='ignore')

    # 生成唯一ID
    # 统一新比例%为 float 类型并保留两位小数
    current_df['新比例%'] = current_df['新比例%'].round(2).astype(float)
    current_df['_id'] = (
        current_df['标的名称'].astype(str) + '_' + # 不用代码是因为有带***的
        current_df['最新价'].map(lambda x: f"{x:.2f}") + '_' +
        current_df['新比例%'].map(lambda x: f"{x:.2f}")+ '_' +
        current_df['时间'].apply(normalize_time)
    )


    # 统一历史数据类型
    # history_df['代码'] = history_df['代码'].astype(str).str.zfill(6)
    history_df['新比例%'] = history_df['新比例%'].round(2).astype(float)
    history_df['_id'] = (
        history_df['标的名称'].astype(str) + '_' +
        history_df['最新价'].map(lambda x: f"{x:.2f}") + '_' +
        history_df['新比例%'].map(lambda x: f"{x:.2f}") + '_' +
        history_df['时间'].apply(normalize_time)
    )

    # 找出新增记录
    new_mask_df = ~current_df['_id'].isin(history_df['_id'])

    # 合并并找到新增记录
    # merged_df = pd.merge(current_df, history_df, how='left', indicator=True)
    # new_records = merged_df[merged_df['_merge'] == 'left_only'].drop(columns=['_merge'])

    # 添加调试信息
    # logger.debug(f"新记录总数: {len(current_df)} {current_df}")
    # logger.debug(f"历史记录总数: {len(history_df)} {history_df}")
    # logger.debug(f"匹配到新增记录: {len(new_mask_df)} {new_mask_df}")

    new_data_df = current_df[new_mask_df].drop(columns=['_id'], errors='ignore')
    return new_data_df

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
