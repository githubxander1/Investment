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
    
    # 处理NaN值，使用前向填充
    df['收盘'].fillna(method='ffill', inplace=True)
    df['均价'].fillna(method='ffill', inplace=True)
    
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
    # 将偏离度放大50倍显示，使变化更明显
    df['Price_MA_Ratio_Amplified'] = (df['收盘'] / df['均价'] - 1) * 100 * 50
    # 正常偏离度
    df['Price_MA_Ratio'] = (df['收盘'] / df['均价'] - 1) * 100
    
    # 计算成交量移动平均和量比
    df['Volume_MA'] = df['成交量'].rolling(window=5, min_periods=1).mean()
    df['Volume_Ratio'] = df['成交量'] / df['Volume_MA']
    
    # 处理可能的无穷大值
    df['Volume_Ratio'].replace([np.inf, -np.inf], np.nan, inplace=True)
    
    # 成交量分析
    df['Volume_Increase'] = df['Volume_Ratio'] > 1.5  # 成交量放大
    df['Volume_Decrease'] = df['Volume_Ratio'] < 0.5  # 成交量萎缩
    
    # 策略参数（调整阈值以便更容易产生信号）
    buy_threshold = -0.5  # 低于均价0.5%时买入（放宽条件）
    sell_threshold = 0.5  # 高于均价0.5%时卖出（放宽条件）
    
    # 生成买卖信号
    # 买入信号：偏离度 < -0.5 且 成交量放大
    df['Buy_Signal'] = (df['Price_MA_Ratio'] < buy_threshold) & (df['Volume_Ratio'] > 1.2)  # 放宽成交量条件
    
    # 卖出信号：偏离度 > 0.5 且 (成交量放大 或 收盘价 > 均价)
    df['Sell_Signal'] = (df['Price_MA_Ratio'] > sell_threshold) & (
        (df['Volume_Ratio'] > 1.2) | (df['收盘'] > df['均价'])  # 放宽成交量条件
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


def fetch_intraday_data(stock_code: str, trade_date: str) -> Optional[pd.DataFrame]:
    """
    获取分时数据（优先从缓存读取，缓存不存在时从API获取）
    
    Args:
        stock_code: 股票代码
        trade_date: 交易日期
    
    Returns:
        分时数据DataFrame
    """
    logger.info(f"="*60)
    logger.info(f"开始加载分时数据")
    logger.info(f"股票代码: {stock_code}")
    logger.info(f"交易日期: {trade_date}")
    
    # 尝试使用akshare获取真实数据
    try:
        # 确保 trade_date 是正确的格式
        if isinstance(trade_date, str):
            try:
                # 尝试使用 YYYY-MM-DD 格式解析
                trade_date_obj = datetime.strptime(trade_date, '%Y-%m-%d')
                logger.info(f"日期格式: YYYY-MM-DD")
            except ValueError:
                try:
                    # 如果失败，尝试使用 YYYYMMDD 格式解析
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
        
        # 获取当前时间
        now = datetime.now()
        today_str = now.strftime('%Y%m%d')
        current_time = now.time()
        
        # 对于今天的数据，强制重新生成，不使用缓存
        if trade_date_str == today_str:
            logger.info(f"⚠️  今天的数据总是重新生成，不使用缓存，确保数据只到当前时间 {current_time}")
            # 删除缓存文件（如果存在）
            if os.path.exists(cache_file):
                os.remove(cache_file)
                logger.info(f"已删除旧缓存文件: {cache_file}")
        # 对于非今天的数据，如果缓存存在则使用缓存
        elif os.path.exists(cache_file):
            logger.info(f"✅ 从缓存文件读取历史数据")
            df = pd.read_csv(cache_file)
            
            # 处理时间列
            if '时间' in df.columns:
                df['时间'] = pd.to_datetime(df['时间'])
            
            return df
        
        # 缓存不存在或需要重新生成，尝试从API获取数据
        logger.info(f"❌ 缓存文件不存在或需要更新，尝试获取数据")
        
        # 使用当前日期格式（YYYY-MM-DD）
        api_date_format = trade_date_obj.strftime('%Y-%m-%d')
        
        # 尝试使用akshare获取真实数据
        try:
            logger.info(f"尝试使用akshare获取真实数据")
            
            # 根据股票代码添加市场标识
            if stock_code.startswith('6'):
                # 上海市场
                market_stock_code = f'sh{stock_code}'
            else:
                # 深圳市场
                market_stock_code = f'sz{stock_code}'
            
            # 使用akshare的stock_zh_a_minute接口获取分时数据
            # df = ak.stock_zh_a_minute(symbol=market_stock_code, period="1", adjust="qfq")
            df = ak.stock_zh_a_hist_min_em(symbol=market_stock_code, period="1", adjust="qfq")

            if df is not None and not df.empty:
                logger.info(f"✅ 成功获取akshare数据，数据行数: {len(df)}")
                logger.info(f"原始数据列名: {df.columns.tolist()}")
                logger.info(f"原始数据日期范围: {df['day'].min()} 到 {df['day'].max()}")
                logger.info(f"原始数据前5行:\n{df.head()}")
                
                # 确保列名正确
                if len(df.columns) >= 7:
                    df.columns = ['时间', '开盘', '收盘', '最高', '最低', '成交量', '成交额']
                elif len(df.columns) >= 6:
                    df.columns = ['时间', '开盘', '收盘', '最高', '最低', '成交量']
                    # 如果没有成交额列，我们可以通过价格和成交量计算
                    if '成交额' not in df.columns:
                        # 确保数据类型正确后再进行计算
                        df['开盘'] = pd.to_numeric(df['开盘'], errors='coerce')
                        df['收盘'] = pd.to_numeric(df['收盘'], errors='coerce')
                        df['成交量'] = pd.to_numeric(df['成交量'], errors='coerce')
                        df['成交额'] = ((df['开盘'] + df['收盘']) / 2 * df['成交量'] * 100).astype('float')  # 成交量单位是手
                
                logger.info(f"重命名后数据列名: {df.columns.tolist()}")
                logger.info(f"重命名后数据前5行:\n{df.head()}")
                
                # 过滤指定日期的数据
                df['时间'] = pd.to_datetime(df['时间'])
                df = df[df['时间'].dt.date == trade_date_obj.date()]
                
                logger.info(f"过滤指定日期({trade_date_obj.date()})后数据行数: {len(df)}")
                
                # 检查数据有效性，如果大部分数据是NaN，则尝试其他方法
                if df is not None and not df.empty:
                    valid_data_count = len(df.dropna(subset=['收盘', '开盘', '最高', '最低']))
                    logger.info(f"有效数据行数: {valid_data_count}")
                    
                    # 如果有效数据少于总数据的10%，则尝试其他方法
                    if valid_data_count < len(df) * 0.1:
                        logger.warning(f"akshare数据质量不佳，有效数据不足10%，尝试其他数据源")
                        df = None
                
                if df is not None and not df.empty:
                    logger.info(f"✅ 成功获取akshare数据，数据行数: {len(df)}")
                    
                    # 确保缓存目录存在
                    os.makedirs(cache_dir, exist_ok=True)
                    
                    # 保存到缓存
                    df.to_csv(cache_file, index=False)
                    logger.info(f"✅ 数据已保存到缓存: {cache_file}")
                    
                    # 处理数据格式
                    if '时间' in df.columns:
                        df['时间'] = pd.to_datetime(df['时间'])
                    
                    # 对于今天的数据，确保只包含到当前时间的数据
                    if trade_date_str == today_str and '时间' in df.columns:
                        # 过滤掉当前时间之后的数据
                        df = df[df['时间'].apply(lambda x: x.time() <= current_time)]
                        logger.info(f"⚠️  已过滤今天的数据，只保留到当前时间 {current_time} 的数据")
                        logger.info(f"过滤后剩余 {len(df)} 条数据")
                    
                    # 过滤午休时间
                    if '时间' in df.columns:
                        original_len = len(df)
                        df = df[~((df['时间'].dt.hour == 11) & (df['时间'].dt.minute >= 30)) & \
                                ~((df['时间'].dt.hour == 12))]
                        logger.info(f"过滤午休时间后: {len(df)} 行数据 (删除了 {original_len - len(df)} 行)")
                    
                    logger.info(f"数据列: {', '.join(df.columns.tolist())}")
                    logger.info(f"✅ 成功加载 {stock_code} 的分时数据")
                    logger.info(f"="*60)
                    
                    return df
                else:
                    logger.warning(f"指定日期({trade_date_obj.date()})没有数据或数据质量不佳")

        except Exception as e:
            logger.error(f"使用akshare获取数据失败: {e}")
            import traceback
            traceback.print_exc()
            
        # 如果akshare失败，尝试使用data2dfcf.py中的方法
        try:
            logger.info("尝试使用data2dfcf.py中的方法获取数据")
            # 导入data2dfcf.py中的函数
            sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
            from data2dfcf import get_eastmoney_fenshi_with_pandas
            
            # 构造secid (1表示沪市，0表示深市)
            if stock_code.startswith('6'):
                secid = f"1.{stock_code}"
            else:
                secid = f"0.{stock_code}"
                
            # 获取数据
            df = get_eastmoney_fenshi_with_pandas(secid=secid)
            
            if df is not None and not df.empty:
                logger.info(f"✅ 成功使用data2dfcf获取数据，数据行数: {len(df)}")
                
                # 重命名列以匹配所需格式
                df = df.rename(columns={
                    '时间': '时间',
                    '最新价': '收盘',
                    '成交量(手)': '成交量'
                })
                
                # 添加缺失的列
                if '开盘' not in df.columns:
                    df['开盘'] = df['收盘']
                if '最高' not in df.columns:
                    df['最高'] = df['收盘']
                if '最低' not in df.columns:
                    df['最低'] = df['收盘']
                if '成交额' not in df.columns:
                    # 确保数据类型正确后再进行计算
                    df['收盘'] = pd.to_numeric(df['收盘'], errors='coerce')
                    df['成交量'] = pd.to_numeric(df['成交量'], errors='coerce')
                    df['成交额'] = (df['收盘'] * df['成交量'] * 100).astype('float')  # 成交量单位是手，需要转换为股
                
                # 确保缓存目录存在
                os.makedirs(cache_dir, exist_ok=True)
                
                # 保存到缓存
                df.to_csv(cache_file, index=False)
                logger.info(f"✅ 数据已保存到缓存: {cache_file}")
                
                # 处理数据格式
                if '时间' in df.columns:
                    df['时间'] = pd.to_datetime(df['时间'])
                
                logger.info(f"数据列: {', '.join(df.columns.tolist())}")
                logger.info(f"✅ 成功加载 {stock_code} 的分时数据")
                logger.info(f"="*60)
                
                return df
        except Exception as e:
            logger.error(f"使用data2dfcf获取数据失败: {e}")
            import traceback
            traceback.print_exc()
        
        logger.error(f"❌ 无法获取分时数据")
        return None
    except Exception as e:
        logger.error(f"fetch_intraday_data 函数执行失败: {e}")
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
        # 发送买入信号通知
        notify_signal('buy', '000333', row['收盘'], signal_time.strftime('%Y-%m-%d %H:%M:%S'))
    
    # 检测卖出信号
    sell_signals = df[df['Sell_Signal']]
    for idx, row in sell_signals.iterrows():
        if isinstance(idx, str):
            signal_time = pd.to_datetime(idx)
        else:
            signal_time = idx
        signals['sell_signals'].append((signal_time, row['收盘']))
        # 发送卖出信号通知
        notify_signal('sell', '000333', row['收盘'], signal_time.strftime('%Y-%m-%d %H:%M:%S'))
    
    return signals


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
        fig.suptitle(f'{stock_code} 价格成交量偏离策略图 ({formatted_date})', fontsize=16)
        
        # 过滤掉无效数据
        df_filtered = df_with_indicators.dropna(subset=['收盘', '均价', 'Price_MA_Ratio', 'Volume_Ratio'])
        
        if df_filtered.empty:
            print("警告: 过滤后的数据为空")
            return None
            
        print(f"过滤后的数据行数: {len(df_filtered)}")
        print(f"数据列: {', '.join(df_filtered.columns.tolist())}")
        
        # 绘制价格和均价
        ax1.plot(range(len(df_filtered)), df_filtered['收盘'], label='收盘价', color='black', linewidth=1)
        ax1.plot(range(len(df_filtered)), df_filtered['均价'], label='均价', color='blue', linewidth=1)
        
        # 绘制买入信号
        for i, (idx, row) in enumerate(df_filtered.iterrows()):
            if row.get('Buy_Signal', False):
                ax1.scatter(i, row['收盘'] * 0.995, marker='^', color='red', s=100, zorder=5)
                ax1.text(i, row['收盘'] * 0.99, '买',
                         color='red', fontsize=12, ha='center', va='top', fontweight='bold')
        
        # 绘制卖出信号
        for i, (idx, row) in enumerate(df_filtered.iterrows()):
            if row.get('Sell_Signal', False):
                ax1.scatter(i, row['收盘'] * 1.005, marker='v', color='green', s=100, zorder=5)
                ax1.text(i, row['收盘'] * 1.01, '卖',
                         color='green', fontsize=12, ha='center', va='bottom', fontweight='bold')
        
        ax1.set_ylabel('价格', fontsize=12)
        ax1.grid(True, linestyle='--', alpha=0.7)
        ax1.legend()
        
        # 绘制价格与均价的比率
        ax2.plot(range(len(df_filtered)), df_filtered['Price_MA_Ratio'], label='价格与均价偏离比率(%)', color='purple', linewidth=1)
        ax2.plot(range(len(df_filtered)), df_filtered['Price_MA_Ratio_Amplified'], label='偏离比率放大50倍', color='orange', linewidth=1)
        ax2.axhline(y=0, color='black', linestyle='-', alpha=0.5)
        ax2.axhline(y=0.3, color='green', linestyle='--', alpha=0.7, label='卖出阈值')
        ax2.axhline(y=-0.3, color='red', linestyle='--', alpha=0.7, label='买入阈值')
        ax2.set_ylabel('偏离比率(%)', fontsize=12)
        ax2.grid(True, linestyle='--', alpha=0.7)
        ax2.legend()
        
        # 绘制量比
        ax3.plot(range(len(df_filtered)), df_filtered['Volume_Ratio'], label='量比', color='brown', linewidth=1)
        ax3.axhline(y=1.5, color='green', linestyle='--', alpha=0.7, label='放量阈值')
        ax3.axhline(y=0.5, color='red', linestyle='--', alpha=0.7, label='缩量阈值')
        ax3.axhline(y=1.0, color='gray', linestyle='-', alpha=0.5)
        ax3.set_ylabel('量比', fontsize=12)
        ax3.set_xlabel('时间', fontsize=12)
        ax3.grid(True, linestyle='--', alpha=0.7)
        ax3.legend()
        
        # 设置x轴标签为时间
        time_labels = df_filtered.index.strftime('%H:%M') if hasattr(df_filtered.index, 'strftime') else df_filtered.index
        # 只显示部分时间标签，避免拥挤
        step = max(1, len(time_labels) // 15)
        ax3.set_xticks(range(0, len(time_labels), step))
        ax3.set_xticklabels(time_labels[::step], rotation=45)
        
        # 调整布局
        plt.tight_layout()
        
        # 保存图表
        output_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'output', 'charts')
        os.makedirs(output_dir, exist_ok=True)
        chart_path = os.path.join(output_dir, f'{stock_code}_price_volume_deviation_{formatted_date.replace("-", "")}.png')
        plt.savefig(chart_path, dpi=300, bbox_inches='tight')
        plt.close()
        
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
            yesterday = datetime.now() - timedelta(days=1)
            trade_date = yesterday.strftime('%Y%m%d')
        
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
    stock_code = "600030"  # 美的集团
    trade_date = '20251030'
    
    result = analyze_strategy(stock_code, trade_date)
    if result:
        df_with_indicators, signals = result
        print(f"📊 检测到 {len(signals['buy_signals'])} 个买入信号和 {len(signals['sell_signals'])} 个卖出信号")

        # 绘制图表
        plot_strategy_chart(stock_code, trade_date)