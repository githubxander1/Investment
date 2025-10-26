#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
价格均线偏离指标模块 (price_ma_deviation.py) - 数据库版

从本地数据库读取数据，不再依赖外部接口

版本: 2.0 - 数据库版本
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
from typing import Optional, Tuple, Dict, List
import matplotlib.font_manager as fm
import os
import sys
import logging
from pathlib import Path

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# 添加项目根目录到Python路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# 导入数据库管理器
try:
    from core.data_manager import DataManager
    from core.db_manager import DBManager
    USE_DATABASE = True
    logger.info("✅ 成功导入数据库管理器")
except ImportError as e:
    logger.warning(f"⚠️ 无法导入数据库管理器: {e}")
    USE_DATABASE = False

# 设置中文字体支持
plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

# 输出目录设置 - 保存到T0_Optimized目录
CHART_OUTPUT_DIR = project_root / 'output' / 'charts'
CHART_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def calculate_price_ma_deviation(df: pd.DataFrame, ma_period: int = 5) -> pd.DataFrame:
    """
    计算价格与均线的偏离策略指标
    
    功能：计算股票价格与指定周期均线之间的偏离度，并生成相应的买卖信号
    
    策略原理：
    1. 计算价格与均线的差值和比率
    2. 当价格低于均线一定比例时买入
    3. 当价格高于均线一定比例时卖出
    
    参数：
        df: 包含价格数据的DataFrame，需包含'收盘'列
        ma_period: 均线周期，默认为5（5日均线）
    
    返回值：
        添加了策略指标的DataFrame，新增列包括：
        - 'MA': 指定周期的移动平均线
        - 'Price_MA_Diff': 价格与均线的差值
        - 'Price_MA_Ratio': 价格与均线的偏离百分比
        - 'Buy_Signal': 买入信号（布尔值）
        - 'Sell_Signal': 卖出信号（布尔值）
    """
    df = df.copy()
    
    # 使用接口返回的均价，不重新计算
    # 如果接口返回的数据中没有均价列，才进行计算
    if '均价' not in df.columns:
        print("警告: 接口返回的数据中没有均价列，使用成交额/成交量计算")
        df['均价'] = df['成交额'] / df['成交量']
        df['均价'] = df['均价'].fillna(method='ffill').fillna(method='bfill')
    
    # 计算指定周期的移动平均线
    df['MA'] = df['收盘'].rolling(window=ma_period, min_periods=1).mean()
    
    # 计算价格与均价的差值和比率（使用接口返回的均价数据）
    df['Price_MA_Diff'] = df['收盘'] - df['均价']
    df['Price_MA_Ratio'] = (df['收盘'] / df['均价'] - 1) * 100  # 转换为百分比
    
    # 策略参数
    buy_threshold = -0.3  # 低于均线0.3%时买入
    sell_threshold = 0.3  # 高于均线0.3%时卖出
    
    # 生成买卖信号
    base_buy_signal = (df['Price_MA_Ratio'] <= buy_threshold) & (df['Price_MA_Ratio'].shift(1) > buy_threshold)
    base_sell_signal = (df['Price_MA_Ratio'] >= sell_threshold) & (df['Price_MA_Ratio'].shift(1) < sell_threshold)
    
    df['Buy_Signal'] = base_buy_signal
    df['Sell_Signal'] = base_sell_signal
    
    # 记录所有信号
    buy_signals = df[df['Buy_Signal']]
    sell_signals = df[df['Sell_Signal']]
    
    print(f"价格均线偏离策略：共检测到 {len(buy_signals)} 个买入信号和 {len(sell_signals)} 个卖出信号")
    
    for idx, row in buy_signals.iterrows():
        buy_time = row['时间'] if '时间' in df.columns else idx
        buy_price = row['收盘']
        buy_ratio = row['Price_MA_Ratio']
        print(f"价格均线偏离策略：买入信号时间点: {buy_time}, 价格: {buy_price:.2f}, 偏离比率: {buy_ratio:.2f}%")
    
    for idx, row in sell_signals.iterrows():
        sell_time = row['时间'] if '时间' in df.columns else idx
        sell_price = row['收盘']
        sell_ratio = row['Price_MA_Ratio']
        print(f"价格均线偏离策略：卖出信号时间点: {sell_time}, 价格: {sell_price:.2f}, 偏离比率: {sell_ratio:.2f}%")
    
    if len(buy_signals) == 0 and len(sell_signals) == 0:
        print("未检测到任何信号")
    
    return df


def fetch_intraday_data(stock_code: str, trade_date: str) -> Optional[pd.DataFrame]:
    """
    从数据库获取分时数据
    
    Args:
        stock_code: 股票代码
        trade_date: 交易日期
    
    Returns:
        分时数据DataFrame
    """
    logger.info("="*60)
    logger.info("📈 开始从数据库加载分时数据")
    logger.info(f"股票代码: {stock_code}")
    logger.info(f"交易日期: {trade_date}")
    
    if not USE_DATABASE:
        logger.error("⚠️ 数据库管理器未加载，无法读取数据")
        return None
    
    try:
        # 解析日期格式
        if isinstance(trade_date, str):
            if '-' in trade_date:
                trade_date_obj = datetime.strptime(trade_date, '%Y-%m-%d')
            else:
                trade_date_obj = datetime.strptime(trade_date, '%Y%m%d')
        else:
            trade_date_obj = trade_date
        
        trade_date_str = trade_date_obj.strftime('%Y-%m-%d')
        logger.info(f"格式化日期: {trade_date_str}")
        
        # 尝试使用DBManager（推荐）
        try:
            db_mgr = DBManager()
            df = db_mgr.get_minute_data(stock_code, trade_date_str)
            db_mgr.close_all()
            
            if df is not None and not df.empty:
                logger.info(f"✅ 使用DBManager成功读取 {len(df)} 条数据")
                logger.info(f"时间范围: {df['时间'].min()} ~ {df['时间'].max()}")
                logger.info(f"数据列: {', '.join(df.columns.tolist())}")
                logger.info("="*60)
                return df
        except Exception as e:
            logger.warning(f"⚠️ DBManager读取失败: {e}")
        
        # 回退到DataManager
        try:
            dm = DataManager()
            df = dm.get_minute_data(stock_code, trade_date_str)
            dm.close()
            
            if df is not None and not df.empty:
                logger.info(f"✅ 使用DataManager成功读取 {len(df)} 条数据")
                logger.info(f"时间范围: {df['时间'].min()} ~ {df['时间'].max()}")
                logger.info("="*60)
                return df
        except Exception as e:
            logger.error(f"❗ DataManager读取失败: {e}")
        
        logger.error(f"❗ 无法从数据库读取 {stock_code} 在 {trade_date_str} 的数据")
        return None
        
    except Exception as e:
        logger.error(f"❗ 获取分时数据失败: {e}")
        import traceback
        traceback.print_exc()
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


def plot_tdx_intraday(stock_code: str, trade_date: Optional[str] = None, df: Optional[pd.DataFrame] = None) -> Optional[str]:
    """
    绘制价格均线偏离策略图表
    
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
        
        # 设置时间索引（与resistance_support_indicators.py保持一致）
        df = df.copy()
        if '时间' in df.columns:
            df['时间'] = pd.to_datetime(df['时间'])
            df = df.set_index('时间')
        
        # 计算指标
        df_with_indicators = calculate_price_ma_deviation(df)
        
        # 创建图形和子图
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(16, 10), gridspec_kw={'height_ratios': [3, 1]})
        fig.suptitle(f'{stock_code} 价格均线偏离策略图 ({trade_date})', fontsize=16)
        
        # 过滤掉无效数据
        df_filtered = df_with_indicators.dropna(subset=['收盘'])
        
        # 绘制价格和均价（使用接口返回的均价数据）
        ax1.plot(range(len(df_filtered)), df_filtered['收盘'], label='收盘价', color='black', linewidth=1)
        ax1.plot(range(len(df_filtered)), df_filtered['均价'], label='均价', color='blue', linewidth=1)
        
        # 绘制买入信号
        buy_signals = df_filtered[df_filtered['Buy_Signal']].dropna()
        for i, (idx, row) in enumerate(df_filtered.iterrows()):
            if row.get('Buy_Signal', False):
                ax1.scatter(i, row['收盘'] * 0.995, marker='^', color='red', s=100, zorder=5)
                ax1.text(i, row['收盘'] * 0.99, '买',
                         color='red', fontsize=12, ha='center', va='top', fontweight='bold')
        
        # 绘制卖出信号
        sell_signals = df_filtered[df_filtered['Sell_Signal']].dropna()
        for i, (idx, row) in enumerate(df_filtered.iterrows()):
            if row.get('Sell_Signal', False):
                ax1.scatter(i, row['收盘'] * 1.005, marker='v', color='green', s=100, zorder=5)
                ax1.text(i, row['收盘'] * 1.01, '卖',
                         color='green', fontsize=12, ha='center', va='bottom', fontweight='bold')
        
        ax1.set_ylabel('价格', fontsize=12)
        ax1.grid(True, linestyle='--', alpha=0.7)
        ax1.legend()
        
        # 绘制价格与均线的比率
        ax2.plot(range(len(df_filtered)), df_filtered['Price_MA_Ratio'], label='价格与均线偏离比率(%)', color='purple', linewidth=1)
        ax2.axhline(y=0, color='black', linestyle='-', alpha=0.5)
        ax2.axhline(y=0.3, color='green', linestyle='--', alpha=0.7, label='卖出阈值')
        ax2.axhline(y=-0.3, color='red', linestyle='--', alpha=0.7, label='买入阈值')
        ax2.set_ylabel('偏离比率(%)', fontsize=12)
        ax2.set_xlabel('时间', fontsize=12)
        ax2.grid(True, linestyle='--', alpha=0.7)
        ax2.legend()
        
        # 设置x轴标签为时间
        time_labels = df_filtered.index.strftime('%H:%M') if hasattr(df_filtered.index, 'strftime') else df_filtered.index
        # 只显示部分时间标签，避免拥挤
        step = max(1, len(time_labels) // 15)
        ax2.set_xticks(range(0, len(time_labels), step))
        ax2.set_xticklabels(time_labels[::step], rotation=45)
        
        # 调整布局
        plt.tight_layout()
        
        # 保存图表
        import os
        output_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'output', 'charts')
        os.makedirs(output_dir, exist_ok=True)
        chart_path = os.path.join(output_dir, f'{stock_code}_price_ma_deviation_{trade_date}.png')
        plt.savefig(chart_path, dpi=300, bbox_inches='tight')
        plt.close()
        
        print(f"📈 图表已保存至: {chart_path}")
        return chart_path
        
    except Exception as e:
        print(f"❌ 绘图失败: {e}")
        import traceback
        traceback.print_exc()
        return None


def analyze_price_ma_deviation(stock_code: str, trade_date: Optional[str] = None) -> Optional[Tuple[pd.DataFrame, Dict[str, List[Tuple[datetime, float]]]]]:
    """
    价格均线偏离策略分析主函数
    
    Args:
        stock_code: 股票代码
        trade_date: 交易日期
    
    Returns:
        (数据框, 信号字典) 或 None
    """
    try:
        # 时间处理 - 与系统其他部分保持一致，使用'%Y%m%d'格式
        if trade_date is None:
            yesterday = datetime.now() - timedelta(days=1)
            trade_date = yesterday.strftime('%Y%m%d')
        
        # 获取数据
        df = fetch_intraday_data(stock_code, trade_date)
        if df is None or df.empty:
            return None
        
        # 设置时间索引（与resistance_support_indicators.py保持一致）
        df = df.copy()
        if '时间' in df.columns:
            df['时间'] = pd.to_datetime(df['时间'])
            df = df.set_index('时间')
        
        # 计算指标
        df_with_indicators = calculate_price_ma_deviation(df)
        
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
    # stock_code = "600030"  # 中信证券
    # 使用缓存数据的日期（2025-10-24）
    trade_date = '20251024'
    
    result = analyze_price_ma_deviation(stock_code, trade_date)
    if result:
        df_with_indicators, signals = result
        print(f"📊 检测到 {len(signals['buy_signals'])} 个买入信号和 {len(signals['sell_signals'])} 个卖出信号")
        
        # 绘制图表
        plot_tdx_intraday(stock_code, trade_date)