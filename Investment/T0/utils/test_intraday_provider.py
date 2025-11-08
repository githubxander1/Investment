#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
测试 IntradayDataProvider 类的功能
"""

import sys
import os

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

# 修复导入路径问题 - 使用相对导入
from .intraday_data_provider import IntradayDataProvider

import pandas as pd


def test_all_data_sources():
    """测试所有数据源"""
    print("=" * 60)
    print("测试 IntradayDataProvider 类")
    print("=" * 60)
    
    # 创建数据提供类实例
    provider = IntradayDataProvider()
    
    # 测试股票代码和日期
    stock_code = "600030"
    trade_date = "2025-11-07"
    
    print(f"测试股票: {stock_code}")
    print(f"交易日期: {trade_date}")
    print()
    
    # 1. 测试 stock_zh_a_hist_min_em 接口
    print("1. 测试 stock_zh_a_hist_min_em 接口:")
    try:
        df_hist_min_em = provider.get_hist_min_em_data(stock_code, trade_date)
        if df_hist_min_em is not None and not df_hist_min_em.empty:
            print(f"   ✅ 成功获取数据，共 {len(df_hist_min_em)} 行")
            print(f"   数据列: {list(df_hist_min_em.columns)}")
            print("   前5行数据:")
            print(df_hist_min_em.head())
        else:
            print("   ❌ 未获取到数据")
    except Exception as e:
        print(f"   ❌ 获取数据时出错: {e}")
    print()
    
    # 2. 测试 stock_zh_a_minute 接口
    print("2. 测试 stock_zh_a_minute 接口:")
    try:
        df_a_minute = provider.get_a_minute_data(stock_code)
        if df_a_minute is not None and not df_a_minute.empty:
            print(f"   ✅ 成功获取数据，共 {len(df_a_minute)} 行")
            print(f"   数据列: {list(df_a_minute.columns)}")
            print("   前5行数据:")
            print(df_a_minute.head())
        else:
            print("   ❌ 未获取到数据")
    except Exception as e:
        print(f"   ❌ 获取数据时出错: {e}")
    print()
    
    # 3. 测试东方财富接口
    print("3. 测试东方财富接口:")
    try:
        df_eastmoney = provider.get_eastmoney_data(stock_code)
        if df_eastmoney is not None and not df_eastmoney.empty:
            print(f"   ✅ 成功获取数据，共 {len(df_eastmoney)} 行")
            print(f"   数据列: {list(df_eastmoney.columns)}")
            print("   前5行数据:")
            print(df_eastmoney.head())
        else:
            print("   ❌ 未获取到数据")
    except Exception as e:
        print(f"   ❌ 获取数据时出错: {e}")
    print()
    
    # 4. 测试统一接口
    print("4. 测试统一接口:")
    try:
        df_unified = provider.get_intraday_data(stock_code, trade_date)
        if df_unified is not None and not df_unified.empty:
            print(f"   ✅ 成功获取数据，共 {len(df_unified)} 行")
            print(f"   数据列: {list(df_unified.columns)}")
            print("   前5行数据:")
            print(df_unified.head())
        else:
            print("   ❌ 未获取到数据")
    except Exception as e:
        print(f"   ❌ 获取数据时出错: {e}")
    print()
    
    print("=" * 60)
    print("测试完成")
    print("=" * 60)


if __name__ == "__main__":
    test_all_data_sources()