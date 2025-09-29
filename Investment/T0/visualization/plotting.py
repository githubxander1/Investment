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
        colors = ['red' if df.loc[i, '收盘'] >= df.loc[i, '开盘'] else 'green' for i in range(len(df)) if '开盘' in df.columns]
        if not colors:
            colors = ['blue'] * len(df)
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


def setup_matplotlib():
    """设置matplotlib（兼容旧版接口）"""
    # 设置matplotlib后端，确保图表能正确显示
    import matplotlib
    matplotlib.use('TkAgg')  # 使用TkAgg后端，适用于大多数环境
    plt.rcParams.update({
        'font.sans-serif': ['SimHei'],
        'axes.unicode_minus': False
    })


def create_intraday_plot(df, stock_code, trade_date, prev_close, notify_signal_func):
    """创建分时图（兼容旧版接口）"""
    try:
        # 移除缺失数据的行，确保只绘制有效数据
        df_filtered = df.dropna(subset=['收盘'])

        # 调试信息
        print("✅ 过滤后数据概览：")
        print(df_filtered[['开盘', '收盘', '最高', '最低']].head())
        print(f"数据时间范围：{df_filtered.index.min()} ~ {df_filtered.index.max()}")
        print(f"有效数据量：{len(df_filtered)} 条")

        # 绘图设置（规范图形创建）
        plt.close('all')  # 关闭之前未关闭的图形，释放资源

        # 创建三个子图，按照要求布局（顶部信息栏、中部价格图、底部时间轴）
        fig = plt.figure(figsize=(12, 10))
        gs = fig.add_gridspec(3, 1, height_ratios=[1, 8, 1], hspace=0.1)

        ax_info = fig.add_subplot(gs[0])  # 顶部信息栏
        ax_price = fig.add_subplot(gs[1])  # 中部价格图
        ax_time = fig.add_subplot(gs[2])  # 底部时间轴

        # 顶部信息栏显示均价、最新价、涨跌幅
        latest_price = df_filtered['收盘'].iloc[-1]
        avg_price = df_filtered['均价'].iloc[-1] if '均价' in df_filtered.columns else latest_price
        change = latest_price - prev_close
        change_pct = (change / prev_close) * 100

        ax_info.clear()
        ax_info.set_xlim(0, 1)
        ax_info.set_ylim(0, 1)
        ax_info.axis('off')

        info_text = f"均价: {avg_price:.2f}    最新: {latest_price:.2f}    涨跌幅: {change:+.2f} ({change_pct:+.2f}%)"
        ax_info.text(0.5, 0.5, info_text, ha='center', va='center', fontsize=14, transform=ax_info.transAxes)

        # 使用T.py中的绘图方式替换原有的中部价格图绘制逻辑
        # 使用数据点索引作为x轴坐标，确保所有数据点之间的距离均匀
        x_values = list(range(len(df_filtered)))

        # 绘制收盘价曲线，严格按照文件中的实际时间点连接
        ax_price.plot(x_values, df_filtered['收盘'], marker='', linestyle='-', color='blue', linewidth=2,
                      label='收盘价')

        # 绘制均价线
        if '均价' in df_filtered.columns and not df_filtered['均价'].isna().all():
            ax_price.plot(x_values, df_filtered['均价'], marker='', linestyle='-', color='yellow', linewidth=1.5,
                          label='均价线')

        # 绘制支撑线和阻力线
        ax_price.plot(x_values, df_filtered['支撑'], marker='', linestyle='--', color='#00DD00', linewidth=1,
                      label='支撑')
        ax_price.plot(x_values, df_filtered['阻力'], marker='', linestyle='--', color='#ff0000', linewidth=1,
                      label='阻力')

        # 绘制黄色柱状线（CROSS(支撑, 现价)）
        cross_support_points = df_filtered[df_filtered['cross_support']]
        for idx in cross_support_points.index:
            x_pos = df_filtered.index.get_loc(idx)
            ax_price.plot([x_pos, x_pos],
                          [cross_support_points.loc[idx, '支撑'], cross_support_points.loc[idx, '阻力']],
                          color='yellow', linewidth=2, alpha=0.7, solid_capstyle='round')

        # 绘制买信号（红三角）
        buy_signals = df_filtered[df_filtered['longcross_support']].dropna()
        for idx, row in buy_signals.iterrows():
            x_pos = df_filtered.index.get_loc(idx)
            ax_price.scatter(x_pos, row['支撑'] * 1.001, marker='^', color='red', s=60, zorder=5)
            ax_price.text(x_pos, row['支撑'] * 1.001, '买',
                          color='red', fontsize=10, ha='center', va='bottom', fontweight='bold')
            # 调用通知函数
            time_str = idx.strftime('%H:%M:%S')
            notify_signal_func('buy', stock_code, row['收盘'], time_str)

        # 绘制卖信号（绿三角）
        sell_signals = df_filtered[df_filtered['longcross_resistance']].dropna()
        for idx, row in sell_signals.iterrows():
            x_pos = df_filtered.index.get_loc(idx)
            ax_price.scatter(x_pos, row['收盘'] * 0.999, marker='v', color='green', s=60, zorder=5)
            ax_price.text(x_pos, row['收盘'] * 0.999, '卖',
                          color='green', fontsize=10, ha='center', va='top', fontweight='bold')
            # 调用通知函数
            time_str = idx.strftime('%H:%M:%S')
            notify_signal_func('sell', stock_code, row['收盘'], time_str)

        # 设置坐标轴标签
        ax_price.set_ylabel('价格', fontsize=12)

        # 设置网格
        ax_price.grid(True, linestyle='--', alpha=0.7)

        # 昨收价参考线
        ax_price.axhline(prev_close, color='gray', linestyle='--', linewidth=1, alpha=0.7)

        # 严格按照CSV文件中的实际时间点设置x轴刻度，不添加CSV中不存在的时间点
        # 只选择部分时间点作为刻度，避免标签过多重叠
        total_points = len(df_filtered)
        if total_points > 100:
            # 数据点非常多时，间隔选择更多点
            step = max(1, total_points // 20)
        elif total_points > 50:
            # 数据点较多时，间隔选择一些点
            step = max(1, total_points // 15)
        elif total_points > 20:
            # 数据点适中时，间隔选择较少点
            step = max(1, total_points // 10)
        else:
            # 数据点较少时，显示所有点
            step = 1

        # 选择要显示的时间点和对应的索引位置
        selected_indices = list(range(0, total_points, step))
        selected_times = df_filtered.index[selected_indices]

        # 设置x轴刻度为数据点索引位置，但显示对应的时间标签
        ax_price.set_xticks(selected_indices)
        ax_price.set_xticklabels([t.strftime('%H:%M') for t in selected_times])

        # 自动旋转x轴标签以避免重叠
        plt.setp(ax_price.get_xticklabels(), rotation=45, ha="right")

        # 隐藏中部图表的x轴标签（因为底部有时间轴）
        # ax_price.set_xticklabels([])  # 注释掉这行，恢复时间标签显示

        # 底部时间轴
        ax_time.set_xlim(0, total_points - 1)
        ax_time.set_ylim(0, 1)
        ax_time.axis('off')

        # 设置时间轴刻度，只显示时间部分
        ax_time.set_xticks(selected_indices)
        ax_time.set_xticklabels([t.strftime('%H:%M') for t in selected_times])

        # 设置图表标题
        fig.suptitle(f'{stock_code} 分时图 - {trade_date}', fontsize=14, y=0.98)

        # 添加图例到价格图
        ax_price.legend(loc='upper left', fontsize=10)

        # 鼠标悬浮显示价格、时间以及当前价格相对于均线的涨跌幅
        annotation = ax_price.annotate('', xy=(0, 0), xytext=(10, 10), textcoords='offset points',
                                       bbox=dict(boxstyle='round', fc='yellow', alpha=0.7),
                                       arrowprops=dict(arrowstyle='->'), fontsize=10)
        annotation.set_visible(False)

        def on_move(event):
            if event.inaxes == ax_price:
                if event.xdata is not None:
                    # 获取最近的整数索引
                    x_index = int(round(event.xdata))
                    # 确保索引在有效范围内
                    if 0 <= x_index < len(df_filtered):
                        data_point = df_filtered.iloc[x_index]
                        time_str = df_filtered.index[x_index].strftime('%H:%M')
                        price = data_point['收盘']
                        avg_price_val = data_point['均价'] if '均价' in data_point else price
                        
                        # 计算当前价格相对于均线的涨跌幅
                        if pd.notna(avg_price_val) and avg_price_val != 0:
                            diff_pct = ((price - avg_price_val) / avg_price_val) * 100
                            annotation.xy = (x_index, price)
                            annotation.set_text(f"时间: {time_str}\n价格: {price:.2f}\n相对均线: {diff_pct:+.2f}%")
                        else:
                            annotation.xy = (x_index, price)
                            annotation.set_text(f"时间: {time_str}\n价格: {price:.2f}\n相对均线: N/A")
                        
                        annotation.set_visible(True)
                        fig.canvas.draw_idle()
                    else:
                        if annotation.get_visible():
                            annotation.set_visible(False)
                            fig.canvas.draw_idle()
            else:
                if annotation.get_visible():
                    annotation.set_visible(False)
                    fig.canvas.draw_idle()

        fig.canvas.mpl_connect('motion_notify_event', on_move)

        plt.tight_layout()
        plt.subplots_adjust(top=0.95)

        return fig

    except Exception as e:
        print(f"❌ 创建分时图错误: {e}")
        import traceback
        traceback.print_exc()
        return None