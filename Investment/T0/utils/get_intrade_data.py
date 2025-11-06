from pprint import pprint

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime, timedelta
from typing import Optional, Tuple, Dict, List
import akshare as ak
import os
import sys

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

try:
    from Investment.T0.data_source.data2dfcf import get_eastmoney_fenshi_with_pandas
    from Investment.T0.utils.logger import setup_logger
except ImportError as e:
    print(f"导入模块失败: {e}")
    # 创建一个简单的logger替代
    import logging
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    setup_logger = lambda name: logging.getLogger(name)

# 直接导入类而不是通过模块
from intraday_data_provider import IntradayDataProvider

logger = setup_logger('get_intrade_data')

def fetch_intraday_data(stock_code: str, trade_date: str) -> Optional[pd.DataFrame]:
    """
    获取分时数据

    Args:
        stock_code: 股票代码
        trade_date: 交易日期

    Returns:
        分时数据DataFrame
    """
    provider = IntradayDataProvider()
    return provider.get_intraday_data(stock_code, trade_date)

# 测试代码
if __name__ == "__main__":
    stock_code = '600030'
    trade_date = '2025-11-06'
    
    # 测试新的数据提供类
    provider = IntradayDataProvider()
    
    # 测试 stock_zh_a_hist_min_em 接口
    print("测试 stock_zh_a_hist_min_em 接口:")
    df_em = provider.get_hist_min_em_data(stock_code, trade_date)
    if df_em is not None and not df_em.empty:
        print(f"✅ 成功获取数据，数据行数: {len(df_em)}")
        print(f"数据列: {df_em.columns.tolist()}")
        print("前5行数据:")
        print(df_em.head())
        df_em.to_csv(f'{stock_code}_hist_min_em.csv', index=False)
    else:
        print("❌ 未获取到数据")
    
    print("\n" + "="*50 + "\n")
    
    # 测试 stock_zh_a_minute 接口
    print("测试 stock_zh_a_minute 接口:")
    df_minute = provider.get_a_minute_data(stock_code)
    if df_minute is not None and not df_minute.empty:
        print(f"✅ 成功获取数据，数据行数: {len(df_minute)}")
        print(f"数据列: {df_minute.columns.tolist()}")
        print("前5行数据:")
        print(df_minute.head())
        df_minute.to_csv(f'{stock_code}_a_minute.csv', index=False)
    else:
        print("❌ 未获取到数据")
    
    print("\n" + "="*50 + "\n")
    
    # 测试统一接口
    print("测试统一接口:")
    df = provider.get_intraday_data(stock_code, trade_date)
    if df is not None and not df.empty:
        print(f"✅ 成功获取数据，数据行数: {len(df)}")
        print(f"数据列: {df.columns.tolist()}")
        print("前5行数据:")
        print(df.head())
    else:
        print("❌ 未获取到数据")