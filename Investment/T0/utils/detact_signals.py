
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime, timedelta
from typing import Optional, Tuple, Dict, List
import akshare as ak
import os
import sys

from Investment.T0.utils.tools import notify_signal
from Investment.THS.ths_trade.utils.logger import setup_logger

logger = setup_logger(__name__)

def detect_trading_signals(df: pd.DataFrame) -> Dict[str, List[Tuple[datetime, float]]]:
    """
    检测交易信号

    Args:
        df: 包含指标的DataFrame

    Returns:
        信号字典
    """
    signals = {
        'buy_signals': [],
        'sell_signals': []
    }

    # 检测买入信号
    buy_signals = df[df['Buy_Signal']]
    for idx, row in buy_signals.iterrows():
        if isinstance(idx, str):
            signal_time = pd.to_datetime(idx)
        else:
            signal_time = idx
        signals['buy_signals'].append((signal_time, row['收盘']))
        # 发送买入信号通知
        notify_signal('buy', row['收盘'], signal_time.strftime('%Y-%m-%d %H:%M:%S'), '')

    # 检测卖出信号
    sell_signals = df[df['Sell_Signal']]
    for idx, row in sell_signals.iterrows():
        if isinstance(idx, str):
            signal_time = pd.to_datetime(idx)
        else:
            signal_time = idx
        signals['sell_signals'].append((signal_time, row['收盘']))
        # 发送卖出信号通知
        notify_signal('sell', row['收盘'], signal_time.strftime('%Y-%m-%d %H:%M:%S'), '')

    return signals