#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
T0策略系统基本用法示例

这个示例展示了如何初始化和使用T0Strategy类进行股票分析
"""

from main import T0Strategy
import sys


def main():
    # 方法1: 使用默认股票池（工商银行、长江电力、中国电信）
    print("\n===== 示例1: 使用默认股票池 =====")
    strategy = T0Strategy()
    print(f"默认监控股票池: {strategy.stock_codes}")
    
    # 方法2: 自定义股票池
    print("\n===== 示例2: 使用自定义股票池 =====")
    custom_stocks = ["600036", "601318", "600519"]  # 招商银行、中国平安、贵州茅台
    custom_strategy = T0Strategy(custom_stocks)
    print(f"自定义监控股票池: {custom_strategy.stock_codes}")
    
    # 方法3: 单独分析一只股票
    print("\n===== 示例3: 单独分析一只股票 =====")
    try:
        stock_code = "601398"  # 工商银行
        print(f"开始分析股票: {stock_code}")
        df = custom_strategy.analyze_stock(stock_code)
        if df is not None:
            print(f"\n股票 {stock_code} 分析结果预览:")
            print(df[['开盘', '收盘', '最高', '最低', '支撑', '阻力']].tail())
            
            # 检查是否有交易信号
            buy_signals = df[df['longcross_support']]
            sell_signals = df[df['longcross_resistance']]
            print(f"\n找到 {len(buy_signals)} 个买入信号")
            print(f"找到 {len(sell_signals)} 个卖出信号")
    except Exception as e:
        print(f"分析股票失败: {e}")
    
    print("\n===== 使用提示 =====")
    print("1. 运行 'python main.py' 启动完整的T0策略监控")
    print("2. 运行 'python main.py 股票代码1 股票代码2 ...' 使用自定义股票池")
    print("3. 非交易时间系统会自动等待，交易时间内每分钟运行一次分析")
    print("4. 发现交易信号时会自动发送通知")


if __name__ == "__main__":
    main()