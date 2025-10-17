import os
import pandas as pd
import akshare as ak
import numpy as np
from datetime import datetime, timedelta


def get_stock_intraday_data(stock_code, start_date=None, end_date=None):
    """
    获取股票分时数据
    
    参数:
    stock_code: 股票代码，例如'600000'
    start_date: 开始日期，格式'YYYYMMDD' (此参数当前版本akshare不支持)
    end_date: 结束日期，格式'YYYYMMDD' (此参数当前版本akshare不支持)
    
    返回:
    df: 分时数据DataFrame
    """
    try:
        # 确保股票代码格式正确（akshare需要sh或sz前缀）
        if stock_code.startswith('6'):
            symbol = f'sh{stock_code}'
        elif stock_code.startswith(('0', '3')):
            symbol = f'sz{stock_code}'
        else:
            symbol = stock_code
            
        # 获取A股分时数据（当前版本akshare不支持日期范围参数）
        df = ak.stock_zh_a_minute(symbol=symbol, period="1", adjust="qfq")
        
        # 检查是否获取到数据
        if df.empty:
            print(f"{stock_code} 股票数据不存在，请检查是否已退市")
            return pd.DataFrame()
        
        # 重命名列以符合系统需求
        column_mapping = {
            'day': '时间',
            'open': '开盘',
            'high': '最高', 
            'low': '最低',
            'close': '收盘',
            'volume': '成交量'
        }
        
        # 只保留需要的列并重命名
        df = df.rename(columns=column_mapping)
        required_columns = ['时间', '开盘', '最高', '最低', '收盘', '成交量']
        df = df[required_columns]
        
        # 确保时间列是datetime类型
        if '时间' in df.columns:
            df['时间'] = pd.to_datetime(df['时间'])
        
        # 排序并重置索引
        df = df.sort_values('时间').reset_index(drop=True)
        
        # 处理NaN值
        df = df.dropna()
        
        return df
        
    except Exception as e:
        print(f"获取分时数据失败: {e}")
        return pd.DataFrame()


def get_previous_close(stock_code, trade_date):
    """
    获取前一日收盘价（处理周末情况）
    
    参数:
    stock_code: 股票代码
    trade_date: 交易日期，格式'YYYYMMDD'
    
    返回:
    float: 前一日收盘价
    """
    try:
        # 确保股票代码格式正确（akshare需要sh或sz前缀）
        if stock_code.startswith('6'):
            symbol = f'sh{stock_code}'
        elif stock_code.startswith(('0', '3')):
            symbol = f'sz{stock_code}'
        else:
            symbol = stock_code
            
        # 将交易日期转换为datetime对象
        trade_date_dt = datetime.strptime(trade_date, '%Y%m%d')
        
        # 如果是周末，获取上周五的收盘价
        weekday = trade_date_dt.weekday()  # 0=Monday, 6=Sunday
        if weekday == 5:  # Saturday
            trade_date_dt = trade_date_dt - timedelta(days=1)  # Friday
        elif weekday == 6:  # Sunday
            trade_date_dt = trade_date_dt - timedelta(days=2)  # Friday
        
        # 获取历史日线数据
        df = ak.stock_zh_a_hist(symbol=symbol, period="daily", adjust="qfq")
        
        if not df.empty:
            # 转换日期列为datetime类型
            df['日期'] = pd.to_datetime(df['日期'])
            
            # 筛选出在交易日期之前的数据
            df_before = df[df['日期'] < trade_date_dt]
            
            if not df_before.empty:
                # 获取最近的收盘价
                prev_close = df_before.iloc[-1]['收盘']
                return float(prev_close)
            else:
                print(f"无法获取股票 {stock_code} 的前一日收盘价")
                return 0.0
        else:
            print(f"无法获取股票 {stock_code} 的历史数据")
            return 0.0
            
    except Exception as e:
        print(f"获取前一日收盘价失败: {e}")
        return 0.0


def validate_data(df):
    """
    验证数据有效性
    
    参数:
    df: DataFrame
    
    返回:
    bool: 数据是否有效
    """
    if df is None or df.empty:
        print("数据为空")
        return False
    
    required_columns = ['时间', '开盘', '最高', '最低', '收盘', '成交量']
    for col in required_columns:
        if col not in df.columns:
            print(f"缺少必要列: {col}")
            return False
    
    # 检查是否有NaN值
    if df.isnull().values.any():
        print("数据包含NaN值")
        # 不直接返回False，因为可以在预处理阶段处理NaN值
    
    return True


def preprocess_data(df):
    """
    数据预处理
    
    参数:
    df: 原始数据DataFrame
    
    返回:
    df: 预处理后的DataFrame
    """
    # 填充NaN值
    df = df.fillna(method='ffill').fillna(method='bfill')
    
    # 确保数值列的数据类型正确
    numeric_columns = ['开盘', '最高', '最低', '收盘', '成交量']
    for col in numeric_columns:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')
    
    # 移除仍有NaN值的行
    df = df.dropna()
    
    return df


def process_time_period(df, start_time='09:30:00', end_time='15:00:00'):
    """
    处理交易时间段数据
    
    参数:
    df: 包含股票数据的DataFrame
    start_time: 开始时间，格式'HH:MM:SS'
    end_time: 结束时间，格式'HH:MM:SS'
    
    返回:
    df: 处理后的DataFrame
    """
    try:
        # 确保时间列是datetime类型
        if not pd.api.types.is_datetime64_any_dtype(df['时间']):
            df['时间'] = pd.to_datetime(df['时间'])
        
        # 提取时间部分
        df['time_part'] = df['时间'].dt.time
        
        # 定义交易时间段
        start_dt = pd.to_datetime(start_time).time()
        end_dt = pd.to_datetime(end_time).time()
        
        # 过滤交易时间段内的数据
        df = df[(df['time_part'] >= start_dt) & (df['time_part'] <= end_dt)]
        
        # 删除临时列
        df = df.drop('time_part', axis=1)
        
        return df
        
    except Exception as e:
        print(f"处理交易时间段数据失败: {e}")
        return df


def fill_missing_data(df, freq='1T'):
    """
    填充缺失的数据点
    
    参数:
    df: 包含股票数据的DataFrame
    freq: 数据频率，默认'1T'（1分钟）
    
    返回:
    df: 填充后的DataFrame
    """
    try:
        # 确保时间列是索引
        if '时间' in df.columns and df.index.name != '时间':
            df = df.set_index('时间')
        
        # 重新采样并填充缺失值
        df = df.asfreq(freq)
        
        # 使用前向填充填充开盘价、最高价、最低价、收盘价
        price_cols = ['开盘', '最高', '最低', '收盘']
        for col in price_cols:
            if col in df.columns:
                df[col] = df[col].ffill()
        
        # 使用0填充成交量和成交额
        volume_cols = ['成交量', '成交额']
        for col in volume_cols:
            if col in df.columns:
                df[col] = df[col].fillna(0)
        
        # 重置索引
        df = df.reset_index()
        
        return df
        
    except Exception as e:
        print(f"填充缺失数据失败: {e}")
        return df


def validate_data(df):
    """
    验证数据有效性
    
    参数:
    df: 包含股票数据的DataFrame
    
    返回:
    bool: 数据是否有效
    """
    # 检查是否为空
    if df.empty:
        print("数据为空")
        return False
    
    # 检查是否包含必要的列
    required_columns = ['时间', '开盘', '最高', '最低', '收盘', '成交量']
    for col in required_columns:
        if col not in df.columns:
            print(f"缺少必要的列: {col}")
            return False
    
    # 检查收盘价是否有异常值
    if df['收盘'].isna().any():
        print("收盘价包含NaN值")
        return False
    
    # 检查最高价是否大于等于收盘价和最低价
    if not (df['最高'] >= df['收盘']).all():
        print("存在最高价小于收盘价的异常数据")
        return False
    
    if not (df['最高'] >= df['最低']).all():
        print("存在最高价小于最低价的异常数据")
        return False
    
    # 检查最低价是否小于等于收盘价
    if not (df['最低'] <= df['收盘']).all():
        print("存在最低价大于收盘价的异常数据")
        return False
    
    # 检查成交量是否为非负数
    if (df['成交量'] < 0).any():
        print("存在成交量为负数的异常数据")
        return False
    
    return True


def get_cached_data(stock_code, date):
    """
    从缓存获取数据
    
    参数:
    stock_code: 股票代码
    date: 日期，格式'YYYYMMDD'
    
    返回:
    df: 缓存的DataFrame，如果没有缓存则返回None
    """
    # 创建缓存目录
    cache_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'cache')
    os.makedirs(cache_dir, exist_ok=True)
    
    # 构建缓存文件路径
    cache_file = os.path.join(cache_dir, f'{stock_code}_{date}.csv')
    
    # 检查缓存文件是否存在
    if os.path.exists(cache_file):
        try:
            df = pd.read_csv(cache_file)
            # 转换时间列为datetime类型
            df['时间'] = pd.to_datetime(df['时间'])
            return df
        except Exception as e:
            print(f"读取缓存数据失败: {e}")
            return None
    
    return None


def save_data_to_cache(df, stock_code, date):
    """
    将数据保存到缓存
    
    参数:
    df: 要缓存的DataFrame
    stock_code: 股票代码
    date: 日期，格式'YYYYMMDD'
    
    返回:
    bool: 是否保存成功
    """
    # 创建缓存目录
    cache_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'cache')
    os.makedirs(cache_dir, exist_ok=True)
    
    # 构建缓存文件路径
    cache_file = os.path.join(cache_dir, f'{stock_code}_{date}.csv')
    
    try:
        # 保存数据到CSV文件
        df.to_csv(cache_file, index=False)
        return True
    except Exception as e:
        print(f"保存数据到缓存失败: {e}")
        return False


def fetch_intraday_data(stock_code, trade_date):
    """获取分时数据（兼容旧版接口）"""
    try:
        df = ak.stock_zh_a_hist_min_em(
            symbol=stock_code,
            period="1",
            start_date=trade_date,
            end_date=trade_date,
            adjust=''
        )
        if df.empty:
            print(f"❌ {stock_code}无分时数据")
            return None

        # 保存到缓存前确保列名正确
        if '时间' not in df.columns:
            # 查找实际的时间列
            time_col = None
            for col in df.columns:
                if '时间' in col or 'date' in col.lower() or 'time' in col.lower():
                    time_col = col
                    break
            if time_col:
                df.rename(columns={time_col: '时间'}, inplace=True)

        return df
    except Exception as e:
        print(f"获取{stock_code}分时数据失败: {e}")
        return None


def preprocess_intraday_data(df, trade_date):
    """预处理分时数据（兼容旧版接口）"""
    try:
        # 如果数据来自缓存，则时间列已经是索引，否则需要转换时间列
        if '时间' in df.columns:
            # 强制转换为 datetime（AkShare 返回的时间已包含日期）
            df['时间'] = pd.to_datetime(df['时间'], errors='coerce')

        df = df[df['时间'].notna()]

        # 只保留指定日期的数据，不延伸到今天
        target_date = pd.to_datetime(trade_date, format='%Y%m%d')
        df = df[df['时间'].dt.date == target_date.date()]

        # 过滤掉 11:30 到 13:00 之间的数据
        df = df[~((df['时间'].dt.hour == 11) & (df['时间'].dt.minute >= 30)) & ~((df['时间'].dt.hour == 12))]
        if df.empty:
            print("❌ 所有时间数据均无效")
            return None

        return df
    except Exception as e:
        print(f"预处理分时数据失败: {e}")
        return None