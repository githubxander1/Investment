#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
T0交易策略系统基本使用示例

本示例展示了如何使用T0Strategy类进行股票分析和交易信号监控
"""

import sys
import os

# 添加项目根目录到路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src import T0Strategy


def basic_example():
    """基本使用示例"""
    print("===== T0交易策略系统基本使用示例 =====")
    
    # 创建策略实例
    print("\n1. 创建T0策略实例（使用默认股票池）")
    strategy = T0Strategy(
        refresh_interval=60,  # 60秒刷新一次数据
        save_charts=True,     # 保存图表到output目录
        notification_enabled=True  # 启用信号通知
    )
    
    # 分析单只股票
    print("\n2. 分析单只股票 '600519'（贵州茅台）")
    result = strategy.analyze_stock('600519')
    
    # 打印分析结果
    if result:
        print(f"\n3. 分析结果摘要:")
        print(f"股票代码: {result['stock_code']}")
        print(f"前一日收盘价: {result['prev_close']:.2f}")
        print(f"最新价格: {result['data'].iloc[-1]['收盘']:.2f}")
        print(f"买入信号数量: {len(result['signals']['buy_signals'])}")
        print(f"卖出信号数量: {len(result['signals']['sell_signals'])}")
        print(f"其他信号数量: {len(result['signals']['other_signals'])}")
        
        # 如果有信号，显示最近的信号
        if result['signals']['buy_signals']:
            latest_buy = max(result['signals']['buy_signals'], key=lambda x: x['time'])
            print(f"最近买入信号: {latest_buy['time'].strftime('%H:%M:%S')}, 价格: {latest_buy['price']:.2f}, 类型: {latest_buy['type']}")
        
        if result['signals']['sell_signals']:
            latest_sell = max(result['signals']['sell_signals'], key=lambda x: x['time'])
            print(f"最近卖出信号: {latest_sell['time'].strftime('%H:%M:%S')}, 价格: {latest_sell['price']:.2f}, 类型: {latest_sell['type']}")
        
        # 显示图表保存路径
        if result['chart_path']:
            print(f"图表保存路径: {result['chart_path']}")
    
    print("\n===== 示例结束 =====")


def custom_stock_pool_example():
    """自定义股票池示例"""
    print("\n\n===== 自定义股票池示例 =====")
    
    # 自定义股票池
    custom_stock_pool = [
        '600036',  # 招商银行
        '000002',  # 万科A
        '601899',  # 紫金矿业
        '002415',  # 海康威视
        '300750'   # 宁德时代
    ]
    
    print(f"使用自定义股票池: {custom_stock_pool}")
    
    # 创建自定义股票池的策略实例
    strategy = T0Strategy(
        stock_pool=custom_stock_pool,
        refresh_interval=30,  # 30秒刷新一次
        save_charts=True,
        notification_enabled=True
    )
    
    # 分析所有股票
    print("\n分析自定义股票池中的所有股票...")
    for stock_code in custom_stock_pool:
        result = strategy.analyze_stock(stock_code)
        if result:
            print(f"\n股票 {stock_code} 分析结果:")
            print(f"  最新价格: {result['data'].iloc[-1]['收盘']:.2f}")
            print(f"  买入信号: {len(result['signals']['buy_signals'])}, 卖出信号: {len(result['signals']['sell_signals'])}")
    
    print("\n===== 自定义股票池示例结束 =====")


def advanced_usage_example():
    """高级使用示例"""
    print("\n\n===== 高级使用示例 =====")
    
    # 创建策略实例
    strategy = T0Strategy(
        stock_pool=['600519'],  # 仅分析贵州茅台
        refresh_interval=60,
        save_charts=True,
        notification_enabled=True
    )
    
    # 分析股票
    result = strategy.analyze_stock('600519')
    
    if result:
        # 获取完整的数据分析结果
        df = result['data']
        
        print("\n获取详细的数据分析结果:")
        print(f"数据时间范围: {df['时间'].min().strftime('%Y-%m-%d %H:%M:%S')} 至 {df['时间'].max().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"数据点数量: {len(df)}")
        
        # 显示最后几行数据
        print("\n最后5行数据:")
        print(df.tail())
        
        # 显示所有计算的指标
        print("\n计算的指标列:")
        indicator_columns = [col for col in df.columns if col not in ['时间', '开盘', '最高', '最低', '收盘', '成交量', '成交额']]
        print(indicator_columns)
    
    print("\n===== 高级使用示例结束 =====")


def run_full_strategy():
    """运行完整策略示例"""
    print("\n\n===== 运行完整策略示例 =====")
    print("注意：此示例将在交易时间内持续运行，非交易时间会等待。按Ctrl+C可中断运行。")
    
    # 询问用户是否要运行完整策略
    choice = input("是否要运行完整策略？(y/n): ")
    
    if choice.lower() == 'y':
        # 创建策略实例
        strategy = T0Strategy(
            stock_pool=['600000', '600519', '000001'],  # 浦发银行、贵州茅台、平安银行
            refresh_interval=60,
            save_charts=True,
            notification_enabled=True
        )
        
        try:
            print("\n开始运行策略...")
            strategy.run()
        except KeyboardInterrupt:
            print("\n用户中断策略运行")
    else:
        print("跳过运行完整策略")
    
    print("\n===== 运行完整策略示例结束 =====")


def main():
    """主函数"""
    print("欢迎使用T0交易策略系统示例")
    print("本示例展示了T0Strategy类的不同使用方法")
    
    # 运行基本示例
    basic_example()
    
    # 运行自定义股票池示例
    custom_stock_pool_example()
    
    # 运行高级使用示例
    advanced_usage_example()
    
    # 运行完整策略示例
    run_full_strategy()
    
    print("\n所有示例运行完毕")
    print("请参考README.md文件了解更多详细信息")


if __name__ == '__main__':
    main()