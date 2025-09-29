import numpy as np
import pandas as pd


def calculate_tdx_indicators(df, prev_close, threshold=0.01):
    """
    通达信公式还原：
    H1:=MAX(昨收, 当日最高价);
    L1:=MIN(昨收, 当日最低价);
    P1:=H1-L1;
    阻力:L1+P1*7/8;
    支撑:L1+P1*0.5/8;
    CROSS(支撑,现价) → 支撑上穿现价（画黄色柱）
    LONGCROSS(支撑,现价,2) → 买信号（红三角）
    LONGCROSS(现价,阻力,2) → 卖信号（绿三角）
    
    参数:
    df: 包含股票数据的DataFrame，必须包含'最高'和'最低'列
    prev_close: 前一日收盘价
    threshold: 信号阈值，默认0.01
    
    返回:
    df: 添加了指标列的DataFrame
    """
    # 获取当日最高价和最低价（不是累积最大值/最小值）
    daily_high = df['最高'].max()
    daily_low = df['最低'].min()

    # 计算 H1、L1（昨收 vs 日内高低）
    df['H1'] = np.maximum(prev_close, daily_high)
    df['L1'] = np.minimum(prev_close, daily_low)

    # 支撑、阻力计算（严格按公式 0.5/8 和 7/8）
    df['P1'] = df['H1'] - df['L1']
    df['支撑'] = df['L1'] + df['P1'] * 0.5 / 8
    df['阻力'] = df['L1'] + df['P1'] * 7 / 8

    # 信号计算（严格对齐通达信逻辑）
    # 1. CROSS(支撑, 现价)：支撑上穿现价（前一周期支撑 < 现价，当前支撑 > 现价）= 现价下穿支撑（信号）
    df['cross_support'] = ((df['支撑'].shift(1) < df['收盘'].shift(1)) & (df['支撑'] > df['收盘'])) & \
                          (abs(df['支撑'] - df['收盘']) > threshold)

    # 2. LONGCROSS(支撑, 现价, 2)：连续2周期支撑 < 现价，当前支撑 > 现价（买信号）
    df['longcross_support'] = ((df['支撑'].shift(2) < df['收盘'].shift(2)) & \
                               (df['支撑'].shift(1) < df['收盘'].shift(1)) & \
                               (df['支撑'] > df['收盘'])) & \
                              (abs(df['支撑'] - df['收盘']) > threshold)

    # 3. LONGCROSS(现价, 阻力, 2)：连续2周期现价 < 阻力，当前现价 > 阻力（卖信号）
    df['longcross_resistance'] = ((df['收盘'].shift(2) < df['阻力'].shift(2)) & \
                                  (df['收盘'].shift(1) < df['阻力'].shift(1)) & \
                                  (df['收盘'] > df['阻力'])) & \
                                 (abs(df['收盘'] - df['阻力']) > threshold)

    return df


def calculate_rsi(df, period=14):
    """
    计算RSI指标
    
    参数:
    df: 包含股票数据的DataFrame，必须包含'收盘'列
    period: RSI计算周期，默认14
    
    返回:
    df: 添加了RSI列的DataFrame
    """
    # 计算价格变化
    delta = df['收盘'].diff()
    
    # 分离涨跌
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
    
    # 计算RSI
    rs = gain / loss
    df['RSI'] = 100 - (100 / (1 + rs))
    
    # 添加超买超卖线
    df['RSI_超买'] = 70
    df['RSI_超卖'] = 30
    
    # 生成RSI交易信号
    df['RSI_买入信号'] = (df['RSI'].shift(1) < 30) & (df['RSI'] >= 30)
    df['RSI_卖出信号'] = (df['RSI'].shift(1) > 70) & (df['RSI'] <= 70)
    
    return df


def calculate_macd(df, fast_period=12, slow_period=26, signal_period=9):
    """
    计算MACD指标
    
    参数:
    df: 包含股票数据的DataFrame，必须包含'收盘'列
    fast_period: 快速EMA周期，默认12
    slow_period: 慢速EMA周期，默认26
    signal_period: 信号线EMA周期，默认9
    
    返回:
    df: 添加了MACD列的DataFrame
    """
    # 计算EMA
    df['EMA_fast'] = df['收盘'].ewm(span=fast_period, adjust=False).mean()
    df['EMA_slow'] = df['收盘'].ewm(span=slow_period, adjust=False).mean()
    
    # 计算MACD线和信号线
    df['MACD'] = df['EMA_fast'] - df['EMA_slow']
    df['MACD_Signal'] = df['MACD'].ewm(span=signal_period, adjust=False).mean()
    
    # 计算MACD柱状图
    df['MACD_Hist'] = df['MACD'] - df['MACD_Signal']
    
    # 生成MACD交易信号
    df['MACD_买入信号'] = (df['MACD'].shift(1) < df['MACD_Signal'].shift(1)) & (df['MACD'] > df['MACD_Signal'])
    df['MACD_卖出信号'] = (df['MACD'].shift(1) > df['MACD_Signal'].shift(1)) & (df['MACD'] < df['MACD_Signal'])
    
    return df


def calculate_bollinger_bands(df, period=20, num_std=2):
    """
    计算布林带指标
    
    参数:
    df: 包含股票数据的DataFrame，必须包含'收盘'列
    period: 计算周期，默认20
    num_std: 标准差倍数，默认2
    
    返回:
    df: 添加了布林带列的DataFrame
    """
    # 计算中轨（20日均线）
    df['布林中轨'] = df['收盘'].rolling(window=period).mean()
    
    # 计算标准差
    df['标准差'] = df['收盘'].rolling(window=period).std()
    
    # 计算上轨和下轨
    df['布林上轨'] = df['布林中轨'] + (df['标准差'] * num_std)
    df['布林下轨'] = df['布林中轨'] - (df['标准差'] * num_std)
    
    # 生成布林带交易信号
    df['布林买入信号'] = (df['收盘'] < df['布林下轨']) & (df['收盘'].shift(1) >= df['布林下轨'].shift(1))
    df['布林卖出信号'] = (df['收盘'] > df['布林上轨']) & (df['收盘'].shift(1) <= df['布林上轨'].shift(1))
    
    return df