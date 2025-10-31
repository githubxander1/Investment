#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
价格成交量偏离指标模块 (price_volume_deviation.py)

该模块实现了基于价格与均价偏离度、成交量分析的交易策略指标计算与分析功能，包括：
1. 价格与均价的偏离度计算（差值和百分比）
2. 成交量分析（5日均量和量比）
3. 基于偏离度和成交量的买卖信号生成
4. 策略回测与绩效分析
5. 可视化展示
6. 信号通知（系统通知和钉钉通知）

使用方法：
    可以调用calculate_price_volume_deviation计算指标，或使用analyze_strategy进行完整策略分析

作者: Assistant
创建日期: 2025-10-30
版本: 1.0
"""

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

from T0.utils.logger import setup_logger
from T0.utils.tools import notify_signal

logger = setup_logger('price_volume_deviation')

# 设置中文字体支持
plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False


def calculate_price_volume_deviation(df: pd.DataFrame, ma_period: int = 5) -> pd.DataFrame:
    """
    计算价格成交量偏离策略指标
    
    功能：计算股票价格与均价的偏离度、成交量分析，并生成相应的买卖信号
    
    策略原理：
    1. 计算价格与均价的差值和比率
    2. 计算成交量的5日均量和量比
    3. 当价格低于均价一定比例且成交量放大时买入
    4. 当价格高于均价一定比例且成交量放大或价格高于均价时卖出
    
    参数：
        df: 包含价格数据的DataFrame，需包含'收盘'、'均价'、'成交量'列
        ma_period: 均线周期，默认为5（5日均线）
    
    返回值：
        添加了策略指标的DataFrame，新增列包括：
        - 'Price_MA_Diff': 价格与均价的差值
        - 'Price_MA_Ratio': 价格与均价的偏离百分比
        - 'Volume_MA': 成交量5日均量
        - 'Volume_Ratio': 量比
        - 'Buy_Signal': 买入信号（布尔值）
        - 'Sell_Signal': 卖出信号（布尔值）
    """
    df = df.copy()
    
    # 确保数据类型正确
    df['收盘'] = pd.to_numeric(df['收盘'], errors='coerce')
    df['成交量'] = pd.to_numeric(df['成交量'], errors='coerce')
    if '成交额' in df.columns:
        df['成交额'] = pd.to_numeric(df['成交额'], errors='coerce')
    
    # 确保均价列存在
    if '均价' not in df.columns:
        # 如果没有均价列，使用成交额/成交量计算（考虑到VOL单位为手，乘以100转换为股）
        df['均价'] = df['成交额'] / (df['成交量'] * 100)
        logger.info("使用成交额/成交量计算均价")
    
    # 确保均价数据类型正确
    df['均价'] = pd.to_numeric(df['均价'], errors='coerce')
    
    # 检查是否有有效的数据
    if df[['收盘', '均价']].isnull().all().all():
        logger.warning("收盘价和均价数据全部为空，无法计算指标")
        # 添加空的指标列
        df['Price_MA_Diff'] = np.nan
        df['Price_MA_Ratio_Amplified'] = np.nan
        df['Price_MA_Ratio'] = np.nan
        df['Volume_MA'] = np.nan
        df['Volume_Ratio'] = np.nan
        df['Volume_Increase'] = False
        df['Volume_Decrease'] = False
        df['Buy_Signal'] = False
        df['Sell_Signal'] = False
        df['Price_Change_Rate'] = 0.0
        return df
    
    # 处理NaN值，使用前向填充 (修复pandas FutureWarning)
    df['收盘'] = df['收盘'].ffill()
    df['均价'] = df['均价'].ffill()
    
    # 再次检查填充后是否还有有效数据
    if df[['收盘', '均价']].isnull().all().all():
        logger.warning("填充后收盘价和均价数据仍然全部为空，无法计算指标")
        # 添加空的指标列
        df['Price_MA_Diff'] = np.nan
        df['Price_MA_Ratio_Amplified'] = np.nan
        df['Price_MA_Ratio'] = np.nan
        df['Volume_MA'] = np.nan
        df['Volume_Ratio'] = np.nan
        df['Volume_Increase'] = False
        df['Volume_Decrease'] = False
        df['Buy_Signal'] = False
        df['Sell_Signal'] = False
        df['Price_Change_Rate'] = 0.0
        return df
    
    # 检查是否有无穷大值
    df.replace([np.inf, -np.inf], np.nan, inplace=True)
    
    # 计算价格与均价的差值和比率（偏离度）
    df['Price_MA_Diff'] = df['收盘'] - df['均价']
    # 计算价格与均价的偏离百分比
    df['Price_MA_Ratio'] = (df['收盘'] / df['均价'] - 1) * 100
    # 为图表显示创建放大版本（不改变实际数据）
    df['Price_MA_Ratio_Scaled'] = df['Price_MA_Ratio'] * 10
    
    # 计算成交量移动平均和量比
    df['Volume_MA'] = df['成交量'].rolling(window=5, min_periods=1).mean()
    df['Volume_Ratio'] = df['成交量'] / df['Volume_MA']
    
    # 处理可能的无穷大值
    df['Volume_Ratio'] = df['Volume_Ratio'].replace([np.inf, -np.inf], np.nan)
    
    # 成交量分析
    df['Volume_Increase'] = df['Volume_Ratio'] > 1.5  # 成交量放大
    df['Volume_Decrease'] = df['Volume_Ratio'] < 0.5  # 成交量萎缩
    
    # 策略参数（调整阈值以便更容易产生信号）
    buy_threshold = -0.3  # 低于均价0.3%时买入
    sell_threshold = 0.3  # 高于均价0.3%时卖出
    
    # 生成买卖信号
    # 买入信号：偏离度 < 阈值 且 成交量放大
    df['Buy_Signal'] = (df['Price_MA_Ratio'] < buy_threshold) & (df['Volume_Ratio'] > 1.2)
    
    # 卖出信号：偏离度 > 阈值 且 (成交量放大 或 收盘价 > 均价)
    df['Sell_Signal'] = (df['Price_MA_Ratio'] > sell_threshold) & (
        (df['Volume_Ratio'] > 1.2) | (df['收盘'] > df['均价'])
    )
    
    # 添加涨跌幅计算
    df['Price_Change_Rate'] = df['收盘'].pct_change() * 100
    df['Price_Change_Rate'] = df['Price_Change_Rate'].fillna(0)
    
    # 添加详细日志，显示各列的统计信息
    valid_price_ma_ratio = df['Price_MA_Ratio'].dropna()
    valid_volume_ratio = df['Volume_Ratio'].dropna()
    
    logger.info(f"价格成交量偏离策略：共检测到 {len(df[df['Buy_Signal']])} 个买入信号和 {len(df[df['Sell_Signal']])} 个卖出信号")
    logger.info(f"Price_MA_Ratio统计信息：")
    if len(valid_price_ma_ratio) > 0:
        logger.info(f"- 最大值: {valid_price_ma_ratio.max():.4f}%")
        logger.info(f"- 最小值: {valid_price_ma_ratio.min():.4f}%")
        logger.info(f"- 平均值: {valid_price_ma_ratio.mean():.4f}%")
    else:
        logger.info("- 无有效数据")
        
    logger.info(f"Volume_Ratio统计信息：")
    if len(valid_volume_ratio) > 0:
        logger.info(f"- 最大值: {valid_volume_ratio.max():.4f}")
        logger.info(f"- 最小值: {valid_volume_ratio.min():.4f}")
        logger.info(f"- 平均值: {valid_volume_ratio.mean():.4f}")
    else:
        logger.info("- 无有效数据")
    
    # 显示前几行的详细数据用于调试
    logger.info("\n前5行数据示例：")
    if not df.empty:
        # 选择关键列显示
        key_columns = ['收盘', '均价', 'Price_MA_Diff', 'Price_MA_Ratio', '成交量', 'Volume_MA', 'Volume_Ratio', 'Buy_Signal', 'Sell_Signal']
        display_columns = [col for col in key_columns if col in df.columns]
        logger.info(f"\n{df[display_columns].head()}")
    
    return df







def plot_strategy_chart(stock_code: str, trade_date: Optional[str] = None, df: Optional[pd.DataFrame] = None) -> Optional[str]:
    """
    绘制价格成交量偏离策略图表
    
    Args:
        stock_code: 股票代码
        trade_date: 交易日期
        df: 数据DataFrame
    
    Returns:
        图表保存路径
    """
    try:
        # 时间处理
        if trade_date is None:
            yesterday = datetime.now() - timedelta(days=1)
            trade_date = yesterday.strftime('%Y-%m-%d')
        
        # 统一日期格式，确保与其他函数保持一致
        try:
            trade_date_obj = datetime.strptime(trade_date, '%Y%m%d')
            formatted_date = trade_date_obj.strftime('%Y-%m-%d')
            date_for_data = trade_date  # 保持原始格式用于数据获取
        except ValueError:
            try:
                trade_date_obj = datetime.strptime(trade_date, '%Y-%m-%d')
                formatted_date = trade_date
                date_for_data = trade_date_obj.strftime('%Y%m%d')
            except ValueError:
                print(f"错误: 无法解析日期格式: {trade_date}")
                return None
        
        # 获取数据
        if df is None:
            df = fetch_intraday_data(stock_code, date_for_data)
        if df is None or df.empty:
            return None
        
        # 设置时间索引
        df = df.copy()
        if '时间' in df.columns:
            df['时间'] = pd.to_datetime(df['时间'])
            df = df.set_index('时间')
        
        # 计算指标
        df_with_indicators = calculate_price_volume_deviation(df)
        
        # 确保必要列存在且不为空
        required_columns = ['Price_MA_Ratio', 'Volume_Ratio']
        for col in required_columns:
            if col not in df_with_indicators.columns:
                print(f"警告: 数据中没有{col}列")
                return None
        
        # 创建图形和子图
        fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(16, 12), gridspec_kw={'height_ratios': [3, 1, 1]})
        fig.suptitle(f'{stock_code} 价均量策略图 ({formatted_date})', fontsize=16)
        
        # 启用交互模式
        plt.ion()
        fig.canvas.manager.set_window_title(f'{stock_code} 价均量策略图')
        
        # 过滤掉无效数据
        df_filtered = df_with_indicators.dropna(subset=['收盘', '均价', 'Price_MA_Ratio', 'Volume_Ratio'])
        
        # 移除非交易时间（11:30到13:00）
        # 创建一个布尔索引，排除午间休市时间
        morning_end = pd.Timestamp('11:30').time()
        afternoon_start = pd.Timestamp('13:00').time()
        mask = ~((df_filtered.index.time >= morning_end) & 
                (df_filtered.index.time < afternoon_start))
        df_filtered = df_filtered[mask]
        
        if df_filtered.empty:
            print("警告: 过滤后的数据为空")
            return None
            
        print(f"过滤后的数据行数: {len(df_filtered)}")
        print(f"数据列: {', '.join(df_filtered.columns.tolist())}")
        
        # 绘制价格和均价
        ax1.plot(df_filtered.index, df_filtered['收盘'], label='收盘价', color='black', linewidth=1)
        ax1.plot(df_filtered.index, df_filtered['均价'], label='均价', color='blue', linewidth=1)
        
        # 绘制买入信号
        buy_signals = df_filtered[df_filtered['Buy_Signal']]
        if not buy_signals.empty:
            ax1.scatter(buy_signals.index, buy_signals['收盘'] * 0.995, marker='^', color='red', s=100, zorder=5)
            for idx, row in buy_signals.iterrows():
                ax1.text(idx, row['收盘'] * 0.99, '买',
                         color='red', fontsize=12, ha='center', va='top', fontweight='bold')
        
        # 绘制卖出信号
        sell_signals = df_filtered[df_filtered['Sell_Signal']]
        if not sell_signals.empty:
            ax1.scatter(sell_signals.index, sell_signals['收盘'] * 1.005, marker='v', color='green', s=100, zorder=5)
            for idx, row in sell_signals.iterrows():
                ax1.text(idx, row['收盘'] * 1.01, '卖',
                         color='green', fontsize=12, ha='center', va='bottom', fontweight='bold')
        
        ax1.set_ylabel('价格', fontsize=12)
        ax1.grid(True, linestyle='--', alpha=0.7)
        ax1.legend()
        
        # 绘制价格与均价的比率
        ax2.plot(df_filtered.index, df_filtered['Price_MA_Ratio'], label='价格与均价偏离比率(%)', color='purple', linewidth=1)
        ax2.plot(df_filtered.index, df_filtered['Price_MA_Ratio_Scaled'], label='偏离比率(放大10倍显示)', color='orange', linewidth=1)
        ax2.axhline(y=0, color='black', linestyle='-', alpha=0.5)
        ax2.axhline(y=0.5, color='green', linestyle='--', alpha=0.7, label='卖出阈值')
        ax2.axhline(y=-0.5, color='red', linestyle='--', alpha=0.7, label='买入阈值')
        ax2.set_ylabel('偏离比率(%)', fontsize=12)
        ax2.grid(True, linestyle='--', alpha=0.7)
        ax2.legend()
        
        # 绘制量比
        ax3.plot(df_filtered.index, df_filtered['Volume_Ratio'], label='量比', color='brown', linewidth=1)
        ax3.axhline(y=1.5, color='green', linestyle='--', alpha=0.7, label='放量阈值')
        ax3.axhline(y=0.5, color='red', linestyle='--', alpha=0.7, label='缩量阈值')
        ax3.axhline(y=1.0, color='gray', linestyle='-', alpha=0.5)
        ax3.set_ylabel('量比', fontsize=12)
        ax3.set_xlabel('时间', fontsize=12)
        ax3.grid(True, linestyle='--', alpha=0.7)
        ax3.legend()
        
        # 格式化x轴时间显示
        import matplotlib.dates as mdates
        ax1.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
        ax2.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
        ax3.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
        plt.setp(ax1.xaxis.get_majorticklabels(), rotation=45)
        plt.setp(ax2.xaxis.get_majorticklabels(), rotation=45)
        plt.setp(ax3.xaxis.get_majorticklabels(), rotation=45)
        
        # 添加鼠标悬停显示功能
        annot = ax1.annotate('', xy=(0, 0), xytext=(20, 20), textcoords='offset points',
                            bbox=dict(boxstyle='round', fc='yellow', alpha=0.7),
                            arrowprops=dict(arrowstyle='->'))
        annot.set_visible(False)
        
        def on_move(event):
            if event.inaxes and len(df_filtered) > 0:
                # 获取最近的数据点
                x_data = df_filtered.index
                try:
                    # 找到最近的时间点
                    nearest_index = abs(x_data - pd.Timestamp(event.xdata).to_pydatetime()).argmin()
                    nearest_time = x_data[nearest_index]
                    row = df_filtered.loc[nearest_time]
                    
                    # 构建显示信息
                    time_str = nearest_time.strftime('%H:%M')
                    price_str = f'{row["收盘"]:.2f}'
                    avg_price_str = f'{row["均价"]:.2f}'
                    ratio_str = f'{row["Price_MA_Ratio"]:.2f}%'
                    volume_ratio_str = f'{row["Volume_Ratio"]:.2f}'
                    
                    info = f'时间: {time_str}\n收盘价: {price_str}\n均价: {avg_price_str}\n偏离率: {ratio_str}\n量比: {volume_ratio_str}'
                    
                    # 更新注释框位置和文本
                    annot.xy = (pd.Timestamp(nearest_time), row["收盘"])
                    annot.set_text(info)
                    annot.set_visible(True)
                    fig.canvas.draw_idle()
                except Exception as e:
                    annot.set_visible(False)
                    fig.canvas.draw_idle()
            else:
                annot.set_visible(False)
                fig.canvas.draw_idle()
        
        # 连接鼠标移动事件
        fig.canvas.mpl_connect('motion_notify_event', on_move)
        
        # 调整布局
        plt.tight_layout()
        
        # 保存图表
        output_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'output', 'charts')
        os.makedirs(output_dir, exist_ok=True)
        chart_path = os.path.join(output_dir, f'{stock_code}_price_volume_deviation_{formatted_date.replace("-", "")}.png')
        plt.savefig(chart_path, dpi=300, bbox_inches='tight')
        
        # 显示图表窗口（阻塞模式，直到用户关闭窗口）
        plt.ioff()  # 关闭交互模式
        plt.show()
        
        print(f"📈 图表已保存至: {chart_path}")
        return chart_path
        
    except Exception as e:
        print(f"❌ 绘图失败: {e}")
        import traceback
        traceback.print_exc()
        return None


def analyze_strategy(stock_code: str, trade_date: Optional[str] = None) -> Optional[Tuple[pd.DataFrame, Dict[str, List[Tuple[datetime, float]]]]]:
    """
    价格成交量偏离策略分析主函数
    
    Args:
        stock_code: 股票代码
        trade_date: 交易日期
    
    Returns:
        (数据框, 信号字典) 或 None
    """
    try:
        # 时间处理 - 与系统其他部分保持一致，使用'%Y%m%d'格式
        if trade_date is None:
            # yesterday = datetime.now() - timedelta(days=1)
            # trade_date = yesterday.strftime('%Y%m%d')

            trade_date = datetime.now().strftime('%Y%m%d')

        # 获取数据
        df = fetch_intraday_data(stock_code, trade_date)
        if df is None or df.empty:
            return None
        
        # 设置时间索引
        df = df.copy()
        if '时间' in df.columns:
            df['时间'] = pd.to_datetime(df['时间'])
            df = df.set_index('时间')
        
        # 计算指标
        df_with_indicators = calculate_price_volume_deviation(df)
        
        # 检测信号
        signals = detect_trading_signals(df_with_indicators)
        
        return df_with_indicators, signals
        
    except Exception as e:
        print(f"❌ 分析失败: {e}")
        import traceback
        traceback.print_exc()
        return None


if __name__ == "__main__":
    # 测试代码
    stock_code = "600030"  # 中信证券
    trade_date = '20251031'
    
    result = analyze_strategy(stock_code, trade_date)
    if result:
        df_with_indicators, signals = result
        print(f"📊 检测到 {len(signals['buy_signals'])} 个买入信号和 {len(signals['sell_signals'])} 个卖出信号")

        # 绘制图表
        plot_strategy_chart(stock_code, trade_date)