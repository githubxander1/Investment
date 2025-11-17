#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ETF测试脚本

使用price_ma_deviation_optimized.py测试510330恒生互联网ETF和510050中概互联网ETF
"""

import os
import sys
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import matplotlib.pyplot as plt

# 添加当前目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# 导入价格均线偏离指标模块
try:
    import price_ma_deviation_optimized as pmdo
except ImportError as e:
    print(f"导入price_ma_deviation_optimized模块失败: {e}")
    sys.exit(1)

def get_real_etf_intraday_data(stock_code, trade_date):
    """
    使用akshare获取真实的ETF分时数据
    
    Args:
        stock_code: ETF代码
        trade_date: 交易日期，格式为'YYYYMMDD'
    
    Returns:
        pandas.DataFrame: 包含ETF分时数据的数据框
    """
    try:
        print(f"正在使用akshare获取{stock_code}的真实分时数据...")
        
        # 使用akshare获取ETF分时数据
        # 注意：akshare的接口可能会更新，这里使用通用的ETF分时数据接口
        import akshare as ak
        
        # 转换日期格式
        date_obj = datetime.strptime(trade_date, '%Y%m%d')
        date_str = date_obj.strftime('%Y-%m-%d')
        
        # 尝试使用akshare获取ETF分时数据
        # 注意：不同市场的ETF可能需要不同的接口
        try:
            # 尝试获取A股ETF分时数据
            df = ak.fund_etf_hist_sina(symbol=stock_code)
            print(f"成功获取A股ETF分时数据，共{len(df)}条记录")
        except Exception as e:
            print(f"获取A股ETF分时数据失败，尝试其他接口: {e}")
            # 如果失败，尝试获取股票分时数据接口（某些ETF可能走这个接口）
            df = ak.stock_zh_a_minute(symbol=stock_code, period='1', adjust='qfq')
            print(f"成功获取股票分时数据，共{len(df)}条记录")
        
        # 检查数据格式并转换为我们需要的格式
        print(f"原始数据列: {', '.join(df.columns.tolist())}")
        
        # 处理数据格式，确保包含必要的列
        result_df = pd.DataFrame()
        
        # 映射不同接口返回的列名到我们需要的格式
        column_mapping = {
            'date': '时间',
            'datetime': '时间',
            'time': '时间',
            'close': '收盘',
            'volume': '成交量',
            'amount': '成交额',
            'volume_amount': '成交额',
            'volume_total': '成交量',
            'price': '收盘'
        }
        
        for col in df.columns:
            lower_col = col.lower()
            for key, target in column_mapping.items():
                if key in lower_col and target not in result_df.columns:
                    result_df[target] = df[col]
                    break
        
        # 如果缺少必要的列，尝试计算
        if '收盘' not in result_df.columns:
            # 假设第一个价格列是收盘价
            if len(df.columns) > 1:
                price_cols = [col for col in df.columns if any(x in col.lower() for x in ['price', 'close', '收盘'])]
                if price_cols:
                    result_df['收盘'] = df[price_cols[0]]
        
        if '成交量' not in result_df.columns:
            # 尝试找成交量相关的列
            volume_cols = [col for col in df.columns if any(x in col.lower() for x in ['volume', 'vol', '成交量'])]
            if volume_cols:
                result_df['成交量'] = df[volume_cols[0]]
        
        if '成交额' not in result_df.columns and '收盘' in result_df.columns and '成交量' in result_df.columns:
            result_df['成交额'] = result_df['收盘'] * result_df['成交量']
        
        # 确保时间列格式正确
        if '时间' in result_df.columns:
            # 尝试转换时间格式
            try:
                # 如果是字符串格式的时间
                if isinstance(result_df['时间'].iloc[0], str):
                    # 检查是否已经包含日期
                    if len(result_df['时间'].iloc[0]) <= 8:  # 假设纯时间格式如'09:30:00'
                        # 添加日期
                        result_df['时间'] = pd.to_datetime(trade_date + ' ' + result_df['时间'])
                    else:
                        result_df['时间'] = pd.to_datetime(result_df['时间'])
            except Exception as e:
                print(f"时间格式转换失败: {e}")
                # 如果转换失败，创建新的时间序列
                trading_hours = []
                # 上午时段 9:30-11:30
                for hour in range(9, 12):
                    start_minute = 30 if hour == 9 else 0
                    end_minute = 30 if hour == 11 else 60
                    for minute in range(start_minute, end_minute):
                        trading_hours.append(f"{hour:02d}:{minute:02d}")
                # 下午时段 13:00-15:00
                for hour in range(13, 15):
                    for minute in range(0, 60):
                        trading_hours.append(f"{hour:02d}:{minute:02d}")
                
                # 截取或填充到数据长度
                if len(trading_hours) > len(result_df):
                    trading_hours = trading_hours[:len(result_df)]
                elif len(trading_hours) < len(result_df):
                    # 如果数据长度超过交易时间，可能是不同的时间粒度
                    pass
                
                # 创建时间戳
                full_times = [datetime.strptime(f"{trade_date} {t}", "%Y%m%d %H:%M") for t in trading_hours]
                result_df['时间'] = full_times[:len(result_df)]
        
        # 设置时间索引
        result_df = result_df.set_index('时间')
        
        # 计算均价列
        if '均价' not in result_df.columns and '成交额' in result_df.columns and '成交量' in result_df.columns:
            result_df['均价'] = result_df['成交额'] / result_df['成交量']
            result_df['均价'] = result_df['均价'].fillna(method='ffill').fillna(method='bfill')
        
        print(f"处理后的数据列: {', '.join(result_df.columns.tolist())}")
        print(f"数据时间范围: {result_df.index.min()} 到 {result_df.index.max()}")
        
        return result_df
    except Exception as e:
        print(f"获取真实ETF分时数据失败: {e}")
        import traceback
        traceback.print_exc()
        return None

def test_etf(stock_code, stock_name, trade_date=None):
    """
    测试单个ETF的价格均线偏离策略
    
    Args:
        stock_code: ETF代码
        stock_name: ETF名称
        trade_date: 交易日期，默认为最近的一个交易日
    """
    print(f"=" * 70)
    print(f"开始测试 {stock_name} ({stock_code})")
    print(f"=" * 70)
    
    # 如果没有指定交易日期，使用当前日期
    if trade_date is None:
        today = datetime.now()
        # 如果今天是周末，往前推到最近的交易日
        if today.weekday() >= 5:  # 周六或周日
            today = today - timedelta(days=today.weekday() - 4)
        trade_date = today.strftime('%Y%m%d')
    
    print(f"测试日期: {trade_date}")
    
    try:
        # 首先尝试使用akshare获取真实的ETF分时数据
        df = get_real_etf_intraday_data(stock_code, trade_date)
        
        # 如果真实数据获取失败，尝试从缓存获取
        if df is None or df.empty:
            print(f"尝试从缓存获取{stock_name}的分时数据...")
            df = pmdo.fetch_intraday_data(stock_code, trade_date)
        
        # 如果所有数据获取方式都失败，才考虑使用模拟数据
        if df is None or df.empty:
            print(f"警告: 无法获取{stock_name}的真实分时数据，尝试使用模拟数据进行测试")
            # 创建模拟数据用于测试
            df = create_mock_data(stock_code, trade_date)
        
        # 确保数据包含必要的列
        required_columns = ['收盘', '成交量', '成交额']
        for col in required_columns:
            if col not in df.columns:
                print(f"警告: 数据缺少必要的列 '{col}'，尝试生成...")
                if col == '收盘':
                    # 生成模拟收盘价数据
                    base_price = 1.0 + np.random.random() * 0.5
                    price_changes = np.random.normal(0, 0.001, len(df))
                    df['收盘'] = base_price * np.exp(np.cumsum(price_changes))
                elif col == '成交量':
                    # 生成模拟成交量数据
                    base_volume = 10000000 + np.random.randint(0, 5000000)
                    volume_changes = np.random.normal(0, base_volume * 0.1, len(df))
                    df['成交量'] = np.maximum(base_volume + volume_changes, 100000)
                elif col == '成交额':
                    # 根据收盘价和成交量计算成交额
                    if '收盘' in df.columns and '成交量' in df.columns:
                        df['成交额'] = df['收盘'] * df['成交量']
        
        # 计算均价列（如果不存在）
        if '均价' not in df.columns and '成交额' in df.columns and '成交量' in df.columns:
            df['均价'] = df['成交额'] / df['成交量']
            df['均价'] = df['均价'].fillna(method='ffill').fillna(method='bfill')
        
        print(f"数据准备完成，共{len(df)}条记录")
        print(f"数据列: {', '.join(df.columns.tolist())}")
        print(f"价格范围: {df['收盘'].min():.4f} - {df['收盘'].max():.4f}")
        
        # 使用价格均线偏离指标进行分析
        print(f"\n正在使用价格均线偏离策略分析{stock_name}...")
        result_df = pmdo.calculate_price_ma_deviation(df)
        
        # 统计信号数量
        buy_signals = result_df['Optimized_Buy_Signal'].sum()
        sell_signals = result_df['Optimized_Sell_Signal'].sum()
        
        print(f"\n{stock_name} ({stock_code}) 分析结果:")
        print(f"找到 {buy_signals} 个优化买入信号")
        print(f"找到 {sell_signals} 个优化卖出信号")
        
        # 可视化结果（可选）
        visualize_results(result_df, stock_code, stock_name, trade_date)
        
        print(f"\n{stock_name} 测试完成")
        print(f"=" * 70)
        
        return result_df
        
    except Exception as e:
        print(f"测试{stock_name}时出错: {e}")
        import traceback
        traceback.print_exc()
        return None

def create_mock_data(stock_code, trade_date):
    """
    创建模拟的分时数据用于测试（仅作为最后的备选）
    
    Args:
        stock_code: ETF代码
        trade_date: 交易日期
    
    Returns:
        模拟的分时数据DataFrame
    """
    print("创建模拟分时数据（仅作为备选方案）...")
    
    # 创建时间序列（9:30-11:30, 13:00-15:00）
    morning_times = [f"09:{minute:02d}" for minute in range(30, 60)] + \
                   [f"10:{minute:02d}" for minute in range(0, 60)] + \
                   [f"11:{minute:02d}" for minute in range(0, 30)]
    afternoon_times = [f"13:{minute:02d}" for minute in range(0, 60)] + \
                     [f"14:{minute:02d}" for minute in range(0, 60)]
    
    times = morning_times + afternoon_times
    
    # 创建完整的时间戳
    full_times = []
    date_str = trade_date
    for t in times:
        hour, minute = map(int, t.split(':'))
        full_times.append(datetime.strptime(f"{date_str} {t}", "%Y%m%d %H:%M"))
    
    # 创建DataFrame
    df = pd.DataFrame({'时间': full_times})
    df = df.set_index('时间')
    
    # 根据ETF代码设置更真实的基础价格和波动性
    if stock_code == '510330':  # 恒生互联网ETF
        base_price = 1.1 + np.random.random() * 0.2  # 价格区间约1.1-1.3
        volatility = 0.003  # 波动性略高
    elif stock_code == '510050':  # 中概互联网ETF
        base_price = 0.9 + np.random.random() * 0.2  # 价格区间约0.9-1.1
        volatility = 0.0025  # 中等波动性
    else:
        base_price = 1.0 + np.random.random() * 0.5
        volatility = 0.002
    
    # 生成更真实的价格数据，包含趋势和反转
    trend_direction = np.random.choice([-1, 1])  # 随机趋势方向
    trend_strength = np.linspace(0, trend_direction * 0.01, len(df))  # 缓慢变化的趋势
    
    # 添加一些反转点
    reversal_points = np.random.choice(range(30, len(df)-30), size=3, replace=False)  # 避免在开头和结尾反转
    for rp in sorted(reversal_points):
        trend_strength[rp:] = trend_strength[rp] - (trend_strength[rp:] - trend_strength[rp]) * 1.5
    
    # 添加周期性波动（模拟市场周期）
    periodic = 0.005 * np.sin(np.linspace(0, 4 * np.pi, len(df)))
    
    # 添加随机噪声
    noise = volatility * np.random.randn(len(df))
    
    # 组合生成价格
    df['收盘'] = base_price * (1 + trend_strength + periodic + noise)
    
    # 添加一些异常点（模拟短期的价格波动和交易机会）
    anomaly_indices = np.random.choice(range(len(df)), size=8, replace=False)
    for idx in anomaly_indices:
        # 生成更大幅度的异常波动，创造交易信号
        direction = np.random.choice([-1, 1])
        df.iloc[idx, df.columns.get_loc('收盘')] *= (1 + direction * (0.01 + 0.02 * np.random.random()))
    
    # 生成更真实的成交量数据，与价格变动相关
    base_volume = 10000000 + np.random.randint(0, 10000000)  # ETF成交量通常较大
    
    # 基础成交量模式：开盘和收盘较高
    volume_pattern = np.ones(len(df))
    volume_pattern[:60] *= 1.8  # 开盘较高
    volume_pattern[-60:] *= 2.0  # 收盘较高
    
    # 价格波动大时成交量也会增大
    price_changes = np.abs(df['收盘'].pct_change())
    volume_responsive = 1 + 3 * price_changes.fillna(0)
    
    # 随机波动
    volume_noise = 0.2 * np.random.randn(len(df))
    
    # 组合生成成交量
    df['成交量'] = base_volume * volume_pattern * volume_responsive * np.exp(volume_noise)
    df['成交量'] = df['成交量'].astype(int)
    
    # 计算成交额
    df['成交额'] = df['收盘'] * df['成交量']
    
    # 计算均价
    df['均价'] = df['成交额'] / df['成交量']
    
    print(f"创建了{len(df)}条更真实的模拟数据，基础价格: {base_price:.4f}, 波动性: {volatility}")
    return df

def visualize_results(df, stock_code, stock_name, trade_date):
    """
    可视化分析结果
    
    Args:
        df: 分析结果DataFrame
        stock_code: ETF代码
        stock_name: ETF名称
        trade_date: 交易日期
    """
    try:
        # 检查是否有matplotlib
        import matplotlib.pyplot as plt
        
        # 设置中文字体
        plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'DejaVu Sans']
        plt.rcParams['axes.unicode_minus'] = False
        
        # 创建图形
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(15, 12), gridspec_kw={'height_ratios': [3, 1]})
        fig.suptitle(f'{stock_name} ({stock_code}) 价格均线偏离分析 - {trade_date}', fontsize=16)
        
        # 绘制价格和均线
        ax1.plot(df.index, df['收盘'], label='收盘价')
        if 'MA' in df.columns:
            ax1.plot(df.index, df['MA'], label='5分钟均线', color='orange')
        if '均价' in df.columns:
            ax1.plot(df.index, df['均价'], label='均价', color='green', linestyle='--')
        
        # 标记买入和卖出信号
        buy_signals = df[df['Optimized_Buy_Signal']]
        sell_signals = df[df['Optimized_Sell_Signal']]
        
        ax1.scatter(buy_signals.index, buy_signals['收盘'], marker='^', color='red', s=100, label='买入信号')
        ax1.scatter(sell_signals.index, sell_signals['收盘'], marker='v', color='green', s=100, label='卖出信号')
        
        ax1.set_title('价格走势与交易信号')
        ax1.set_ylabel('价格')
        ax1.grid(True)
        ax1.legend()
        
        # 绘制偏离率
        ax2.plot(df.index, df['Price_MA_Ratio'], label='价格均价偏离率(%)', color='purple')
        ax2.axhline(y=0, color='black', linestyle='-', alpha=0.3)
        
        # 标记买入和卖出阈值（如果有）
        if 'Adaptive_Params' in df.columns and df['Adaptive_Params'].iloc[0]:
            try:
                import ast
                params = ast.literal_eval(df['Adaptive_Params'].iloc[0])
                if 'buy_threshold' in params:
                    ax2.axhline(y=params['buy_threshold'], color='red', linestyle='--', alpha=0.5, label=f'买入阈值: {params["buy_threshold"]}%')
                if 'sell_threshold' in params:
                    ax2.axhline(y=params['sell_threshold'], color='green', linestyle='--', alpha=0.5, label=f'卖出阈值: {params["sell_threshold"]}%')
            except:
                pass
        
        ax2.set_title('价格均价偏离率')
        ax2.set_xlabel('时间')
        ax2.set_ylabel('偏离率(%)')
        ax2.grid(True)
        ax2.legend()
        
        # 调整布局
        plt.tight_layout()
        plt.subplots_adjust(top=0.92)
        
        # 保存图像
        output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'output', 'charts')
        os.makedirs(output_dir, exist_ok=True)
        output_file = os.path.join(output_dir, f'{stock_code}_{trade_date}_analysis.png')
        plt.savefig(output_file)
        print(f"分析图表已保存至: {output_file}")
        
        # 显示图表（可选，批处理时可注释掉）
        # plt.show()
        
        plt.close()
        
    except Exception as e:
        print(f"可视化时出错: {e}")

def main():
    """
    主函数，测试两个ETF
    """
    print(f"ETF价格均线偏离策略测试 - 使用真实ETF分时数据")
    print(f"=" * 50)
    
    # 可以选择测试特定日期的数据，默认使用最近的交易日
    # 如果需要测试特定日期，取消下面的注释并设置日期
    # trade_date = '20251114'  # 示例日期
    trade_date = None  # 使用默认最近交易日
    
    # 测试510330恒生互联网ETF
    print(f"\n测试510330恒生互联网ETF...")
    result1 = test_etf('510330', '恒生互联网ETF', trade_date)
    
    # 测试510050中概互联网ETF
    print(f"\n测试510050中概互联网ETF...")
    result2 = test_etf('510050', '中概互联网ETF', trade_date)
    
    # 汇总分析
    if result1 is not None and result2 is not None:
        print(f"\n" + "=" * 50)
        print(f"测试结果汇总:")
        print(f"510330恒生互联网ETF: {result1['Optimized_Buy_Signal'].sum()}个买入信号, {result1['Optimized_Sell_Signal'].sum()}个卖出信号")
        print(f"510050中概互联网ETF: {result2['Optimized_Buy_Signal'].sum()}个买入信号, {result2['Optimized_Sell_Signal'].sum()}个卖出信号")
        
        # 分析策略参数
        print(f"\n策略参数分析:")
        for idx, result in enumerate([result1, result2], 1):
            etf_name = '恒生互联网ETF' if idx == 1 else '中概互联网ETF'
            if 'Volatility' in result.columns:
                volatility = result['Volatility'].iloc[0]
                print(f"{etf_name} 波动率: {volatility:.4f}%")
            if 'Adaptive_Params' in result.columns and result['Adaptive_Params'].iloc[0]:
                try:
                    import ast
                    params = ast.literal_eval(result['Adaptive_Params'].iloc[0])
                    print(f"{etf_name} 自适应参数: {params}")
                except:
                    pass
        print(f"=" * 50)
    
    print(f"\n测试完成!")

if __name__ == "__main__":
    main()
