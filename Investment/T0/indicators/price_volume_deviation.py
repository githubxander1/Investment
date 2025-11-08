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
from datetime import datetime
from typing import Optional, Tuple, Dict, List
import os
import sys

# 添加项目根目录到Python路径
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, project_root)

# 尝试导入模块，如果失败则使用本地路径
from Investment.T0.utils.intraday_data_provider import IntradayDataProvider
from Investment.T0.utils.logger import setup_logger
from Investment.T0.utils.notification import send_notification
from Investment.T0.utils.detact_signals import detect_trading_signals

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
    2. 计算成交量的15分钟均量和量比（关键修改：用ROUND保留2位小数）
    3. 当价格低于均价一定比例且成交量放大时买入
    4. 当价格高于均价一定比例且成交量放大或价格高于均价时卖出
    
    参数：
        df: 包含价格数据的DataFrame，需包含'收盘'、'均价'、'成交量'列
        ma_period: 均线周期，默认为5（5日均线）
    
    返回值：
        添加了策略指标的DataFrame，新增列包括：
        - 'Price_MA_Diff': 价格与均价的差值
        - 'Price_MA_Ratio': 价格与均价的偏离百分比
        - 'Volume_MA': 成交量15分钟均量
        - 'Volume_Ratio': 量比（保留2位小数）
        - 'Buy_Signal': 买入信号（布尔值）
        - 'Sell_Signal': 卖出信号（布尔值）
    """
    if df is None or df.empty:
        logger.warning("[重复日志修复] 输入数据为空，无法计算指标")
        return df
    
    df = df.copy()
    
    # 确保数据类型正确
    df['收盘'] = pd.to_numeric(df['收盘'], errors='coerce')
    df['成交量'] = pd.to_numeric(df['成交量'], errors='coerce')
    if '成交额' in df.columns:
        df['成交额'] = pd.to_numeric(df['成交额'], errors='coerce')
    
    # 确保均价列存在（修正单位转换问题确保计算准确性）
    if '均价' not in df.columns:
        # 如果没有均价列，使用成交额/成交量计算（考虑到VOL单位为手，乘以100转换为股）
        df['均价'] = df['成交额'] / (df['成交量'] * 100)
        logger.info("[重复日志修复] 使用成交额/成交量计算均价")
    
    # 确保均价数据类型正确
    df['均价'] = pd.to_numeric(df['均价'], errors='coerce')
    
    # 检查数据是否全部为空
    if df[['收盘', '均价', '成交量']].isnull().all().all():
        logger.warning("[重复日志修复] 关键数据列全部为空，无法计算指标")
        # 添加空的指标列
        df['Price_MA_Diff'] = np.nan
        df['Price_MA_Ratio'] = np.nan
        df['Price_MA_Ratio_Amplified'] = np.nan
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
    df['成交量'] = df['成交量'].ffill()
    
    # 再次检查填充后是否还有有效数据
    if df[['收盘', '均价']].isnull().all().all():
        logger.warning("[重复日志修复] 填充后收盘价和均价数据仍然全部为空，无法计算指标")
        # 添加空的指标列
        df['Price_MA_Diff'] = np.nan
        df['Price_MA_Ratio'] = np.nan
        df['Price_MA_Ratio_Amplified'] = np.nan
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
    
    # 处理均价为0的情况
    df.loc[df['均价'] == 0, '均价'] = np.nan
    
    # 再次填充NaN值
    df['收盘'] = df['收盘'].ffill().bfill()
    df['均价'] = df['均价'].ffill().bfill()
    df['成交量'] = df['成交量'].ffill().bfill()
    
    # 检查是否有有效的数据对
    valid_data = df[['收盘', '均价']].dropna()
    if valid_data.empty:
        logger.warning("[重复日志修复] 没有有效的收盘价和均价数据对，无法计算指标")
        # 添加空的指标列
        df['Price_MA_Diff'] = np.nan
        df['Price_MA_Ratio'] = np.nan
        df['Price_MA_Ratio_Amplified'] = np.nan
        df['Volume_MA'] = np.nan
        df['Volume_Ratio'] = np.nan
        df['Volume_Increase'] = False
        df['Volume_Decrease'] = False
        df['Buy_Signal'] = False
        df['Sell_Signal'] = False
        df['Price_Change_Rate'] = 0.0
        return df
    
    # 计算价格与均价的差值和比率（偏离度）{反映当前价与均价的偏离程度}
    df['Price_MA_Diff'] = df['收盘'] - df['均价']
    # 偏离度:(CLOSE-均价)/均价*100.00;{结果为百分比，保留2位小数}
    df['Price_MA_Ratio'] = (df['收盘'] / df['均价'] - 1) * 100
    
    # 为图表显示创建放大版本（偏离度放大显示 - 增强视觉辨识度）
    # 偏离度放大:偏离度*50,COLORRED,LINETHICK4;{红色粗线绘制，突出偏离趋势}
    df['Price_MA_Ratio_Amplified'] = df['Price_MA_Ratio'] * 50
    
    # 成交量分析 - 量比改为【数值显示】（关键修改：用ROUND保留2位小数，避免分数）
    # VOLUME_5MA := MA(VOL, 15);{计算15分钟成交量均线（分时图中即5个时间单位的平均成交量）}
    df['Volume_MA'] = df['成交量'].rolling(window=15, min_periods=1).mean()
    # 量比数值 := ROUND((VOL / VOLUME_5MA) * 100) / 100;{核心修改：用ROUND保留2位小数，强制数值显示}
    df['Volume_Ratio'] = np.round((df['成交量'] / df['Volume_MA']) * 100) / 100
    
    # 处理可能的无穷大值
    df['Volume_Ratio'] = df['Volume_Ratio'].replace([np.inf, -np.inf], np.nan)
    
    # 成交量分析
    # 成交量放大:= 量比数值 > 1.5;{量比大于1.5判定为放量}
    df['Volume_Increase'] = df['Volume_Ratio'] > 1.5
    # 成交量萎缩:= 量比数值 < 0.5;{量比小于0.5判定为缩量}
    df['Volume_Decrease'] = df['Volume_Ratio'] < 0.5
    
    # 策略参数
    buy_threshold = -0.3  # 低于均价0.3%时买入
    sell_threshold = 0.3  # 高于均价0.3%时卖出
    
    # 生成买卖信号
    # 买入信号 := 偏离度 < -0.3 AND 成交量放大;{当前价低于均价0.3%+放量，触发买入信号}
    df['Buy_Signal'] = (df['Price_MA_Ratio'] < buy_threshold) & (df['Volume_Increase'])
    
    # 卖出信号 := 偏离度 > 0.3 AND (成交量放大 OR CLOSE > 均价);{当前价高于均价0.3%+放量/价超均价，触发卖出信号}
    df['Sell_Signal'] = (df['Price_MA_Ratio'] > sell_threshold) & (
        (df['Volume_Increase']) | (df['收盘'] > df['均价'])
    )
    
    # 添加涨跌幅计算
    # 涨跌幅:(CLOSE-REF(CLOSE,1))/REF(CLOSE,1)*100,COLORRED,LINETHICK1;{红色细线显示涨跌幅（百分比）}
    df['Price_Change_Rate'] = df['收盘'].pct_change(fill_method=None) * 100
    df['Price_Change_Rate'] = df['Price_Change_Rate'].fillna(0)
    
    # 添加详细日志，显示各列的统计信息
    valid_price_ma_ratio = df['Price_MA_Ratio'].dropna()
    valid_volume_ratio = df['Volume_Ratio'].dropna()
    
    logger.info("[重复日志修复] 价格成交量偏离策略：共检测到 {} 个买入信号和 {} 个卖出信号".format(
        len(df[df['Buy_Signal']]), len(df[df['Sell_Signal']])))
    logger.info("[重复日志修复] Price_MA_Ratio统计信息：")
    if len(valid_price_ma_ratio) > 0:
        logger.info("[重复日志修复] - 最大值: {:.4f}%".format(valid_price_ma_ratio.max()))
        logger.info("[重复日志修复] - 最小值: {:.4f}%".format(valid_price_ma_ratio.min()))
        logger.info("[重复日志修复] - 平均值: {:.4f}%".format(valid_price_ma_ratio.mean()))
    else:
        logger.info("[重复日志修复] - 无有效数据")
        
    logger.info("[重复日志修复] Volume_Ratio统计信息：")
    if len(valid_volume_ratio) > 0:
        logger.info("[重复日志修复] - 最大值: {:.4f}".format(valid_volume_ratio.max()))
        logger.info("[重复日志修复] - 最小值: {:.4f}".format(valid_volume_ratio.min()))
        logger.info("[重复日志修复] - 平均值: {:.4f}".format(valid_volume_ratio.mean()))
    else:
        logger.info("[重复日志修复] - 无有效数据")
    
    # 显示前几行的详细数据用于调试
    logger.info("[重复日志修复] 前5行数据示例：")
    if not df.empty:
        # 选择关键列显示
        key_columns = ['收盘', '均价', 'Price_MA_Diff', 'Price_MA_Ratio', '成交量', 'Volume_MA', 'Volume_Ratio', 'Buy_Signal', 'Sell_Signal']
        display_columns = [col for col in key_columns if col in df.columns]
        logger.info("\n{}".format(df[display_columns].head()))
    
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
            # yesterday = datetime.now() - timedelta(days=1)
            # trade_date = yesterday.strftime('%Y-%m-%d')
            trade_date = datetime.now().strftime('%Y-%m-%d')
        
        # # 统一日期格式，确保与其他函数保持一致
        # try:
        #     trade_date_obj = datetime.strptime(trade_date, '%Y%m%d')
        #     formatted_date = trade_date_obj.strftime('%Y-%m-%d')
        #     date_for_data = trade_date  # 保持原始格式用于数据获取
        # except ValueError:
        #     try:
        #         trade_date_obj = datetime.strptime(trade_date, '%Y-%m-%d')
        #         formatted_date = trade_date
        #         date_for_data = trade_date_obj.strftime('%Y%m%d')
        #     except ValueError:
        #         print(f"错误: 无法解析日期格式: {trade_date}")
        #         return None
        
        # 获取数据
        if df is None:
            provider = IntradayDataProvider()
            df = provider.get_intraday_data(stock_code, trade_date)
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
        required_columns = ['Price_MA_Ratio', 'Volume_Ratio', 'Price_MA_Ratio_Amplified']
        for col in required_columns:
            if col not in df_with_indicators.columns:
                print(f"警告: 数据中没有{col}列")
                return None
        
        # 创建图形和子图
        fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(16, 12), gridspec_kw={'height_ratios': [3, 1, 1]})
        fig.suptitle(f'{stock_code} 价均量策略图 ({trade_date})', fontsize=16)
        
        # 启用交互模式
        plt.ion()
        fig.canvas.manager.set_window_title(f'{stock_code} 价均量策略图')
        
        # 过滤掉无效数据
        df_filtered = df_with_indicators.dropna(subset=['收盘', '均价', 'Price_MA_Ratio', 'Volume_Ratio'])
        
        # 移除非交易时间（11:30到13:00）
        # 创建一个布尔索引，完全排除午间休市时间
        morning_end = pd.Timestamp('11:30').time()
        afternoon_start = pd.Timestamp('13:00').time()
        # 完全排除11:30到13:00之间的所有数据
        mask = ~((df_filtered.index.time >= morning_end) & 
                (df_filtered.index.time < afternoon_start))
        df_filtered = df_filtered[mask]
        
        # 确保过滤彻底，打印过滤前后的数据量
        print(f"午休时间过滤前数据行数: {len(df_with_indicators)}")
        print(f"午休时间过滤后数据行数: {len(df_filtered)}")
        
        if df_filtered.empty:
            print("警告: 过滤后的数据为空")
            return None
            
        print(f"过滤后的数据行数: {len(df_filtered)}")
        print(f"数据列: {', '.join(df_filtered.columns.tolist())}")
        
        # 绘制价格和均价，在上午收盘和下午开盘之间创建断点
        # 分离上午和下午的数据
        morning_data = df_filtered[df_filtered.index.time < morning_end]
        afternoon_data = df_filtered[df_filtered.index.time >= afternoon_start]
        
        # 分别绘制上午和下午的数据，避免在午休时间绘制连线
        if not morning_data.empty:
            ax1.plot(morning_data.index, morning_data['收盘'], label='收盘价' if not ax1.get_lines() else '', color='black', linewidth=1)
            ax1.plot(morning_data.index, morning_data['均价'], label='均价' if not ax1.get_lines() else '', color='blue', linewidth=1)
        
        if not afternoon_data.empty:
            ax1.plot(afternoon_data.index, afternoon_data['收盘'], color='black', linewidth=1)
            ax1.plot(afternoon_data.index, afternoon_data['均价'], color='blue', linewidth=1)
        
        # 绘制买入信号
        buy_signals = df_filtered[df_filtered['Buy_Signal']]
        if not buy_signals.empty:
            # DRAWICON(买入信号, 偏离度放大-1, 1);{买入信号：红色向上箭头（位置微调，避免遮挡）}
            ax1.scatter(buy_signals.index, buy_signals['收盘'] * 0.995, marker='^', color='red', s=100, zorder=5)
            for idx, row in buy_signals.iterrows():
                ax1.text(idx, row['收盘'] * 0.99, '买',
                         color='red', fontsize=12, ha='center', va='top', fontweight='bold')
        
        # 绘制卖出信号
        sell_signals = df_filtered[df_filtered['Sell_Signal']]
        if not sell_signals.empty:
            # DRAWICON(卖出信号, 偏离度放大+1, 2);{卖出信号：绿色向下箭头（位置微调，避免遮挡）}
            ax1.scatter(sell_signals.index, sell_signals['收盘'] * 1.005, marker='v', color='green', s=100, zorder=5)
            for idx, row in sell_signals.iterrows():
                ax1.text(idx, row['收盘'] * 1.01, '卖',
                         color='green', fontsize=12, ha='center', va='bottom', fontweight='bold')
        
        ax1.set_ylabel('价格', fontsize=12)
        ax1.grid(True, linestyle='--', alpha=0.7)
        ax1.legend()
        
        # 绘制价格与均价的比率，在上午收盘和下午开盘之间创建断点
        # 偏离度放大:偏离度*50,COLORRED,LINETHICK4;{红色粗线绘制，突出偏离趋势}
        if not morning_data.empty:
            ax2.plot(morning_data.index, morning_data['Price_MA_Ratio_Amplified'], 
                    label='偏离度放大(偏离度*50)' if not ax2.get_lines() else '', color='red', linewidth=2)
        if not afternoon_data.empty:
            ax2.plot(afternoon_data.index, afternoon_data['Price_MA_Ratio_Amplified'], 
                    color='red', linewidth=2)
        ax2.axhline(y=0, color='black', linestyle='-', alpha=0.5)
        ax2.axhline(y=15, color='green', linestyle='--', alpha=0.7, label='卖出阈值')
        ax2.axhline(y=-15, color='red', linestyle='--', alpha=0.7, label='买入阈值')
        ax2.set_ylabel('偏离度放大值', fontsize=12)
        ax2.grid(True, linestyle='--', alpha=0.7)
        ax2.legend()
        
        # 绘制量比，在上午收盘和下午开盘之间创建断点
        # 量比:量比数值,COLORGREEN,LINETHICK1;{绿色细线显示量比，格式为XX.XX（如1.85、0.42）}
        if not morning_data.empty:
            ax3.plot(morning_data.index, morning_data['Volume_Ratio'], 
                    label='量比' if not ax3.get_lines() else '', color='green', linewidth=1)
        if not afternoon_data.empty:
            ax3.plot(afternoon_data.index, afternoon_data['Volume_Ratio'], 
                    color='green', linewidth=1)
        ax3.axhline(y=1.5, color='green', linestyle='--', alpha=0.7, label='放量阈值')
        ax3.axhline(y=0.5, color='red', linestyle='--', alpha=0.7, label='缩量阈值')
        ax3.axhline(y=1.0, color='gray', linestyle='-', alpha=0.5)
        ax3.set_ylabel('量比', fontsize=12)
        ax3.set_xlabel('时间', fontsize=12)
        ax3.grid(True, linestyle='--', alpha=0.7)
        ax3.legend()
        
        # 格式化x轴时间显示
        import matplotlib.dates as mdates
        
        # 为所有子图设置相同的x轴格式和范围
        for ax in [ax1, ax2, ax3]:
            ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
            # 优化x轴刻度，确保不显示午休时间段
            ax.xaxis.set_major_locator(mdates.MinuteLocator(byminute=[0, 15, 30, 45]))
        
        plt.setp(ax1.xaxis.get_majorticklabels(), rotation=45)
        plt.setp(ax2.xaxis.get_majorticklabels(), rotation=45)
        plt.setp(ax3.xaxis.get_majorticklabels(), rotation=45)
        
        
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
        # 先清除之前的绘图，重新绘制
        for ax in [ax1, ax2, ax3]:
            ax.clear()
        
        # 重新设置标题和标签
        fig.suptitle(f'{stock_code} 价均量策略图 ({trade_date})', fontsize=16)
        
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
            buy_morning = buy_signals[buy_signals.index.time < morning_end]
            buy_afternoon = buy_signals[buy_signals.index.time >= afternoon_start]
            
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
            sell_morning = sell_signals[sell_signals.index.time < morning_end]
            sell_afternoon = sell_signals[sell_signals.index.time >= afternoon_start]
            
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
        
        # 计算新的x轴范围
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
        
        # 设置x轴时间格式
        for ax in [ax1, ax2, ax3]:
            ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
            ax.xaxis.set_major_locator(mdates.MinuteLocator(byminute=[0, 15, 30, 45]))
        
        # 设置刻度标签旋转角度
        plt.setp(ax1.xaxis.get_majorticklabels(), rotation=45)
        plt.setp(ax2.xaxis.get_majorticklabels(), rotation=45)
        plt.setp(ax3.xaxis.get_majorticklabels(), rotation=45)
        
        # 添加鼠标悬停显示功能
        annot = ax1.annotate('', xy=(0, 0), xytext=(20, 20), textcoords='offset points',
                            bbox=dict(boxstyle='round', fc='yellow', alpha=0.7),
                            arrowprops=dict(arrowstyle='->'))
        annot.set_visible(False)
        
        def on_move(event):
            if event.inaxes and event.inaxes == ax1 and len(df_filtered) > 0:
                # 获取最近的数据点
                try:
                    # 修复：正确处理event.xdata为浮点数的情况
                    x_pos = event.xdata
                    if isinstance(x_pos, (int, float)):
                        # 将matplotlib日期浮点数转换为datetime对象
                        x_datetime = mdates.num2date(x_pos)
                        
                        # 检查是上午还是下午数据，并相应地调整查询
                        # 首先检查是否在调整后的下午时间段
                        if not morning_data.empty and not afternoon_data.empty:
                            last_morning_time_original = morning_data.index[-1]
                            first_afternoon_time_original = afternoon_data.index[0]
                            time_gap = first_afternoon_time_original - last_morning_time_original
                            
                            # 确定鼠标位置对应的原始时间
                            if x_datetime > last_morning_time_original:
                                # 这是调整后的下午时间，需要转换回原始时间
                                original_datetime = x_datetime + time_gap
                                # 查询原始的下午数据
                                target_data = afternoon_data
                            else:
                                # 这是上午时间，直接使用
                                original_datetime = x_datetime
                                target_data = morning_data
                        elif not morning_data.empty:
                            # 只有上午数据
                            original_datetime = x_datetime
                            target_data = morning_data
                        elif not afternoon_data.empty:
                            # 只有下午数据
                            original_datetime = x_datetime
                            target_data = afternoon_data
                        else:
                            annot.set_visible(False)
                            fig.canvas.draw_idle()
                            return
                        
                        # 找到最近的时间点
                        if not target_data.empty:
                            time_diff = np.abs(target_data.index - original_datetime)
                            nearest_index = time_diff.argmin()
                            nearest_time = target_data.index[nearest_index]
                            
                            # 确保索引存在
                            if nearest_time in df_filtered.index:
                                row = df_filtered.loc[nearest_time]
                                
                                # 构建显示信息
                                time_str = nearest_time.strftime('%H:%M')
                                price_str = f'{row["收盘"]:.2f}'
                                avg_price_str = f'{row["均价"]:.2f}'
                                ratio_str = f'{row["Price_MA_Ratio"]:.2f}%'
                                volume_ratio_str = f'{row["Volume_Ratio"]:.2f}'
                                
                                # 添加信号信息
                                signal_info = ''
                                if 'Buy_Signal' in row and row['Buy_Signal']:
                                    signal_info = '买入信号'
                                elif 'Sell_Signal' in row and row['Sell_Signal']:
                                    signal_info = '卖出信号'
                                
                                if signal_info:
                                    info = f'时间: {time_str}\n收盘价: {price_str}\n均价: {avg_price_str}\n偏离率: {ratio_str}\n量比: {volume_ratio_str}\n信号: {signal_info}'
                                else:
                                    info = f'时间: {time_str}\n收盘价: {price_str}\n均价: {avg_price_str}\n偏离率: {ratio_str}\n量比: {volume_ratio_str}'
                                
                                # 计算显示位置的坐标
                                # 如果是下午数据，需要使用调整后的时间坐标
                                display_x = x_pos  # 使用鼠标事件提供的x坐标
                                
                                # 更新注释框位置和文本
                                annot.xy = (display_x, row["收盘"])
                                annot.set_text(info)
                                annot.set_visible(True)
                                fig.canvas.draw_idle()
                            else:
                                annot.set_visible(False)
                                fig.canvas.draw_idle()
                        else:
                            annot.set_visible(False)
                            fig.canvas.draw_idle()
                    else:
                        annot.set_visible(False)
                        fig.canvas.draw_idle()
                except Exception as e:
                    print(f"鼠标悬浮错误: {e}")
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
        output_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'charts')
        os.makedirs(output_dir, exist_ok=True)
        chart_path = os.path.join(output_dir, f'{stock_code}_price_volume_deviation_{trade_date.replace("-", "")}.png')
        plt.savefig(chart_path, dpi=300, bbox_inches='tight')
        
        # 显示图表窗口（阻塞模式，直到用户关闭窗口）
        plt.ioff()  # 关闭交互模式
        # plt.show()  # 注释掉显示，改为直接保存
        
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
        # 时间处理 - 与系统其他部分保持一致，使用'%Y-%m-%d'格式
        if trade_date is None:
            # yesterday = datetime.now() - timedelta(days=1)
            # trade_date = yesterday.strftime('%Y%m%d')

            trade_date = datetime.now().strftime('%Y-%m-%d')

        # 获取数据
        provider = IntradayDataProvider()
        df = provider.get_intraday_data(stock_code, trade_date)
        logger.info('[重复日志修复] 分时数据前五行：\n{}\n后五行:\n{}'.format(df.head(5), df.tail(5)))

        if df is None or df.empty:
            return None
        
        # 设置时间索引
        df = df.copy()
        if '时间' in df.columns:
            df['时间'] = pd.to_datetime(df['时间'])
            df = df.set_index('时间')
        
        # 计算指标
        df_with_indicators = calculate_price_volume_deviation(df)
        # print(df_with_indicators)
        
        # 检测收集信号，传入股票代码
        signals = detect_trading_signals(df_with_indicators, stock_code)
        # print(signals)
        
        return df_with_indicators, signals
        
    except Exception as e:
        print(f"❌ 分析失败: {e}")
        import traceback
        traceback.print_exc()
        return None

def indicator_main():
    # 整合函数，同时监控多支股票
    stock_codes = ["600030", "002415"]  # 中信证券和海康威视
    # trade_date = "2025-11-06"
    trade_date = datetime.now().strftime('%Y-%m-%d')
    
    results = {}
    for stock_code in stock_codes:
        print(f"正在分析股票 {stock_code}...")
        result = analyze_strategy(stock_code, trade_date)
        if result is not None:
            df, signals = result
            plot_strategy_chart(stock_code, trade_date, df)
            
            # 检查是否有新的信号并发送通知
            if signals and ('buy_signals' in signals or 'sell_signals' in signals):
                # 检查买入信号
                if 'buy_signals' in signals and signals['buy_signals']:
                    for signal_time, price in signals['buy_signals']:
                        # 构造通知消息
                        message = f"[{stock_code}] 买入信号\n时间: {signal_time}\n价格: {price}\n指标: 价格成交量偏离策略"
                        print(f"🔔 买入信号: {message}")
                        # 发送通知
                        send_notification(message)
                
                # 检查卖出信号
                if 'sell_signals' in signals and signals['sell_signals']:
                    for signal_time, price in signals['sell_signals']:
                        # 构造通知消息
                        message = f"[{stock_code}] 卖出信号\n时间: {signal_time}\n价格: {price}\n指标: 价格成交量偏离策略"
                        print(f"🔔 卖出信号: {message}")
                        # 发送通知
                        send_notification(message)
            
            results[stock_code] = (df, signals)
            print(f"股票 {stock_code} 分析完成")
        else:
            print(f"股票 {stock_code} 没有数据或分析失败")
    
    return results if results else None


def monitor_stocks():
    """持续监控股票信号"""
    import time
    stock_codes = ["600030", "002415"]  # 中信证券和海康威视
    trade_date = datetime.now().strftime('%Y-%m-%d')
    
    # 用于记录已发送的通知，避免重复发送
    sent_notifications = set()
    
    print(f"开始监控股票: {', '.join(stock_codes)}")
    print("按 Ctrl+C 停止监控")
    
    try:
        while True:
            current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            print(f"\n[{current_time}] 检查信号...")
            
            for stock_code in stock_codes:
                print(f"正在分析股票 {stock_code}...")
                result = analyze_strategy(stock_code, trade_date)
                if result is not None:
                    df, signals = result
                    plot_strategy_chart(stock_code, trade_date, df)
                    
                    # 检查是否有新的信号并发送通知
                    if signals and ('buy_signals' in signals or 'sell_signals' in signals):
                        # 检查买入信号
                        if 'buy_signals' in signals and signals['buy_signals']:
                            for signal_time, price in signals['buy_signals']:
                                # 创建信号标识以避免重复通知
                                signal_id = f"{stock_code}_buy_{signal_time}"
                                if signal_id not in sent_notifications:
                                    # 构造通知消息
                                    message = f"[{stock_code}] 买入信号\n时间: {signal_time}\n价格: {price}\n指标: 价格成交量偏离策略"
                                    print(f"🔔 买入信号: {message}")
                                    # 发送通知
                                    send_notification(message)
                                    # 记录已发送的通知
                                    sent_notifications.add(signal_id)
                        
                        # 检查卖出信号
                        if 'sell_signals' in signals and signals['sell_signals']:
                            for signal_time, price in signals['sell_signals']:
                                # 创建信号标识以避免重复通知
                                signal_id = f"{stock_code}_sell_{signal_time}"
                                if signal_id not in sent_notifications:
                                    # 构造通知消息
                                    message = f"[{stock_code}] 卖出信号\n时间: {signal_time}\n价格: {price}\n指标: 价格成交量偏离策略"
                                    print(f"🔔 卖出信号: {message}")
                                    # 发送通知
                                    send_notification(message)
                                    # 记录已发送的通知
                                    sent_notifications.add(signal_id)
                    
                    print(f"股票 {stock_code} 分析完成")
                else:
                    print(f"股票 {stock_code} 没有数据或分析失败")
            
            # 等待30秒后再次检查
            time.sleep(30)
            
    except KeyboardInterrupt:
        print("\n监控已停止")


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "--monitor":
        monitor_stocks()
    else:
        indicator_main()