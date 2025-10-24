#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
综合T+0策略多股票多日期测试脚本

该脚本用于测试综合T+0策略在不同股票、不同日期的表现情况，生成详细的统计报告和图表。
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
import os
import sys
from typing import Dict, List, Optional, Tuple
import matplotlib.pyplot as plt

# 添加当前目录的父目录到Python路径，便于导入同目录下的模块
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# 导入综合T+0策略模块
from indicators.comprehensive_t0_strategy import analyze_comprehensive_t0, plot_comprehensive_t0

# 设置中文字体支持
plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

# 输出目录设置
OUTPUT_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'output', 'test_results')
CHART_OUTPUT_DIR = os.path.join(OUTPUT_DIR, 'charts')
os.makedirs(CHART_OUTPUT_DIR, exist_ok=True)


def get_trading_dates(start_date: str, end_date: str) -> List[str]:
    """
    获取两个日期之间的交易日列表
    注意：这里使用简化方法，实际应该查询交易日历
    """
    start = datetime.strptime(start_date, '%Y-%m-%d')
    end = datetime.strptime(end_date, '%Y-%m-%d')
    
    trading_dates = []
    current = start
    
    while current <= end:
        # 排除周末
        if current.weekday() < 5:  # 0=周一, 4=周五
            trading_dates.append(current.strftime('%Y-%m-%d'))
        current += timedelta(days=1)
    
    return trading_dates


def select_random_dates(dates: List[str], count: int) -> List[str]:
    """
    从日期列表中随机选择指定数量的日期
    """
    if len(dates) <= count:
        return dates
    return sorted(random.sample(dates, count))


def run_stock_strategy(stock_code: str, stock_name: str, dates: List[str]) -> Dict[str, any]:
    """
    测试单支股票在多个日期的策略表现
    """
    print(f"\n===== 开始测试股票: {stock_code}({stock_name}) =====")
    
    # 初始化统计数据
    stats = {
        'stock_code': stock_code,
        'stock_name': stock_name,
        'total_days': len(dates),
        'trading_days': 0,  # 有交易信号的天数
        'total_trades': 0,
        'profitable_trades': 0,
        'total_profit': 0.0,
        'avg_profit_per_trade': 0.0,
        'avg_profit_per_day': 0.0,
        'win_rate': 0.0,
        'best_trade': {'profit': -float('inf'), 'date': '', 'details': None},
        'worst_trade': {'profit': float('inf'), 'date': '', 'details': None},
        'daily_results': []
    }
    
    for date in dates:
        print(f"\n--- 测试日期: {date} ---")
        
        # 执行分析
        result = analyze_comprehensive_t0(stock_code, date, has_open_position=False)
        
        if result is None:
            print(f"❌ {date} 数据获取失败或分析失败，跳过该日期")
            continue
        
        df, trades = result
        
        # 生成并保存图表
        chart_path = plot_comprehensive_t0(stock_code, date, has_open_position=False)
        print(f"图表已保存: {chart_path}")
        
        # 统计当日结果
        daily_stats = {
            'date': date,
            'trades': len(trades),
            'profitable_trades': 0,
            'daily_profit': 0.0,
            'avg_hold_time': 0.0,
            'trades_details': trades
        }
        
        if trades:
            stats['trading_days'] += 1
            stats['total_trades'] += len(trades)
            
            daily_profit = 0.0
            total_hold_time = 0.0
            
            for trade in trades:
                profit = trade['profit_pct']
                daily_profit += profit
                total_hold_time += trade['hold_time_minutes']
                
                if profit > 0:
                    stats['profitable_trades'] += 1
                    daily_stats['profitable_trades'] += 1
                
                # 更新最佳和最差交易
                if profit > stats['best_trade']['profit']:
                    stats['best_trade'] = {
                        'profit': profit,
                        'date': date,
                        'details': trade
                    }
                if profit < stats['worst_trade']['profit']:
                    stats['worst_trade'] = {
                        'profit': profit,
                        'date': date,
                        'details': trade
                    }
            
            daily_stats['daily_profit'] = daily_profit
            daily_stats['avg_hold_time'] = total_hold_time / len(trades)
            stats['total_profit'] += daily_profit
        
        stats['daily_results'].append(daily_stats)
    
    # 计算汇总统计
    if stats['total_trades'] > 0:
        stats['win_rate'] = (stats['profitable_trades'] / stats['total_trades']) * 100
        stats['avg_profit_per_trade'] = stats['total_profit'] / stats['total_trades']
    
    if stats['trading_days'] > 0:
        stats['avg_profit_per_day'] = stats['total_profit'] / stats['trading_days']
    
    print(f"\n===== {stock_code}({stock_name}) 测试完成 =====")
    print(f"- 有效交易天数: {stats['trading_days']}/{stats['total_days']}")
    print(f"- 总交易次数: {stats['total_trades']}")
    print(f"- 盈利交易次数: {stats['profitable_trades']}")
    print(f"- 胜率: {stats['win_rate']:.2f}%")
    print(f"- 总收益率: {stats['total_profit']:.2f}%")
    print(f"- 平均每笔交易收益率: {stats['avg_profit_per_trade']:.2f}%")
    print(f"- 平均每日收益率: {stats['avg_profit_per_day']:.2f}%")
    
    if stats['best_trade']['details']:
        print(f"- 最佳交易: 日期 {stats['best_trade']['date']}, 收益率 {stats['best_trade']['profit']:+.2f}%")
    if stats['worst_trade']['details']:
        print(f"- 最差交易: 日期 {stats['worst_trade']['date']}, 收益率 {stats['worst_trade']['profit']:+.2f}%")
    
    return stats


def generate_summary_report(all_stats: List[Dict[str, any]]) -> str:
    """
    生成汇总报告
    """
    report_path = os.path.join(OUTPUT_DIR, 'summary_report.md')
    
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(f"# 综合T+0策略多股票测试报告\n\n")
        f.write(f"**测试日期:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        f.write(f"## 1. 总体统计\n\n")
        
        # 计算总体统计
        total_stocks = len(all_stats)
        total_days = sum(s['total_days'] for s in all_stats)
        total_trading_days = sum(s['trading_days'] for s in all_stats)
        total_trades = sum(s['total_trades'] for s in all_stats)
        total_profitable_trades = sum(s['profitable_trades'] for s in all_stats)
        total_profit = sum(s['total_profit'] for s in all_stats)
        
        overall_win_rate = (total_profitable_trades / total_trades * 100) if total_trades > 0 else 0
        overall_avg_profit_per_trade = (total_profit / total_trades) if total_trades > 0 else 0
        overall_avg_profit_per_day = (total_profit / total_trading_days) if total_trading_days > 0 else 0
        
        f.write(f"- 测试股票数量: {total_stocks}\n")
        f.write(f"- 测试日期总数: {total_days}\n")
        f.write(f"- 有效交易天数: {total_trading_days} ({total_trading_days/total_days*100:.1f}%)\n")
        f.write(f"- 总交易次数: {total_trades}\n")
        f.write(f"- 盈利交易次数: {total_profitable_trades}\n")
        f.write(f"- 总体胜率: {overall_win_rate:.2f}%\n")
        f.write(f"- 总收益率: {total_profit:.2f}%\n")
        f.write(f"- 平均每笔交易收益率: {overall_avg_profit_per_trade:.2f}%\n")
        f.write(f"- 平均每日收益率: {overall_avg_profit_per_day:.2f}%\n\n")
        
        # 各股票详细统计
        f.write("## 2. 各股票表现\n\n")
        
        for stats in all_stats:
            f.write(f"### {stats['stock_code']} - {stats['stock_name']}\n\n")
            f.write(f"- 测试天数: {stats['total_days']}\n")
            # 添加检查避免除零错误
            trading_days_pct = (stats['trading_days']/stats['total_days']*100) if stats['total_days'] > 0 else 0.0
            f.write(f"- 有效交易天数: {stats['trading_days']} ({trading_days_pct:.1f}%)\n")
            f.write(f"- 交易次数: {stats['total_trades']}\n")
            f.write(f"- 盈利交易: {stats['profitable_trades']}\n")
            f.write(f"- 胜率: {stats['win_rate']:.2f}%\n")
            f.write(f"- 总收益率: {stats['total_profit']:.2f}%\n")
            f.write(f"- 平均每笔交易收益率: {stats['avg_profit_per_trade']:.2f}%\n")
            f.write(f"- 平均每日收益率: {stats['avg_profit_per_day']:.2f}%\n")
            
            if stats['best_trade']['details']:
                f.write(f"- 最佳交易: {stats['best_trade']['date']}, 收益率 {stats['best_trade']['profit']:+.2f}%\n")
            if stats['worst_trade']['details']:
                f.write(f"- 最差交易: {stats['worst_trade']['date']}, 收益率 {stats['worst_trade']['profit']:+.2f}%\n")
            
            f.write("\n")
        
        # 每日详细结果
        f.write("## 3. 每日交易详情\n\n")
        
        for stats in all_stats:
            f.write(f"### {stats['stock_code']} - {stats['stock_name']}\n\n")
            f.write("| 日期 | 交易次数 | 盈利次数 | 当日收益率(%) | 平均持有时间(分钟) |\n")
            f.write("|------|----------|----------|--------------|--------------------|\n")
            
            for day in stats['daily_results']:
                f.write(f"| {day['date']} | {day['trades']} | {day['profitable_trades']} | {day['daily_profit']:+.2f} | {day['avg_hold_time']:.0f} |\n")
            
            f.write("\n")
    
    print(f"\n汇总报告已生成: {report_path}")
    return report_path


def generate_summary_charts(all_stats: List[Dict[str, any]]):
    """
    生成汇总图表
    """
    # 1. 各股票胜率对比图
    plt.figure(figsize=(10, 6))
    stocks = [f"{s['stock_code']}\n{s['stock_name']}" for s in all_stats]
    win_rates = [s['win_rate'] for s in all_stats]
    
    bars = plt.bar(stocks, win_rates, color='skyblue')
    for bar, rate in zip(bars, win_rates):
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height + 0.5,
                 f'{rate:.1f}%', ha='center', va='bottom')
    
    plt.title('各股票T+0策略胜率对比')
    plt.ylabel('胜率(%)')
    plt.ylim(0, 100)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.savefig(os.path.join(CHART_OUTPUT_DIR, 'win_rate_comparison.png'), dpi=300, bbox_inches='tight')
    plt.close()
    
    # 2. 各股票平均收益率对比图
    plt.figure(figsize=(10, 6))
    avg_profits = [s['avg_profit_per_trade'] for s in all_stats]
    
    # 为不同收益率的柱状图设置颜色
    colors = []
    for p in avg_profits:
        if p > 0:
            colors.append('green')
        elif p < 0:
            colors.append('red')
        else:
            colors.append('gray')
            
    bars = plt.bar(stocks, avg_profits, color=colors)
    
    for bar, profit in zip(bars, avg_profits):
        height = bar.get_height()
        y_pos = height + 0.05 if height > 0 else height - 0.2
        plt.text(bar.get_x() + bar.get_width()/2., y_pos,
                 f'{profit:+.2f}%', ha='center', va='bottom')
    
    plt.title('各股票T+0策略平均每笔交易收益率对比')
    plt.ylabel('平均收益率(%)')
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.savefig(os.path.join(CHART_OUTPUT_DIR, 'avg_profit_comparison.png'), dpi=300, bbox_inches='tight')
    plt.close()
    
    # 3. 各股票日收益分布图
    plt.figure(figsize=(12, 8))
    
    # 收集所有日收益数据
    all_daily_profits = []
    labels = []
    
    for stats in all_stats:
        daily_profits = [day['daily_profit'] for day in stats['daily_results'] if day['trades'] > 0]
        if daily_profits:  # 只添加有数据的股票
            all_daily_profits.append(daily_profits)
            labels.append(f"{stats['stock_code']}\n{stats['stock_name']}")
    
    if all_daily_profits:  # 只有当有数据时才绘制箱线图
        plt.boxplot(all_daily_profits, tick_labels=labels)  # 使用正确的参数名
    plt.title('各股票T+0策略日收益率分布')
    plt.ylabel('日收益率(%)')
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.savefig(os.path.join(CHART_OUTPUT_DIR, 'daily_profit_distribution.png'), dpi=300, bbox_inches='tight')
    plt.close()
    
    print("\n汇总图表已生成:")
    print(f"1. 胜率对比图: {os.path.join(CHART_OUTPUT_DIR, 'win_rate_comparison.png')}")
    print(f"2. 平均收益率对比图: {os.path.join(CHART_OUTPUT_DIR, 'avg_profit_comparison.png')}")
    print(f"3. 日收益率分布图: {os.path.join(CHART_OUTPUT_DIR, 'daily_profit_distribution.png')}")


def main():
    """
    主函数 - 使用用户确认可用的日期范围进行测试
    """
    print("===== 综合T+0策略多股票测试 =====")
    
    # 导入必要的库
    import akshare as ak
    from datetime import datetime
    import pandas as pd
    
    # 定义测试股票和用户确认可用的日期范围
    test_stocks = [
        {"code": "600030", "name": "中信证券"},
        {"code": "000333", "name": "美的集团"},
        {"code": "002415", "name": "海康威视"}
    ]
    
    # 使用当前年份（2025年）的日期范围 - 测试显示近期数据可获取
    available_dates = [
        # 10月的交易日 - 使用当前年份
        '2025-10-13', '2025-10-14', '2025-10-15', '2025-10-16', '2025-10-17',
        '2025-10-20', '2025-10-21', '2025-10-22', '2025-10-23', '2025-10-24'
    ]
    
    print(f"测试股票数量: {len(test_stocks)}")
    print(f"测试日期: {', '.join(available_dates)}")
    print("注意: 直接使用ak.stock_zh_a_hist_min_em接口获取分时数据")
    
    # 创建输出目录
    for stock in test_stocks:
        stock_output_dir = os.path.join(OUTPUT_DIR, stock['code'])
        os.makedirs(stock_output_dir, exist_ok=True)
    
    # 测试每支股票
    all_results = {}
    for stock in test_stocks:
        print(f"\n\n==================================================================")
        print(f"开始测试: {stock['code']} - {stock['name']}")
        print(f"==================================================================")
        
        stock_results = []
        
        # 测试每一个确认可用的日期
        for test_date in available_dates[:10]:  # 限制为10个日期以符合要求
            print(f"\n\n----- 测试日期: {test_date} -----")
            try:
                # 直接使用akshare接口获取5分钟K线数据
                print(f"正在使用ak.stock_zh_a_hist_min_em获取 {stock['code']} 在 {test_date} 的5分钟K线数据...")
                
                # 构建时间范围 - 尝试不同格式
                start_time = f'{test_date} 09:30:00'
                end_time = f'{test_date} 15:00:00'
                print(f"  时间范围: {start_time} 至 {end_time}")
                print(f"  调用参数: symbol={stock['code']}, period=5, adjust=''")
                
                # 调用接口 - 使用5分钟数据（测试显示1分钟数据不可用，但5分钟及以上可用）
                df = ak.stock_zh_a_hist_min_em(
                    symbol=stock['code'],
                    period="5",  # 5分钟数据（测试显示可用）
                    start_date=start_time,
                    end_date=end_time,
                    adjust=''  # 不复权
                )
                
                if df is None or df.empty:
                    print(f"❌ 警告: 未能获取5分钟K线数据，返回None或空数据框")
                    
                    # 尝试获取其他周期数据作为备选
                    print(f"  尝试获取60分钟K线数据作为备选...")
                    try:
                        df_60min = ak.stock_zh_a_hist_min_em(
                            symbol=stock['code'],
                            period="60",  # 60分钟数据
                            start_date=start_time,
                            end_date=end_time,
                            adjust=""
                        )
                        if df_60min is not None and not df_60min.empty:
                            print(f"✅ 成功获取60分钟K线数据! 数据形状: {df_60min.shape}")
                            df = df_60min  # 使用60分钟数据继续测试
                        else:
                            print(f"❌ 60分钟数据也无法获取")
                            continue
                    except Exception as e2:
                        print(f"❌ 获取60分钟数据时发生异常: {type(e2).__name__}: {str(e2)}")
                        continue
                else:
                    print(f"✅ 成功获取5分钟K线数据! 数据形状: {df.shape}")
                    # 打印数据框的列名来了解实际结构
                    print(f"  数据列: {df.columns.tolist()}")
                    # 打印前几行数据来查看内容
                    print(f"  前3行数据:")
                    print(df.head(3).to_string(index=False))
                
                print(f"✅ 成功获取数据! 数据形状: {df.shape}")
                print(f"数据列名: {df.columns.tolist()}")
                print(f"数据前5行:\n{df.head()}")
                
                # 保存原始数据到CSV以便检查
                csv_path = os.path.join(OUTPUT_DIR, stock['code'], f"{stock['code']}_{test_date}_data.csv")
                df.to_csv(csv_path)
                print(f"数据已保存到: {csv_path}")
                
                # 现在尝试调用comprehensive_t0_strategy进行分析
                print("\n开始策略分析...")
                
                # 检查是否能成功调用分析函数
                try:
                    result = analyze_comprehensive_t0(stock['code'], test_date, has_open_position=False)
                    
                    if result:
                        df_result, trades = result
                        print(f"✅ 策略分析完成! 生成了 {len(trades)} 个交易对")
                        
                        # 统计交易结果
                        daily_result = {
                            'date': test_date,
                            'trades_count': len(trades),
                            'profitable_trades': sum(1 for t in trades if t['profit_pct'] > 0),
                            'total_profit': sum(t['profit_pct'] for t in trades),
                            'win_rate': (sum(1 for t in trades if t['profit_pct'] > 0) / len(trades) * 100) if trades else 0
                        }
                        stock_results.append(daily_result)
                        
                        print(f"当日统计: 交易{len(trades)}笔, 盈利{daily_result['profitable_trades']}笔, 胜率{daily_result['win_rate']:.2f}%, 总收益{daily_result['total_profit']:+.2f}%")
                        
                        # 生成图表
                        chart_path = plot_comprehensive_t0(stock['code'], test_date, has_open_position=False)
                        print(f"✅ 图表已生成: {chart_path}")
                    else:
                        print("❌ 策略分析失败，未返回结果")
                        
                except Exception as e:
                    print(f"❌ 调用分析函数时发生错误: {str(e)}")
                    print("尝试手动运行策略核心逻辑...")
                    
                    # 尝试手动执行一些基本的T+0逻辑作为备用
                    # 这里只是简单的买卖信号检测，作为演示
                    if len(df) > 20:
                        # 计算一些基本指标
                        df['price_change'] = df['close'].pct_change()
                        df['signal'] = 0
                        
                        # 简单的买入卖出信号逻辑
                        df.loc[df['price_change'] < -0.01, 'signal'] = 1  # 下跌超过1%买入
                        df.loc[df['price_change'] > 0.01, 'signal'] = -1  # 上涨超过1%卖出
                        
                        # 计算交易对
                        buy_signals = df[df['signal'] == 1]
                        sell_signals = df[df['signal'] == -1]
                        
                        print(f"手动分析: 发现{len(buy_signals)}个买入信号, {len(sell_signals)}个卖出信号")
                        
                        # 保存手动分析结果
                        df.to_csv(os.path.join(OUTPUT_DIR, stock['code'], f"{stock['code']}_{test_date}_manual_analysis.csv"))
                
            except Exception as e:
                print(f"❌ 测试 {stock['code']} 在 {test_date} 时发生异常")
                print(f"异常类型: {type(e).__name__}")
                print(f"异常信息: {str(e)}")
                import traceback
                print("详细错误堆栈:")
                traceback.print_exc()
        
        # 保存股票测试结果
        all_results[stock['code']] = {
            'name': stock['name'],
            'results': stock_results
        }
        
        # 打印股票的总体统计
        if stock_results:
            total_trades = sum(r['trades_count'] for r in stock_results)
            total_profitable = sum(r['profitable_trades'] for r in stock_results)
            total_profit = sum(r['total_profit'] for r in stock_results)
            avg_win_rate = sum(r['win_rate'] for r in stock_results) / len(stock_results)
            
            print(f"\n📊 {stock['code']}({stock['name']}) 总体统计:")
            print(f"- 有效交易日: {len(stock_results)}/{len(available_dates[:10])}")
            print(f"- 总交易次数: {total_trades}")
            print(f"- 盈利交易次数: {total_profitable}")
            print(f"- 总体胜率: {avg_win_rate:.2f}%")
            print(f"- 总收益率: {total_profit:+.2f}%")
            if total_trades > 0:
                print(f"- 平均每笔收益率: {total_profit/total_trades:+.2f}%")
    
    # 生成简单的汇总报告
    report_path = os.path.join(OUTPUT_DIR, 'simple_summary_report.md')
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write("# T+0策略测试简单汇总报告\n\n")
        f.write(f"**测试时间:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        
        for stock_code, stock_data in all_results.items():
            f.write(f"## {stock_code} - {stock_data['name']}\n\n")
            
            if stock_data['results']:
                f.write("| 日期 | 交易次数 | 盈利次数 | 总收益(%) | 胜率(%) |\n")
                f.write("|------|----------|----------|----------|--------|\n")
                
                for r in stock_data['results']:
                    f.write(f"| {r['date']} | {r['trades_count']} | {r['profitable_trades']} | {r['total_profit']:+.2f} | {r['win_rate']:.1f} |\n")
                
                # 计算汇总统计
                total_trades = sum(r['trades_count'] for r in stock_data['results'])
                total_profitable = sum(r['profitable_trades'] for r in stock_data['results'])
                total_profit = sum(r['total_profit'] for r in stock_data['results'])
                
                # 添加检查避免除零错误
                win_rate = (total_profitable/total_trades*100) if total_trades > 0 else 0.0
                avg_return = (total_profit/total_trades) if total_trades > 0 else 0.0
                
                f.write(f"\n### 汇总统计\n\n")
                f.write(f"- 有效交易日: {len(stock_data['results'])}\n")
                f.write(f"- 总交易次数: {total_trades}\n")
                f.write(f"- 盈利交易次数: {total_profitable}\n")
                f.write(f"- 总体胜率: {win_rate:.2f}%\n")
                f.write(f"- 总收益率: {total_profit:+.2f}%\n")
                if total_trades > 0:
                    f.write(f"- 平均每笔收益率: {avg_return:+.2f}%\n")
            else:
                f.write("暂无有效交易数据\n")
            
            f.write("\n")
    
    print("\n\n===== 测试完成 =====")
    print(f"简单汇总报告已生成: {report_path}")
    print(f"详细数据和图表保存在: {OUTPUT_DIR}")


if __name__ == "__main__":
    main()