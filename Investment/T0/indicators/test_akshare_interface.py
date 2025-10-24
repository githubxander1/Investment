#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
最小化测试脚本 - 用于验证akshare接口是否能正常获取股票分时数据
"""

import sys
import os
import akshare as ak
from datetime import datetime

print("=== akshare接口测试脚本 ===")
print(f"Python版本: {sys.version}")
print(f"akshare版本: {ak.__version__}")
print(f"当前时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print()

# 测试用的股票和日期
# 先从用户提到的股票代码开始
STOCKS_TO_TEST = [
    "600030",  # 中信证券
    "000333",  # 美的集团
    "002415"   # 海康威视
]

# 测试几个不同的日期范围，包括最近的、用户提到的日期
TEST_DATES = [
    "2025-10-13",  # 用户在代码中使用的日期
    "2024-10-13",  # 去年的今天
    "2023-10-13",  # 用户提到的日期
    "2023-09-11"   # 用户提到的日期
]

# 创建输出目录
OUTPUT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "output", "akshare_test"))
os.makedirs(OUTPUT_DIR, exist_ok=True)
print(f"输出目录: {OUTPUT_DIR}")
print()

# 开始测试
print("开始测试akshare.stock_zh_a_hist_min_em接口...")
print("-" * 70)

# 测试每个股票和日期的组合
success_count = 0
failure_count = 0

test_results = {}

for stock_code in STOCKS_TO_TEST:
    stock_results = []
    print(f"\n测试股票: {stock_code}")
    print("-" * 50)
    
    for test_date in TEST_DATES:
        # 构建时间范围
        start_time = f'{test_date} 09:30:00'
        end_time = f'{test_date} 15:00:00'
        
        print(f"测试日期: {test_date}")
        print(f"  时间范围: {start_time} 至 {end_time}")
        
        try:
            # 直接调用akshare接口
            print("  调用接口...", end=" ")
            
            # 打印调用参数以便调试
            print(f"ak.stock_zh_a_hist_min_em(symbol='{stock_code}', period='1', start_date='{start_time}', end_date='{end_time}', adjust='')")
            
            # 实际调用接口
            df = ak.stock_zh_a_hist_min_em(
                symbol=stock_code,
                period="1",  # 1分钟数据
                start_date=start_time,
                end_date=end_time,
                adjust=""    # 不复权
            )
            
            # 检查结果
            if df is None:
                print("❌ 返回None")
                failure_count += 1
                stock_results.append({
                    'date': test_date,
                    'success': False,
                    'reason': '返回None'
                })
            elif df.empty:
                print("❌ 返回空数据框")
                failure_count += 1
                stock_results.append({
                    'date': test_date,
                    'success': False,
                    'reason': '返回空数据框'
                })
            else:
                success_count += 1
                print(f"✅ 成功获取数据! 数据形状: {df.shape}")
                
                # 打印一些数据细节
                print(f"  数据列: {df.columns.tolist()}")
                if len(df) > 0:
                    print(f"  数据范围: {df.iloc[0]['datetime']} 至 {df.iloc[-1]['datetime']}")
                    print(f"  价格范围: {df['close'].min():.2f} 至 {df['close'].max():.2f}")
                
                # 保存数据到CSV
                csv_filename = f"{stock_code}_{test_date}.csv"
                csv_path = os.path.join(OUTPUT_DIR, csv_filename)
                df.to_csv(csv_path)
                print(f"  数据已保存到: {csv_path}")
                
                stock_results.append({
                    'date': test_date,
                    'success': True,
                    'shape': df.shape
                })
                
        except Exception as e:
            failure_count += 1
            print(f"❌ 发生异常: {type(e).__name__}: {str(e)}")
            stock_results.append({
                'date': test_date,
                'success': False,
                'reason': f"异常: {type(e).__name__}: {str(e)}"
            })
    
    test_results[stock_code] = stock_results

# 打印汇总信息
print("\n" + "=" * 70)
print("测试汇总")
print("=" * 70)
print(f"总测试次数: {success_count + failure_count}")
print(f"成功次数: {success_count}")
print(f"失败次数: {failure_count}")
print(f"成功率: {success_count/(success_count + failure_count)*100:.1f}%" if success_count + failure_count > 0 else "无测试数据")
print()

# 生成详细的结果报告
print("详细结果:")
for stock_code, results in test_results.items():
    print(f"\n股票 {stock_code}:")
    for r in results:
        status = "✅ 成功" if r['success'] else "❌ 失败"
        if r['success']:
            print(f"  - {r['date']}: {status} (数据形状: {r['shape']})")
        else:
            print(f"  - {r['date']}: {status} ({r['reason']})")

# 测试其他可能的数据接口
print("\n" + "=" * 70)
print("测试其他可能的数据接口...")
print("=" * 70)

# 尝试获取日线数据作为参考
try:
    print("\n测试日线数据接口 ak.stock_zh_a_hist():")
    print("-" * 50)
    
    # 测试最近30天的日线数据
    df_daily = ak.stock_zh_a_hist(
        symbol="600030",  # 中信证券
        period="daily",
        start_date="2025-09-01",
        end_date="2025-10-13",
        adjust=""
    )
    
    if df_daily is not None and not df_daily.empty:
        print(f"✅ 成功获取日线数据! 数据形状: {df_daily.shape}")
        print(f"  数据日期范围: {df_daily.iloc[0]['date']} 至 {df_daily.iloc[-1]['date']}")
        
        # 保存日线数据
        csv_path = os.path.join(OUTPUT_DIR, "600030_daily_sample.csv")
        df_daily.to_csv(csv_path)
        print(f"  日线数据已保存到: {csv_path}")
    else:
        print("❌ 未能获取日线数据")
        
except Exception as e:
    print(f"❌ 获取日线数据时发生异常: {type(e).__name__}: {str(e)}")

# 检查是否有其他分时数据接口
try:
    print("\n检查akshare的其他分时数据接口:")
    print("-" * 50)
    
    # 尝试不同的period参数
    print("测试不同的period参数:")
    for period in ["5", "15", "30", "60"]:
        print(f"  period={period}:")
        try:
            df = ak.stock_zh_a_hist_min_em(
                symbol="600030",
                period=period,
                start_date="2025-10-13 09:30:00",
                end_date="2025-10-13 15:00:00",
                adjust=""
            )
            
            if df is not None and not df.empty:
                print(f"    ✅ 成功获取数据! 数据形状: {df.shape}")
            else:
                print(f"    ❌ 返回None或空数据框")
                
        except Exception as e:
            print(f"    ❌ 异常: {type(e).__name__}: {str(e)}")
            
except Exception as e:
    print(f"❌ 测试其他接口时发生异常: {type(e).__name__}: {str(e)}")

print("\n" + "=" * 70)
print("测试完成")
print(f"详细结果保存在: {OUTPUT_DIR}")
print("=" * 70)