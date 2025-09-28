#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
自定义指标集成示例

本示例展示了如何添加自定义指标并将其集成到T0交易策略系统中
"""

import sys
import os
import pandas as pd
import numpy as np

# 添加项目根目录到路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# 导入系统模块
from src.indicators import tdx_indicators
from src.data import data_handler
from src.visualization import plotting
from src.utils import tools
from src.main import T0Strategy


# 自定义指标计算函数
def calculate_rsi(df, period=14):
    """
    计算RSI指标（自定义实现）
    
    参数:
    df: 包含股票数据的DataFrame
    period: 计算周期
    
    返回:
    df: 添加了RSI指标的DataFrame
    """
    # 计算价格变化
    delta = df['收盘'].diff()
    
    # 分离涨跌
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
    
    # 计算RSI
    rs = gain / loss
    df['Custom_RSI'] = 100 - (100 / (1 + rs))
    
    # 添加超买超卖线
    df['Custom_RSI_超买'] = 70
    df['Custom_RSI_超卖'] = 30
    
    # 生成交易信号
    df['Custom_RSI_买入信号'] = (df['Custom_RSI'].shift(1) < 30) & (df['Custom_RSI'] >= 30)
    df['Custom_RSI_卖出信号'] = (df['Custom_RSI'].shift(1) > 70) & (df['Custom_RSI'] <= 70)
    
    return df


def calculate_macd(df, fast_period=12, slow_period=26, signal_period=9):
    """
    计算MACD指标（自定义实现）
    
    参数:
    df: 包含股票数据的DataFrame
    fast_period: 快速EMA周期
    slow_period: 慢速EMA周期
    signal_period: 信号线EMA周期
    
    返回:
    df: 添加了MACD指标的DataFrame
    """
    # 计算EMA
    df['Custom_EMA_fast'] = df['收盘'].ewm(span=fast_period, adjust=False).mean()
    df['Custom_EMA_slow'] = df['收盘'].ewm(span=slow_period, adjust=False).mean()
    
    # 计算MACD线
    df['Custom_MACD'] = df['Custom_EMA_fast'] - df['Custom_EMA_slow']
    
    # 计算信号线
    df['Custom_MACD_Signal'] = df['Custom_MACD'].ewm(span=signal_period, adjust=False).mean()
    
    # 计算MACD柱状图
    df['Custom_MACD_Hist'] = df['Custom_MACD'] - df['Custom_MACD_Signal']
    
    # 生成交易信号
    df['Custom_MACD_买入信号'] = (df['Custom_MACD'].shift(1) < df['Custom_MACD_Signal'].shift(1)) & \
                              (df['Custom_MACD'] > df['Custom_MACD_Signal'])
    df['Custom_MACD_卖出信号'] = (df['Custom_MACD'].shift(1) > df['Custom_MACD_Signal'].shift(1)) & \
                              (df['Custom_MACD'] < df['Custom_MACD_Signal'])
    
    return df


def calculate_kdj(df, n=9, m1=3, m2=3):
    """
    计算KDJ指标（新增指标）
    
    参数:
    df: 包含股票数据的DataFrame
    n: RSV计算周期
    m1: K值平滑周期
    m2: D值平滑周期
    
    返回:
    df: 添加了KDJ指标的DataFrame
    """
    # 计算RSV
    low_n = df['最低'].rolling(window=n).min()
    high_n = df['最高'].rolling(window=n).max()
    df['RSV'] = (df['收盘'] - low_n) / (high_n - low_n) * 100
    
    # 计算K值
    df['K'] = df['RSV'].ewm(com=m1-1, adjust=False).mean()
    
    # 计算D值
    df['D'] = df['K'].ewm(com=m2-1, adjust=False).mean()
    
    # 计算J值
    df['J'] = 3 * df['K'] - 2 * df['D']
    
    # 添加超买超卖线
    df['KDJ_超买'] = 80
    df['KDJ_超卖'] = 20
    
    # 生成交易信号
    df['KDJ_买入信号'] = (df['K'].shift(1) < df['D'].shift(1)) & (df['K'] > df['D']) & (df['K'] < 20)
    df['KDJ_卖出信号'] = (df['K'].shift(1) > df['D'].shift(1)) & (df['K'] < df['D']) & (df['K'] > 80)
    
    return df


def analyze_with_custom_indicators(stock_code):
    """
    使用自定义指标分析股票
    
    参数:
    stock_code: 股票代码
    
    返回:
    df: 分析后的DataFrame
    prev_close: 前一日收盘价
    """
    print(f"使用自定义指标分析股票: {stock_code}")
    
    # 获取股票数据
    current_date = tools.get_current_date_str()
    df = data_handler.get_stock_intraday_data(stock_code)
    
    # 验证数据
    if not data_handler.validate_data(df):
        print(f"股票{stock_code}数据无效")
        return None, None
    
    # 处理数据
    df = data_handler.process_time_period(df)
    df = data_handler.fill_missing_data(df)
    
    # 获取前一日收盘价
    prev_close = data_handler.get_prev_close(stock_code)
    if prev_close is None:
        print(f"无法获取股票{stock_code}的前一日收盘价")
        return None, None
    
    # 计算通达信指标
    df = tdx_indicators.calculate_tdx_indicators(df, prev_close)
    
    # 应用自定义指标
    df = calculate_rsi(df)
    df = calculate_macd(df)
    df = calculate_kdj(df)
    
    return df, prev_close


# 自定义策略类
class CustomIndicatorStrategy(T0Strategy):
    """
    集成自定义指标的策略类
    """
    
    def analyze_stock(self, stock_code):
        """
        重写分析方法，集成自定义指标
        """
        try:
            print(f"使用自定义指标分析股票: {stock_code}")
            
            # 获取当前日期
            current_date = tools.get_current_date_str()
            
            # 尝试从缓存获取数据
            df = data_handler.get_cached_data(stock_code, current_date)
            
            # 如果缓存中没有数据，从API获取
            if df is None or df.empty:
                df = data_handler.get_stock_intraday_data(stock_code)
                
                # 验证数据
                if not data_handler.validate_data(df):
                    print(f"股票{stock_code}数据无效")
                    return None
                
                # 处理交易时间段
                df = data_handler.process_time_period(df)
                
                # 填充缺失数据
                df = data_handler.fill_missing_data(df)
                
                # 保存到缓存
                data_handler.save_data_to_cache(df, stock_code, current_date)
            
            # 获取前一日收盘价
            prev_close = data_handler.get_prev_close(stock_code)
            if prev_close is None:
                print(f"无法获取股票{stock_code}的前一日收盘价")
                return None
            
            # 计算通达信指标
            df = tdx_indicators.calculate_tdx_indicators(df, prev_close)
            
            # 应用自定义指标
            df = calculate_rsi(df)
            df = calculate_macd(df)
            df = calculate_kdj(df)
            
            # 检查交易信号（包括自定义指标的信号）
            signals = self._check_signals(df)
            
            # 生成图表
            if self.save_charts:
                chart_path = self._generate_custom_charts(df, stock_code, prev_close)
            else:
                chart_path = None
            
            # 记录结果
            result = {
                'stock_code': stock_code,
                'data': df,
                'prev_close': prev_close,
                'signals': signals,
                'chart_path': chart_path,
                'timestamp': tools.get_current_time_str()
            }
            
            self.results[stock_code] = result
            
            # 发送信号通知
            if self.notification_enabled:
                self._send_signal_notifications(stock_code, df, signals)
            
            return result
            
        except Exception as e:
            print(f"分析股票{stock_code}失败: {e}")
            return None
    
    def _check_signals(self, df):
        """
        重写信号检查方法，包括自定义指标的信号
        """
        # 调用父类的方法获取基础信号
        signals = super()._check_signals(df)
        
        # 添加自定义RSI信号
        if 'Custom_RSI_买入信号' in df.columns:
            rsi_buy_signals = df[df['Custom_RSI_买入信号']]
            for _, row in rsi_buy_signals.iterrows():
                signals['buy_signals'].append({
                    'time': row['时间'],
                    'price': row['收盘'],
                    'type': 'Custom_RSI_buy'
                })
        
        if 'Custom_RSI_卖出信号' in df.columns:
            rsi_sell_signals = df[df['Custom_RSI_卖出信号']]
            for _, row in rsi_sell_signals.iterrows():
                signals['sell_signals'].append({
                    'time': row['时间'],
                    'price': row['收盘'],
                    'type': 'Custom_RSI_sell'
                })
        
        # 添加自定义MACD信号
        if 'Custom_MACD_买入信号' in df.columns:
            macd_buy_signals = df[df['Custom_MACD_买入信号']]
            for _, row in macd_buy_signals.iterrows():
                signals['buy_signals'].append({
                    'time': row['时间'],
                    'price': row['收盘'],
                    'type': 'Custom_MACD_buy'
                })
        
        if 'Custom_MACD_卖出信号' in df.columns:
            macd_sell_signals = df[df['Custom_MACD_卖出信号']]
            for _, row in macd_sell_signals.iterrows():
                signals['sell_signals'].append({
                    'time': row['时间'],
                    'price': row['收盘'],
                    'type': 'Custom_MACD_sell'
                })
        
        # 添加KDJ信号
        if 'KDJ_买入信号' in df.columns:
            kdj_buy_signals = df[df['KDJ_买入信号']]
            for _, row in kdj_buy_signals.iterrows():
                signals['buy_signals'].append({
                    'time': row['时间'],
                    'price': row['收盘'],
                    'type': 'KDJ_buy'
                })
        
        if 'KDJ_卖出信号' in df.columns:
            kdj_sell_signals = df[df['KDJ_卖出信号']]
            for _, row in kdj_sell_signals.iterrows():
                signals['sell_signals'].append({
                    'time': row['时间'],
                    'price': row['收盘'],
                    'type': 'KDJ_sell'
                })
        
        return signals
    
    def _generate_custom_charts(self, df, stock_code, prev_close):
        """
        生成包含自定义指标的图表
        """
        try:
            # 创建股票特定的输出目录
            stock_output_dir = os.path.join(self.output_dir, stock_code)
            tools.create_directory(stock_output_dir)
            
            # 生成带信号的分时图
            timestamp = tools.get_current_time_str('%Y%m%d_%H%M%S')
            chart_path = os.path.join(stock_output_dir, f'{stock_code}_custom_signals_{timestamp}.png')
            
            # 绘制包含自定义指标的图表
            title = f'{stock_code} 分时图与自定义指标信号'
            
            # 创建图形和子图布局
            fig, (ax1, ax2, ax3, ax4) = plt.subplots(4, 1, figsize=(14, 16), gridspec_kw={'height_ratios': [2, 1, 1, 1]})
            
            # 第一部分：价格和支撑阻力线
            ax1.plot(df['时间'], df['收盘'], 'b-', label='现价')
            ax1.plot(df['时间'], df['支撑'], 'g--', label='支撑')
            ax1.plot(df['时间'], df['阻力'], 'r--', label='阻力')
            
            # 绘制昨收价参考线
            ax1.axhline(y=prev_close, color='k', linestyle=':', label=f'昨收价: {prev_close}')
            
            # 添加买卖信号标记
            buy_signals = df[df[['Custom_RSI_买入信号', 'Custom_MACD_买入信号', 'KDJ_买入信号']].any(axis=1)]
            sell_signals = df[df[['Custom_RSI_卖出信号', 'Custom_MACD_卖出信号', 'KDJ_卖出信号']].any(axis=1)]
            
            ax1.scatter(buy_signals['时间'], buy_signals['收盘'], marker='^', color='r', s=100, label='买入信号')
            ax1.scatter(sell_signals['时间'], sell_signals['收盘'], marker='v', color='g', s=100, label='卖出信号')
            
            # 设置第一部分标题和标签
            ax1.set_title(title, fontsize=14)
            ax1.set_ylabel('价格', fontsize=12)
            ax1.grid(True, linestyle='--', alpha=0.7)
            ax1.legend()
            
            # 第二部分：成交量
            ax2.bar(df['时间'], df['成交量'], color='blue', alpha=0.5, label='成交量')
            ax2.set_ylabel('成交量', fontsize=12)
            ax2.grid(True, linestyle='--', alpha=0.7)
            ax2.legend()
            
            # 第三部分：自定义RSI
            if 'Custom_RSI' in df.columns:
                ax3.plot(df['时间'], df['Custom_RSI'], 'blue', label='Custom_RSI')
                ax3.axhline(y=70, color='red', linestyle='--', label='超买线(70)')
                ax3.axhline(y=30, color='green', linestyle='--', label='超卖线(30)')
                ax3.set_ylabel('Custom_RSI', fontsize=12)
                ax3.set_ylim(0, 100)
                ax3.grid(True, linestyle='--', alpha=0.7)
                ax3.legend()
            
            # 第四部分：KDJ指标
            if 'K' in df.columns and 'D' in df.columns and 'J' in df.columns:
                ax4.plot(df['时间'], df['K'], 'blue', label='K线')
                ax4.plot(df['时间'], df['D'], 'orange', label='D线')
                ax4.plot(df['时间'], df['J'], 'purple', label='J线')
                ax4.axhline(y=80, color='red', linestyle='--', label='超买线(80)')
                ax4.axhline(y=20, color='green', linestyle='--', label='超卖线(20)')
                ax4.set_xlabel('时间', fontsize=12)
                ax4.set_ylabel('KDJ', fontsize=12)
                ax4.grid(True, linestyle='--', alpha=0.7)
                ax4.legend()
            
            # 设置x轴日期格式
            ax1.xaxis.set_major_formatter(plotting.mdates.DateFormatter('%H:%M'))
            ax2.xaxis.set_major_formatter(plotting.mdates.DateFormatter('%H:%M'))
            ax3.xaxis.set_major_formatter(plotting.mdates.DateFormatter('%H:%M'))
            ax4.xaxis.set_major_formatter(plotting.mdates.DateFormatter('%H:%M'))
            
            plt.xticks(rotation=45)
            
            # 调整布局
            plt.tight_layout()
            
            # 保存图表
            plt.savefig(chart_path, dpi=300)
            plt.close(fig)
            
            # 生成MACD柱状图
            if 'Custom_MACD_Hist' in df.columns:
                macd_path = os.path.join(stock_output_dir, f'{stock_code}_custom_macd_{timestamp}.png')
                fig, ax = plt.subplots(figsize=(12, 6))
                ax.bar(df['时间'], df['Custom_MACD_Hist'], color=['red' if x > 0 else 'green' for x in df['Custom_MACD_Hist']], alpha=0.5)
                ax.plot(df['时间'], df['Custom_MACD'], 'blue', label='MACD')
                ax.plot(df['时间'], df['Custom_MACD_Signal'], 'orange', label='信号线')
                ax.set_title(f'{stock_code} 自定义MACD指标', fontsize=14)
                ax.set_xlabel('时间', fontsize=12)
                ax.set_ylabel('MACD', fontsize=12)
                ax.xaxis.set_major_formatter(plotting.mdates.DateFormatter('%H:%M'))
                plt.xticks(rotation=45)
                ax.grid(True, linestyle='--', alpha=0.7)
                ax.legend()
                plt.tight_layout()
                plt.savefig(macd_path, dpi=300)
                plt.close(fig)
            
            return chart_path
            
        except Exception as e:
            print(f"生成自定义图表失败: {e}")
            return None


# 示例主函数
def main():
    """
    示例主函数
    """
    print("===== 自定义指标集成示例 =====