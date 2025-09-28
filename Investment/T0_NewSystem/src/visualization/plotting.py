import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from matplotlib.ticker import FuncFormatter
import matplotlib.dates as mdates
from datetime import datetime


def plot_stock_intraday(df, title=None, save_path=None):
    """
    绘制股票分时图
    
    参数:
    df: 包含股票数据的DataFrame，必须包含'时间'和'收盘'列
    title: 图表标题
    save_path: 保存路径，None则不保存
    
    返回:
    fig: matplotlib图形对象
    """
    try:
        # 创建图形和子图
        fig, ax = plt.subplots(figsize=(12, 6))
        
        # 确保时间列是datetime类型
        if not pd.api.types.is_datetime64_any_dtype(df['时间']):
            df['时间'] = pd.to_datetime(df['时间'])
        
        # 绘制收盘价曲线
        ax.plot(df['时间'], df['收盘'], 'b-', label='收盘价')
        
        # 设置标题和标签
        if title:
            ax.set_title(title, fontsize=14)
        ax.set_xlabel('时间', fontsize=12)
        ax.set_ylabel('价格', fontsize=12)
        
        # 设置x轴日期格式
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
        plt.xticks(rotation=45)
        
        # 添加网格线
        ax.grid(True, linestyle='--', alpha=0.7)
        
        # 添加图例
        ax.legend()
        
        # 调整布局
        plt.tight_layout()
        
        # 保存图表
        if save_path:
            plt.savefig(save_path, dpi=300)
        
        return fig
        
    except Exception as e:
        print(f"绘制分时图失败: {e}")
        return None


def plot_with_indicators(df, indicators=['支撑', '阻力'], title=None, save_path=None):
    """
    绘制带指标的股票分时图
    
    参数:
    df: 包含股票数据和指标的DataFrame
    indicators: 要绘制的指标列表
    title: 图表标题
    save_path: 保存路径，None则不保存
    
    返回:
    fig: matplotlib图形对象
    """
    try:
        # 创建图形和子图
        fig, ax = plt.subplots(figsize=(12, 6))
        
        # 确保时间列是datetime类型
        if not pd.api.types.is_datetime64_any_dtype(df['时间']):
            df['时间'] = pd.to_datetime(df['时间'])
        
        # 绘制收盘价曲线
        ax.plot(df['时间'], df['收盘'], 'b-', label='收盘价')
        
        # 绘制指定的指标
        for indicator in indicators:
            if indicator in df.columns:
                if indicator == '支撑':
                    ax.plot(df['时间'], df[indicator], 'g--', label=indicator)
                elif indicator == '阻力':
                    ax.plot(df['时间'], df[indicator], 'r--', label=indicator)
                else:
                    ax.plot(df['时间'], df[indicator], label=indicator)
        
        # 设置标题和标签
        if title:
            ax.set_title(title, fontsize=14)
        ax.set_xlabel('时间', fontsize=12)
        ax.set_ylabel('价格', fontsize=12)
        
        # 设置x轴日期格式
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
        plt.xticks(rotation=45)
        
        # 添加网格线
        ax.grid(True, linestyle='--', alpha=0.7)
        
        # 添加图例
        ax.legend()
        
        # 调整布局
        plt.tight_layout()
        
        # 保存图表
        if save_path:
            plt.savefig(save_path, dpi=300)
        
        return fig
        
    except Exception as e:
        print(f"绘制带指标的分时图失败: {e}")
        return None


def plot_with_signals(df, prev_close, title=None, save_path=None):
    """
    绘制带买卖信号的股票分时图
    
    参数:
    df: 包含股票数据和信号的DataFrame
    prev_close: 前一日收盘价
    title: 图表标题
    save_path: 保存路径，None则不保存
    
    返回:
    fig: matplotlib图形对象
    """
    try:
        # 创建图形和子图布局
        fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(14, 12), gridspec_kw={'height_ratios': [2, 1, 1]})
        
        # 确保时间列是datetime类型
        if not pd.api.types.is_datetime64_any_dtype(df['时间']):
            df['时间'] = pd.to_datetime(df['时间'])
        
        # 第一部分：价格和指标
        ax1.plot(df['时间'], df['收盘'], 'b-', label='现价')
        ax1.plot(df['时间'], df['支撑'], 'g--', label='支撑')
        ax1.plot(df['时间'], df['阻力'], 'r--', label='阻力')
        
        # 绘制昨收价参考线
        ax1.axhline(y=prev_close, color='k', linestyle=':', label=f'昨收价: {prev_close}')
        
        # 添加买卖信号标记
        # 买信号（红三角）
        if 'longcross_support' in df.columns:
            buy_signals = df[df['longcross_support']]
            ax1.scatter(buy_signals['时间'], buy_signals['收盘'], marker='^', color='r', s=100, label='买信号')
        
        # 卖信号（绿三角）
        if 'longcross_resistance' in df.columns:
            sell_signals = df[df['longcross_resistance']]
            ax1.scatter(sell_signals['时间'], sell_signals['收盘'], marker='v', color='g', s=100, label='卖信号')
        
        # 支撑上穿现价（黄色柱）
        if 'cross_support' in df.columns:
            cross_signals = df[df['cross_support']]
            for _, row in cross_signals.iterrows():
                ax1.axvline(x=row['时间'], color='y', alpha=0.3, linestyle='-')
        
        # 设置第一部分标题和标签
        if title:
            ax1.set_title(title, fontsize=14)
        ax1.set_ylabel('价格', fontsize=12)
        ax1.grid(True, linestyle='--', alpha=0.7)
        ax1.legend()
        
        # 第二部分：成交量
        ax2.bar(df['时间'], df['成交量'], color='blue', alpha=0.5, label='成交量')
        ax2.set_ylabel('成交量', fontsize=12)
        ax2.grid(True, linestyle='--', alpha=0.7)
        ax2.legend()
        
        # 第三部分：MACD（如果存在）
        if 'MACD_Hist' in df.columns:
            # 绘制MACD柱状图
            ax3.bar(df['时间'], df['MACD_Hist'], color=['red' if x > 0 else 'green' for x in df['MACD_Hist']], alpha=0.5)
            # 绘制MACD线和信号线
            if 'MACD' in df.columns:
                ax3.plot(df['时间'], df['MACD'], 'blue', label='MACD')
            if 'MACD_Signal' in df.columns:
                ax3.plot(df['时间'], df['MACD_Signal'], 'orange', label='信号线')
            ax3.set_xlabel('时间', fontsize=12)
            ax3.set_ylabel('MACD', fontsize=12)
            ax3.grid(True, linestyle='--', alpha=0.7)
            ax3.legend()
        
        # 设置x轴日期格式
        ax1.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
        ax2.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
        ax3.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
        
        plt.xticks(rotation=45)
        
        # 调整布局
        plt.tight_layout()
        
        # 保存图表
        if save_path:
            plt.savefig(save_path, dpi=300)
        
        return fig
        
    except Exception as e:
        print(f"绘制带买卖信号的分时图失败: {e}")
        return None


def plot_volume_price(df, title=None, save_path=None):
    """
    绘制量价关系图
    
    参数:
    df: 包含股票数据的DataFrame
    title: 图表标题
    save_path: 保存路径，None则不保存
    
    返回:
    fig: matplotlib图形对象
    """
    try:
        # 创建图形和子图
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10), gridspec_kw={'height_ratios': [2, 1]})
        
        # 确保时间列是datetime类型
        if not pd.api.types.is_datetime64_any_dtype(df['时间']):
            df['时间'] = pd.to_datetime(df['时间'])
        
        # 第一部分：价格
        ax1.plot(df['时间'], df['收盘'], 'b-', label='收盘价')
        ax1.fill_between(df['时间'], df['最高'], df['最低'], color='blue', alpha=0.1)
        
        # 设置第一部分标题和标签
        if title:
            ax1.set_title(title, fontsize=14)
        ax1.set_ylabel('价格', fontsize=12)
        ax1.grid(True, linestyle='--', alpha=0.7)
        ax1.legend()
        
        # 第二部分：成交量
        # 根据价格变化设置成交量颜色
        colors = ['red' if df.loc[i, '收盘'] >= df.loc[i, '开盘'] else 'green' for i in range(len(df))]
        ax2.bar(df['时间'], df['成交量'], color=colors, alpha=0.5, label='成交量')
        
        # 设置第二部分标题和标签
        ax2.set_xlabel('时间', fontsize=12)
        ax2.set_ylabel('成交量', fontsize=12)
        ax2.grid(True, linestyle='--', alpha=0.7)
        ax2.legend()
        
        # 设置x轴日期格式
        ax1.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
        ax2.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
        plt.xticks(rotation=45)
        
        # 调整布局
        plt.tight_layout()
        
        # 保存图表
        if save_path:
            plt.savefig(save_path, dpi=300)
        
        return fig
        
    except Exception as e:
        print(f"绘制量价关系图失败: {e}")
        return None


def plot_rsi(df, period=14, title=None, save_path=None):
    """
    绘制RSI指标图
    
    参数:
    df: 包含股票数据和RSI的DataFrame
    period: RSI计算周期
    title: 图表标题
    save_path: 保存路径，None则不保存
    
    返回:
    fig: matplotlib图形对象
    """
    try:
        # 检查是否包含RSI列
        if 'RSI' not in df.columns:
            print("DataFrame中不包含RSI列")
            return None
        
        # 创建图形和子图
        fig, ax = plt.subplots(figsize=(12, 6))
        
        # 确保时间列是datetime类型
        if not pd.api.types.is_datetime64_any_dtype(df['时间']):
            df['时间'] = pd.to_datetime(df['时间'])
        
        # 绘制RSI曲线
        ax.plot(df['时间'], df['RSI'], 'blue', label=f'RSI({period})')
        
        # 绘制超买超卖线
        ax.axhline(y=70, color='red', linestyle='--', label='超买线(70)')
        ax.axhline(y=30, color='green', linestyle='--', label='超卖线(30)')
        
        # 设置标题和标签
        if title:
            ax.set_title(title, fontsize=14)
        ax.set_xlabel('时间', fontsize=12)
        ax.set_ylabel('RSI值', fontsize=12)
        
        # 设置y轴范围
        ax.set_ylim(0, 100)
        
        # 设置x轴日期格式
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
        plt.xticks(rotation=45)
        
        # 添加网格线
        ax.grid(True, linestyle='--', alpha=0.7)
        
        # 添加图例
        ax.legend()
        
        # 调整布局
        plt.tight_layout()
        
        # 保存图表
        if save_path:
            plt.savefig(save_path, dpi=300)
        
        return fig
        
    except Exception as e:
        print(f"绘制RSI指标图失败: {e}")
        return None


def set_chinese_font():
    """
    设置matplotlib中文字体
    """
    # 设置中文字体支持
    plt.rcParams["font.family"] = ["SimHei", "WenQuanYi Micro Hei", "Heiti TC"]
    # 解决负号显示问题
    plt.rcParams['axes.unicode_minus'] = False