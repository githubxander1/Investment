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
    start_date: 开始日期，格式'YYYYMMDD'
    end_date: 结束日期，格式'YYYYMMDD'
    
    返回:
    df: 分时数据DataFrame
    """
    try:
        # 如果没有指定日期，使用今天的日期
        if start_date is None or end_date is None:
            today = datetime.now().strftime('%Y%m%d')
            start_date = today
            end_date = today
            
        # 获取A股分时数据
        df = ak.stock_zh_a_minute(symbol=stock_code, period="1", adjust="qfq", start_date=start_date, end_date=end_date)
        
        # 重命名列以符合系统需求
        column_mapping = {
            '开盘': '开盘',
            '最高': '最高', 
            '最低': '最低',
            '收盘': '收盘',
            '成交量': '成交量',
            '成交额': '成交额',
            '时间': '时间'
        }
        
        # 只保留需要的列
        df = df.rename(columns=column_mapping)
        
        # 确保时间列是datetime类型
        if '时间' in df.columns:
            df['时间'] = pd.to_datetime(df['时间'])
        
        # 排序并重置索引
        df = df.sort_values('时间').reset_index(drop=True)
        
        return df
        
    except Exception as e:
        print(f"获取分时数据失败: {e}")
        return pd.DataFrame()


def get_prev_close(stock_code):
    """
    获取股票前一日收盘价
    
    参数:
    stock_code: 股票代码，例如'600000'
    
    返回:
    prev_close: 前一日收盘价
    """
    try:
        # 获取股票历史行情
        stock_zh_a_daily = ak.stock_zh_a_daily(symbol=stock_code, adjust="qfq")
        
        # 检查是否有数据
        if stock_zh_a_daily.empty:
            print(f"无法获取股票{stock_code}的历史数据")
            return None
        
        # 获取前一日收盘价（倒数第二行的收盘价）
        prev_close = stock_zh_a_daily.iloc[-2]['close'] if len(stock_zh_a_daily) > 1 else stock_zh_a_daily.iloc[-1]['close']
        
        return prev_close
        
    except Exception as e:
        print(f"获取前一日收盘价失败: {e}")
        return None


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
    cache_dir = os.path.join(os.path.dirname(__file__), '../../cache')
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
    cache_dir = os.path.join(os.path.dirname(__file__), '../../cache')
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