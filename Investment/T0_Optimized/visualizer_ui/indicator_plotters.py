#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
指标绘图模块 - 负责各种指标的具体绘图逻辑
"""

import sys
import logging
import pandas as pd
import numpy as np
from pathlib import Path

# 添加项目根目录
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

logger = logging.getLogger(__name__)

# 导入指标模块
def define_mock_indicators():
    """定义模拟指标函数"""
    def mock_analyze_comprehensive_t0(df):
        result_df = df.copy()
        if '涨跌幅' in df.columns:
            result_df['Composite_Score'] = df['涨跌幅'] * 10
            result_df['Buy_Signal'] = df['涨跌幅'] < -0.5
            result_df['Sell_Signal'] = df['涨跌幅'] > 0.5
        trades = []
        return result_df, trades

    def mock_analyze_deviation_strategy(df):
        result = df.copy()
        if '均价' in df.columns and '收盘' in df.columns:
            result['Price_MA_Ratio'] = ((df['收盘'] - df['均价']) / df['均价']) * 100
        else:
            result['Price_MA_Ratio'] = df['涨跌幅'] if '涨跌幅' in df.columns else 0
        # 修正阈值：降低到-0.3%和+0.3%，更容易触发信号
        result['Buy_Signal'] = result['Price_MA_Ratio'] < -0.3
        result['Sell_Signal'] = result['Price_MA_Ratio'] > 0.3
        return result

    def mock_analyze_deviation_strategy_optimized(df):
        result = df.copy()
        if '均价' in df.columns and '收盘' in df.columns:
            result['Price_MA_Ratio'] = ((df['收盘'] - df['均价']) / df['均价']) * 100
            ma5 = result['Price_MA_Ratio'].rolling(window=5, min_periods=1).mean()
            result['Price_MA_Ratio_Smooth'] = ma5
            result['Buy_Signal'] = ma5 < -0.8
            result['Sell_Signal'] = ma5 > 0.8
        else:
            result['Price_MA_Ratio'] = df['涨跌幅'] if '涨跌幅' in df.columns else 0
            result['Buy_Signal'] = result['Price_MA_Ratio'] < -0.5
            result['Sell_Signal'] = result['Price_MA_Ratio'] > 0.5
        return result
    
    return mock_analyze_comprehensive_t0, mock_analyze_deviation_strategy, mock_analyze_deviation_strategy_optimized

# 初始化模拟函数
analyze_comprehensive_t0, analyze_deviation_strategy, analyze_deviation_strategy_optimized = define_mock_indicators()

# 尝试导入真实指标模块
try:
    from indicators.comprehensive_t0_strategy import analyze_comprehensive_t0 as real_analyze_comprehensive_t0
    # 创建包装函数，优先使用DataFrame
    def wrapper_comprehensive_t0(df_or_code, date=None):
        if isinstance(df_or_code, pd.DataFrame):
            # 直接使用DataFrame计算
            return define_mock_indicators()[0](df_or_code)
        else:
            # 从数据库读取
            return real_analyze_comprehensive_t0(df_or_code, date)
    analyze_comprehensive_t0 = wrapper_comprehensive_t0
    logger.info("✅ 成功导入综合T0策略模块")
except ImportError:
    logger.warning("无法导入综合T0策略模块，使用模拟函数")

try:
    from indicators.price_ma_deviation import analyze_deviation_strategy as real_analyze_deviation_strategy
    analyze_deviation_strategy = real_analyze_deviation_strategy
    logger.info("✅ 成功导入价格均线偏离策略模块")
except ImportError:
    logger.warning("无法导入价格均线偏离策略模块，使用模拟函数")

try:
    from indicators.price_ma_deviation_optimized import analyze_deviation_strategy as real_analyze_deviation_strategy_optimized  
    # 创建包装函数，优先使用DataFrame
    def wrapper_deviation_optimized(df_or_code, date=None):
        if isinstance(df_or_code, pd.DataFrame):
            # 直接使用DataFrame计算
            return define_mock_indicators()[2](df_or_code)
        else:
            # 从数据库读取
            return real_analyze_deviation_strategy_optimized(df_or_code, date)
    analyze_deviation_strategy_optimized = wrapper_deviation_optimized
    logger.info("✅ 成功导入优化版价格均线偏离策略模块")
except ImportError:
    logger.warning("无法导入优化版价格均线偏离策略模块，使用模拟函数")


class IndicatorPlotters:
    """指标绘图器集合"""
    
    @staticmethod
    def plot_comprehensive_t0(fig, df, stock_code):
        """绘制综合T0策略指标"""
        try:
            logger.info("调用 analyze_comprehensive_t0 函数...")
            
            # 尝试直接传入DataFrame
            try:
                result = analyze_comprehensive_t0(df.copy())
            except TypeError:
                # 如果函数期望(stock_code, date)，则从数据中提取日期
                if '时间' in df.columns and len(df) > 0:
                    trade_date = pd.to_datetime(df['时间'].iloc[0]).strftime('%Y-%m-%d')
                    result = analyze_comprehensive_t0(stock_code, trade_date)
                else:
                    result = analyze_comprehensive_t0(stock_code, '2025-10-24')
            
            if result is not None:
                if isinstance(result, tuple) and len(result) == 2:
                    analyzed_df, trades = result
                elif isinstance(result, pd.DataFrame):
                    analyzed_df = result
                else:
                    analyzed_df = None
                
                if analyzed_df is not None and not analyzed_df.empty and 'Composite_Score' in analyzed_df.columns:
                    # 创建3个子图
                    ax1 = fig.add_subplot(311)  # 带信号的分时图
                    ax2 = fig.add_subplot(312)  # 复合评分
                    ax3 = fig.add_subplot(313)  # 其他分析
                    
                    # 子图1：带信号的分时图
                    x_indices = list(range(len(analyzed_df)))
                    
                    # 使用analyzed_df的数据（如果有涨跌幅），否则使用原始df
                    if '涨跌幅' in analyzed_df.columns:
                        ax1.plot(x_indices, analyzed_df['涨跌幅'], 'b-', linewidth=1, label='分时线')
                        price_data = analyzed_df['涨跌幅']
                    elif '涨跌幅' in df.columns:
                        ax1.plot(x_indices, df['涨跌幅'], 'b-', linewidth=1, label='分时线')
                        price_data = df['涨跌幅']
                    else:
                        logger.warning("没有找到涨跌幅数据")
                        price_data = None
                    
                    if price_data is not None:
                        if 'Buy_Signal' in analyzed_df.columns:
                            buy_signals = analyzed_df[analyzed_df['Buy_Signal'] == True]
                            for idx in buy_signals.index:
                                x_pos = analyzed_df.index.get_loc(idx)
                                ax1.scatter(x_pos, price_data.iloc[x_pos], 
                                          color='red', marker='^', s=80, zorder=5)
                        
                        if 'Sell_Signal' in analyzed_df.columns:
                            sell_signals = analyzed_df[analyzed_df['Sell_Signal'] == True]
                            for idx in sell_signals.index:
                                x_pos = analyzed_df.index.get_loc(idx)
                                ax1.scatter(x_pos, price_data.iloc[x_pos], 
                                          color='green', marker='v', s=80, zorder=5)
                    
                    ax1.set_title(f'{stock_code} - 综合T0策略信号', fontsize=10)
                    ax1.set_ylabel('涨跌幅 (%)', fontsize=9)
                    ax1.grid(True, alpha=0.3)
                    ax1.legend(loc='upper right', fontsize=8)
                    
                    # 子图2：复合评分
                    ax2.plot(x_indices, analyzed_df['Composite_Score'], 'b-', linewidth=1, label='复合评分')
                    ax2.axhline(y=0, color='gray', linestyle='--', alpha=0.3)
                    ax2.set_ylabel('评分', fontsize=9)
                    ax2.set_title('复合评分', fontsize=10)
                    ax2.grid(True, alpha=0.3)
                    ax2.legend(loc='upper right', fontsize=8)
                    
                    # 子图3：信号统计
                    if 'Buy_Signal' in analyzed_df.columns and 'Sell_Signal' in analyzed_df.columns:
                        buy_count = analyzed_df['Buy_Signal'].sum()
                        sell_count = analyzed_df['Sell_Signal'].sum()
                        ax3.text(0.5, 0.5, f'买入信号: {buy_count}\n卖出信号: {sell_count}', 
                                ha='center', va='center', fontsize=12)
                    else:
                        ax3.text(0.5, 0.5, '交易对分析', ha='center', va='center', fontsize=12)
                    ax3.set_title('交易分析', fontsize=10)
                    ax3.axis('off')
                    
                    fig.tight_layout()
                    return True
            
            logger.warning("analyze_comprehensive_t0 返回 None 或无效数据")
            return False
            
        except Exception as e:
            logger.error(f"绘制综合T0策略指标失败: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    @staticmethod
    def plot_price_ma_deviation(fig, df, stock_code):
        """绘制价格均线偏离（基础）指标 - 单图表显示"""
        try:
            result = analyze_deviation_strategy(df.copy())
            
            if isinstance(result, pd.DataFrame) and 'Price_MA_Ratio' in result.columns:
                # 创建单个图表，使用双Y轴
                ax1 = fig.add_subplot(111)
                ax2 = ax1.twinx()  # 创建共享X轴的第二个Y轴
                
                x_indices = list(range(len(result)))
                
                # 左Y轴：价格和均线
                # 绘制分时线（价格）
                if '收盘' in df.columns:
                    line1 = ax1.plot(x_indices, df['收盘'], 'black', linewidth=1.5, label='价格', alpha=0.8)
                else:
                    line1 = ax1.plot(x_indices, df['涨跌幅'], 'black', linewidth=1.5, label='涨跌幅', alpha=0.8)
                
                # 绘制均线（蓝色）
                if '均价' in df.columns:
                    line2 = ax1.plot(x_indices, df['均价'], 'blue', linewidth=1.5, label='均线', alpha=0.8)
                
                # 绘制买卖信号
                if 'Buy_Signal' in result.columns:
                    buy_signals = result[result['Buy_Signal']]
                    for idx in buy_signals.index:
                        x_pos = result.index.get_loc(idx)
                        if '收盘' in df.columns:
                            ax1.scatter(x_pos, df.iloc[x_pos]['收盘'], 
                                      color='red', marker='^', s=100, zorder=5, label='买入信号' if x_pos == buy_signals.index[0] else '')
                        else:
                            ax1.scatter(x_pos, df.iloc[x_pos]['涨跌幅'], 
                                      color='red', marker='^', s=100, zorder=5, label='买入信号' if x_pos == buy_signals.index[0] else '')
                
                if 'Sell_Signal' in result.columns:
                    sell_signals = result[result['Sell_Signal']]
                    for idx in sell_signals.index:
                        x_pos = result.index.get_loc(idx)
                        if '收盘' in df.columns:
                            ax1.scatter(x_pos, df.iloc[x_pos]['收盘'], 
                                      color='green', marker='v', s=100, zorder=5, label='卖出信号' if x_pos == sell_signals.index[0] else '')
                        else:
                            ax1.scatter(x_pos, df.iloc[x_pos]['涨跌幅'], 
                                      color='green', marker='v', s=100, zorder=5, label='卖出信号' if x_pos == sell_signals.index[0] else '')
                
                # 右Y轴：偏离率
                line3 = ax2.plot(x_indices, result['Price_MA_Ratio'], 'purple', linewidth=1.5, label='偏离率', alpha=0.7)
                ax2.axhline(y=0, color='gray', linestyle='--', alpha=0.3)
                
                # 设置标题和标签
                ax1.set_title(f'{stock_code} - 价格均线偏离(基础)', fontsize=11, fontweight='bold')
                ax1.set_xlabel('时间点', fontsize=9)
                ax1.set_ylabel('价格', fontsize=9)
                ax2.set_ylabel('偏离率 (%)', fontsize=9)
                
                # 网格
                ax1.grid(True, alpha=0.3)
                
                # 合并图例
                lines1, labels1 = ax1.get_legend_handles_labels()
                lines2, labels2 = ax2.get_legend_handles_labels()
                # 去重图侌
                seen = set()
                unique_lines = []
                unique_labels = []
                for line, label in zip(lines1 + lines2, labels1 + labels2):
                    if label and label not in seen:
                        seen.add(label)
                        unique_lines.append(line)
                        unique_labels.append(label)
                ax1.legend(unique_lines, unique_labels, loc='upper left', fontsize=8)
                
                fig.tight_layout()
                return True
            
            return False
            
        except Exception as e:
            logger.error(f"绘制价格均线偏离（基础）指标失败: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    @staticmethod
    def plot_price_ma_deviation_optimized(fig, df, stock_code):
        """绘制价格均线偏离（优化）指标 - 单图表显示"""
        try:
            result = analyze_deviation_strategy_optimized(df.copy())
            
            if isinstance(result, pd.DataFrame) and 'Price_MA_Ratio' in result.columns:
                # 创建单个图表，使用双Y轴
                ax1 = fig.add_subplot(111)
                ax2 = ax1.twinx()  # 创建共享X轴的第二个Y轴
                
                x_indices = list(range(len(result)))
                
                buy_col = 'Optimized_Buy_Signal' if 'Optimized_Buy_Signal' in result.columns else 'Buy_Signal'
                sell_col = 'Optimized_Sell_Signal' if 'Optimized_Sell_Signal' in result.columns else 'Sell_Signal'
                
                # 左Y轴：价格和均线
                # 绘制分时线（价格）
                if '收盘' in df.columns:
                    line1 = ax1.plot(x_indices, df['收盘'], 'black', linewidth=1.5, label='价格', alpha=0.8)
                else:
                    line1 = ax1.plot(x_indices, df['涨跌幅'], 'black', linewidth=1.5, label='涨跌幅', alpha=0.8)
                
                # 绘制均线（蓝色）
                if '均价' in df.columns:
                    line2 = ax1.plot(x_indices, df['均价'], 'blue', linewidth=1.5, label='均线', alpha=0.8)
                
                # 绘制买卖信号
                if buy_col in result.columns:
                    buy_signals = result[result[buy_col]]
                    for idx in buy_signals.index:
                        x_pos = result.index.get_loc(idx)
                        if '收盘' in df.columns:
                            ax1.scatter(x_pos, df.iloc[x_pos]['收盘'], 
                                      color='red', marker='^', s=100, zorder=5, label='买入信号' if x_pos == buy_signals.index[0] else '')
                        else:
                            ax1.scatter(x_pos, df.iloc[x_pos]['涨跌幅'], 
                                      color='red', marker='^', s=100, zorder=5, label='买入信号' if x_pos == buy_signals.index[0] else '')
                
                if sell_col in result.columns:
                    sell_signals = result[result[sell_col]]
                    for idx in sell_signals.index:
                        x_pos = result.index.get_loc(idx)
                        if '收盘' in df.columns:
                            ax1.scatter(x_pos, df.iloc[x_pos]['收盘'], 
                                      color='green', marker='v', s=100, zorder=5, label='卖出信号' if x_pos == sell_signals.index[0] else '')
                        else:
                            ax1.scatter(x_pos, df.iloc[x_pos]['涨跌幅'], 
                                      color='green', marker='v', s=100, zorder=5, label='卖出信号' if x_pos == sell_signals.index[0] else '')
                
                # 右Y轴：偏离率（优化版使用平滑后的值）
                if 'Price_MA_Ratio_Smooth' in result.columns:
                    line3 = ax2.plot(x_indices, result['Price_MA_Ratio_Smooth'], 'orange', linewidth=1.5, label='偏离率(平滑)', alpha=0.7)
                else:
                    line3 = ax2.plot(x_indices, result['Price_MA_Ratio'], 'orange', linewidth=1.5, label='偏离率', alpha=0.7)
                ax2.axhline(y=0, color='gray', linestyle='--', alpha=0.3)
                
                # 设置标题和标签
                ax1.set_title(f'{stock_code} - 价格均线偏离(优化)', fontsize=11, fontweight='bold')
                ax1.set_xlabel('时间点', fontsize=9)
                ax1.set_ylabel('价格', fontsize=9)
                ax2.set_ylabel('偏离率 (%)', fontsize=9)
                
                # 网格
                ax1.grid(True, alpha=0.3)
                
                # 合并图例
                lines1, labels1 = ax1.get_legend_handles_labels()
                lines2, labels2 = ax2.get_legend_handles_labels()
                # 去重图侌
                seen = set()
                unique_lines = []
                unique_labels = []
                for line, label in zip(lines1 + lines2, labels1 + labels2):
                    if label and label not in seen:
                        seen.add(label)
                        unique_lines.append(line)
                        unique_labels.append(label)
                ax1.legend(unique_lines, unique_labels, loc='upper left', fontsize=8)
                
                fig.tight_layout()
                return True
            
            return False
            
        except Exception as e:
            logger.error(f"绘制价格均线偏离（优化）指标失败: {e}")
            import traceback
            traceback.print_exc()
            return False
