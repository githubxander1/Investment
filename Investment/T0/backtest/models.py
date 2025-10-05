import pandas as pd
import numpy as np
from datetime import datetime
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass
from enum import Enum

class SignalType(Enum):
    """信号类型"""
    BUY = "BUY"
    SELL = "SELL"

@dataclass
class Signal:
    """交易信号"""
    timestamp: datetime
    signal_type: SignalType
    price: float
    indicator: str  # 指标来源

@dataclass
class Trade:
    """交易记录"""
    timestamp: datetime
    trade_type: SignalType
    price: float
    quantity: int
    commission: float
    indicator: str  # 指标来源

@dataclass
class Position:
    """持仓信息"""
    quantity: int
    avg_price: float
    entry_time: datetime

@dataclass
class BacktestResult:
    """回测结果"""
    symbol: str
    indicator: str
    initial_capital: float
    final_capital: float
    total_return: float
    total_trades: int
    win_rate: float
    max_drawdown: float
    sharpe_ratio: float
    trades: List[Trade]
    signals: List[Signal]
    
    @property
    def profit(self):
        return self.final_capital - self.initial_capital
    
    @property
    def profit_rate(self):
        return (self.final_capital / self.initial_capital - 1) * 100 if self.initial_capital > 0 else 0