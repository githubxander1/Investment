#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
综合T+0策略指标 (comprehensive_t0_strategy.py)

该模块实现了一个综合T+0交易策略指标，整合了以下核心功能：
1. 自适应参数系统（根据股票波动性自动调整参数）
2. 改进的阻力支撑位计算（避免信号不断变化）
3. 复合信号机制（多指标加权评分）
4. 智能时间管理和未完成T操作的处理
5. 风险控制（最大持有时间、止损机制）

使用方法：
    可以直接调用analyze_comprehensive_t0函数进行分析，或使用plot_comprehensive_t0函数绘制指标图表

作者: AI Assistant
创建日期: 2024-01-01
版本: 1.0
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
from typing import Optional, Tuple, Dict, List, Any
import akshare as ak
import os
import sys
import logging

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# 导入我们优化的东方财富接口
from data2dfcf import stock_zh_a_hist_min_em as eastmoney_fenshi
from data2dfcf import random_delay

# 代理配置（可根据需要修改）
DEFAULT_PROXY = None  # 默认不使用代理
# DEFAULT_PROXY = {'http': 'http://127.0.0.1:7890', 'https': 'http://127.0.0.1:7890'}  # 如需代理可启用此行

# 设置中文字体支持
plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

# 输出目录设置
CHART_OUTPUT_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'output', 'charts')
os.makedirs(CHART_OUTPUT_DIR, exist_ok=True)


def calculate_volatility(df: pd.DataFrame, window: int = 20) -> float:
    """
    计算股票波动性
    
    功能：使用历史数据计算股票的日内波动率，用于判断高波动股和低波动股
    
    参数：
        df: 包含价格数据的DataFrame
        window: 计算波动率的窗口大小
    
    返回值：
        波动率值（百分比的标准差）
    """
    # 计算每分钟收益率
    df['returns'] = df['收盘'].pct_change() * 100
    
    # 使用标准差衡量波动率
    volatility = df['returns'].rolling(window=window, min_periods=1).std().mean()
    
    return volatility if not np.isnan(volatility) else 0.5  # 默认中等波动


def get_adaptive_parameters(volatility: float) -> Dict[str, float]:
    """
    根据波动率获取自适应参数
    
    功能：根据股票波动性自动调整交易参数
    波动分类：
    - 低波动股: volatility < 0.3%，日内波动较小，适合宽松参数
    - 中等波动: 0.3% <= volatility <= 0.8%，大多数股票属于此类
    - 高波动股: volatility > 0.8%，波动较大，需要更敏感的参数
    
    参数：
        volatility: 股票波动率
    
    返回值：
        包含自适应参数的字典
    """
    if volatility < 0.3:  # 低波动股
        return {
            'price_ma_threshold': 0.4,       # 价格均线偏离阈值更大
            'signal_interval_minutes': 25,   # 信号间隔更长
            'volume_threshold': 0.8,         # 成交量阈值更宽松
            'max_hold_minutes': 100          # 持有时间更长
        }
    elif volatility > 0.8:  # 高波动股
        return {
            'price_ma_threshold': 0.2,       # 价格均线偏离阈值更小
            'signal_interval_minutes': 15,   # 信号间隔更短
            'volume_threshold': 1.0,         # 成交量阈值更严格
            'max_hold_minutes': 70           # 持有时间更短
        }
    else:  # 中等波动股（默认）
        return {
            'price_ma_threshold': 0.3,       # 适中的偏离阈值
            'signal_interval_minutes': 20,   # 适中的信号间隔
            'volume_threshold': 0.9,         # 适中的成交量阈值
            'max_hold_minutes': 90           # 最大持有时间90分钟
        }


def calculate_improved_support_resistance(df: pd.DataFrame, prev_close: float, time_slice: Optional[str] = 'early') -> pd.DataFrame:
    """
    计算改进的支撑阻力位
    
    功能：修复原始阻力支撑指标中信号不断变化的问题
    改进点：
    1. 使用固定时段的高低点计算支撑阻力，避免随时间不断变化
    2. 增加多级别支撑阻力位
    3. 使用更稳定的计算方法
    
    参数：
        df: 包含价格数据的DataFrame
        prev_close: 昨收价
        time_slice: 使用哪个时段的数据计算，'early'表示早盘前30分钟，'all'表示全天
    
    返回值：
        添加了支撑阻力指标的DataFrame
    """
    df = df.copy()
    
    # 根据time_slice选择数据范围
    if time_slice == 'early' and hasattr(df.index, 'hour'):
        # 使用早盘前30分钟的数据（9:30-10:00）
        early_data = df[(df.index.hour == 9) & (df.index.minute >= 30) | 
                        (df.index.hour == 10) & (df.index.minute == 0)]
        if not early_data.empty:
            daily_high = early_data['最高'].max()
            daily_low = early_data['最低'].min()
        else:
            # 如果没有早盘数据，回退到全天数据
            daily_high = df['最高'].max()
            daily_low = df['最低'].min()
    else:
        # 使用全天数据
        daily_high = df['最高'].max()
        daily_low = df['最低'].min()
    
    # 计算H1、L1（昨收 vs 日内高低）
    H1 = max(prev_close, daily_high)
    L1 = min(prev_close, daily_low)
    P1 = H1 - L1
    
    # 计算多级别支撑阻力位
    # 1. 主要支撑阻力（基于通达信公式）
    main_support = L1 + P1 * 0.5 / 8
    main_resistance = L1 + P1 * 7 / 8
    
    # 2. 次要支撑阻力
    secondary_support = L1 + P1 * 1.5 / 8
    secondary_resistance = L1 + P1 * 6.5 / 8
    
    # 3. 紧急支撑阻力
    emergency_support = L1
    emergency_resistance = H1
    
    # 将支撑阻力位填充到整个DataFrame（固定值，不随时间变化）
    df['支撑'] = main_support
    df['阻力'] = main_resistance
    df['次要支撑'] = secondary_support
    df['次要阻力'] = secondary_resistance
    df['紧急支撑'] = emergency_support
    df['紧急阻力'] = emergency_resistance
    
    # 信号计算
    # 1. 支撑位信号：价格下穿支撑位
    df['support_signal'] = ((df['收盘'].shift(1) > df['支撑']) & 
                            (df['收盘'] <= df['支撑']))
    
    # 2. 阻力位信号：价格上穿阻力位
    df['resistance_signal'] = ((df['收盘'].shift(1) < df['阻力']) & 
                              (df['收盘'] >= df['阻力']))
    
    # 3. 强支撑信号（紧急支撑）
    df['strong_support_signal'] = ((df['收盘'].shift(1) > df['紧急支撑']) & 
                                 (df['收盘'] <= df['紧急支撑']))
    
    # 4. 强阻力信号（紧急阻力）
    df['strong_resistance_signal'] = ((df['收盘'].shift(1) < df['紧急阻力']) & 
                                    (df['收盘'] >= df['紧急阻力']))
    
    return df


def calculate_price_ma_deviation(df: pd.DataFrame, ma_period: int = 5) -> pd.DataFrame:
    """
    计算价格均线偏离指标
    
    功能：计算价格与均线的偏离度，作为主信号源
    
    参数：
        df: 包含价格数据的DataFrame
        ma_period: 均线周期
    
    返回值：
        添加了均线偏离指标的DataFrame
    """
    df = df.copy()
    
    # 使用接口返回的均价，如果没有则计算
    if '均价' not in df.columns:
        print("警告: 接口返回的数据中没有均价列，使用成交额/成交量计算")
        df['均价'] = df['成交额'] / df['成交量']
        df['均价'] = df['均价'].fillna(method='ffill').fillna(method='bfill')
    
    # 计算移动平均线
    df['MA'] = df['收盘'].rolling(window=ma_period, min_periods=1).mean()
    
    # 计算价格与均价的差值和比率
    df['Price_MA_Diff'] = df['收盘'] - df['均价']
    df['Price_MA_Ratio'] = (df['收盘'] / df['均价'] - 1) * 100  # 转换为百分比
    
    # 计算成交量移动平均
    df['Volume_MA'] = df['成交量'].rolling(window=20, min_periods=1).mean()
    
    # 计算价格趋势
    df['Trend_MA'] = df['收盘'].rolling(window=30, min_periods=1).mean()
    df['Is_Up_Trend'] = df['收盘'] > df['Trend_MA']
    
    return df


def calculate_momentum_indicator(df: pd.DataFrame, momentum_window: int = 10) -> pd.DataFrame:
    """
    计算动量指标
    
    功能：计算价格变化率作为动量指标，用于判断短期反转
    
    参数：
        df: 包含价格数据的DataFrame
        momentum_window: 动量计算窗口
    
    返回值：
        添加了动量指标的DataFrame
    """
    df = df.copy()
    
    # 计算价格变化率（动量指标）
    df['Price_Change'] = df['收盘'].pct_change(periods=momentum_window) * 100
    
    # 计算动量的均值和标准差
    df['Momentum_Mean'] = df['Price_Change'].rolling(window=momentum_window*3, min_periods=1).mean()
    df['Momentum_Std'] = df['Price_Change'].rolling(window=momentum_window*3, min_periods=1).std()
    
    # 动态阈值（默认使用0.5%作为基础阈值）
    df['Upper_Threshold'] = df['Momentum_Mean'] + 0.5
    df['Lower_Threshold'] = df['Momentum_Mean'] - 0.5
    
    # 超买超卖信号
    df['oversold'] = df['Price_Change'] <= df['Lower_Threshold']
    df['overbought'] = df['Price_Change'] >= df['Upper_Threshold']
    
    # 动量反转信号
    df['momentum_buy_signal'] = ((df['Price_Change'].shift(1) > df['Lower_Threshold'].shift(1)) & 
                                (df['Price_Change'] <= df['Lower_Threshold']))
    df['momentum_sell_signal'] = ((df['Price_Change'].shift(1) < df['Upper_Threshold'].shift(1)) & 
                                 (df['Price_Change'] >= df['Upper_Threshold']))
    
    return df


def calculate_composite_score(df: pd.DataFrame, params: Dict[str, float]) -> pd.DataFrame:
    """
    计算复合信号评分
    
    功能：综合多个指标给出加权评分，用于最终信号判断
    评分规则：
    - 价格均线偏离信号（主信号）：权重40%
    - 支撑阻力信号（位置确认）：权重30%
    - 动量反转信号（时机判断）：权重20%
    - 趋势确认（方向确认）：权重10%
    
    参数：
        df: 包含所有指标的DataFrame
        params: 自适应参数字典
    
    返回值：
        添加了复合评分的DataFrame
    """
    df = df.copy()
    
    # 初始化评分列
    df['buy_score'] = 0
    df['sell_score'] = 0
    
    # 1. 价格均线偏离信号评分（权重40%）
    threshold = params['price_ma_threshold']
    
    # 买入评分（价格低于均线）
    df.loc[df['Price_MA_Ratio'] <= -threshold, 'buy_score'] += 40
    # 额外奖励：偏离程度越大，评分越高
    df.loc[df['Price_MA_Ratio'] <= -threshold*2, 'buy_score'] += 10
    
    # 卖出评分（价格高于均线）
    df.loc[df['Price_MA_Ratio'] >= threshold, 'sell_score'] += 40
    # 额外奖励：偏离程度越大，评分越高
    df.loc[df['Price_MA_Ratio'] >= threshold*2, 'sell_score'] += 10
    
    # 2. 支撑阻力信号评分（权重30%）
    # 买入信号：触及支撑位
    df.loc[df['support_signal'], 'buy_score'] += 20
    df.loc[df['strong_support_signal'], 'buy_score'] += 30
    
    # 卖出信号：触及阻力位
    df.loc[df['resistance_signal'], 'sell_score'] += 20
    df.loc[df['strong_resistance_signal'], 'sell_score'] += 30
    
    # 3. 动量反转信号评分（权重20%）
    df.loc[df['momentum_buy_signal'], 'buy_score'] += 20
    df.loc[df['oversold'], 'buy_score'] += 10
    
    df.loc[df['momentum_sell_signal'], 'sell_score'] += 20
    df.loc[df['overbought'], 'sell_score'] += 10
    
    # 4. 趋势确认评分（权重10%）
    # 上升趋势中增强买入信号，减弱卖出信号
    df.loc[df['Is_Up_Trend'], 'buy_score'] += 10
    df.loc[df['Is_Up_Trend'], 'sell_score'] -= 5
    
    # 下降趋势中增强卖出信号，减弱买入信号
    df.loc[~df['Is_Up_Trend'], 'sell_score'] += 10
    df.loc[~df['Is_Up_Trend'], 'buy_score'] -= 5
    
    # 成交量确认（额外加分项）
    volume_threshold = params['volume_threshold']
    df.loc[df['成交量'] >= volume_threshold * df['Volume_MA'], 'buy_score'] += 5
    df.loc[df['成交量'] >= volume_threshold * df['Volume_MA'], 'sell_score'] += 5
    
    # 确保评分不为负
    df['buy_score'] = df['buy_score'].clip(lower=0)
    df['sell_score'] = df['sell_score'].clip(lower=0)
    
    return df


def generate_trading_signals(df: pd.DataFrame, params: Dict[str, float], has_open_position: bool = False) -> pd.DataFrame:
    """
    生成交易信号
    
    功能：基于复合评分生成最终交易信号，包含智能时间管理和未完成T操作处理
    
    参数：
        df: 包含复合评分的DataFrame
        params: 自适应参数字典
        has_open_position: 是否有未完成的T操作
    
    返回值：
        添加了交易信号的DataFrame
    """
    df = df.copy()
    
    # 初始化信号列
    df['Buy_Signal'] = False
    df['Sell_Signal'] = False
    
    # 设置信号阈值
    buy_threshold = 50  # 买入信号阈值
    sell_threshold = 50  # 卖出信号阈值
    
    # 紧急信号阈值（不考虑时间间隔和尾盘限制）
    emergency_threshold = 80
    
    # 获取评分超过阈值的候选信号
    buy_candidates = df[df['buy_score'] >= buy_threshold].index
    sell_candidates = df[df['sell_score'] >= sell_threshold].index
    
    # 紧急信号
    emergency_buys = df[df['buy_score'] >= emergency_threshold].index
    emergency_sells = df[df['sell_score'] >= emergency_threshold].index
    
    # 初始化最后信号时间
    last_buy_time = None
    last_sell_time = None
    
    # 处理买入信号
    for idx in buy_candidates:
        # 检查是否为紧急信号
        is_emergency = idx in emergency_buys
        
        # 时间有效性检查
        if hasattr(idx, 'hour'):
            hour, minute = idx.hour, idx.minute
            
            # 智能时间过滤：
            # 1. 紧急信号不考虑时间限制
            # 2. 有未完成T操作时，尾盘也允许操作
            # 3. 正常情况下避开尾盘
            if not is_emergency and not has_open_position:
                if hour == 14 and minute >= 50:
                    continue
        
        # 时间间隔过滤（紧急信号除外）
        if not is_emergency and last_buy_time is not None:
            if isinstance(idx, pd.Timestamp):
                time_diff = (idx - last_buy_time).total_seconds() / 60
                if time_diff < params['signal_interval_minutes']:
                    continue
        
        # 成交量过滤
        if df.loc[idx, '成交量'] < params['volume_threshold'] * df.loc[idx, 'Volume_MA']:
            # 紧急信号可以放宽成交量要求
            if not is_emergency:
                continue
        
        # 确认买入信号
        df.loc[idx, 'Buy_Signal'] = True
        last_buy_time = idx
    
    # 处理卖出信号
    for idx in sell_candidates:
        # 检查是否为紧急信号
        is_emergency = idx in emergency_sells
        
        # 时间有效性检查
        if hasattr(idx, 'hour'):
            hour, minute = idx.hour, idx.minute
            
            # 智能时间过滤：
            # 1. 紧急信号不考虑时间限制
            # 2. 有未完成T操作时，尾盘也允许操作
            # 3. 正常情况下避开尾盘
            if not is_emergency and not has_open_position:
                if hour == 14 and minute >= 50:
                    continue
        
        # 时间间隔过滤（紧急信号除外）
        if not is_emergency and last_sell_time is not None:
            if isinstance(idx, pd.Timestamp):
                time_diff = (idx - last_sell_time).total_seconds() / 60
                if time_diff < params['signal_interval_minutes']:
                    continue
        
        # 成交量过滤
        if df.loc[idx, '成交量'] < params['volume_threshold'] * df.loc[idx, 'Volume_MA']:
            # 紧急信号可以放宽成交量要求
            if not is_emergency:
                continue
        
        # 确认卖出信号
        df.loc[idx, 'Sell_Signal'] = True
        last_sell_time = idx
    
    return df


def match_trade_pairs(df: pd.DataFrame, max_hold_minutes: int = 90) -> List[Dict[str, Any]]:
    """
    匹配交易对并分析收益
    
    功能：匹配买入和卖出信号，计算每笔交易的收益率和持有时间
    为什么设置最大持有时间不超过90分钟：
    1. T+0交易的核心是当日完成，避免持仓过夜风险
    2. 研究表明，日内持仓时间过长会增加不确定性和风险暴露
    3. 90分钟是一个平衡点，既能捕捉足够的波动，又能控制风险
    4. 符合A股日内交易的实际节奏和波动特性
    5. 避免在一个方向上过度持仓，保持灵活性
    
    参数：
        df: 包含交易信号的DataFrame
        max_hold_minutes: 最大持有时间（分钟）
    
    返回值：
        交易对列表
    """
    # 获取所有买入和卖出信号
    buy_signals = df[df['Buy_Signal']].index.tolist()
    sell_signals = df[df['Sell_Signal']].index.tolist()
    
    # 排序信号
    buy_signals.sort()
    sell_signals.sort()
    
    # 匹配交易对
    trades = []
    i, j = 0, 0
    
    while i < len(buy_signals) and j < len(sell_signals):
        buy_time = buy_signals[i]
        
        # 找到在买入信号之后的第一个卖出信号
        while j < len(sell_signals) and sell_signals[j] <= buy_time:
            j += 1
        
        if j < len(sell_signals):
            sell_time = sell_signals[j]
            
            # 计算持有时间
            if isinstance(buy_time, pd.Timestamp) and isinstance(sell_time, pd.Timestamp):
                hold_time_minutes = (sell_time - buy_time).total_seconds() / 60
                
                # 检查是否超过最大持有时间
                if hold_time_minutes <= max_hold_minutes:
                    buy_price = df.loc[buy_time, '收盘']
                    sell_price = df.loc[sell_time, '收盘']
                    profit_pct = (sell_price / buy_price - 1) * 100
                    
                    trades.append({
                        'buy_time': buy_time,
                        'sell_time': sell_time,
                        'buy_price': buy_price,
                        'sell_price': sell_price,
                        'profit_pct': profit_pct,
                        'hold_time_minutes': hold_time_minutes,
                        'buy_score': df.loc[buy_time, 'buy_score'],
                        'sell_score': df.loc[sell_time, 'sell_score']
                    })
                    
                    i += 1
                    j += 1
                else:
                    # 超过最大持有时间，跳过这个买入信号
                    i += 1
            else:
                # 非时间戳索引，简单匹配
                buy_price = df.loc[buy_time, '收盘']
                sell_price = df.loc[sell_time, '收盘']
                profit_pct = (sell_price / buy_price - 1) * 100
                
                trades.append({
                    'buy_time': buy_time,
                    'sell_time': sell_time,
                    'buy_price': buy_price,
                    'sell_price': sell_price,
                    'profit_pct': profit_pct,
                    'hold_time_minutes': 0,  # 未知时间间隔
                    'buy_score': df.loc[buy_time, 'buy_score'],
                    'sell_score': df.loc[sell_time, 'sell_score']
                })
                
                i += 1
                j += 1
        else:
            break
    
    return trades


def fetch_intraday_data(stock_code: str, trade_date: str, proxy: Optional[Dict[str, str]] = None) -> Optional[pd.DataFrame]:
    """
    获取分时数据（从缓存文件读取）
    
    Args:
        stock_code: 股票代码
        trade_date: 交易日期
        proxy: 代理字典（已废弃，保留参数仅为兼容性）
    
    Returns:
        分时数据DataFrame
    """
    logger.info(f"="*60)
    logger.info(f"开始从缓存加载分时数据")
    logger.info(f"股票代码: {stock_code}")
    logger.info(f"交易日期: {trade_date}")
    
    try:
        # 确保 trade_date 是正确的格式
        if isinstance(trade_date, str):
            try:
                trade_date_obj = datetime.strptime(trade_date, '%Y-%m-%d')
                logger.info(f"日期格式: YYYY-MM-DD")
            except ValueError:
                try:
                    trade_date_obj = datetime.strptime(trade_date, '%Y%m%d')
                    logger.info(f"日期格式: YYYYMMDD")
                except ValueError:
                    logger.error(f"无法解析日期格式: {trade_date}")
                    raise ValueError(f"无法解析日期格式: {trade_date}")
        else:
            trade_date_obj = trade_date
            
        # 格式化为缓存文件需要的日期格式 (YYYYMMDD)
        trade_date_str = trade_date_obj.strftime('%Y%m%d')
        logger.info(f"格式化日期: {trade_date_str}")
        
        # 构造缓存文件路径
        cache_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'cache', 'fenshi_data')
        cache_file = os.path.join(cache_dir, f'{stock_code}_{trade_date_str}_fenshi.csv')
        
        logger.info(f"缓存目录: {cache_dir}")
        logger.info(f"缓存文件: {cache_file}")
        
        # 从缓存文件读取数据
        if not os.path.exists(cache_file):
            logger.error(f"❌ 缓存文件不存在: {cache_file}")
            return None
        
        logger.info(f"✅ 找到缓存文件，开始读取...")
        df = pd.read_csv(cache_file)
        logger.info(f"读取到 {len(df)} 行数据")
        
        if df.empty:
            logger.warning(f"❌ {stock_code} 在 {trade_date} 无分时数据")
            return None
        
        # 处理数据格式
        if '时间' in df.columns:
            logger.info(f"处理时间列...")
            df['时间'] = pd.to_datetime(df['时间'])
            df = df.set_index('时间')
            logger.info(f"时间范围: {df.index.min()} 到 {df.index.max()}")
        
        # 过滤掉午休时间
        original_len = len(df)
        df = df[~((df.index.hour == 11) & (df.index.minute >= 30)) & 
                ~((df.index.hour == 12))]
        logger.info(f"过滤午休时间后: {len(df)} 行数据 (删除了 {original_len - len(df)} 行)")
        
        # 填充缺失值
        df = df.ffill().bfill()
        logger.info(f"数据列: {', '.join(df.columns.tolist())}")
        logger.info(f"✅ 成功从缓存加载 {stock_code} 的分时数据")
        logger.info(f"="*60)
        
        return df
            
    except Exception as e:
        logger.error(f"❌ 获取分时数据过程中发生错误: {e}")
        import traceback
        traceback.print_exc()
        return None


def get_prev_close(stock_code: str, trade_date: str) -> float:
    """
    获取前一日收盘价
    
    Args:
        stock_code: 股票代码
        trade_date: 交易日期
    
    Returns:
        前一日收盘价
    """
    try:
        # 尝试从当天数据的开盘价推断
        df = fetch_intraday_data(stock_code, trade_date, proxy=DEFAULT_PROXY)
        if df is not None and not df.empty:
            # 使用当天第一分钟的开盘价作为昨收价的近似
            return df['开盘'].iloc[0]
        
        # 如果失败，返回一个默认值
        return 10.0
    except Exception:
        return 10.0


def analyze_comprehensive_t0(stock_code: str, trade_date: Optional[str] = None, 
                           has_open_position: bool = False) -> Optional[Tuple[pd.DataFrame, List[Dict[str, Any]]]]:
    """
    综合T+0策略分析主函数
    
    Args:
        stock_code: 股票代码
        trade_date: 交易日期
        has_open_position: 是否有未完成的T操作
    
    Returns:
        (数据框, 交易对列表) 或 None
    """
    try:
        # 时间处理
        if trade_date is None:
            # yesterday = datetime.now() - timedelta(days=1)
            # trade_date = yesterday.strftime('%Y-%m-%d')
            trade_date = datetime.now().strftime('%Y-%m-%d')
        
        # 获取数据
        df = fetch_intraday_data(stock_code, trade_date, proxy=DEFAULT_PROXY)
        if df is None or df.empty:
            return None
        
        # 获取前一日收盘价
        prev_close = get_prev_close(stock_code, trade_date)
        
        # 计算波动率并获取自适应参数
        volatility = calculate_volatility(df)
        params = get_adaptive_parameters(volatility)
        
        print(f"\n📊 股票: {stock_code} 波动率分析")
        print(f"- 计算波动率: {volatility:.2f}%")
        if volatility < 0.3:
            print(f"- 股票类型: 低波动股")
        elif volatility > 0.8:
            print(f"- 股票类型: 高波动股")
        else:
            print(f"- 股票类型: 中等波动股")
        print(f"- 自适应参数: {params}")
        
        # 计算各指标
        # 1. 价格均线偏离指标
        df = calculate_price_ma_deviation(df)
        
        # 2. 改进的支撑阻力指标
        df = calculate_improved_support_resistance(df, prev_close)
        
        # 3. 动量指标
        df = calculate_momentum_indicator(df)
        
        # 4. 计算复合评分
        df = calculate_composite_score(df, params)
        
        # 5. 生成交易信号
        df = generate_trading_signals(df, params, has_open_position)
        
        # 6. 匹配交易对
        trades = match_trade_pairs(df, params['max_hold_minutes'])
        
        # 打印信号统计
        buy_signals = df[df['Buy_Signal']]
        sell_signals = df[df['Sell_Signal']]
        
        print(f"\n🚦 信号统计")
        print(f"- 买入信号数量: {len(buy_signals)}")
        print(f"- 卖出信号数量: {len(sell_signals)}")
        print(f"- 匹配交易对数量: {len(trades)}")
        
        # 打印交易对分析
        if trades:
            total_profit = sum(trade['profit_pct'] for trade in trades)
            avg_profit = total_profit / len(trades)
            
            print(f"\n📈 交易对分析")
            print(f"- 总收益率: {total_profit:.2f}%")
            print(f"- 平均收益率: {avg_profit:.2f}%")
            print(f"- 最大持有时间: {params['max_hold_minutes']}分钟")
            
            for i, trade in enumerate(trades, 1):
                print(f"\n交易 {i}:")
                print(f"  买入时间: {trade['buy_time'].strftime('%H:%M')}")
                print(f"  买入价格: {trade['buy_price']:.2f}")
                print(f"  买入评分: {trade['buy_score']:.1f}")
                print(f"  卖出时间: {trade['sell_time'].strftime('%H:%M')}")
                print(f"  卖出价格: {trade['sell_price']:.2f}")
                print(f"  卖出评分: {trade['sell_score']:.1f}")
                print(f"  收益率: {trade['profit_pct']:+.2f}%")
                print(f"  持有时间: {trade['hold_time_minutes']:.0f}分钟")
        
        return df, trades
        
    except Exception as e:
        print(f"❌ 分析失败: {e}")
        import traceback
        traceback.print_exc()
        return None


def plot_comprehensive_t0(stock_code: str, trade_date: Optional[str] = None, 
                          has_open_position: bool = False) -> Optional[str]:
    """
    绘制综合T+0策略图表
    
    Args:
        stock_code: 股票代码
        trade_date: 交易日期
        has_open_position: 是否有未完成的T操作
    
    Returns:
        图表保存路径
    """
    try:
        # 时间处理
        if trade_date is None:
            yesterday = datetime.now() - timedelta(days=1)
            trade_date = yesterday.strftime('%Y-%m-%d')
        
        # 执行分析
        result = analyze_comprehensive_t0(stock_code, trade_date, has_open_position)
        if result is None:
            return None
        
        df, trades = result
        
        # 创建图表
        fig, (ax1, ax2, ax3, ax4) = plt.subplots(4, 1, figsize=(16, 16), 
                                              gridspec_kw={'height_ratios': [3, 1, 1, 1]})
        fig.suptitle(f'{stock_code} 综合T+0策略分析图 ({trade_date})', fontsize=16)
        
        # 过滤掉无效数据
        df_filtered = df.dropna(subset=['收盘'])
        x_values = list(range(len(df_filtered)))
        
        # 图表1: 价格、均线、支撑阻力位和交易信号
        ax1.plot(x_values, df_filtered['收盘'], label='收盘价', color='black', linewidth=1)
        ax1.plot(x_values, df_filtered['均价'], label='均价', color='blue', linewidth=1)
        ax1.plot(x_values, df_filtered['支撑'], label='支撑位', color='green', linewidth=1.5, linestyle='--')
        ax1.plot(x_values, df_filtered['阻力'], label='阻力位', color='red', linewidth=1.5, linestyle='--')
        ax1.plot(x_values, df_filtered['次要支撑'], label='次要支撑', color='lightgreen', linewidth=1, linestyle=':')
        ax1.plot(x_values, df_filtered['次要阻力'], label='次要阻力', color='lightcoral', linewidth=1, linestyle=':')
        
        # 绘制买入信号
        for i, (idx, row) in enumerate(df_filtered.iterrows()):
            if row['Buy_Signal']:
                ax1.scatter(i, row['收盘'] * 0.99, marker='^', color='red', s=100, zorder=5)
                ax1.text(i, row['收盘'] * 0.97, '买', color='red', fontsize=12, 
                        ha='center', va='top', fontweight='bold')
        
        # 绘制卖出信号
        for i, (idx, row) in enumerate(df_filtered.iterrows()):
            if row['Sell_Signal']:
                ax1.scatter(i, row['收盘'] * 1.01, marker='v', color='green', s=100, zorder=5)
                ax1.text(i, row['收盘'] * 1.03, '卖', color='green', fontsize=12, 
                        ha='center', va='bottom', fontweight='bold')
        
        # 绘制交易对连线
        for trade in trades:
            buy_idx = df_filtered.index.get_loc(trade['buy_time'])
            sell_idx = df_filtered.index.get_loc(trade['sell_time'])
            ax1.plot([buy_idx, sell_idx], [trade['buy_price'], trade['sell_price']], 
                    color='purple', linestyle='-', linewidth=1.5, alpha=0.7)
        
        ax1.set_ylabel('价格', fontsize=12)
        ax1.grid(True, linestyle='--', alpha=0.7)
        ax1.legend(loc='upper left')
        
        # 图表2: 价格均线偏离比率
        ax2.plot(x_values, df_filtered['Price_MA_Ratio'], label='价格均线偏离比率(%)', 
                color='purple', linewidth=1)
        ax2.axhline(y=0, color='black', linestyle='-', alpha=0.5)
        
        # 动态阈值线（基于自适应参数）
        volatility = calculate_volatility(df)
        params = get_adaptive_parameters(volatility)
        threshold = params['price_ma_threshold']
        
        ax2.axhline(y=threshold, color='green', linestyle='--', alpha=0.7, label=f'卖出阈值 ({threshold}%)')
        ax2.axhline(y=-threshold, color='red', linestyle='--', alpha=0.7, label=f'买入阈值 ({-threshold}%)')
        
        ax2.set_ylabel('偏离比率(%)', fontsize=12)
        ax2.grid(True, linestyle='--', alpha=0.7)
        ax2.legend()
        
        # 图表3: 动量指标
        ax3.plot(x_values, df_filtered['Price_Change'], label='价格变化率(%)', color='blue', linewidth=1)
        ax3.plot(x_values, df_filtered['Upper_Threshold'], label='超买阈值', color='red', linestyle='--')
        ax3.plot(x_values, df_filtered['Lower_Threshold'], label='超卖阈值', color='green', linestyle='--')
        ax3.axhline(y=0, color='black', linestyle='-', alpha=0.5)
        
        ax3.set_ylabel('动量指标(%)', fontsize=12)
        ax3.grid(True, linestyle='--', alpha=0.7)
        ax3.legend()
        
        # 图表4: 复合评分
        ax4.plot(x_values, df_filtered['buy_score'], label='买入评分', color='red', linewidth=1)
        ax4.plot(x_values, df_filtered['sell_score'], label='卖出评分', color='green', linewidth=1)
        ax4.axhline(y=50, color='orange', linestyle='--', alpha=0.7, label='信号阈值')
        ax4.axhline(y=80, color='darkorange', linestyle=':', alpha=0.7, label='紧急信号阈值')
        
        ax4.set_ylabel('复合评分', fontsize=12)
        ax4.set_xlabel('时间', fontsize=12)
        ax4.grid(True, linestyle='--', alpha=0.7)
        ax4.legend()
        
        # 设置x轴标签为时间
        time_labels = df_filtered.index.strftime('%H:%M')
        step = max(1, len(time_labels) // 15)
        
        for ax in [ax1, ax2, ax3, ax4]:
            ax.set_xticks(range(0, len(time_labels), step))
            ax.set_xticklabels(time_labels[::step], rotation=45)
        
        # 调整布局
        plt.tight_layout()
        plt.subplots_adjust(top=0.95)
        
        # 保存图表
        chart_filename = os.path.join(CHART_OUTPUT_DIR, 
                                    f'{stock_code}_comprehensive_t0_{trade_date}.png')
        plt.savefig(chart_filename, dpi=300, bbox_inches='tight')
        plt.close()
        
        print(f"\n📊 图表已保存至: {chart_filename}")
        return chart_filename
        
    except Exception as e:
        print(f"❌ 绘图失败: {e}")
        import traceback
        traceback.print_exc()
        return None


if __name__ == "__main__":
    # 测试代码 - 扩展测试更多股票，覆盖不同行业和波动特征
    stock_codes = [
        "000333",  # 美的集团 - 家电龙头
        "600030",  # 中信证券 - 券商龙头
        # "000002",  # 万科A - 地产龙头
        # "600519",  # 贵州茅台 - 白酒龙头
        # "000858",  # 五粮液 - 白酒
        "002415",  # 海康威视 - 安防
        # "300750",  # 宁德时代 - 新能源
        # "600000",  # 浦发银行 - 银行
        # "600900",  # 长江电力 - 公用事业
        # "601318"   # 中国平安 - 保险
    ]
    # 使用缓存数据的日期（2025-10-24）
    trade_date = '20251024'
    
    # 记录总体统计数据
    total_trades = 0
    profitable_trades = 0
    total_profit = 0
    
    for stock_code in stock_codes:
        print(f"\n===== 分析股票: {stock_code} =====")
        # 使用plot_comprehensive_t0函数生成图表并获取数据
        chart_path = plot_comprehensive_t0(stock_code, trade_date, has_open_position=False)
        
        if chart_path:
            print(f"图表已成功生成: {chart_path}")
            # 获取分析结果以进行统计
            result = analyze_comprehensive_t0(stock_code, trade_date, has_open_position=False)
            if result:
                df, trades = result
                total_trades += len(trades)
                
                # 计算盈利交易数和总盈利
                for trade in trades:
                    if trade['profit_pct'] > 0:
                        profitable_trades += 1
                    total_profit += trade['profit_pct']
    
    # 打印总体统计
    print(f"\n===== 总体策略表现统计 =====")
    print(f"测试股票数量: {len(stock_codes)}")
    print(f"总交易对数量: {total_trades}")
    print(f"盈利交易数量: {profitable_trades}")
    
    if total_trades > 0:
        success_rate = (profitable_trades / total_trades) * 100
        avg_profit = total_profit / total_trades
        print(f"成功率: {success_rate:.2f}%")
        print(f"平均收益率: {avg_profit:.2f}%")
    else:
        print("未产生交易对")