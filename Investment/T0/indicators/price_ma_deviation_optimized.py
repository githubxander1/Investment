#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
价格均线偏离指标模块 - 优化增强版 (price_ma_deviation_optimized.py)

该模块实现了基于价格与均线偏离度的交易策略指标计算与分析功能，并添加了信号过滤优化，包括：
1. 价格与均线的偏离度计算（差值和百分比）
2. 基于偏离度的买卖信号生成
3. 信号优化过滤（自适应参数、时间间隔、趋势、成交量等）
4. 智能时间管理和风险控制
5. 可视化展示和性能分析

使用方法：
    可以调用calculate_price_ma_deviation计算指标，或使用analyze_deviation_strategy进行完整策略分析

作者:
创建日期:
版本: 3.0 - 添加自适应参数系统和性能优化
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
from typing import Optional, Tuple, Dict, List, Any
import akshare as ak
import matplotlib.font_manager as fm
import os
import sys
import logging

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

# 导入我们优化的东方财富接口
# 移除东方财富接口依赖，使用缓存或模拟数据
# 定义获取分时数据的函数，优先使用缓存，没有则生成模拟数据
def get_fenshi_data(stock_code, date, **kwargs):
    """
    从缓存或生成模拟数据获取分时数据
    
    Args:
        stock_code: 股票代码
        date: 日期，格式为'YYYYMMDD'
        **kwargs: 其他参数
        
    Returns:
        pandas.DataFrame: 分时数据
    """
    # 尝试从缓存获取数据
    import os
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    cache_dir = os.path.join(project_root, 'cache', 'fenshi_data')
    cache_file = os.path.join(cache_dir, f'{stock_code}_{date}_fenshi.csv')
    
    # 如果找不到，也尝试在T0_Optimized项目的缓存目录查找
    if not os.path.exists(cache_file):
        optimized_cache_dir = os.path.join(os.path.dirname(project_root), 'T0_Optimized', 'cache', 'fenshi_data')
        cache_file = os.path.join(optimized_cache_dir, f'{stock_code}_{date}_fenshi.csv')
    
    if os.path.exists(cache_file):
        import pandas as pd
        df = pd.read_csv(cache_file)
        print(f"从缓存文件 {cache_file} 读取股票分时数据")
        return df
    
    # 生成模拟数据
    print(f"未找到缓存数据，生成模拟分时数据 for {stock_code} {date}")
    import pandas as pd
    import numpy as np
    
    # 创建时间序列（模拟交易日的分时数据）
    times = []
    for hour in [9, 10, 11, 13, 14]:
        start_min = 30 if hour == 9 else 0
        end_min = 31 if hour == 11 else 60
        for minute in range(start_min, end_min):
            if (hour == 11 and minute > 30) or (hour > 14):
                break
            times.append(f"{hour:02d}:{minute:02d}:00")
    
    # 生成模拟价格数据
    base_price = np.random.uniform(10, 100)
    price_changes = np.random.normal(0, 0.01, len(times))
    prices = base_price * np.exp(np.cumsum(price_changes))
    
    # 创建DataFrame
    df = pd.DataFrame({
        '时间': times,
        '开盘': prices,
        '最高': prices * (1 + np.random.uniform(0, 0.02, len(times))),
        '最低': prices * (1 - np.random.uniform(0, 0.02, len(times))),
        '收盘': prices,
        '成交量': np.random.randint(1000, 100000, len(times))
    })
    
    return df

def random_delay(min_delay=0.1, max_delay=0.3):
    """模拟随机延迟函数"""
    import time
    import random
    delay = random.uniform(min_delay, max_delay)
    time.sleep(delay)

# 代理配置（可根据需要修改）
DEFAULT_PROXY = None  # 默认不使用代理
# DEFAULT_PROXY = {'http': 'http://127.0.0.1:7890', 'https': 'http://127.0.0.1:7890'}  # 如需代理可启用此行

# 设置中文字体支持
plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

# 输出目录设置
CHART_OUTPUT_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'output', 'charts')
os.makedirs(CHART_OUTPUT_DIR, exist_ok=True)

def calculate_volatility(df: pd.DataFrame, window: int = 30) -> float:
    """
    计算股票的波动率
    
    Args:
        df: 包含价格数据的DataFrame
        window: 计算波动率的窗口大小
    
    Returns:
        平均波动率百分比
    """
    # 计算涨跌幅百分比
    df['pct_change'] = df['收盘'].pct_change() * 100
    # 计算波动率（标准差）
    volatility = df['pct_change'].rolling(window=window).std().mean()
    return volatility if not np.isnan(volatility) else 0.0

def get_adaptive_parameters(volatility: float) -> Dict:
    """
    根据波动率获取自适应参数
    
    Args:
        volatility: 股票的平均波动率
    
    Returns:
        自适应参数字典
    """
    logger.info(f"股票波动率: {volatility:.2f}%")
    
    # 低波动股 (< 0.3%)
    if volatility < 0.3:
        # 调整为更容易触发信号
        return {
            'buy_threshold': -0.4,      # 降低阈值使信号更容易触发
            'sell_threshold': 0.4,
            'min_time_interval': 25,    # 缩短时间间隔
            'volume_threshold': 0.6,    # 降低成交量要求
            'max_holding_time': 110
        }
    # 中波动股 (0.3% - 0.8%)
    elif 0.3 <= volatility < 0.8:
        # 这是大多数股票的情况，包括美的集团，需要更合理的参数
        return {
            'buy_threshold': -0.35,     # 降低阈值
            'sell_threshold': 0.35,
            'min_time_interval': 20,    # 缩短时间间隔
            'volume_threshold': 0.7,    # 降低成交量要求
            'max_holding_time': 95
        }
    # 高波动股 (>= 0.8%)
    else:
        # 保持较敏感的参数
        return {
            'buy_threshold': -0.3,
            'sell_threshold': 0.3,
            'min_time_interval': 15,
            'volume_threshold': 0.9,    # 稍微降低成交量要求
            'max_holding_time': 70
        }

def calculate_price_ma_deviation(df: pd.DataFrame, ma_period: int = 5) -> pd.DataFrame:
    """
    计算价格与均线的偏离策略指标 - 优化增强版
    
    功能：计算股票价格与指定周期均线之间的偏离度，并生成相应的买卖信号，
    包含自适应参数系统和信号过滤优化
    
    策略原理：
    1. 计算价格与均价的差值和比率
    2. 根据股票波动率自适应调整买卖阈值
    3. 当价格低于均线一定比例时买入
    4. 当价格高于均线一定比例时卖出
    5. 添加信号过滤机制减少过多信号
    
    参数：
        df: 包含价格数据的DataFrame，需包含'收盘'列
        ma_period: 均线周期，默认为5（5分钟均线）
    
    返回值：
        添加了策略指标的DataFrame，新增列包括：
        - 'MA': 指定周期的移动平均线
        - 'Price_MA_Diff': 价格与均线的差值
        - 'Price_MA_Ratio': 价格与均线的偏离百分比
        - 'Buy_Signal': 买入信号（布尔值）
        - 'Sell_Signal': 卖出信号（布尔值）
        - 'Optimized_Buy_Signal': 优化后的买入信号
        - 'Optimized_Sell_Signal': 优化后的卖出信号
        - 'Adaptive_Params': 自适应参数信息
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
    
    # 计算成交量移动平均，用于成交量过滤
    df['Volume_MA'] = df['成交量'].rolling(window=20, min_periods=1).mean()
    
    # 计算价格趋势（使用较长周期的均线判断趋势）
    df['Trend_MA'] = df['收盘'].rolling(window=30, min_periods=1).mean()
    df['Is_Up_Trend'] = df['收盘'] > df['Trend_MA']
    
    # 计算波动率
    volatility = calculate_volatility(df)
    print(f"股票波动率: {volatility:.2f}%")
    
    # 获取自适应参数
    adaptive_params = get_adaptive_parameters(volatility)
    print(f"自适应参数: {adaptive_params}")
    
    # 生成基础买卖信号
    base_buy_signal = (df['Price_MA_Ratio'] <= adaptive_params['buy_threshold']) & \
                     (df['Price_MA_Ratio'].shift(1) > adaptive_params['buy_threshold'])
    base_sell_signal = (df['Price_MA_Ratio'] >= adaptive_params['sell_threshold']) & \
                      (df['Price_MA_Ratio'].shift(1) < adaptive_params['sell_threshold'])
    
    df['Buy_Signal'] = base_buy_signal
    df['Sell_Signal'] = base_sell_signal
    
    # 添加偏离率的绝对值列用于调试
    df['Abs_Deviation'] = abs(df['Price_MA_Ratio'])
    
    # 打印最大偏离情况，便于调试
    if not df.empty:
        max_dev_idx = df['Abs_Deviation'].idxmax()
        logger.debug(f"最大偏离率: {df.loc[max_dev_idx, 'Abs_Deviation']:.2f}% 在 {max_dev_idx}")
    
    # 初始化优化后的信号列
    df['Optimized_Buy_Signal'] = False
    df['Optimized_Sell_Signal'] = False
    
    # 设置信号阈值 - 降低阈值使信号更容易触发
    buy_threshold = adaptive_params['buy_threshold'] * 0.8  # 降低20%
    sell_threshold = adaptive_params['sell_threshold'] * 0.8  # 降低20%
    min_time_interval = adaptive_params['min_time_interval']
    volume_threshold = adaptive_params['volume_threshold'] * 0.7  # 降低成交量要求
    max_holding_time = adaptive_params['max_holding_time']
    
    logger.info(f"使用的实际阈值 - 买入: {buy_threshold}, 卖出: {sell_threshold}, 成交量: {volume_threshold}")
    
    # 重新计算基础信号，使用调整后的阈值
    adjusted_buy_signal = (df['Price_MA_Ratio'] <= buy_threshold) & \
                         (df['Price_MA_Ratio'].shift(1) > buy_threshold)
    adjusted_sell_signal = (df['Price_MA_Ratio'] >= sell_threshold) & \
                          (df['Price_MA_Ratio'].shift(1) < sell_threshold)
    
    # 获取调整后信号的索引
    buy_indices = df[adjusted_buy_signal].index
    sell_indices = df[adjusted_sell_signal].index
    
    # 打印候选信号数量，便于调试
    logger.info(f"找到 {len(buy_indices)} 个买入候选信号和 {len(sell_indices)} 个卖出候选信号")
    
    # 优化买入信号
    last_signal_time = None
    for idx in buy_indices:
        # 检查是否在有效时间范围内 - 放宽开盘时间限制
        if hasattr(idx, 'hour'):
            hour, minute = idx.hour, idx.minute
            # 稍微放宽限制
            if hour == 14 and minute >= 40:
                continue
            # 放宽早盘过滤，从原来的<=45改为<=32
            elif hour == 9 and minute <= 32:
                continue
        
        # 时间间隔过滤
        if last_signal_time is not None:
            if isinstance(idx, pd.Timestamp):
                time_diff = (idx - last_signal_time).total_seconds() / 60
                if time_diff < min_time_interval:
                    continue
        
        # 成交量过滤 - 降低要求
        if df.loc[idx, '成交量'] < volume_threshold * df.loc[idx, 'Volume_MA']:
            # 对于中等波动股，在价格严重偏离时可以适当降低成交量要求
            if df.loc[idx, 'Price_MA_Ratio'] > buy_threshold * 1.2:  # 偏离不够严重
                continue
        
        # 通过所有过滤条件，设置优化后的买入信号
        df.loc[idx, 'Optimized_Buy_Signal'] = True
        logger.debug(f"生成买入信号: {idx}, 偏离率: {df.loc[idx, 'Price_MA_Ratio']:.2f}%")
        last_signal_time = idx
    
    # 优化卖出信号
    last_signal_time = None
    for idx in sell_indices:
        # 检查是否在有效时间范围内 - 稍微放宽限制
        if hasattr(idx, 'hour'):
            hour, minute = idx.hour, idx.minute
            # 稍微放宽尾盘过滤，从原来的>=40改为>=57
            if hour == 14 and minute >= 57:
                continue
        
        # 时间间隔过滤
        if last_signal_time is not None:
            if isinstance(idx, pd.Timestamp):
                time_diff = (idx - last_signal_time).total_seconds() / 60
                if time_diff < min_time_interval:
                    continue
        
        # 成交量过滤 - 降低要求
        if df.loc[idx, '成交量'] < volume_threshold * df.loc[idx, 'Volume_MA']:
            # 对于中等波动股，在价格严重偏离时可以适当降低成交量要求
            if df.loc[idx, 'Price_MA_Ratio'] < sell_threshold * 1.2:  # 偏离不够严重
                continue
        
        # 通过所有过滤条件，设置优化后的卖出信号
        df.loc[idx, 'Optimized_Sell_Signal'] = True
        logger.debug(f"生成卖出信号: {idx}, 偏离率: {df.loc[idx, 'Price_MA_Ratio']:.2f}%")
        last_signal_time = idx
    
    # 打印最终信号数量
    buy_signals_count = df['Optimized_Buy_Signal'].sum()
    sell_signals_count = df['Optimized_Sell_Signal'].sum()
    logger.info(f"最终生成 {buy_signals_count} 个买入信号和 {sell_signals_count} 个卖出信号")
    
    # 记录优化后的信号
    optimized_buy_signals = df[df['Optimized_Buy_Signal']]
    optimized_sell_signals = df[df['Optimized_Sell_Signal']]
    
    print(f"价格均线偏离策略 - 优化版：共检测到 {len(optimized_buy_signals)} 个优化买入信号和 {len(optimized_sell_signals)} 个优化卖出信号")
    print(f"基础信号数量：{len(buy_indices)} 个买入信号和 {len(sell_indices)} 个卖出信号")
    
    # 按时间排序信号
    sorted_buys = sorted(optimized_buy_signals.index)
    sorted_sells = sorted(optimized_sell_signals.index)
    
    # 分析潜在交易对和收益，考虑最大持有时间
    trades = []
    i, j = 0, 0
    while i < len(sorted_buys) and j < len(sorted_sells):
        # 找到匹配的买卖对
        if sorted_sells[j] > sorted_buys[i]:
            buy_price = df.loc[sorted_buys[i], '收盘']
            sell_price = df.loc[sorted_sells[j], '收盘']
            profit_pct = (sell_price / buy_price - 1) * 100
            
            # 计算交易时间间隔
            time_diff = (sorted_sells[j] - sorted_buys[i]).total_seconds() / 60
            
            # 应用最大持有时间限制
            if time_diff <= adaptive_params['max_holding_time']:
                trades.append({
                    'buy_time': sorted_buys[i],
                    'sell_time': sorted_sells[j],
                    'buy_price': buy_price,
                    'sell_price': sell_price,
                    'profit_pct': profit_pct,
                    'time_diff_minutes': time_diff
                })
                
                i += 1
                j += 1
            else:
                # 如果超过最大持有时间，尝试寻找更早的卖出信号
                # 这里简化处理，直接移动到下一个买入信号
                i += 1
        else:
            j += 1
    
    # 打印交易对和收益分析
    if trades:
        print("\n🔍 潜在交易分析：")
        total_profit = 0
        for trade in trades:
            print(f"买入: {trade['buy_time']}, 价格: {trade['buy_price']:.2f} | 卖出: {trade['sell_time']}, 价格: {trade['sell_price']:.2f} | 收益率: {trade['profit_pct']:.2f}% | 持有时间: {trade['time_diff_minutes']:.0f}分钟")
            total_profit += trade['profit_pct']
        
        print(f"\n📊 交易统计：")
        print(f"总交易次数: {len(trades)}")
        print(f"总收益率: {total_profit:.2f}%")
        if trades:
            avg_profit = total_profit / len(trades)
            print(f"平均每次收益率: {avg_profit:.2f}%")
    
    # 打印单个信号
    for idx, row in optimized_buy_signals.iterrows():
        buy_time = row['时间'] if '时间' in df.columns else idx
        buy_price = row['收盘']
        buy_ratio = row['Price_MA_Ratio']
        print(f"价格均线偏离策略：优化买入信号时间点: {buy_time}, 价格: {buy_price:.2f}, 偏离比率: {buy_ratio:.2f}%")
    
    for idx, row in optimized_sell_signals.iterrows():
        sell_time = row['时间'] if '时间' in df.columns else idx
        sell_price = row['收盘']
        sell_ratio = row['Price_MA_Ratio']
        print(f"价格均线偏离策略：优化卖出信号时间点: {sell_time}, 价格: {sell_price:.2f}, 偏离比率: {sell_ratio:.2f}%")
    
    # 添加交易建议
    if len(optimized_buy_signals) > 0 or len(optimized_sell_signals) > 0:
        print("\n💡 T+0交易建议：")
        print(f"1. 关注价格低于均价约{abs(adaptive_params['buy_threshold'])}%的买入机会，特别是在成交量配合的情况下")
        print(f"2. 当价格回升至高于均价约{adaptive_params['sell_threshold']}%时考虑卖出，锁定利润")
        print(f"3. 信号时间间隔至少{adaptive_params['min_time_interval']}分钟，避免过于频繁交易增加成本")
        print(f"4. 最大持有时间控制在{adaptive_params['max_holding_time']}分钟以内，降低风险")
        print(f"5. 结合大市和个股趋势，可以进一步提高胜率")
    
    # 添加自适应参数信息到DataFrame（便于后续分析）
    df['Adaptive_Params'] = str(adaptive_params)
    df['Volatility'] = volatility
    
    return df

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

def detect_trading_signals(df: pd.DataFrame, use_optimized: bool = True) -> Dict[str, List[Tuple[datetime, float]]]:
    """
    检测交易信号
    
    Args:
        df: 包含指标的DataFrame
        use_optimized: 是否使用优化后的信号
    
    Returns:
        信号字典
    """
    signals = {
        'buy_signals': [],
        'sell_signals': []
    }
    
    # 根据参数选择使用优化信号还是基础信号
    buy_signal_col = 'Optimized_Buy_Signal' if (use_optimized and 'Optimized_Buy_Signal' in df.columns) else 'Buy_Signal'
    sell_signal_col = 'Optimized_Sell_Signal' if (use_optimized and 'Optimized_Sell_Signal' in df.columns) else 'Sell_Signal'
    
    # 检测买入信号
    buy_signals = df[df[buy_signal_col]]
    for idx, row in buy_signals.iterrows():
        if isinstance(idx, str):
            signal_time = pd.to_datetime(idx)
        else:
            signal_time = idx
        signals['buy_signals'].append((signal_time, row['收盘']))
    
    # 检测卖出信号
    sell_signals = df[df[sell_signal_col]]
    for idx, row in sell_signals.iterrows():
        if isinstance(idx, str):
            signal_time = pd.to_datetime(idx)
        else:
            signal_time = idx
        signals['sell_signals'].append((signal_time, row['收盘']))
    
    return signals

def plot_tdx_intraday(stock_code: str, trade_date: Optional[str] = None, df: Optional[pd.DataFrame] = None, use_optimized: bool = True) -> Optional[str]:
    """
    绘制价格均线偏离策略图表
    
    Args:
        stock_code: 股票代码
        trade_date: 交易日期
        use_optimized: 是否使用优化后的信号
    
    Returns:
        图表保存路径
    """
    try:
        # 时间处理
        if trade_date is None:
            yesterday = datetime.now() - timedelta(days=1)
            trade_date = yesterday.strftime('%Y-%m-%d')
        
        # 获取数据
        df = fetch_intraday_data(stock_code, trade_date, proxy=DEFAULT_PROXY)
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
        fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(16, 12), gridspec_kw={'height_ratios': [3, 1, 1]})
        fig.suptitle(f'{stock_code} 价格均线偏离策略图 - 优化版 ({trade_date})', fontsize=16)
        
        # 过滤掉无效数据
        df_filtered = df_with_indicators.dropna(subset=['收盘'])
        
        # 绘制价格和均价（使用接口返回的均价数据）
        ax1.plot(range(len(df_filtered)), df_filtered['收盘'], label='收盘价', color='black', linewidth=1)
        ax1.plot(range(len(df_filtered)), df_filtered['均价'], label='均价', color='blue', linewidth=1)
        ax1.plot(range(len(df_filtered)), df_filtered['Trend_MA'], label='趋势线', color='purple', linewidth=1.5, linestyle='--')
        
        # 选择信号类型
        buy_signal_col = 'Optimized_Buy_Signal' if (use_optimized and 'Optimized_Buy_Signal' in df_filtered.columns) else 'Buy_Signal'
        sell_signal_col = 'Optimized_Sell_Signal' if (use_optimized and 'Optimized_Sell_Signal' in df_filtered.columns) else 'Sell_Signal'
        
        # 绘制买入信号
        for i, (idx, row) in enumerate(df_filtered.iterrows()):
            if row.get(buy_signal_col, False):
                ax1.scatter(i, row['收盘'] * 0.995, marker='^', color='red', s=100, zorder=5)
                ax1.text(i, row['收盘'] * 0.99, '买',
                         color='red', fontsize=12, ha='center', va='top', fontweight='bold')
        
        # 绘制卖出信号
        for i, (idx, row) in enumerate(df_filtered.iterrows()):
            if row.get(sell_signal_col, False):
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
        ax2.axhline(y=0.5, color='darkgreen', linestyle=':', alpha=0.7, label='上涨趋势卖出阈值')
        ax2.axhline(y=-0.5, color='darkred', linestyle=':', alpha=0.7, label='下跌趋势买入阈值')
        ax2.set_ylabel('偏离比率(%)', fontsize=12)
        ax2.grid(True, linestyle='--', alpha=0.7)
        ax2.legend()
        
        # 绘制成交量
        ax3.bar(range(len(df_filtered)), df_filtered['成交量'], label='成交量', color='gray', alpha=0.7)
        ax3.plot(range(len(df_filtered)), df_filtered['Volume_MA'], label='均量线', color='orange', linewidth=2)
        ax3.axhline(y=0, color='black', linestyle='-', alpha=0.5)
        ax3.set_ylabel('成交量', fontsize=12)
        ax3.set_xlabel('时间', fontsize=12)
        ax3.grid(True, linestyle='--', alpha=0.7)
        ax3.legend()
        
        # 设置x轴标签为时间
        time_labels = df_filtered.index.strftime('%H:%M') if hasattr(df_filtered.index, 'strftime') else df_filtered.index
        # 只显示部分时间标签，避免拥挤
        step = max(1, len(time_labels) // 15)
        ax3.set_xticks(range(0, len(time_labels), step))
        ax3.set_xticklabels(time_labels[::step], rotation=45)
        ax2.set_xticks(range(0, len(time_labels), step))
        ax2.set_xticklabels(time_labels[::step], rotation=45)
        
        # 调整布局
        plt.tight_layout()
        
        # 保存图表
        import os
        output_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'output', 'charts')
        os.makedirs(output_dir, exist_ok=True)
        chart_path = os.path.join(output_dir, f'{stock_code}_price_ma_deviation_optimized_{trade_date}.png')
        plt.savefig(chart_path, dpi=300, bbox_inches='tight')
        plt.close()
        
        print(f"📈 优化版图表已保存至: {chart_path}")
        return chart_path
        
    except Exception as e:
        print(f"❌ 绘图失败: {e}")
        import traceback
        traceback.print_exc()
        return None

def analyze_price_ma_deviation(stock_code: str, trade_date: Optional[str] = None, use_optimized: bool = True) -> Optional[Tuple[pd.DataFrame, Dict[str, List[Tuple[datetime, float]]]]]:
    """
    价格均线偏离策略分析主函数
    
    Args:
        stock_code: 股票代码
        trade_date: 交易日期
        use_optimized: 是否使用优化后的信号
    
    Returns:
        (数据框, 信号字典) 或 None
    """
    try:
        # 时间处理 - 与系统其他部分保持一致，使用'%Y%m%d'格式
        if trade_date is None:
            yesterday = datetime.now() - timedelta(days=1)
            trade_date = yesterday.strftime('%Y%m%d')
        
        # 获取数据
        df = fetch_intraday_data(stock_code, trade_date, proxy=DEFAULT_PROXY)
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
        signals = detect_trading_signals(df_with_indicators, use_optimized)
        
        return df_with_indicators, signals
        
    except Exception as e:
        print(f"❌ 分析失败: {e}")
        import traceback
        traceback.print_exc()
        return None

def analyze_deviation_strategy(stock_code: str, trade_date: Optional[str] = None) -> Optional[Dict[str, any]]:
    """
    分析价格均线偏离策略的完整表现
    
    Args:
        stock_code: 股票代码
        trade_date: 交易日期
    
    Returns:
        策略表现字典
    """
    try:
        # 获取数据
        df = fetch_intraday_data(stock_code, trade_date, proxy=DEFAULT_PROXY)
        if df is None or df.empty:
            return None
        
        # 设置时间索引
        if '时间' in df.columns:
            df['时间'] = pd.to_datetime(df['时间'])
            df = df.set_index('时间')
        
        # 计算指标
        df_with_indicators = calculate_price_ma_deviation(df)
        
        # 获取优化后的信号
        optimized_buy_signals = df_with_indicators[df_with_indicators['Optimized_Buy_Signal']]
        optimized_sell_signals = df_with_indicators[df_with_indicators['Optimized_Sell_Signal']]
        
        # 分析交易对
        sorted_buys = sorted(optimized_buy_signals.index)
        sorted_sells = sorted(optimized_sell_signals.index)
        
        trades = []
        i, j = 0, 0
        while i < len(sorted_buys) and j < len(sorted_sells):
            if sorted_sells[j] > sorted_buys[i]:
                buy_price = df_with_indicators.loc[sorted_buys[i], '收盘']
                sell_price = df_with_indicators.loc[sorted_sells[j], '收盘']
                profit_pct = (sell_price / buy_price - 1) * 100
                time_diff = (sorted_sells[j] - sorted_buys[i]).total_seconds() / 60
                
                # 获取自适应参数
                volatility = df_with_indicators['Volatility'].iloc[0]
                adaptive_params = get_adaptive_parameters(volatility)
                
                if time_diff <= adaptive_params['max_holding_time']:
                    trades.append({
                        'buy_time': sorted_buys[i],
                        'sell_time': sorted_sells[j],
                        'buy_price': buy_price,
                        'sell_price': sell_price,
                        'profit_pct': profit_pct,
                        'time_diff_minutes': time_diff
                    })
                    
                    i += 1
                    j += 1
                else:
                    i += 1
            else:
                j += 1
        
        # 计算策略表现
        if trades:
            total_profit = sum(trade['profit_pct'] for trade in trades)
            successful_trades = sum(1 for trade in trades if trade['profit_pct'] > 0)
            success_rate = (successful_trades / len(trades)) * 100
            avg_profit = total_profit / len(trades)
            
            return {
                'stock_code': stock_code,
                'trade_date': trade_date,
                'volatility': df_with_indicators['Volatility'].iloc[0],
                'total_trades': len(trades),
                'successful_trades': successful_trades,
                'success_rate': success_rate,
                'total_profit': total_profit,
                'avg_profit': avg_profit,
                'trades': trades
            }
        else:
            return {
                'stock_code': stock_code,
                'trade_date': trade_date,
                'volatility': df_with_indicators['Volatility'].iloc[0],
                'total_trades': 0,
                'successful_trades': 0,
                'success_rate': 0,
                'total_profit': 0,
                'avg_profit': 0,
                'trades': []
            }
    except Exception as e:
        print(f"分析策略失败: {e}")
        return None

def main():
    """
    主函数 - 测试多只股票并进行性能对比
    """
    # 使用与综合T+0策略相同的测试股票集
    test_stocks = [
        # '000651',  # 格力电器 - 家电行业龙头
        '600030',  # 中信证券 - 券商龙头
        # '000002',  # 万科A - 地产龙头
        # '600519',  # 贵州茅台 - 白酒龙头
        # '002415',  # 海康威视 - 安防龙头
        # '300750',  # 宁德时代 - 新能源龙头
        # '601398',  # 工商银行 - 银行龙头
        # '600900',  # 长江电力 - 公用事业龙头
        # '601318',  # 中国平安 - 保险龙头
        '000333',  # 美的集团 - 家电龙头
    ]
    
    # 使用缓存数据的日期（2025-10-24）
    trade_date = '20251024'
    
    print(f"\n📊 开始测试价格均线偏离策略 - 优化版\n")
    print(f"测试日期: {trade_date}\n")
    
    # 总体统计
    total_trades_all = 0
    successful_trades_all = 0
    total_profit_all = 0
    results = []
    
    # 测试每只股票
    for stock in test_stocks:
        print(f"\n========================================")
        print(f"测试股票: {stock}")
        print(f"========================================")
        
        # 生成可视化图表
        chart_path = plot_tdx_intraday(stock, trade_date)
        if chart_path:
            print(f"图表已保存至: {chart_path}")
        
        # 分析策略表现
        result = analyze_deviation_strategy(stock, trade_date)
        if result:
            results.append(result)
            total_trades_all += result['total_trades']
            successful_trades_all += result['successful_trades']
            total_profit_all += result['total_profit']
            
            print(f"\n📈 {stock} 策略表现:")
            print(f"波动率: {result['volatility']:.2f}%")
            print(f"总交易对: {result['total_trades']}")
            print(f"成功交易: {result['successful_trades']}")
            print(f"成功率: {result['success_rate']:.2f}%")
            print(f"总收益率: {result['total_profit']:.2f}%")
            print(f"平均收益率: {result['avg_profit']:.2f}%")
    
    # 打印总体统计
    print(f"\n========================================")
    print(f"📊 价格均线偏离策略 - 总体表现统计")
    print(f"========================================")
    print(f"测试股票数量: {len(test_stocks)}")
    print(f"总交易对数量: {total_trades_all}")
    if total_trades_all > 0:
        overall_success_rate = (successful_trades_all / total_trades_all) * 100
        overall_avg_profit = total_profit_all / total_trades_all
        print(f"总体成功率: {overall_success_rate:.2f}%")
        print(f"总体平均收益率: {overall_avg_profit:.2f}%")
    else:
        print("无交易信号生成")
    
    # 按波动率分类统计
    low_vol_stocks = [r for r in results if r['volatility'] < 0.3]
    mid_vol_stocks = [r for r in results if 0.3 <= r['volatility'] < 0.8]
    high_vol_stocks = [r for r in results if r['volatility'] >= 0.8]
    
    print(f"\n📊 按波动率分类统计:")
    print(f"低波动股 (<0.3%): {len(low_vol_stocks)}只")
    print(f"中波动股 (0.3%-0.8%): {len(mid_vol_stocks)}只")
    print(f"高波动股 (>=0.8%): {len(high_vol_stocks)}只")

if __name__ == "__main__":
    main()