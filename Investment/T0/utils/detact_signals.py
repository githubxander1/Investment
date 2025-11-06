import pandas as pd
import numpy as np
from datetime import datetime
import os
import sys

# 添加项目根目录到Python路径
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

# 尝试导入模块
try:
    from Investment.T0.utils.tools import notify_signal
except ImportError:
    try:
        # 尝试相对导入
        sys.path.insert(0, os.path.join(project_root, "Investment", "T0"))
        from utils.tools import notify_signal
    except ImportError:
        # 最后尝试使用绝对路径导入
        sys.path.append(os.path.dirname(os.path.abspath(__file__)))
        from tools import notify_signal


def detect_trading_signals(df: pd.DataFrame, stock_code: str = "") -> dict:
    """
    检测交易信号
    
    Args:
        df: 包含交易信号的数据框
        stock_code: 股票代码
        
    Returns:
        信号字典，包含买入和卖出信号列表
    """
    buy_signals = []
    sell_signals = []
    
    if df is not None and not df.empty:
        # 检查是否有Buy_Signal列
        if 'Buy_Signal' in df.columns:
            buy_signal_data = df[df['Buy_Signal']]
            for index, row in buy_signal_data.iterrows():
                buy_signals.append((index, row['收盘']))
                
        # 检查是否有Sell_Signal列
        if 'Sell_Signal' in df.columns:
            sell_signal_data = df[df['Sell_Signal']]
            for index, row in sell_signal_data.iterrows():
                sell_signals.append((index, row['收盘']))
    
    # 返回信号字典
    return {
        'buy_signals': buy_signals,
        'sell_signals': sell_signals
    }