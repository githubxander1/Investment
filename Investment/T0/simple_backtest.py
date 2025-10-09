"""
简化版回测脚本 - 专门用于测试9月份的数据
"""

import pandas as pd
import akshare as ak
import sys
import os
from datetime import datetime, timedelta

# 添加项目根目录到路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from backtest.data_loader import load_stock_data, get_prev_close
from backtest.strategies import (
    detect_resistance_support_signals,
    detect_extended_signals,
    detect_volume_price_signals_func
)
from backtest.engine import BacktestEngine
from config.settings import DEFAULT_STOCK_POOL

def simple_backtest_single_stock(symbol='000333', start_date='20250901', end_date='20250930'):
    """
    简化版回测 - 单个股票
    
    Args:
        symbol: 股票代码
        start_date: 开始日期 (YYYYMMDD)
        end_date: 结束日期 (YYYYMMDD)
    """
    print(f"开始回测股票: {symbol}")
    print(f"回测期间: {start_date} 到 {end_date}")
    print("=" * 50)
    
    # 1. 加载数据
    print("1. 加载数据...")
    data = load_stock_data(symbol, start_date, end_date)
    if data.empty:
        print("❌ 无法加载数据")
        return
    
    print(f"✅ 成功加载 {len(data)} 条数据")
    
    # 2. 获取前收盘价
    print("2. 获取前收盘价...")
    prev_close = get_prev_close(symbol, start_date)
    if prev_close is None:
        prev_close = data['开盘'].iloc[0] if not data.empty else 0
        print(f"⚠️ 无法获取前收盘价，使用开盘价替代: {prev_close:.2f}")
    else:
        print(f"✅ 前收盘价: {prev_close:.2f}")
    
    # 3. 创建回测引擎
    engine = BacktestEngine()
    
    # 4. 测试各个指标
    indicators = ['resistance_support', 'extended', 'volume_price']
    
    for indicator in indicators:
        print(f"\n3.{indicators.index(indicator)+1}. 测试 {indicator} 指标...")
        try:
            result = engine.run_backtest(symbol, indicator, data, start_date, end_date)
            print(f"  初始资金: {result.initial_capital:.2f}")
            print(f"  最终资金: {result.final_capital:.2f}")
            print(f"  收益: {result.profit:.2f} ({result.profit_rate:.2f}%)")
            print(f"  交易次数: {result.total_trades}")
            print(f"  胜率: {result.win_rate:.2f}")
        except Exception as e:
            print(f"  ❌ 测试 {indicator} 指标时出错: {e}")
            import traceback
            traceback.print_exc()
    
    # 5. 保存结果
    print("\n4. 保存回测结果...")
    engine.save_results(f"simple_backtest_{symbol}_{start_date}_{end_date}.csv")
    engine.plot_results()
    
    print("回测完成!")

if __name__ == "__main__":
    # 测试默认股票池中的第一个股票
    stock_code = DEFAULT_STOCK_POOL[0] if DEFAULT_STOCK_POOL else '000333'
    simple_backtest_single_stock(stock_code, '20250901', '20250930')