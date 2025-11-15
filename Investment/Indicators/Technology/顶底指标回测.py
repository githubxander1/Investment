import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime, timedelta
import os

# 设置中文显示
plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号

def run_backtest_for_china_telecom():
    """运行中国电信的顶底指标回测"""
    # 计算近一年的日期范围
    end_date = datetime.now().strftime('%Y%m%d')
    start_date = (datetime.now() - timedelta(days=365)).strftime('%Y%m%d')
    
    print(f"日期范围: {start_date} 到 {end_date}")
    
    # 中国电信的股票代码
    stock_code = "sh601728"  # 使用带市场前缀的代码
    stock_name = "中国电信"
    
    print(f"=====================================")
    print(f"开始回测 {stock_name}({stock_code}) 的顶底指标策略")
    print(f"=====================================")
    
    # 使用新的顶底策略类运行回测
    from utils.backtest_engine import run_backtest
    from Technology.top_bottom_strategy import TopBottomStrategy
    
    backtester = run_backtest(
        backtester_class=TopBottomStrategy,
        stock_code=stock_code,
        start_date=start_date,
        end_date=end_date,
        initial_capital=100000
    )
    
    print(f"{stock_name} 回测完成！")
    return backtester

if __name__ == "__main__":
    run_backtest_for_china_telecom()
    print("\n所有回测完成！")
