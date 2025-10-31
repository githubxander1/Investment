#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
量价指标模块 (volume_price_indicators.py)

该模块实现了基于量价关系的技术分析指标和策略，包括：
1. 量价关系计算与分析
2. 买卖盘力量对比
3. 成交量异常检测
4. 量价配合度评估
5. 交易信号生成与可视化

使用方法：
    可以调用calculate_volume_price_indicators计算基础量价指标，或使用其他高级分析函数进行完整分析

作者: 
创建日期: 
版本: 1.0
"""

import os
import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import matplotlib.dates as mdates
from typing import Optional, Tuple, Dict, Any
import akshare as ak

# 添加项目根目录到系统路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# 设置matplotlib中文字体支持
plt.rcParams['font.sans-serif'] = ['SimHei', 'WenQuanYi Micro Hei', 'Heiti TC']
plt.rcParams['axes.unicode_minus'] = False

# 全局变量
CACHE_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'cache')
OUTPUT_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'output', 'charts')

# 确保目录存在
os.makedirs(CACHE_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

# 设置matplotlib后端，确保图表能正确显示
import matplotlib

matplotlib.use('Agg')  # 使用Agg后端，不显示图形界面


def calculate_volume_price_indicators(df: pd.DataFrame, prev_close: float) -> Tuple[pd.DataFrame, float, float, float]:
    """
    计算量价指标
    
    功能：分析价格与成交量的关系，计算买卖盘力量对比及量价配合度
    
    参数：
        df: 包含价格和成交量数据的DataFrame，需包含'成交量'和'收盘'列
        prev_close: 前收盘价，用于价格参考
    
    返回值：
        元组 (df, 买方占比, 卖方占比, 买卖差占比)
        - df: 添加了量价指标的DataFrame
        - 买方占比: 买方力量占总力量的百分比
        - 卖方占比: 卖方力量占总力量的百分比
        - 买卖差占比: 买卖力量差额占总力量的百分比
    
    计算逻辑：
    1. 计算量价指标 = (成交量/收盘价)/3
    2. 计算买方力量(A2)：当日收盘价高于前一日收盘价且量价>0.20的量价之和
    3. 计算卖方力量(A3)：当日收盘价低于前一日收盘价且量价>0.20的量价之和
    4. 计算总力量(A6) = A2 + A3
    5. 计算买卖力量占比和差额占比
    """
    # 计算量价指标
    df['量价'] = (df['成交量'] / df['收盘']) / 3
    
    # 计算A2（买方力量）
    condition_a2 = (df['量价'] > 0.20) & (df['收盘'] > df['收盘'].shift(1))
    df['A2'] = np.where(condition_a2, df['量价'], 0)
    
    # 计算A3（卖方力量）
    condition_a3 = (df['量价'] > 0.20) & (df['收盘'] < df['收盘'].shift(1))
    df['A3'] = np.where(condition_a3, df['量价'], 0)
    
    # 累计求和
    df['A2_cum'] = df['A2'].cumsum()
    df['A3_cum'] = df['A3'].cumsum()
    
    # 计算其他指标
    df['A6_cum'] = df['A2_cum'] + df['A3_cum']
    
    # 最新值
    latest_a2 = df['A2_cum'].iloc[-1] if len(df) > 0 else 0
    latest_a3 = df['A3_cum'].iloc[-1] if len(df) > 0 else 0
    latest_a6 = df['A6_cum'].iloc[-1] if len(df) > 0 else 0
    
    # 避免除零错误
    if latest_a6 != 0:
        buy_ratio = (100 * latest_a2) / latest_a6
        sell_ratio = (100 * latest_a3) / latest_a6
        diff_ratio = (100 * (latest_a2 - latest_a3)) / latest_a6
    else:
        buy_ratio = 0
        sell_ratio = 0
        diff_ratio = 0
    
    return df, buy_ratio, sell_ratio, diff_ratio


def calculate_support_resistance(df, prev_close) -> pd.DataFrame:
    """
    计算支撑和阻力位：
    H1:=MAX(DYNAINFO(3),DYNAINFO(5));
    L1:=MIN(DYNAINFO(3),DYNAINFO(6));P1:=H1-L1;
    支撑:L1+P1*1/8,POINTDOT,COLORMAGENTA;
    阻力:=L1+P1*7/8,COLORGREEN;
    章鱼底参考:L1+P1/3,POINTDOT,COLORBLUE;
    """
    # 获取当日最高价和最低价
    daily_high = df['最高'].max()
    daily_low = df['最低'].min()
    
    # 计算 H1、L1（昨收 vs 日内高低）
    df['H1'] = np.maximum(prev_close, daily_high)
    df['L1'] = np.minimum(prev_close, daily_low)
    
    # 支撑、阻力计算
    df['P1'] = df['H1'] - df['L1']
    df['支撑'] = df['L1'] + df['P1'] * 1 / 8
    df['阻力'] = df['L1'] + df['P1'] * 7 / 8
    df['章鱼底参考'] = df['L1'] + df['P1'] / 3
    
    return df


def calculate_fund_flow_indicators(df) -> pd.DataFrame:
    """
    计算资金流向指标：
    XX:=SUM(AMOUNT,BARSCOUNT(CLOSE))/SUM(V*100,BARSCOUNT(CLOSE));
    主力:=EXPMA(CLOSE/XX,20);
    大户:=EXPMA(CLOSE/XX,60);
    散户:=EXPMA(CLOSE/XX,120);
    """
    # 计算XX值
    df['XX'] = df['成交额'].cumsum() / (df['成交量'] * 100).cumsum()
    
    # 处理可能的除零情况
    df['CLOSE_XX'] = df['收盘'] / df['XX']
    df['CLOSE_XX'] = df['CLOSE_XX'].replace([np.inf, -np.inf], np.nan)
    df['CLOSE_XX'] = df['CLOSE_XX'].ffill().bfill()
    
    # 计算主力、大户、散户资金流向
    df['主力'] = df['CLOSE_XX'].ewm(span=20, adjust=False).mean()
    df['大户'] = df['CLOSE_XX'].ewm(span=60, adjust=False).mean()
    df['散户'] = df['CLOSE_XX'].ewm(span=120, adjust=False).mean()
    
    return df


def calculate_precise_lines(df) -> pd.DataFrame:
    """
    计算精准线：
    N01:=3;L00:=0.00;L01:=ABS(L-REF(L,1))<=L00;L02:=ABS(L-REF(L,2))<=L00;
    L03:=ABS(L-REF(L,3))<=L00;L04:=ABS(L-REF(L,4))<=L00;L05:=ABS(L-REF(L,5))<=L00;
    精准线首次:=L01 OR L02 OR L03 OR L04 OR L05;
    精准左:=FILTER(精准线首次,N01) ;
    """
    # 参数设置
    n01 = 3
    l00 = 0.00
    
    # 计算精准线条件
    df['L01'] = (df['最低'] - df['最低'].shift(1)).abs() <= l00
    df['L02'] = (df['最低'] - df['最低'].shift(2)).abs() <= l00
    df['L03'] = (df['最低'] - df['最低'].shift(3)).abs() <= l00
    df['L04'] = (df['最低'] - df['最低'].shift(4)).abs() <= l00
    df['L05'] = (df['最低'] - df['最低'].shift(5)).abs() <= l00
    
    # 精准线首次
    df['精准线首次'] = df['L01'] | df['L02'] | df['L03'] | df['L04'] | df['L05']
    
    # 精准左（FILTER函数模拟）
    df['精准左'] = df['精准线首次'].rolling(window=n01).apply(
        lambda x: x.iloc[-1] and not x.iloc[:-1].any(), raw=False
    ).fillna(0).astype(bool)
    
    # 高点精准线
    df['G1'] = (df['最高'] - df['最高'].shift(1)).abs() <= l00
    df['G2'] = (df['最高'] - df['最高'].shift(2)).abs() <= l00
    df['G3'] = (df['最高'] - df['最高'].shift(3)).abs() <= l00
    df['G4'] = (df['最高'] - df['最高'].shift(4)).abs() <= l00
    df['G5'] = (df['最高'] - df['最高'].shift(5)).abs() <= l00
    
    # 精准线首次（高点）
    df['精准线首次1'] = df['G1'] | df['G2'] | df['G3'] | df['G4'] | df['G5']
    
    # 精准左1（FILTER函数模拟）
    df['精准左1'] = df['精准线首次1'].rolling(window=n01).apply(
        lambda x: x.iloc[-1] and not x.iloc[:-1].any(), raw=False
    ).fillna(0).astype(bool)
    
    return df


def detect_signals(df) -> pd.DataFrame:
    """
    检测买卖信号
    """
    # 支撑位买入信号（LONGCROSS(支撑1,C,2)）
    df['支撑1'] = df['支撑']
    condition_buy = (
        (df['支撑1'].shift(2) < df['收盘'].shift(2)) &
        (df['支撑1'].shift(1) < df['收盘'].shift(1)) &
        (df['支撑1'] > df['收盘'])
    )
    df['买入信号'] = condition_buy
    
    # 阻力位卖出信号（LONGCROSS(C,阻力,2)）
    condition_sell = (
        (df['收盘'].shift(2) < df['阻力'].shift(2)) &
        (df['收盘'].shift(1) < df['阻力'].shift(1)) &
        (df['收盘'] > df['阻力'])
    )
    df['卖出信号'] = condition_sell
    
    # 主力资金信号
    df['主力>大户'] = df['主力'] > df['大户']
    df['大户>散户'] = df['大户'] > df['散户']
    df['C>EXPMA20'] = df['收盘'] > df['收盘'].ewm(span=20, adjust=False).mean()
    df['EXPMA10>EXPMA20'] = df['收盘'].ewm(span=10, adjust=False).mean() > df['收盘'].ewm(span=20, adjust=False).mean()
    df['EXPMA20>EXPMA60'] = df['收盘'].ewm(span=20, adjust=False).mean() > df['收盘'].ewm(span=60, adjust=False).mean()
    df['主力=HHV30'] = df['主力'] == df['主力'].rolling(window=30).max()
    df['CROSS主力1.003'] = (df['主力'].shift(1) <= 1.003) & (df['主力'] > 1.003)
    
    # 主力资金流入信号
    df['主力资金流入'] = (
        df['主力>大户'] & df['大户>散户'] & df['C>EXPMA20'] & 
        df['EXPMA10>EXPMA20'] & df['EXPMA20>EXPMA60'] & 
        df['主力=HHV30'] & df['CROSS主力1.003']
    )
    
    # 改进：增加趋势确认机制，避免虚假信号
    # 计算短期均线和长期均线
    df['short_ma'] = df['收盘'].rolling(window=5, min_periods=1).mean()
    df['long_ma'] = df['收盘'].rolling(window=20, min_periods=1).mean()
    
    # 增加趋势过滤条件：买入信号需要短期均线上穿长期均线或处于上升趋势
    df['trend_filter_buy'] = (df['short_ma'] > df['long_ma']) | (df['short_ma'] > df['short_ma'].shift(1))
    
    # 增加趋势过滤条件：卖出信号需要短期均线下穿长期均线或处于下降趋势
    df['trend_filter_sell'] = (df['short_ma'] < df['long_ma']) | (df['short_ma'] < df['short_ma'].shift(1))
    
    # 应用趋势过滤器到买卖信号
    df['买入信号_filtered'] = df['买入信号'] & df['trend_filter_buy']
    df['卖出信号_filtered'] = df['卖出信号'] & df['trend_filter_sell']
    
    # 改进：收集所有信号而非仅第一次信号
    buy_signals = df[df['买入信号_filtered']]
    sell_signals = df[df['卖出信号_filtered']]
    
    print(f"量价指标：共检测到 {len(buy_signals)} 个买入信号和 {len(sell_signals)} 个卖出信号")
    
    for idx, row in buy_signals.iterrows():
        buy_time = idx
        buy_price = row['收盘']
        # 计算相对均线的涨跌幅
        if '均价' in df.columns:
            buy_avg_price = row['均价']
            if pd.notna(buy_avg_price) and buy_avg_price != 0:
                diff_pct = ((buy_price - buy_avg_price) / buy_avg_price) * 100
                print(f"量价指标：买入信号时间点: {buy_time.strftime('%Y-%m-%d %H:%M:%S')}, 价格: {buy_price:.2f}, 相对均线涨跌幅: {diff_pct:+.2f}%")
            else:
                print(f"量价指标：买入信号时间点: {buy_time.strftime('%Y-%m-%d %H:%M:%S')}, 价格: {buy_price:.2f}, 相对均线涨跌幅: N/A")
        else:
            print(f"量价指标：买入信号时间点: {buy_time.strftime('%Y-%m-%d %H:%M:%S')}, 价格: {buy_price:.2f}")
    
    for idx, row in sell_signals.iterrows():
        sell_time = idx
        sell_price = row['收盘']
        # 计算相对均线的涨跌幅
        if '均价' in df.columns:
            sell_avg_price = row['均价']
            if pd.notna(sell_avg_price) and sell_avg_price != 0:
                diff_pct = ((sell_price - sell_avg_price) / sell_avg_price) * 100
                print(f"量价指标：卖出信号时间点: {sell_time.strftime('%Y-%m-%d %H:%M:%S')}, 价格: {sell_price:.2f}, 相对均线涨跌幅: {diff_pct:+.2f}%")
            else:
                print(f"量价指标：卖出信号时间点: {sell_time.strftime('%Y-%m-%d %H:%M:%S')}, 价格: {sell_price:.2f}, 相对均线涨跌幅: N/A")
        else:
            print(f"量价指标：卖出信号时间点: {sell_time.strftime('%Y-%m-%d %H:%M:%S')}, 价格: {sell_price:.2f}")

    if len(buy_signals) == 0 and len(sell_signals) == 0:
        print("未检测到任何信号")

    return df


def plot_indicators(df, stock_code, trade_date, buy_ratio, sell_ratio, diff_ratio) -> str:
    """
    绘图量价指标图并返回图表保存路径
    """
    """
    绘图量价指标图
    """
    # 创建图形和子图
    fig = plt.figure(figsize=(16, 10))
    gs = fig.add_gridspec(3, 1, height_ratios=[1, 8, 1], hspace=0.1)
    
    ax_info = fig.add_subplot(gs[0])  # 顶部信息栏
    ax_price = fig.add_subplot(gs[1])  # 中部价格图
    ax_time = fig.add_subplot(gs[2])  # 底部时间轴
    
    # 顶部信息栏显示买卖比例
    ax_info.clear()
    ax_info.set_xlim(0, 1)
    ax_info.set_ylim(0, 1)
    ax_info.axis('off')
    
    info_text = f"买: {buy_ratio:.0f}%    卖: {sell_ratio:.0f}%    差: {diff_ratio:.0f}%"
    ax_info.text(0.5, 0.5, info_text, ha='center', va='center', fontsize=14, transform=ax_info.transAxes)
    
    # 使用数据点索引作为x轴坐标
    df_filtered = df.dropna(subset=['收盘'])
    x_values = list(range(len(df_filtered)))
    
    # 创建注释框用于鼠标悬浮显示
    annotation = ax_price.annotate('', xy=(0, 0), xytext=(10, 10), textcoords='offset points',
                                   bbox=dict(boxstyle='round', fc='yellow', alpha=0.7),
                                   arrowprops=dict(arrowstyle='->'), fontsize=10)
    annotation.set_visible(False)
    
    # 绘制收盘价曲线
    ax_price.plot(x_values, df_filtered['收盘'], marker='', linestyle='-', color='blue', linewidth=2, label='收盘价')
    
    # 绘制支撑线和阻力线
    ax_price.plot(x_values, df_filtered['支撑'], marker='', linestyle='--', color='magenta', linewidth=1, label='支撑')
    ax_price.plot(x_values, df_filtered['阻力'], marker='', linestyle='--', color='green', linewidth=1, label='阻力')
    ax_price.plot(x_values, df_filtered['章鱼底参考'], marker='', linestyle=':', color='blue', linewidth=1, label='章鱼底参考')
    
    # 绘制买入信号（红三角 + 红色文字 + 红色竖线）
    buy_signals = df_filtered[df_filtered['买入信号']].dropna()
    for idx in buy_signals.index:
        if idx in df_filtered.index:
            x_pos = df_filtered.index.get_loc(idx)
            ax_price.scatter(x_pos, buy_signals.loc[idx, '支撑'] * 0.999, marker='^', color='red', s=60, zorder=5)
            ax_price.text(x_pos, buy_signals.loc[idx, '支撑'] * 0.995, '买',
                          color='red', fontsize=10, ha='center', va='top', fontweight='bold')
            # 添加红色竖线
            ax_price.axvline(x=x_pos, color='red', linestyle='-', alpha=0.7, linewidth=2, zorder=3)
    
    # 绘制卖出信号（绿三角 + 绿色文字 + 绿色竖线）
    sell_signals = df_filtered[df_filtered['卖出信号']].dropna()
    for idx in sell_signals.index:
        if idx in df_filtered.index:
            x_pos = df_filtered.index.get_loc(idx)
            ax_price.scatter(x_pos, sell_signals.loc[idx, '阻力'] * 1.001, marker='v', color='green', s=60, zorder=5)
            ax_price.text(x_pos, sell_signals.loc[idx, '阻力'] * 1.002, '卖',
                          color='green', fontsize=10, ha='center', va='bottom', fontweight='bold')
            # 添加绿色竖线
            ax_price.axvline(x=x_pos, color='green', linestyle='-', alpha=0.7, linewidth=2, zorder=3)
    
    # 绘制主力资金流入信号
    fund_signals = df_filtered[df_filtered['主力资金流入']].dropna()
    for idx in fund_signals.index:
        if idx in df_filtered.index:
            x_pos = df_filtered.index.get_loc(idx)
            ax_price.scatter(x_pos, fund_signals.loc[idx, '收盘'] * 1.005, marker='*', color='purple', s=80, zorder=5)
    
    # 绘制精准线（底部支撑）
    precise_signals = df_filtered[df_filtered['精准左']].dropna()
    for idx in precise_signals.index:
        if idx in df_filtered.index:
            x_pos = df_filtered.index.get_loc(idx)
            support_val = precise_signals.loc[idx, '支撑']
            ax_price.plot([x_pos-2, x_pos+2], [support_val, support_val], color='magenta', linewidth=2)
    
    # 绘制精准线（顶部阻力）
    precise_signals1 = df_filtered[df_filtered['精准左1']].dropna()
    for idx in precise_signals1.index:
        if idx in df_filtered.index:
            x_pos = df_filtered.index.get_loc(idx)
            resistance_val = precise_signals1.loc[idx, '阻力']
            ax_price.plot([x_pos-2, x_pos+2], [resistance_val, resistance_val], color='cyan', linewidth=2)
    
    # 设置坐标轴标签
    ax_price.set_ylabel('价格', fontsize=12)
    
    # 设置网格
    ax_price.grid(True, linestyle='--', alpha=0.7)
    
    # 设置标题
    # 确保 trade_date 是正确的格式 (YYYY-MM-DD)
    if isinstance(trade_date, str):
        if '-' in trade_date:
            trade_date_formatted = trade_date
        else:
            trade_date_obj = datetime.strptime(trade_date, '%Y%m%d')
            trade_date_formatted = trade_date_obj.strftime('%Y-%m-%d')
    else:
        trade_date_formatted = trade_date.strftime('%Y-%m-%d')
        
    fig.suptitle(f'{stock_code} 量价指标 - {trade_date_formatted}', fontsize=14, y=0.98)
    
    # 添加图例
    ax_price.legend(loc='upper left', fontsize=10)
    
    # 设置x轴刻度
    total_points = len(df_filtered)
    if total_points > 0:
        step = max(1, total_points // 10)
        selected_indices = list(range(0, total_points, step))
        selected_times = df_filtered.index[selected_indices]
        
        ax_price.set_xticks(selected_indices)
        ax_price.set_xticklabels([t.strftime('%H:%M') if hasattr(t, 'strftime') else str(t) for t in selected_times])
        plt.setp(ax_price.get_xticklabels(), rotation=45, ha="right")
        
        # 底部时间轴
        ax_time.set_xlim(0, total_points - 1)
        ax_time.set_ylim(0, 1)
        ax_time.axis('off')
        ax_time.set_xticks(selected_indices)
        ax_time.set_xticklabels([t.strftime('%H:%M') if hasattr(t, 'strftime') else str(t) for t in selected_times])
    
    # 使用 constrained_layout 替代 tight_layout 来避免警告
    plt.rcParams['figure.constrained_layout.use'] = True
    
    # 保存图表到output目录
    output_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'output', 'charts')
    os.makedirs(output_dir, exist_ok=True)
    
    # 确保 trade_date 是正确的格式 (YYYY-MM-DD)
    if isinstance(trade_date, str):
        if '-' in trade_date:
            trade_date_formatted = trade_date
        else:
            trade_date_obj = datetime.strptime(trade_date, '%Y%m%d')
            trade_date_formatted = trade_date_obj.strftime('%Y-%m-%d')
    else:
        trade_date_formatted = trade_date.strftime('%Y-%m-%d')
        
    chart_filename = os.path.join(output_dir, f'{stock_code}_{trade_date_formatted}_量价指标.png')
    
    # 直接保存，覆盖同名文件
    plt.savefig(chart_filename, dpi=300, bbox_inches='tight', format='png')
    
    # 鼠标悬浮功能 - 修复_on_mouse_move方法
    def _on_mouse_move(event):
        if event.inaxes == ax_price:
            if event.xdata is not None:
                # 获取最近的整数索引
                x_index = int(round(event.xdata))
                # 确保索引在有效范围内
                if 0 <= x_index < len(df_filtered):
                    data_point = df_filtered.iloc[x_index]
                    time_str = df_filtered.index[x_index].strftime('%H:%M')
                    price = data_point['收盘']
                    
                    # 准备显示的文本内容
                    text_lines = [f"时间: {time_str}", f"价格: {price:.2f}"]
                    
                    # 添加其他可用的指标信息
                    if '支撑' in data_point and pd.notna(data_point['支撑']):
                        text_lines.append(f"支撑: {data_point['支撑']:.2f}")
                    if '阻力' in data_point and pd.notna(data_point['阻力']):
                        text_lines.append(f"阻力: {data_point['阻力']:.2f}")
                    if '量价' in data_point and pd.notna(data_point['量价']):
                        text_lines.append(f"量价: {data_point['量价']:.2f}")
                    
                    # 检查是否有信号
                    signal_text = []
                    if '买入信号' in data_point and data_point['买入信号']:
                        signal_text.append('买入信号')
                    if '卖出信号' in data_point and data_point['卖出信号']:
                        signal_text.append('卖出信号')
                    if '主力资金流入' in data_point and data_point['主力资金流入']:
                        signal_text.append('主力资金流入')
                    
                    if signal_text:
                        text_lines.append(f"信号: {', '.join(signal_text)}")
                    
                    # 更新注释框位置和内容
                    annotation.xy = (x_index, price)
                    annotation.set_text('\n'.join(text_lines))
                    annotation.set_visible(True)
                    fig.canvas.draw_idle()
                else:
                    if annotation.get_visible():
                        annotation.set_visible(False)
                        fig.canvas.draw_idle()
        else:
            if annotation.get_visible():
                annotation.set_visible(False)
                fig.canvas.draw_idle()
    
    # 连接鼠标移动事件
    fig.canvas.mpl_connect('motion_notify_event', _on_mouse_move)
    
    # 关闭图形以避免阻塞
    plt.close(fig)
    
    return fig


def analyze_volume_price(stock_code: str, trade_date: Optional[str] = None) -> Optional[pd.DataFrame]:
    """
    分析量价关系主函数
    
    Args:
        stock_code: 股票代码
        trade_date: 交易日期，格式为YYYY-MM-DD或YYYYMMDD，默认为今天
    
    Returns:
        包含分析结果的DataFrame，如果失败则返回None
    """
    try:
        import akshare as ak
        
        # 1. 时间处理
        # 如果没有提供交易日期，则使用今天的日期
        if trade_date is None:
            # 获取今天的日期
            today = datetime.now()
            trade_date = today.strftime('%Y-%m-%d')
        
        # 确保 trade_date 是正确的格式
        if isinstance(trade_date, str):
            if '-' in trade_date:
                trade_date_obj = datetime.strptime(trade_date, '%Y-%m-%d')
            else:
                trade_date_obj = datetime.strptime(trade_date, '%Y%m%d')
        else:
            trade_date_obj = trade_date
            
        # 格式化为 akshare 接口需要的日期格式
        trade_date_str = trade_date_obj.strftime('%Y%m%d')
        
        # 构造 akshare 需要的时间格式 (YYYY-MM-DD HH:MM:SS)
        start_time = f'{trade_date_obj.strftime("%Y-%m-%d")} 09:30:00'
        end_time = f'{trade_date_obj.strftime("%Y-%m-%d")} 15:00:00'

        # 2. 获取数据
        df = ak.stock_zh_a_hist_min_em(
            symbol=stock_code,
            period="1",
            start_date=start_time,
            end_date=end_time,
            adjust=''
        )
        
        if df.empty:
            print("❌ 无分时数据")
            return None
        
        # 重命名列以匹配我们的代码
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
        target_date = pd.to_datetime(trade_date_obj)
        df_original = df.copy()  # 保存原始数据
        df = df[df['时间'].dt.date == target_date.date()]
        
        # 过滤掉 11:30 到 13:00 之间的午休时间数据
        # 条件1: 排除11点30分及以后的数据
        # 条件2: 排除12点整的数据
        # 条件3: 排除13点前但不是11点的数据（即12点1分至12点59分）
        df = df[~(
            ((df['时间'].dt.hour == 11) & (df['时间'].dt.minute >= 30)) | 
            (df['时间'].dt.hour == 12) |
            ((df['时间'].dt.hour == 13) & (df['时间'].dt.minute < 0))
        )]

        if df.empty:
            print("❌ 所有时间数据均无效")
            return None
        
        # 分离上午和下午的数据
        morning_data = df[df['时间'].dt.hour < 12]
        afternoon_data = df[df['时间'].dt.hour >= 13]
        
        # 强制校准时间索引
        morning_index = pd.date_range(
            start=f"{trade_date_obj.strftime('%Y-%m-%d')} 09:30:00",
            end=f"{trade_date_obj.strftime('%Y-%m-%d')} 11:30:00",
            freq='1min'
        )
        afternoon_index = pd.date_range(
            start=f"{trade_date_obj.strftime('%Y-%m-%d')} 13:00:00",
            end=f"{trade_date_obj.strftime('%Y-%m-%d')} 15:00:00",
            freq='1min'
        )
        
        # 合并索引
        full_index = morning_index.union(afternoon_index)
        df = df.set_index('时间').reindex(full_index)
        df.index.name = '时间'
        
        try:
            from Investment.T0.utils.get_pre_close import get_prev_close
            prev_close = get_prev_close(stock_code, trade_date)
        except:
            prev_close = df['开盘'].dropna().iloc[0]
        
        # 填充缺失值
        df = df.ffill().bfill()
        
        # 计算各种指标
        df, buy_ratio, sell_ratio, diff_ratio = calculate_volume_price_indicators(df, prev_close)
        df = calculate_support_resistance(df, prev_close)
        df = calculate_fund_flow_indicators(df)
        df = calculate_precise_lines(df)
        df = detect_signals(df)
        
        # 绘图
        fig = plot_indicators(df, stock_code, trade_date, buy_ratio, sell_ratio, diff_ratio)
        
        return df
        
    except Exception as e:
        print(f"❌ 错误: {e}")
        import traceback
        traceback.print_exc()
        return None


def fetch_intraday_data(stock_code: str, trade_date: str) -> Optional[pd.DataFrame]:
    """
    获取股票分时数据
    
    Args:
        stock_code: 股票代码
        trade_date: 交易日期，格式为YYYY-MM-DD
    
    Returns:
        分时数据DataFrame，如果失败则返回None
    """
    try:
        # 构造 akshare 需要的时间格式
        trade_date_obj = datetime.strptime(trade_date, '%Y-%m-%d')
        start_time = f'{trade_date} 09:30:00'
        end_time = f'{trade_date} 15:00:00'

        # 获取数据
        df = ak.stock_zh_a_hist_min_em(
            symbol=stock_code,
            period="1",
            start_date=start_time,
            end_date=end_time,
            adjust=''  # 不复权
        )
        
        if df.empty:
            print(f"❌ {stock_code}在{trade_date}无分时数据")
            return None
        
        # 处理数据
        df = df.rename(columns={
            '时间': '时间',
            '开盘': '开盘',
            '收盘': '收盘',
            '最高': '最高',
            '最低': '最低',
            '成交量': '成交量',
            '成交额': '成交额'
        })
        
        # 转换时间列
        df['时间'] = pd.to_datetime(df['时间'], errors='coerce')
        df = df[df['时间'].notna()]
        
        # 过滤数据
        df = df[df['时间'].dt.date == trade_date_obj.date()]
        # 过滤掉 11:30 到 13:00 之间的午休时间数据
        # 条件1: 排除11点30分及以后的数据
        # 条件2: 排除12点整的数据
        # 条件3: 排除13点前但不是11点的数据（即12点1分至12点59分）
        df = df[~(
            ((df['时间'].dt.hour == 11) & (df['时间'].dt.minute >= 30)) | 
            (df['时间'].dt.hour == 12) |
            ((df['时间'].dt.hour == 13) & (df['时间'].dt.minute < 0))
        )]
        
        # 生成完整时间索引
        morning_index = pd.date_range(start=f"{trade_date} 09:30:00", end=f"{trade_date} 11:30:00", freq='1min')
        afternoon_index = pd.date_range(start=f"{trade_date} 13:00:00", end=f"{trade_date} 15:00:00", freq='1min')
        full_index = morning_index.union(afternoon_index)
        
        df = df.set_index('时间').reindex(full_index)
        df.index.name = '时间'
        df = df.ffill().bfill()
        
        return df
    except Exception as e:
        print(f"获取{stock_code}在{trade_date}的分时数据失败: {e}")
        return None

def detect_trading_signals(df: pd.DataFrame) -> Dict[str, Any]:
    """
    检测交易信号
    
    Args:
        df: 包含指标的DataFrame
    
    Returns:
        包含信号信息的字典
    """
    signals = {
        'buy_signals': df[df['买入信号_filtered']].index.tolist() if '买入信号_filtered' in df.columns else [],
        'sell_signals': df[df['卖出信号_filtered']].index.tolist() if '卖出信号_filtered' in df.columns else [],
        'fund_signals': df[df['主力资金流入']].index.tolist() if '主力资金流入' in df.columns else []
    }
    
    # 打印所有信号信息
    if signals['buy_signals']:
        for buy_signal in signals['buy_signals']:
            price = df.loc[buy_signal, '收盘']
            print(f"量价指标：买入信号时间点: {buy_signal.strftime('%Y-%m-%d %H:%M:%S')}, 价格: {price:.2f}")
    else:
        print("未检测到买入信号")
    
    if signals['sell_signals']:
        for sell_signal in signals['sell_signals']:
            price = df.loc[sell_signal, '收盘']
            print(f"量价指标：卖出信号时间点: {sell_signal.strftime('%Y-%m-%d %H:%M:%S')}, 价格: {price:.2f}")
    else:
        print("未检测到卖出信号")
    
    return signals

def main(stock_code: str = '000333', trade_date: Optional[str] = None) -> None:
    """
    主函数，用于独立运行生成量价指标图表
    
    Args:
        stock_code: 股票代码
        trade_date: 交易日期，格式为YYYY-MM-DD或YYYYMMDD，默认为今天
    """
    # 时间处理
    if trade_date is None:
        today = datetime.now()
        trade_date = today.strftime('%Y-%m-%d')
    
    # 标准化日期格式
    if isinstance(trade_date, str):
        if '-' not in trade_date:
            trade_date = datetime.strptime(trade_date, '%Y%m%d').strftime('%Y-%m-%d')
    
    print(f"开始分析{stock_code}在{trade_date}的量价指标")
    
    # 分析并绘图
    result_df = analyze_volume_price(stock_code, trade_date)
    
    if result_df is not None:
        print(f"图表已保存到{OUTPUT_DIR}目录")
    else:
        print("图表生成失败")

# 主程序入口
if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='量价指标分析工具')
    parser.add_argument('--code', type=str, default='000333', help='股票代码')
    parser.add_argument('--date', type=str, default=None, help='交易日期 (YYYY-MM-DD 或 YYYYMMDD)')
    
    args = parser.parse_args()
    main(stock_code=args.code, trade_date=args.date)
