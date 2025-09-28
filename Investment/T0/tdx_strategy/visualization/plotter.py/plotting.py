import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from datetime import datetime


def setup_matplotlib():
    """设置matplotlib环境"""
    plt.rcParams.update({
        'font.sans-serif': ['SimHei'],
        'axes.unicode_minus': False
    })


def create_intraday_plot(df, stock_code, trade_date, prev_close, notify_callback=None):
    """创建分时图"""
    try:
        # 绘图设置
        plt.close('all')  # 关闭之前未关闭的图形，释放资源

        # 创建三个子图，按照要求布局（顶部信息栏、中部价格图、底部时间轴）
        fig = plt.figure(figsize=(12, 10))
        gs = fig.add_gridspec(3, 1, height_ratios=[1, 8, 1], hspace=0.1)

        ax_info = fig.add_subplot(gs[0])  # 顶部信息栏
        ax_price = fig.add_subplot(gs[1])  # 中部价格图
        ax_time = fig.add_subplot(gs[2])  # 底部时间轴

        # 移除缺失数据的行，确保只绘制有效数据
        df_filtered = df.dropna(subset=['收盘'])

        # 顶部信息栏显示均价、最新价、涨跌幅
        latest_price = df_filtered['收盘'].iloc[-1]
        avg_price = df_filtered['均价'].iloc[-1]
        change = latest_price - prev_close
        change_pct = (change / prev_close) * 100

        ax_info.clear()
        ax_info.set_xlim(0, 1)
        ax_info.set_ylim(0, 1)
        ax_info.axis('off')

        info_text = f"均价: {avg_price:.2f}    最新: {latest_price:.2f}    涨跌幅: {change:+.2f} ({change_pct:+.2f}%)"
        ax_info.text(0.5, 0.5, info_text, ha='center', va='center', fontsize=14, transform=ax_info.transAxes)

        # 使用数据点索引作为x轴坐标，确保所有数据点之间的距离均匀
        x_values = list(range(len(df_filtered)))

        # 绘制收盘价曲线
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
            if notify_callback:
                time_str = idx.strftime('%H:%M:%S')
                notify_callback('buy', stock_code, row['收盘'], time_str)

        # 绘制卖信号（绿三角）
        sell_signals = df_filtered[df_filtered['longcross_resistance']].dropna()
        for idx, row in sell_signals.iterrows():
            x_pos = df_filtered.index.get_loc(idx)
            ax_price.scatter(x_pos, row['收盘'] * 0.999, marker='v', color='green', s=60, zorder=5)
            ax_price.text(x_pos, row['收盘'] * 0.999, '卖',
                          color='green', fontsize=10, ha='center', va='top', fontweight='bold')
            # 调用通知函数
            if notify_callback:
                time_str = idx.strftime('%H:%M:%S')
                notify_callback('sell', stock_code, row['收盘'], time_str)

        # 设置坐标轴标签
        ax_price.set_ylabel('价格', fontsize=12)

        # 设置网格
        ax_price.grid(True, linestyle='--', alpha=0.7)

        # 昨收价参考线
        ax_price.axhline(prev_close, color='gray', linestyle='--', linewidth=1, alpha=0.7)

        # 设置x轴刻度
        total_points = len(df_filtered)
        if total_points > 100:
            step = max(1, total_points // 20)
        elif total_points > 50:
            step = max(1, total_points // 15)
        elif total_points > 20:
            step = max(1, total_points // 10)
        else:
            step = 1

        # 选择要显示的时间点和对应的索引位置
        selected_indices = list(range(0, total_points, step))
        selected_times = df_filtered.index[selected_indices]

        # 设置x轴刻度为数据点索引位置，但显示对应的时间标签
        ax_price.set_xticks(selected_indices)
        ax_price.set_xticklabels([t.strftime('%H:%M') for t in selected_times])

        # 自动旋转x轴标签以避免重叠
        plt.setp(ax_price.get_xticklabels(), rotation=45, ha="right")

        # 底部时间轴
        ax_time.set_xlim(0, total_points - 1)
        ax_time.set_ylim(0, 1)
        ax_time.axis('off')

        # 设置时间轴刻度
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
                        avg_price = data_point['均价']
                        
                        # 计算当前价格相对于均线的涨跌幅
                        if pd.notna(avg_price) and avg_price != 0:
                            diff_pct = ((price - avg_price) / avg_price) * 100
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
        print(f"绘图错误: {e}")
        return None