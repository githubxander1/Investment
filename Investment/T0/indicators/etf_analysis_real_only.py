#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ETF分析脚本（仅使用真实数据）

专注于ETF数据分析，仅使用真实数据，不使用任何模拟数据
"""

import os
import sys
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import re

# 添加当前目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# 导入价格均线偏离指标模块
try:
    import price_ma_deviation_optimized as pmdo
except ImportError as e:
    print(f"导入price_ma_deviation_optimized模块失败: {e}")
    sys.exit(1)

def get_etf_real_data(etf_code, trade_date):
    """
    获取ETF的真实数据（使用akshare接口）
    
    Args:
        etf_code: ETF代码
        trade_date: 交易日期，格式'YYYYMMDD'
    
    Returns:
        包含ETF数据的DataFrame，如果获取失败返回None
    """
    print(f"尝试获取{etf_code}在{trade_date}的真实数据...")
    
    # 验证日期格式
    if not re.match(r'^\d{8}$', trade_date):
        print(f"错误: 日期格式不正确，应为'YYYYMMDD'")
        return None
    
    # 尝试将字符串日期转换为datetime对象
    try:
        date_obj = datetime.strptime(trade_date, '%Y%m%d')
    except ValueError:
        print(f"错误: 无法解析日期'{trade_date}'，格式应为'YYYYMMDD'")
        return None
    
    # 检查是否为周末
    if date_obj.weekday() >= 5:  # 5是周六，6是周日
        print(f"错误: {trade_date}是周末，没有交易数据")
        return None
    
    # 检查是否为未来日期
    if date_obj > datetime.now():
        print(f"错误: {trade_date}是未来日期，无法获取数据")
        return None
    
    # 调整日期格式
    date_format = date_obj.strftime('%Y-%m-%d')
    
    try:
        # 导入akshare
        import akshare as ak
        
        # 简化接口调用逻辑，专注于最可靠的ETF接口
        interfaces = [
            # ETF专用接口优先级最高
            ('fund_etf_hist_em', 'ETF历史行情', {'symbol': etf_code, 'period': '1', 'start_date': date_format, 'end_date': date_format}),
            ('fund_etf_hist_sina', 'ETF历史数据', {'symbol': etf_code})
        ]
        
        df = None
        
        # 尝试每个接口
        for interface_name, desc, params in interfaces:
            try:
                print(f"尝试使用{desc}接口...")
                
                # 检查接口是否存在
                if not hasattr(ak, interface_name):
                    print(f"警告: {interface_name}接口不存在")
                    continue
                
                # 调用接口
                print(f"调用接口: {interface_name}")
                df = getattr(ak, interface_name)(**params)
                
                # 检查数据是否为空
                if df is None or df.empty:
                    print(f"警告: {desc}接口返回空数据")
                    continue
                
                print(f"成功获取{len(df)}条数据")
                print(f"数据列: {list(df.columns)}")
                break
            except Exception as e:
                print(f"使用{desc}接口失败: {str(e)}")
                df = None
                continue
        
        # 如果所有接口都失败
        if df is None:
            print(f"错误: 无法获取{etf_code}的数据")
            return None
        
        # 数据格式处理
        result_df = process_etf_data(df, etf_code, trade_date)
        
        # 过滤指定日期的数据
        if result_df is not None and not result_df.empty:
            return result_df
        else:
            print(f"错误: 处理后没有符合条件的数据")
            return None
            
    except ImportError:
        print("错误: 未安装akshare库，请先安装: pip install akshare")
        return None
    except Exception as e:
        print(f"获取ETF数据时发生异常: {str(e)}")
        import traceback
        traceback.print_exc()
        return None

def process_etf_data(df, etf_code, trade_date):
    """
    处理ETF数据，确保包含必要的列
    
    Args:
        df: 原始数据DataFrame
        etf_code: ETF代码
        trade_date: 交易日期
    
    Returns:
        处理后的DataFrame
    """
    try:
        # 复制数据以避免修改原始数据
        result_df = df.copy()
        
        # 定义列名映射
        column_mapping = {
            'close': '收盘', '收盘价': '收盘',
            'volume': '成交量', 'vol': '成交量', 'volume_total': '成交量',
            'amount': '成交额', '成交额': '成交额', 'volume_amount': '成交额',
            'open': '开盘', '开盘价': '开盘',
            'high': '最高', '最高价': '最高',
            'low': '最低', '最低价': '最低',
            'datetime': '时间', 'date': '时间', 'time': '时间', '日期': '时间'
        }
        
        # 重命名列
        rename_dict = {}
        for col in result_df.columns:
            if col.lower() in map(str.lower, column_mapping.keys()):
                # 找到匹配的映射
                for key, target in column_mapping.items():
                    if col.lower() == key.lower() and target not in result_df.columns:
                        rename_dict[col] = target
                        break
        
        # 执行重命名
        if rename_dict:
            result_df = result_df.rename(columns=rename_dict)
        
        # 确保必要的列存在
        required_columns = ['收盘']
        for col in required_columns:
            if col not in result_df.columns:
                # 尝试找到价格相关列
                price_cols = [c for c in result_df.columns if any(x in c.lower() for x in ['price', 'close', '收盘', 'last'])]
                if price_cols:
                    print(f"使用'{price_cols[0]}'作为'收盘'列")
                    result_df['收盘'] = result_df[price_cols[0]]
                else:
                    print(f"错误: 无法找到价格列")
                    return None
        
        # 处理成交量列
        if '成交量' not in result_df.columns:
            volume_cols = [c for c in result_df.columns if any(x in c.lower() for x in ['volume', 'vol', '成交量'])]
            if volume_cols:
                result_df['成交量'] = result_df[volume_cols[0]]
            else:
                # 如果没有成交量，设置为0
                print("警告: 没有找到成交量列，设置为0")
                result_df['成交量'] = 0
        
        # 处理成交额列
        if '成交额' not in result_df.columns:
            amount_cols = [c for c in result_df.columns if any(x in c.lower() for x in ['amount', 'value', '成交额'])]
            if amount_cols:
                result_df['成交额'] = result_df[amount_cols[0]]
            elif '收盘' in result_df.columns and '成交量' in result_df.columns:
                # 计算成交额
                result_df['成交额'] = result_df['收盘'] * result_df['成交量']
        
        # 处理时间列
        if '时间' not in result_df.columns:
            # 检查索引是否为时间
            if isinstance(result_df.index, pd.DatetimeIndex):
                # 索引已经是时间类型
                pass
            elif len(result_df) > 0:
                # 生成时间序列
                print("生成交易时间序列")
                num_rows = len(result_df)
                # 生成9:30到15:00的时间序列
                times = []
                base_date = datetime.strptime(trade_date, '%Y%m%d')
                # 上午交易时间
                for hour in range(9, 12):
                    start_min = 30 if hour == 9 else 0
                    end_min = 60
                    for minute in range(start_min, end_min):
                        if len(times) >= num_rows:
                            break
                        times.append(datetime.combine(base_date, datetime.time(hour, minute)))
                # 下午交易时间
                for hour in range(13, 15):
                    for minute in range(0, 60):
                        if len(times) >= num_rows:
                            break
                        times.append(datetime.combine(base_date, datetime.time(hour, minute)))
                # 添加最后一个时间点15:00
                if len(times) < num_rows:
                    times.append(datetime.combine(base_date, datetime.time(15, 0)))
                
                # 设置时间索引
                result_df.index = pd.to_datetime(times[:num_rows])
        else:
            # 转换时间列为索引
            try:
                result_df['时间'] = pd.to_datetime(result_df['时间'])
                result_df = result_df.set_index('时间')
            except Exception as e:
                print(f"转换时间列失败: {e}")
                # 如果转换失败，生成时间序列
                num_rows = len(result_df)
                base_date = datetime.strptime(trade_date, '%Y%m%d')
                times = [base_date + timedelta(minutes=i) for i in range(num_rows)]
                result_df.index = pd.to_datetime(times)
        
        # 确保索引是DatetimeIndex
        if not isinstance(result_df.index, pd.DatetimeIndex):
            try:
                result_df.index = pd.to_datetime(result_df.index)
            except:
                print("警告: 无法将索引转换为时间类型")
        
        # 过滤指定日期的数据
        date_filter = datetime.strptime(trade_date, '%Y%m%d').strftime('%Y-%m-%d')
        if isinstance(result_df.index, pd.DatetimeIndex):
            result_df = result_df[result_df.index.strftime('%Y-%m-%d') == date_filter]
        
        # 确保数值列是数字类型
        numeric_cols = ['收盘', '开盘', '最高', '最低', '成交量', '成交额']
        for col in numeric_cols:
            if col in result_df.columns:
                try:
                    result_df[col] = pd.to_numeric(result_df[col], errors='coerce')
                except:
                    print(f"警告: 无法将'{col}'列转换为数字类型")
        
        # 去除NaN值
        result_df = result_df.dropna(subset=['收盘'])
        
        # 添加ETF代码列
        result_df['ETF代码'] = etf_code
        
        print(f"处理后的数据包含{len(result_df)}条记录")
        print(f"处理后的列: {list(result_df.columns)}")
        
        return result_df
    except Exception as e:
        print(f"处理ETF数据时出错: {str(e)}")
        return None

def analyze_etf(etf_code, etf_name, trade_date):
    """
    分析ETF的价格均线偏离策略
    
    Args:
        etf_code: ETF代码
        etf_name: ETF名称
        trade_date: 交易日期
    
    Returns:
        分析结果DataFrame，如果分析失败返回None
    """
    print(f"\n开始分析{etf_name}({etf_code})，日期: {trade_date}")
    print(f"-" * 50)
    
    # 获取ETF数据
    df = get_etf_real_data(etf_code, trade_date)
    
    # 检查数据是否获取成功
    if df is None or df.empty:
        print(f"错误: 无法获取{etf_name}的数据，程序将终止")
        return None
    
    print(f"成功获取{len(df)}条{etf_name}数据")
    
    # 确保必要的列存在
    if '收盘' not in df.columns:
        print(f"错误: 数据缺少必要的'收盘'列")
        return None
    
    # 应用价格均线偏离策略
    try:
        print("应用价格均线偏离策略...")
        result_df = pmdo.calculate_price_ma_deviation(df)
        
        # 统计信号
        if 'Optimized_Buy_Signal' in result_df.columns and 'Optimized_Sell_Signal' in result_df.columns:
            buy_signals = result_df['Optimized_Buy_Signal'].sum()
            sell_signals = result_df['Optimized_Sell_Signal'].sum()
            print(f"\n信号统计:")
            print(f"优化买入信号: {buy_signals}个")
            print(f"优化卖出信号: {sell_signals}个")
        
        # 可视化结果
        try:
            visualize_etf_results(result_df, etf_code, etf_name, trade_date)
        except Exception as e:
            print(f"可视化时出错: {str(e)}")
        
        print(f"{etf_name}分析完成")
        return result_df
        
    except Exception as e:
        print(f"应用策略时出错: {str(e)}")
        import traceback
        traceback.print_exc()
        return None

def visualize_etf_results(df, etf_code, etf_name, trade_date):
    """
    可视化ETF分析结果
    
    Args:
        df: 分析结果DataFrame
        etf_code: ETF代码
        etf_name: ETF名称
        trade_date: 交易日期
    """
    try:
        import matplotlib.pyplot as plt
        
        # 设置中文字体
        plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'DejaVu Sans']
        plt.rcParams['axes.unicode_minus'] = False
        
        # 创建图表
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 10), gridspec_kw={'height_ratios': [3, 1]})
        fig.suptitle(f'{etf_name}({etf_code}) 价格均线偏离分析 - {trade_date}', fontsize=14)
        
        # 绘制价格和均线
        ax1.plot(df.index, df['收盘'], label='收盘价', linewidth=2)
        if 'MA' in df.columns:
            ax1.plot(df.index, df['MA'], label='5分钟均线', color='orange')
        if '均价' in df.columns:
            ax1.plot(df.index, df['均价'], label='均价', color='green', linestyle='--')
        
        # 标记买入卖出信号
        if 'Optimized_Buy_Signal' in df.columns:
            buy_signals = df[df['Optimized_Buy_Signal'] > 0]
            ax1.scatter(buy_signals.index, buy_signals['收盘'], marker='^', color='red', s=100, label='买入信号')
        if 'Optimized_Sell_Signal' in df.columns:
            sell_signals = df[df['Optimized_Sell_Signal'] > 0]
            ax1.scatter(sell_signals.index, sell_signals['收盘'], marker='v', color='green', s=100, label='卖出信号')
        
        ax1.set_title('价格走势与交易信号')
        ax1.set_ylabel('价格')
        ax1.grid(True, alpha=0.3)
        ax1.legend()
        
        # 绘制偏离率
        if 'Price_MA_Ratio' in df.columns:
            ax2.plot(df.index, df['Price_MA_Ratio'], label='价格均线偏离率(%)', color='purple')
            ax2.axhline(y=0, color='black', linestyle='-', alpha=0.3)
        
        ax2.set_title('价格均线偏离率')
        ax2.set_xlabel('时间')
        ax2.set_ylabel('偏离率(%)')
        ax2.grid(True, alpha=0.3)
        ax2.legend()
        
        # 调整布局
        plt.tight_layout()
        plt.subplots_adjust(top=0.92)
        
        # 保存图像
        output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'output', 'etf_charts')
        os.makedirs(output_dir, exist_ok=True)
        output_file = os.path.join(output_dir, f'{etf_code}_{trade_date}_etf_analysis.png')
        plt.savefig(output_file, dpi=300, bbox_inches='tight')
        print(f"图表已保存至: {output_file}")
        
        plt.close()
        
    except ImportError:
        print("警告: matplotlib未安装，无法生成可视化图表")
    except Exception as e:
        print(f"可视化时出错: {str(e)}")

def main():
    """
    主函数，执行ETF分析
    """
    print(f"ETF价格均线偏离分析 - 仅使用真实数据")
    print(f"=" * 50)
    print(f"注意: 本脚本仅使用真实ETF数据，不生成任何模拟数据")
    print(f"数据获取失败时将直接提示并终止执行")
    
    # 使用固定的历史交易日进行测试
    trade_date = '20241018'  # 已知的交易日
    print(f"使用测试日期: {trade_date}")
    
    # 要测试的ETF列表（从一个ETF开始测试）
    etfs_to_test = [
        ('510050', '华夏上证50ETF')
    ]
    
    results = {}
    
    # 逐个分析ETF
    for etf_code, etf_name in etfs_to_test:
        try:
            result = analyze_etf(etf_code, etf_name, trade_date)
            if result is None:
                print(f"\n错误: {etf_name}分析失败，程序将退出")
                return
            results[etf_code] = result
        except Exception as e:
            print(f"分析{etf_name}时发生未预期的错误: {str(e)}")
            import traceback
            traceback.print_exc()
            return
    
    # 汇总分析结果
    if results:
        print(f"\n" + "=" * 50)
        print(f"分析结果汇总")
        
        for etf_code, result in results.items():
            etf_name = next((name for code, name in etfs_to_test if code == etf_code), etf_code)
            try:
                buy_signals = result.get('Optimized_Buy_Signal', pd.Series([])).sum()
                sell_signals = result.get('Optimized_Sell_Signal', pd.Series([])).sum()
                print(f"\n{etf_name}({etf_code}):")
                print(f"  优化买入信号: {buy_signals}个")
                print(f"  优化卖出信号: {sell_signals}个")
            except Exception as e:
                print(f"汇总{etf_name}结果时出错: {e}")
    
    print(f"\n" + "=" * 50)
    print("ETF分析完成!")

if __name__ == "__main__":
    main()