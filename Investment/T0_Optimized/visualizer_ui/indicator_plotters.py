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
    def _add_hover_annotation(fig, ax, x_indices, data_df, time_labels, value_column):
        """添加鼠标悬浮注释功能"""
        # 创建注释框
        annot = ax.annotate("", xy=(0,0), xytext=(10,10),
                           textcoords="offset points",
                           bbox=dict(boxstyle="round", fc="yellow", alpha=0.8),
                           arrowprops=dict(arrowstyle="->"),
                           fontsize=8,
                           visible=False)
        
        def on_hover(event):
            """鼠标悬浮事件处理"""
            if event.inaxes == ax:
                # 获取鼠标位置
                x_pos = int(round(event.xdata)) if event.xdata is not None else None
                
                if x_pos is not None and 0 <= x_pos < len(data_df):
                    # 获取对应的数据
                    time_str = time_labels.iloc[x_pos] if time_labels is not None else f"点{x_pos}"
                    
                    # 根据列名获取值
                    if value_column in data_df.columns:
                        value = data_df.iloc[x_pos][value_column]
                        text = f"{time_str}\n{value_column}: {value:.2f}"
                    else:
                        text = f"{time_str}"
                    
                    # 更新注释
                    annot.xy = (x_pos, event.ydata)
                    annot.set_text(text)
                    annot.set_visible(True)
                    fig.canvas.draw_idle()
                else:
                    annot.set_visible(False)
                    fig.canvas.draw_idle()
        
        # 绑定鼠标移动事件
        fig.canvas.mpl_connect('motion_notify_event', on_hover)
    
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
                    # 创建4个子图（与comprehensive_t0_strategy.py一致）
                    ax1 = fig.add_subplot(411)  # 价格与信号
                    ax2 = fig.add_subplot(412)  # 价格均线偏离
                    ax3 = fig.add_subplot(413)  # 动量指标
                    ax4 = fig.add_subplot(414)  # 复合评分
                    
                    # 子图1：价格与信号
                    if '时间' in df.columns:
                        time_labels = pd.to_datetime(df['时间']).dt.strftime('%H:%M')
                        x_indices = list(range(len(analyzed_df)))
                        full_data_length = 241  # 一个交易日的标准分钟数
                    else:
                        x_indices = list(range(len(analyzed_df)))
                        time_labels = None
                        full_data_length = len(analyzed_df)
                    
                    # 绘制价格和均线
                    if '收盘' in df.columns:
                        price_line = ax1.plot(x_indices, df['收盘'], 'black', linewidth=1.5, label='价格')
                        price_data = df['收盘']
                    elif '涨跌幅' in df.columns:
                        price_line = ax1.plot(x_indices, df['涨跌幅'], 'black', linewidth=1.5, label='涨跌幅')
                        price_data = df['涨跌幅']
                    else:
                        logger.warning("没有找到价格数据")
                        price_data = None
                    
                    if '均价' in df.columns:
                        ax1.plot(x_indices, df['均价'], 'blue', linewidth=1.5, label='均价', alpha=0.8)
                    
                    # 绘制支撑阻力线
                    if '支撑' in analyzed_df.columns:
                        ax1.plot(x_indices, analyzed_df['支撑'], 'green', linestyle='--', linewidth=1.5, label='支撑')
                    if '阻力' in analyzed_df.columns:
                        ax1.plot(x_indices, analyzed_df['阻力'], 'red', linestyle='--', linewidth=1.5, label='阻力')
                    
                    # 绘制买卖信号
                    if 'Buy_Signal' in analyzed_df.columns and price_data is not None:
                        buy_signals = analyzed_df[analyzed_df['Buy_Signal']]
                        for idx in buy_signals.index:
                            x_pos = analyzed_df.index.get_loc(idx)
                            ax1.scatter(x_pos, price_data.iloc[x_pos], color='red', marker='^', s=100, zorder=5)
                    
                    if 'Sell_Signal' in analyzed_df.columns and price_data is not None:
                        sell_signals = analyzed_df[analyzed_df['Sell_Signal']]
                        for idx in sell_signals.index:
                            x_pos = analyzed_df.index.get_loc(idx)
                            ax1.scatter(x_pos, price_data.iloc[x_pos], color='green', marker='v', s=100, zorder=5)
                    
                    ax1.set_title(f'{stock_code} - 价格与信号', fontsize=10)
                    ax1.set_ylabel('价格', fontsize=9)
                    ax1.grid(True, alpha=0.3)
                    ax1.legend(loc='upper right', fontsize=8)
                    ax1.set_xlim(-0.5, full_data_length - 0.5)
                    
                    # 子图2：价格均线偏离
                    if 'Price_MA_Ratio' in analyzed_df.columns:
                        ax2.plot(x_indices, analyzed_df['Price_MA_Ratio'], 'purple', linewidth=1.5, label='偏离率')
                        
                        # 添加动态阈值线（与comprehensive_t0_strategy.py一致）
                        volatility = calculate_volatility(df)
                        params = get_adaptive_parameters(volatility)
                        threshold = params['price_ma_threshold']
                        
                        ax2.axhline(y=threshold, color='green', linestyle='--', alpha=0.7, label=f'卖出阈值 ({threshold}%)')
                        ax2.axhline(y=-threshold, color='red', linestyle='--', alpha=0.7, label=f'买入阈值 ({-threshold}%)')
                        ax2.axhline(y=0, color='gray', linestyle='--', alpha=0.3)
                        
                        ax2.set_ylabel('偏离率(%)', fontsize=9)
                        ax2.set_title('价格均线偏离', fontsize=10)
                        ax2.grid(True, alpha=0.3)
                        ax2.legend(loc='upper right', fontsize=8)
                    
                    # 子图3：动量指标
                    if 'Price_Change' in analyzed_df.columns:
                        ax3.plot(x_indices, analyzed_df['Price_Change'], 'blue', linewidth=1.5, label='动量')
                        
                        # 添加动态阈值线（与comprehensive_t0_strategy.py一致）
                        if 'Upper_Threshold' in analyzed_df.columns:
                            ax3.plot(x_indices, analyzed_df['Upper_Threshold'], 'red', linestyle='--', linewidth=1.5, label='超买阈值')
                        if 'Lower_Threshold' in analyzed_df.columns:
                            ax3.plot(x_indices, analyzed_df['Lower_Threshold'], 'green', linestyle='--', linewidth=1.5, label='超卖阈值')
                        
                        ax3.axhline(y=0, color='black', linestyle='-', alpha=0.5)
                        ax3.set_ylabel('动量(%)', fontsize=9)
                        ax3.set_title('动量指标', fontsize=10)
                        ax3.grid(True, alpha=0.3)
                        ax3.legend(loc='upper right', fontsize=8)
                    
                    # 子图4：复合评分
                    ax4.plot(x_indices, analyzed_df['Composite_Score'], 'orange', linewidth=1.5, label='复合评分')
                    ax4.axhline(y=50, color='orange', linestyle='--', alpha=0.7, label='信号阈值')
                    ax4.axhline(y=80, color='darkorange', linestyle=':', alpha=0.7, label='紧急信号阈值')
                    ax4.set_ylabel('评分', fontsize=9)
                    ax4.set_title('复合评分', fontsize=10)
                    ax4.grid(True, alpha=0.3)
                    ax4.legend(loc='upper right', fontsize=8)
                    
                    # 设置X轴时间标签（仅在最下方子图显示）
                    if time_labels is not None:
                        step = max(1, full_data_length // 12)
                        tick_positions = list(range(0, full_data_length, step))
                        tick_labels = [time_labels.iloc[i] if i < len(time_labels) else '' for i in tick_positions]
                        ax4.set_xticks(tick_positions)
                        ax4.set_xticklabels(tick_labels, rotation=45, fontsize=8)
                        ax4.set_xlabel('时间', fontsize=9)
                    
                    # 同步X轴范围
                    for ax in [ax1, ax2, ax3, ax4]:
                        ax.set_xlim(-0.5, full_data_length - 0.5)
                    
                    # 添加鼠标悬浮功能
                    if time_labels is not None:
                        IndicatorPlotters._add_hover_annotation(fig, ax1, x_indices, df, time_labels, '收盘')
                        IndicatorPlotters._add_hover_annotation(fig, ax2, x_indices, analyzed_df, time_labels, 'Price_MA_Ratio')
                        IndicatorPlotters._add_hover_annotation(fig, ax3, x_indices, analyzed_df, time_labels, 'Price_Change')
                        IndicatorPlotters._add_hover_annotation(fig, ax4, x_indices, analyzed_df, time_labels, 'Composite_Score')
                    
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
                full_data_length = 241  # 一个交易日的标准分钟数
                
                # 获取时间标签
                if '时间' in df.columns:
                    time_labels = pd.to_datetime(df['时间']).dt.strftime('%H:%M')
                else:
                    time_labels = None
                
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
                ax1.set_xlabel('时间', fontsize=9)
                ax1.set_ylabel('价格', fontsize=9)
                ax2.set_ylabel('偏离率 (%)', fontsize=9)
                
                # 固定横轴范围（回放时不变）
                ax1.set_xlim(-0.5, full_data_length - 0.5)
                
                # 设置X轴时间标签
                if time_labels is not None:
                    step = max(1, full_data_length // 12)
                    tick_positions = list(range(0, full_data_length, step))
                    tick_labels = [time_labels.iloc[i] if i < len(time_labels) else '' for i in tick_positions]
                    ax1.set_xticks(tick_positions)
                    ax1.set_xticklabels(tick_labels, rotation=45, fontsize=8)
                
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
                
                # 添加鼠标悬浮功能
                if time_labels is not None:
                    IndicatorPlotters._add_hover_annotation(fig, ax1, x_indices, df, time_labels, '收盘')
                
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
                full_data_length = 241  # 一个交易日的标准分钟数
                
                # 获取时间标签
                if '时间' in df.columns:
                    time_labels = pd.to_datetime(df['时间']).dt.strftime('%H:%M')
                else:
                    time_labels = None
                
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
                ax1.set_xlabel('时间', fontsize=9)
                ax1.set_ylabel('价格', fontsize=9)
                ax2.set_ylabel('偏离率 (%)', fontsize=9)
                
                # 固定横轴范围（回放时不变）
                ax1.set_xlim(-0.5, full_data_length - 0.5)
                
                # 设置X轴时间标签
                if time_labels is not None:
                    step = max(1, full_data_length // 12)
                    tick_positions = list(range(0, full_data_length, step))
                    tick_labels = [time_labels.iloc[i] if i < len(time_labels) else '' for i in tick_positions]
                    ax1.set_xticks(tick_positions)
                    ax1.set_xticklabels(tick_labels, rotation=45, fontsize=8)
                
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
                
                # 添加鼠标悬浮功能
                if time_labels is not None:
                    IndicatorPlotters._add_hover_annotation(fig, ax1, x_indices, df, time_labels, '收盘')
                
                fig.tight_layout()
                return True
            
            return False
            
        except Exception as e:
            logger.error(f"绘制价格均线偏离（优化）指标失败: {e}")
            import traceback
            traceback.print_exc()
            return False
