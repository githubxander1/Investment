"""
测试单个指标在单个交易日上的表现
"""

import pandas as pd
import akshare as ak
import sys
import os
from datetime import datetime

# 添加项目根目录到路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from indicators.resistance_support_indicators import calculate_tdx_indicators
from backtest.data_loader import get_prev_close

def test_single_indicator(symbol='000333', trade_date='20250925'):
    """
    测试单个指标在单个交易日上的表现
    
    Args:
        symbol: 股票代码
        trade_date: 交易日期 (YYYYMMDD)
    """
    print(f"测试股票: {symbol}")
    print(f"测试日期: {trade_date}")
    print("=" * 50)
    
    # 1. 获取分时数据
    print("1. 获取分时数据...")
    try:
        df = ak.stock_zh_a_hist_min_em(
            symbol=symbol,
            period="1",
            start_date=trade_date,
            end_date=trade_date,
            adjust=''
        )
        
        if df.empty:
            print("❌ 无分时数据")
            return None
            
        print(f"✅ 成功获取 {len(df)} 条分时数据")
        
        # 重命名列
        df = df.rename(columns={
            '时间': '时间',
            '开盘': '开盘',
            '收盘': '收盘',
            '最高': '最高',
            '最低': '最低',
            '成交量': '成交量',
            '成交额': '成交额'
        })
        
        # 转换时间列为datetime类型
        df['时间'] = pd.to_datetime(df['时间'], errors='coerce')
        df = df[df['时间'].notna()]
        
        # 只保留指定日期的数据
        target_date = pd.to_datetime(trade_date, format='%Y%m%d')
        df = df[df['时间'].dt.date == target_date.date()]
        
        # 过滤掉午休时间
        df = df[~((df['时间'].dt.hour == 11) & (df['时间'].dt.minute >= 30)) & ~((df['时间'].dt.hour == 12))]
        
        if df.empty:
            print("❌ 所有时间数据均无效")
            return None
            
        # 分离上午和下午的数据
        morning_data = df[df['时间'].dt.hour < 12]
        afternoon_data = df[df['时间'].dt.hour >= 13]
        
        # 强制校准时间索引
        morning_index = pd.date_range(
            start=f"{trade_date} 09:30:00",
            end=f"{trade_date} 11:30:00",
            freq='1min'
        )
        afternoon_index = pd.date_range(
            start=f"{trade_date} 13:00:00",
            end=f"{trade_date} 15:00:00",
            freq='1min'
        )
        
        # 合并索引
        full_index = morning_index.union(afternoon_index)
        df = df.set_index('时间').reindex(full_index)
        df.index.name = '时间'
        
    except Exception as e:
        print(f"❌ 获取分时数据时出错: {e}")
        return None
    
    # 2. 获取前收盘价
    print("2. 获取前收盘价...")
    prev_close = get_prev_close(symbol, trade_date)
    if prev_close is None:
        prev_close = df['开盘'].dropna().iloc[0] if not df['开盘'].dropna().empty else 0
        print(f"⚠️ 无法获取前收盘价，使用开盘价替代: {prev_close:.2f}")
    else:
        print(f"✅ 前收盘价: {prev_close:.2f}")
    
    # 3. 计算指标
    print("3. 计算阻力支撑指标...")
    try:
        df_with_indicators = calculate_tdx_indicators(df.copy(), prev_close)
        if df_with_indicators is None:
            print("❌ 指标计算失败")
            return None
        print("✅ 指标计算完成")
    except Exception as e:
        print(f"❌ 指标计算时出错: {e}")
        import traceback
        traceback.print_exc()
        return None
    
    # 4. 分析信号
    print("4. 分析交易信号...")
    buy_signals = df_with_indicators[df_with_indicators['longcross_support'] == True]
    sell_signals = df_with_indicators[df_with_indicators['longcross_resistance'] == True]
    
    print(f"买入信号数量: {len(buy_signals)}")
    print(f"卖出信号数量: {len(sell_signals)}")
    
    if not buy_signals.empty:
        print("\n买入信号详情:")
        for timestamp, row in buy_signals.iterrows():
            print(f"  时间: {timestamp.strftime('%H:%M:%S')}, 价格: {row['收盘']:.2f}")
    
    if not sell_signals.empty:
        print("\n卖出信号详情:")
        for timestamp, row in sell_signals.iterrows():
            print(f"  时间: {timestamp.strftime('%H:%M:%S')}, 价格: {row['收盘']:.2f}")
    
    # 5. 保存结果到CSV
    print("5. 保存结果到CSV...")
    try:
        output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'test_output')
        os.makedirs(output_dir, exist_ok=True)
        
        filename = f"{symbol}_{trade_date}_resistance_support_analysis.csv"
        filepath = os.path.join(output_dir, filename)
        
        df_with_indicators.to_csv(filepath, encoding='utf-8-sig')
        print(f"✅ 结果已保存到: {filepath}")
    except Exception as e:
        print(f"❌ 保存结果时出错: {e}")
    
    print("\n测试完成!")
    return df_with_indicators

if __name__ == "__main__":
    # 测试指定股票和日期
    test_single_indicator('000333', '20250925')