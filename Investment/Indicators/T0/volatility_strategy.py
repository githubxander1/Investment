#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
波动率策略指标模块 (volatility_strategy.py)

该模块实现了基于价格波动率的交易策略指标计算与分析功能，包括：
1. 价格波动率计算（使用标准差）
2. 基于波动率的买卖信号生成
3. 策略回测与绩效分析
4. 可视化展示

使用方法：
    可以调用calculate_volatility_strategy计算指标，或使用analyze_volatility_strategy进行完整策略分析

作者: 
创建日期: 
版本: 1.0
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
from typing import Optional, Tuple, Dict, List
import akshare as ak
import matplotlib.font_manager as fm
import os
import sys

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from T0.utils.logger import setup_logger

logger = setup_logger('volatility_strategy')

# 设置中文字体支持
plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False


def calculate_volatility_strategy(df: pd.DataFrame, window: int = 20, multiplier: float = 2.0) -> pd.DataFrame:
    """
    计算基于波动率的交易策略指标
    
    功能：计算股票价格波动率，并基于波动率生成买卖信号
    
    策略原理：
    1. 计算价格收益率的标准差作为波动率指标
    2. 使用波动率构建上下轨阈值
    3. 当价格突然大幅上涨超过上轨时卖出（认为会回调）
    4. 当价格突然大幅下跌超过下轨时买入（认为会反弹）
    
    参数：
        df: 包含价格数据的DataFrame，需包含'收盘'列
        window: 波动率计算窗口，默认为20
        multiplier: 波动率倍数阈值，默认为2.0
    
    返回值：
        添加了策略指标的DataFrame，新增列包括：
        - 'Return': 日收益率
        - 'Volatility': 价格波动率（标准差）
        - 'Avg_Return': 平均收益率
        - 'Buy_Threshold': 买入阈值
        - 'Sell_Threshold': 卖出阈值
    """
    df = df.copy()
    
    # 计算收益率
    df['Return'] = df['收盘'].pct_change()
    
    # 计算波动率（标准差）
    df['Volatility'] = df['Return'].rolling(window=window, min_periods=1).std()
    
    # 计算平均收益率
    df['Avg_Return'] = df['Return'].rolling(window=window, min_periods=1).mean()
    
    # 计算买入和卖出阈值
    df['Buy_Threshold'] = df['Avg_Return'] - multiplier * df['Volatility']
    df['Sell_Threshold'] = df['Avg_Return'] + multiplier * df['Volatility']
    
    # 生成买卖信号
    # 买入信号：当收益率低于买入阈值时
    df['Buy_Signal'] = (df['Return'] <= df['Buy_Threshold']) & (df['Return'].shift(1) > df['Buy_Threshold'].shift(1))
    
    # 卖出信号：当收益率高于卖出阈值时
    df['Sell_Signal'] = (df['Return'] >= df['Sell_Threshold']) & (df['Return'].shift(1) < df['Sell_Threshold'].shift(1))
    
    # 记录所有信号
    buy_signals = df[df['Buy_Signal']]
    sell_signals = df[df['Sell_Signal']]
    
    print(f"波动率策略：共检测到 {len(buy_signals)} 个买入信号和 {len(sell_signals)} 个卖出信号")
    
    for idx, row in buy_signals.iterrows():
        buy_time = row['时间'] if '时间' in df.columns else idx
        buy_price = row['收盘']
        buy_return = row['Return'] * 100
        print(f"波动率策略：买入信号时间点: {buy_time}, 价格: {buy_price:.2f}, 收益率: {buy_return:.2f}%")
    
    for idx, row in sell_signals.iterrows():
        sell_time = row['时间'] if '时间' in df.columns else idx
        sell_price = row['收盘']
        sell_return = row['Return'] * 100
        print(f"波动率策略：卖出信号时间点: {sell_time}, 价格: {sell_price:.2f}, 收益率: {sell_return:.2f}%")
    
    if len(buy_signals) == 0 and len(sell_signals) == 0:
        print("未检测到任何信号")
    
    return df

def fetch_intraday_data(stock_code: str, trade_date: str) -> Optional[pd.DataFrame]:
    """
    获取分时数据
    
    Args:
        stock_code: 股票代码
        trade_date: 交易日期
    
    Returns:
        分时数据DataFrame
    """
    try:
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

        # 如果缓存没有数据，则从网络获取
        df = ak.stock_zh_a_hist_min_em(
            symbol=stock_code,
            period="1",
            start_date=start_time,
            end_date=end_time,
            adjust=''
        )

        if df.empty:
            print(f"❌ {stock_code} 在 {trade_date} 无分时数据")
            return None
            
        return df
    except Exception as e:
        print(f"❌ 获取分时数据失败: {e}")
        return None

def detect_trading_signals(df: pd.DataFrame) -> Dict[str, List[Tuple[datetime, float]]]:
    """
    检测交易信号
    
    Args:
        df: 包含指标的DataFrame
    
    Returns:
        信号字典
    """
    signals = {
        'buy_signals': [],
        'sell_signals': []
    }
    
    # 检测买入信号
    buy_signals = df[df['Buy_Signal']]
    for idx, row in buy_signals.iterrows():
        if isinstance(idx, str):
            signal_time = pd.to_datetime(idx)
        else:
            signal_time = idx
        signals['buy_signals'].append((signal_time, row['收盘']))
    
    # 检测卖出信号
    sell_signals = df[df['Sell_Signal']]
    for idx, row in sell_signals.iterrows():
        if isinstance(idx, str):
            signal_time = pd.to_datetime(idx)
        else:
            signal_time = idx
        signals['sell_signals'].append((signal_time, row['收盘']))
    
    return signals

def plot_volatility_strategy(stock_code: str, trade_date: Optional[str] = None) -> Optional[str]:
    """
    绘制波动率策略图表
    
    Args:
        stock_code: 股票代码
        trade_date: 交易日期
    
    Returns:
        图表保存路径
    """
    try:
        # 时间处理
        if trade_date is None:
            yesterday = datetime.now() - timedelta(days=1)
            trade_date = yesterday.strftime('%Y-%m-%d')
        
        # 获取数据
        df = fetch_intraday_data(stock_code, trade_date)
        if df is None or df.empty:
            return None
        
        # 计算指标
        df_with_indicators = calculate_volatility_strategy(df)
        
        # 创建图形和子图
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(16, 10), gridspec_kw={'height_ratios': [3, 1]})
        fig.suptitle(f'{stock_code} 波动率策略图 ({trade_date})', fontsize=16)
        
        # 过滤掉无效数据
        df_filtered = df_with_indicators.dropna(subset=['收盘'])
        
        # 绘制价格
        ax1.plot(df_filtered.index, df_filtered['收盘'], label='收盘价', color='black', linewidth=1)
        
        # 绘制买入信号
        buy_signals = df_filtered[df_filtered['Buy_Signal']].dropna()
        for idx, row in buy_signals.iterrows():
            x_pos = df_filtered.index.get_loc(idx)
            ax1.scatter(x_pos, row['收盘'] * 0.995, marker='^', color='red', s=100, zorder=5)
            ax1.text(x_pos, row['收盘'] * 0.99, '买',
                     color='red', fontsize=12, ha='center', va='top', fontweight='bold')
        
        # 绘制卖出信号
        sell_signals = df_filtered[df_filtered['Sell_Signal']].dropna()
        for idx, row in sell_signals.iterrows():
            x_pos = df_filtered.index.get_loc(idx)
            ax1.scatter(x_pos, row['收盘'] * 1.005, marker='v', color='green', s=100, zorder=5)
            ax1.text(x_pos, row['收盘'] * 1.01, '卖',
                     color='green', fontsize=12, ha='center', va='bottom', fontweight='bold')
        
        ax1.set_ylabel('价格', fontsize=12)
        ax1.grid(True, linestyle='--', alpha=0.7)
        ax1.legend()
        
        # 绘制收益率和阈值
        ax2.plot(df_filtered.index, df_filtered['Return'] * 100, label='收益率(%)', color='blue', linewidth=1)
        ax2.plot(df_filtered.index, df_filtered['Buy_Threshold'] * 100, label='买入阈值', color='red', linewidth=1, linestyle='--')
        ax2.plot(df_filtered.index, df_filtered['Sell_Threshold'] * 100, label='卖出阈值', color='green', linewidth=1, linestyle='--')
        ax2.axhline(y=0, color='black', linestyle='-', alpha=0.5)
        ax2.set_ylabel('收益率(%)', fontsize=12)
        ax2.set_xlabel('时间', fontsize=12)
        ax2.grid(True, linestyle='--', alpha=0.7)
        ax2.legend()
        
        # 自动旋转时间标签
        plt.setp(ax2.xaxis.get_majorticklabels(), rotation=45)
        
        # 调整布局
        plt.tight_layout()
        
        # 保存图表
        import os
        output_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'output', 'charts')
        os.makedirs(output_dir, exist_ok=True)
        chart_path = os.path.join(output_dir, f'{stock_code}_volatility_strategy_{trade_date}.png')
        plt.savefig(chart_path, dpi=300, bbox_inches='tight')
        plt.close()
        
        print(f"📈 图表已保存至: {chart_path}")
        return chart_path
        
    except Exception as e:
        print(f"❌ 绘图失败: {e}")
        import traceback
        traceback.print_exc()
        return None

def analyze_volatility_strategy(stock_code: str, trade_date: Optional[str] = None) -> Optional[Tuple[pd.DataFrame, Dict[str, List[Tuple[datetime, float]]]]]:
    """
    波动率策略分析主函数
    
    Args:
        stock_code: 股票代码
        trade_date: 交易日期
    
    Returns:
        (数据框, 信号字典) 或 None
    """
    try:
        # 时间处理
        if trade_date is None:
            yesterday = datetime.now() - timedelta(days=1)
            trade_date = yesterday.strftime('%Y-%m-%d')
        
        # 获取数据
        df = fetch_intraday_data(stock_code, trade_date)
        if df is None or df.empty:
            return None
        
        # 计算指标
        df_with_indicators = calculate_volatility_strategy(df)
        
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
    stock_code = "000333"  # 美的集团
    trade_date = datetime.now().strftime('%Y-%m-%d')
    
    result = analyze_volatility_strategy(stock_code, trade_date)
    if result:
        df_with_indicators, signals = result
        print(f"📊 检测到 {len(signals['buy_signals'])} 个买入信号和 {len(signals['sell_signals'])} 个卖出信号")
        
        # 绘制图表
        plot_volatility_strategy(stock_code, trade_date)