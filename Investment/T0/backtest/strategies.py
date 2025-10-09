import pandas as pd
import numpy as np
from datetime import datetime
from typing import List, Dict, Tuple
from .models import Signal, SignalType
from indicators.resistance_support_indicators import calculate_tdx_indicators as calc_resistance_support
from indicators.extended_indicators import calculate_tdx_indicators as calc_extended
from indicators.volume_price_indicators import (
    calculate_volume_price_indicators,
    calculate_support_resistance,
    detect_signals as detect_volume_price_signals
)

def detect_resistance_support_signals(df: pd.DataFrame, prev_close: float) -> List[Signal]:
    """
    检测阻力支撑指标信号
    
    Args:
        df: 分时数据
        prev_close: 前收盘价
        
    Returns:
        List[Signal]: 信号列表
    """
    signals = []
    
    # 计算指标
    df_with_indicators = calc_resistance_support(df.copy(), prev_close)
    
    # 检测买入信号
    buy_signals = df_with_indicators[df_with_indicators['longcross_support'] == True]
    for timestamp, row in buy_signals.iterrows():
        signals.append(Signal(
            timestamp=timestamp,
            signal_type=SignalType.BUY,
            price=row['收盘'],
            indicator='resistance_support'
        ))
    
    # 检测卖出信号
    sell_signals = df_with_indicators[df_with_indicators['longcross_resistance'] == True]
    for timestamp, row in sell_signals.iterrows():
        signals.append(Signal(
            timestamp=timestamp,
            signal_type=SignalType.SELL,
            price=row['收盘'],
            indicator='resistance_support'
        ))
    
    return signals

def detect_extended_signals(df: pd.DataFrame, prev_close: float, daily_data: pd.DataFrame) -> List[Signal]:
    """
    检测扩展指标信号
    
    Args:
        df: 分时数据
        prev_close: 前收盘价
        daily_data: 日线数据
        
    Returns:
        List[Signal]: 信号列表
    """
    signals = []
    
    # 计算指标
    df_with_indicators = calc_extended(df.copy(), prev_close, daily_data)
    
    # 检测买入信号
    buy_signals = df_with_indicators[df_with_indicators['longcross_support'] == True]
    for timestamp, row in buy_signals.iterrows():
        signals.append(Signal(
            timestamp=timestamp,
            signal_type=SignalType.BUY,
            price=row['收盘'],
            indicator='extended'
        ))
    
    # 检测卖出信号
    sell_signals = df_with_indicators[df_with_indicators['longcross_resistance'] == True]
    for timestamp, row in sell_signals.iterrows():
        signals.append(Signal(
            timestamp=timestamp,
            signal_type=SignalType.SELL,
            price=row['收盘'],
            indicator='extended'
        ))
    
    return signals

def detect_volume_price_signals_func(df: pd.DataFrame, prev_close: float) -> List[Signal]:
    """
    检测量价指标信号
    
    Args:
        df: 分时数据
        prev_close: 前收盘价
        
    Returns:
        List[Signal]: 信号列表
    """
    signals = []
    
    # 计算指标
    df_with_indicators, _, _, _ = calculate_volume_price_indicators(df.copy(), prev_close)
    df_with_indicators = calculate_support_resistance(df_with_indicators, prev_close)
    df_with_indicators = detect_volume_price_signals(df_with_indicators)
    
    # 确保必要的列存在
    required_columns = ['买入信号', '卖出信号', '主力', '大户', '散户']
    for col in required_columns:
        if col not in df_with_indicators.columns:
            df_with_indicators[col] = False
    
    # 检测买入信号
    buy_signals = df_with_indicators[df_with_indicators['买入信号'] == True]
    for timestamp, row in buy_signals.iterrows():
        signals.append(Signal(
            timestamp=timestamp,
            signal_type=SignalType.BUY,
            price=row['收盘'],
            indicator='volume_price'
        ))
    
    # 检测卖出信号
    sell_signals = df_with_indicators[df_with_indicators['卖出信号'] == True]
    for timestamp, row in sell_signals.iterrows():
        signals.append(Signal(
            timestamp=timestamp,
            signal_type=SignalType.SELL,
            price=row['收盘'],
            indicator='volume_price'
        ))
    
    return signals