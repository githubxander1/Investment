#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
价格均线偏离指标模块 (price_ma_deviation.py)

该模块实现了基于价格与均线偏离度的交易策略指标计算与分析功能，包括：
1. 价格与均线的偏离度计算（差值和百分比）
2. 基于偏离度的买卖信号生成
3. 策略回测与绩效分析
4. 可视化展示

使用方法：
    可以调用calculate_price_ma_deviation计算指标，或使用analyze_deviation_strategy进行完整策略分析

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

logger = setup_logger('price_ma_deviation')

# 设置中文字体支持
plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False


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
    
    # 计算指定周期的移动平均线
    df['MA'] = df['收盘'].rolling(window=ma_period, min_periods=1).mean()
    
    # 修改计算逻辑：使用移动平均线（MA）代替均价来计算偏离度
    print(f"使用{ma_period}周期移动平均线计算偏离度")
    
    # 计算价格与移动均线的差值和比率
    df['Price_MA_Diff'] = df['收盘'] - df['MA']
    # 确保分母不为零，避免除以零错误
    df['Price_MA_Ratio'] = np.where(df['MA'] != 0, (df['收盘'] / df['MA'] - 1) * 100, 0)
    
    # 策略参数
    buy_threshold = -0.3  # 低于均线0.3%时买入
    sell_threshold = 0.3  # 高于均线0.3%时卖出
    
    # 生成买卖信号
    base_buy_signal = (df['Price_MA_Ratio'] <= buy_threshold) & (df['Price_MA_Ratio'].shift(1) > buy_threshold)
    base_sell_signal = (df['Price_MA_Ratio'] >= sell_threshold) & (df['Price_MA_Ratio'].shift(1) < sell_threshold)
    
    df['Buy_Signal'] = base_buy_signal
    df['Sell_Signal'] = base_sell_signal
    
    # 添加详细日志，显示Price_MA_Ratio列的统计信息
    print(f"价格均线偏离策略：共检测到 {len(df[df['Buy_Signal']])} 个买入信号和 {len(df[df['Sell_Signal']])} 个卖出信号")
    print(f"Price_MA_Ratio统计信息：")
    print(f"- 最大值: {df['Price_MA_Ratio'].max():.4f}%")
    print(f"- 最小值: {df['Price_MA_Ratio'].min():.4f}%")
    print(f"- 平均值: {df['Price_MA_Ratio'].mean():.4f}%")
    print(f"- 非零值数量: {len(df[df['Price_MA_Ratio'] != 0])}")
    print(f"- 空值数量: {df['Price_MA_Ratio'].isnull().sum()}")
    
    # 显示前几行的详细数据用于调试
    print("\n前5行数据示例：")
    if not df.empty:
        # 选择关键列显示
        key_columns = ['收盘', 'MA', 'Price_MA_Diff', 'Price_MA_Ratio', 'Buy_Signal', 'Sell_Signal']
        display_columns = [col for col in key_columns if col in df.columns]
        print(df[display_columns].head())
    
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
            df = ak.stock_zh_a_minute(symbol=market_stock_code, period="1", adjust="qfq")
            
            # 转换列名以匹配所需格式
            df.columns = ['时间', '开盘', '收盘', '最高', '最低', '成交量', '成交额']
            
            # 过滤指定日期的数据
            df['时间'] = pd.to_datetime(df['时间'])
            df = df[df['时间'].dt.date == trade_date_obj.date()]
            
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
                
                # 过滤掉午休时间
                original_len = len(df)
                if '时间' in df.columns:
                    df = df[~((df['时间'].dt.hour == 11) & (df['时间'].dt.minute >= 30)) & \
                            ~((df['时间'].dt.hour == 12))]
                    logger.info(f"过滤午休时间后: {len(df)} 行数据 (删除了 {original_len - len(df)} 行)")
                
                logger.info(f"数据列: {', '.join(df.columns.tolist())}")
                logger.info(f"✅ 成功加载 {stock_code} 的分时数据")
                logger.info(f"="*60)
                
                return df
        except Exception as e:
            logger.error(f"使用akshare获取数据失败: {e}")
        
        # 如果akshare获取失败，尝试使用备用方法
        try:
            logger.info(f"尝试使用备用方法获取数据")
            # 导入get_fenshi_data函数
            from T0.indicators.comprehensive_t0_strategy import get_fenshi_data
            # 使用备用方法
            df = get_fenshi_data(stock_code=stock_code, date=api_date_format)
            
            if df is not None and not df.empty:
                logger.info(f"✅ 成功获取数据，数据行数: {len(df)}")
                
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
                
                # 过滤掉午休时间
                original_len = len(df)
                if '时间' in df.columns:
                    df = df[~((df['时间'].dt.hour == 11) & (df['时间'].dt.minute >= 30)) & \
                            ~((df['时间'].dt.hour == 12))]
                    logger.info(f"过滤午休时间后: {len(df)} 行数据 (删除了 {original_len - len(df)} 行)")
                
                logger.info(f"数据列: {', '.join(df.columns.tolist())}")
                logger.info(f"✅ 成功加载 {stock_code} 的分时数据")
                logger.info(f"="*60)
                
                return df
        except Exception as e:
            logger.error(f"获取数据失败: {e}")
        
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
        df = fetch_intraday_data(stock_code, date_for_data)
        if df is None or df.empty:
            return None
        
        # 设置时间索引（与resistance_support_indicators.py保持一致）
        df = df.copy()
        if '时间' in df.columns:
            df['时间'] = pd.to_datetime(df['时间'])
            df = df.set_index('时间')
        
        # 计算指标
        df_with_indicators = calculate_price_ma_deviation(df)
        
        # 确保Price_MA_Ratio列存在且不为空
        if 'Price_MA_Ratio' not in df_with_indicators.columns:
            print("警告: 数据中没有Price_MA_Ratio列")
            return None
            
        if df_with_indicators['Price_MA_Ratio'].isnull().all():
            print("警告: Price_MA_Ratio列全部为空")
            return None
        
        # 创建图形和子图
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(16, 10), gridspec_kw={'height_ratios': [3, 1]})
        fig.suptitle(f'{stock_code} 价格均线偏离策略图 ({formatted_date})', fontsize=16)
        
        # 过滤掉无效数据
        df_filtered = df_with_indicators.dropna(subset=['收盘', 'Price_MA_Ratio'])
        
        if df_filtered.empty:
            print("警告: 过滤后的数据为空")
            return None
            
        print(f"过滤后的数据行数: {len(df_filtered)}")
        print(f"数据列: {', '.join(df_filtered.columns.tolist())}")
        
        # 绘制价格和均价（使用接口返回的均价数据）
        ax1.plot(range(len(df_filtered)), df_filtered['收盘'], label='收盘价', color='black', linewidth=1)
        if '均价' in df_filtered.columns:
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
        output_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'output', 'charts')
        os.makedirs(output_dir, exist_ok=True)
        chart_path = os.path.join(output_dir, f'{stock_code}_price_ma_deviation_{formatted_date.replace("-", "")}.png')
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
    trade_date = '20251027'
    
    result = analyze_price_ma_deviation(stock_code, trade_date)
    if result:
        df_with_indicators, signals = result
        print(f"📊 检测到 {len(signals['buy_signals'])} 个买入信号和 {len(signals['sell_signals'])} 个卖出信号")
        
        # 绘制图表
        plot_tdx_intraday(stock_code, trade_date)