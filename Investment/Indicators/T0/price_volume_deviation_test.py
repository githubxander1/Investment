#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
简化版价格成交量偏离指标测试脚本
仅用于测试图表中间空白区域的修复
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime, timedelta
import os
import sys

# 设置中文字体支持
plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

# 交易时间常量
MORNING_START = datetime.strptime('09:30', '%H:%M').time()
MORNING_END = datetime.strptime('11:30', '%H:%M').time()
AFTERNOON_START = datetime.strptime('13:00', '%H:%M').time()
AFTERNOON_END = datetime.strptime('15:00', '%H:%M').time()

def create_sample_data():
    """
    创建示例分时数据用于测试
    """
    # 创建时间序列
    today = datetime.now().date()
    morning_times = pd.date_range(start=f"{today} 09:30", end=f"{today} 11:30", freq="1min")
    afternoon_times = pd.date_range(start=f"{today} 13:00", end=f"{today} 15:00", freq="1min")
    
    # 合并时间序列
    times = morning_times.union(afternoon_times)
    
    # 创建示例数据
    base_price = 29.5
    # 上午价格小幅波动
    morning_prices = base_price + np.sin(np.linspace(0, 3, len(morning_times))) * 0.3 + np.random.randn(len(morning_times)) * 0.05
    # 下午价格继续波动
    afternoon_prices = morning_prices[-1] + np.sin(np.linspace(0, 4, len(afternoon_times))) * 0.2 + np.random.randn(len(afternoon_times)) * 0.05
    
    # 合并价格数据
    prices = np.concatenate([morning_prices, afternoon_prices])
    
    # 生成均价（略低于收盘价）
    avg_prices = prices - np.random.rand(len(prices)) * 0.05
    
    # 生成成交量（上午波动大，下午相对平稳）
    morning_volumes = np.abs(np.sin(np.linspace(0, 2, len(morning_times))) * 5000 + np.random.randn(len(morning_times)) * 1000)
    afternoon_volumes = np.abs(np.sin(np.linspace(0, 3, len(afternoon_times))) * 3000 + np.random.randn(len(afternoon_times)) * 800)
    volumes = np.concatenate([morning_volumes, afternoon_volumes])
    
    # 创建DataFrame
    df = pd.DataFrame({
        '收盘': prices,
        '均价': avg_prices,
        '成交量': volumes
    }, index=times)
    
    # 计算偏离度
    df['Price_MA_Ratio'] = (df['收盘'] - df['均价']) / df['均价'] * 100
    df['Price_MA_Ratio_Amplified'] = df['Price_MA_Ratio'] * 50
    
    # 计算量比（示例）
    df['Volume_Ratio'] = 1.0 + np.random.randn(len(df)) * 0.2
    
    # 生成一些买卖信号（示例）
    df['Buy_Signal'] = False
    df['Sell_Signal'] = False
    
    # 随机选择一些位置作为信号点
    buy_indices = np.random.choice(len(df), 5, replace=False)
    sell_indices = np.random.choice(len(df), 5, replace=False)
    
    df.iloc[buy_indices, df.columns.get_loc('Buy_Signal')] = True
    df.iloc[sell_indices, df.columns.get_loc('Sell_Signal')] = True
    
    return df

def visualize_strategy(stock_code, df):
    """
    可视化策略，修复了图表中间空白区域的问题
    """
    # 获取今天的日期
    today = df.index[0].date()
    
    # 过滤掉非交易时间
    df_filtered = df.copy()
    
    # 分离上午和下午的数据
    morning_data = df_filtered[(df_filtered.index.time >= MORNING_START) & 
                              (df_filtered.index.time <= MORNING_END)]
    afternoon_data = df_filtered[(df_filtered.index.time >= AFTERNOON_START) & 
                               (df_filtered.index.time <= AFTERNOON_END)]
    
    # 获取买入和卖出信号
    buy_signals = df_filtered[df_filtered['Buy_Signal']]
    sell_signals = df_filtered[df_filtered['Sell_Signal']]
    
    # 创建图形和子图
    fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(14, 12), gridspec_kw={'height_ratios': [2, 1, 1]})
    fig.subplots_adjust(hspace=0.4)
    
    # 格式化日期
    formatted_date = df_filtered.index[0].strftime('%Y-%m-%d')
    
    # 为了完全消除中间空白区域，我们需要创建一个不连续的x轴
    # 这个方法使用虚拟的时间戳，将下午的数据紧接在上午数据之后显示
    
    # 创建一个新的虚拟时间索引，让下午数据紧接在上午数据之后
    # 首先，创建一个副本避免修改原始数据
    morning_data_plot = morning_data.copy()
    afternoon_data_plot = afternoon_data.copy()
    
    if not morning_data.empty and not afternoon_data.empty:
        # 计算上午最后一个时间点和下午第一个时间点
        last_morning_time = morning_data.index[-1]
        first_afternoon_time = afternoon_data.index[0]
        
        # 计算时间差（实际是午休时间）
        time_gap = first_afternoon_time - last_morning_time
        
        # 创建一个映射函数，将下午时间减去午休时间间隔
        def adjust_afternoon_time(ts):
            return ts - time_gap
        
        # 应用映射到下午数据
        afternoon_data_plot.index = afternoon_data_plot.index.map(adjust_afternoon_time)
    
    # 现在分别绘制调整后的上午和下午数据
    # 绘制价格和均价
    if not morning_data.empty:
        ax1.plot(morning_data_plot.index, morning_data_plot['收盘'], label='收盘价', color='black', linewidth=1)
        ax1.plot(morning_data_plot.index, morning_data_plot['均价'], label='均价', color='blue', linewidth=1)
    if not afternoon_data.empty:
        ax1.plot(afternoon_data_plot.index, afternoon_data_plot['收盘'], color='black', linewidth=1)
        ax1.plot(afternoon_data_plot.index, afternoon_data_plot['均价'], color='blue', linewidth=1)
    
    # 绘制买入信号
    if not buy_signals.empty:
        # 为买入信号也调整下午的时间戳
        buy_morning = buy_signals[buy_signals.index.time < MORNING_END]
        buy_afternoon = buy_signals[buy_signals.index.time >= AFTERNOON_START]
        
        if not buy_morning.empty:
            ax1.scatter(buy_morning.index, buy_morning['收盘'] * 0.995, marker='^', color='red', s=100, zorder=5)
            for idx, row in buy_morning.iterrows():
                ax1.text(idx, row['收盘'] * 0.99, '买',
                         color='red', fontsize=12, ha='center', va='top', fontweight='bold')
        
        if not buy_afternoon.empty and not morning_data.empty and not afternoon_data.empty:
            # 调整下午买入信号的时间戳
            buy_afternoon_adj = buy_afternoon.copy()
            buy_afternoon_adj.index = buy_afternoon_adj.index.map(adjust_afternoon_time)
            
            ax1.scatter(buy_afternoon_adj.index, buy_afternoon_adj['收盘'] * 0.995, marker='^', color='red', s=100, zorder=5)
            for idx, row in buy_afternoon_adj.iterrows():
                ax1.text(idx, row['收盘'] * 0.99, '买',
                         color='red', fontsize=12, ha='center', va='top', fontweight='bold')
    
    # 绘制卖出信号
    if not sell_signals.empty:
        # 为卖出信号也调整下午的时间戳
        sell_morning = sell_signals[sell_signals.index.time < MORNING_END]
        sell_afternoon = sell_signals[sell_signals.index.time >= AFTERNOON_START]
        
        if not sell_morning.empty:
            ax1.scatter(sell_morning.index, sell_morning['收盘'] * 1.005, marker='v', color='green', s=100, zorder=5)
            for idx, row in sell_morning.iterrows():
                ax1.text(idx, row['收盘'] * 1.01, '卖',
                         color='green', fontsize=12, ha='center', va='bottom', fontweight='bold')
        
        if not sell_afternoon.empty and not morning_data.empty and not afternoon_data.empty:
            # 调整下午卖出信号的时间戳
            sell_afternoon_adj = sell_afternoon.copy()
            sell_afternoon_adj.index = sell_afternoon_adj.index.map(adjust_afternoon_time)
            
            ax1.scatter(sell_afternoon_adj.index, sell_afternoon_adj['收盘'] * 1.005, marker='v', color='green', s=100, zorder=5)
            for idx, row in sell_afternoon_adj.iterrows():
                ax1.text(idx, row['收盘'] * 1.01, '卖',
                         color='green', fontsize=12, ha='center', va='bottom', fontweight='bold')
    
    # 设置第一个子图的属性
    ax1.set_ylabel('价格', fontsize=12)
    ax1.grid(True, linestyle='--', alpha=0.7)
    ax1.legend()
    
    # 绘制价格与均价的比率
    if not morning_data.empty:
        ax2.plot(morning_data_plot.index, morning_data_plot['Price_MA_Ratio_Amplified'], 
                label='偏离度放大(偏离度*50)', color='red', linewidth=2)
    if not afternoon_data.empty:
        ax2.plot(afternoon_data_plot.index, afternoon_data_plot['Price_MA_Ratio_Amplified'], 
                color='red', linewidth=2)
    
    ax2.axhline(y=0, color='black', linestyle='-', alpha=0.5)
    ax2.axhline(y=15, color='green', linestyle='--', alpha=0.7, label='卖出阈值')
    ax2.axhline(y=-15, color='red', linestyle='--', alpha=0.7, label='买入阈值')
    ax2.set_ylabel('偏离度放大值', fontsize=12)
    ax2.grid(True, linestyle='--', alpha=0.7)
    ax2.legend()
    
    # 绘制量比
    if not morning_data.empty:
        ax3.plot(morning_data_plot.index, morning_data_plot['Volume_Ratio'], 
                label='量比', color='green', linewidth=1)
    if not afternoon_data.empty:
        ax3.plot(afternoon_data_plot.index, afternoon_data_plot['Volume_Ratio'], 
                color='green', linewidth=1)
    
    ax3.axhline(y=1.5, color='green', linestyle='--', alpha=0.7, label='放量阈值')
    ax3.axhline(y=0.5, color='red', linestyle='--', alpha=0.7, label='缩量阈值')
    ax3.axhline(y=1.0, color='gray', linestyle='-', alpha=0.5)
    ax3.set_ylabel('量比', fontsize=12)
    ax3.set_xlabel('时间', fontsize=12)
    ax3.grid(True, linestyle='--', alpha=0.7)
    ax3.legend()
    
    # 为了确保时间轴正确显示（11:30之后直接显示13:00），我们需要自定义时间轴刻度
    # 首先设置x轴范围
    min_time = None
    max_time = None
    
    if not morning_data.empty:
        min_time = morning_data_plot.index.min()
        max_time = morning_data_plot.index.max()
    
    if not afternoon_data.empty:
        if min_time is None:
            min_time = afternoon_data_plot.index.min()
        if max_time is None or afternoon_data_plot.index.max() > max_time:
            max_time = afternoon_data_plot.index.max()
    
    # 为所有子图设置相同的x轴范围
    if min_time is not None and max_time is not None:
        for ax in [ax1, ax2, ax3]:
            ax.set_xlim(min_time, max_time)
    
    # 设置x轴时间格式和刻度
    for ax in [ax1, ax2, ax3]:
        # 创建自定义的时间刻度标签
        if not morning_data.empty and not afternoon_data.empty:
            # 上午的时间点
            morning_times = []
            current = morning_data_plot.index.min()
            end = morning_data_plot.index.max()
            while current <= end:
                morning_times.append(current)
                current += timedelta(minutes=30)  # 每30分钟一个刻度
            
            # 下午的时间点（使用原始时间而不是调整后的时间）
            afternoon_times = []
            current = pd.Timestamp(f"{today} {AFTERNOON_START}")
            end = pd.Timestamp(f"{today} {AFTERNOON_END}")
            while current <= end:
                afternoon_times.append(current)
                current += timedelta(minutes=30)  # 每30分钟一个刻度
            
            # 创建虚拟时间到实际时间的映射
            afternoon_time_map = {}
            last_morning_time = morning_data_plot.index[-1]
            first_afternoon_time = afternoon_data.index[0]
            time_gap = first_afternoon_time - last_morning_time
            
            # 为每个下午时间创建对应的虚拟时间
            for real_time in afternoon_times:
                virtual_time = real_time - time_gap
                afternoon_time_map[virtual_time] = real_time
            
            # 合并上午时间和下午虚拟时间作为刻度位置
            all_ticks = morning_times.copy()
            all_ticks.extend(afternoon_time_map.keys())
            
            # 相应的标签文本（使用实际时间格式）
            all_labels = [time.strftime('%H:%M') for time in morning_times]
            all_labels.extend([time.strftime('%H:%M') for time in afternoon_time_map.values()])
            
            # 设置自定义刻度和标签
            ax.set_xticks(all_ticks)
            ax.set_xticklabels(all_labels)
        else:
            # 如果只有上午或下午数据，使用标准格式
            ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
            ax.xaxis.set_major_locator(mdates.MinuteLocator(byminute=[0, 15, 30, 45]))
    
    # 设置刻度标签旋转角度
    plt.setp(ax1.xaxis.get_majorticklabels(), rotation=45)
    plt.setp(ax2.xaxis.get_majorticklabels(), rotation=45)
    plt.setp(ax3.xaxis.get_majorticklabels(), rotation=45)
    
    # 添加标题
    fig.suptitle(f'{stock_code} 价均量策略图 ({formatted_date})', fontsize=16)
    
    # 显示图表
    plt.tight_layout()
    plt.subplots_adjust(top=0.92)
    plt.show()

if __name__ == "__main__":
    # 创建示例数据
    df = create_sample_data()
    print(f"创建了示例数据，共{len(df)}条记录")
    
    # 可视化
    visualize_strategy("600030", df)