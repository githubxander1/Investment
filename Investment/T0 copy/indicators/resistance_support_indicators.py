import akshare as ak
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime, timedelta
import os
import time

# 设置matplotlib后端，确保图表能正确显示
import matplotlib

matplotlib.use('Agg')  # 使用Agg后端，不显示图形界面
plt.rcParams.update({
    'font.sans-serif': ['SimHei'],
    'axes.unicode_minus': False
})


# ---------------------- 1. 指标计算（严格还原通达信公式） ----------------------
def calculate_tdx_indicators(df, prev_close, threshold=0.005):
    """
    通达信公式还原：
    H1:=MAX(昨收, 当日最高价);
    L1:=MIN(昨收, 当日最低价);
    P1:=H1-L1;
    阻力:L1+P1*7/8;
    支撑:L1+P1*0.5/8;
    CROSS(支撑,现价) → 支撑上穿现价（画黄色柱）
    LONGCROSS(支撑,现价,2) → 买信号（红三角）
    LONGCROSS(现价,阻力,2) → 卖信号（绿三角）
    """
    # 获取当日最高价和最低价（不是累积最大值/最小值）
    daily_high = df['最高'].max()
    daily_low = df['最低'].min()

    # 计算 H1、L1（昨收 vs 日内高低）
    # 注意：在通达信中，H1和L1是基于动态行情数据的，这里尽量还原
    df['H1'] = np.maximum(prev_close, daily_high)
    df['L1'] = np.minimum(prev_close, daily_low)

    # 支撑、阻力计算（严格按通达信公式：L1+P1*0.5/8 和 L1+P1*7/8）
    # 注意：这里的计算与通达信公式完全一致
    df['P1'] = df['H1'] - df['L1']
    df['支撑'] = df['L1'] + df['P1'] * 0.5 / 8
    df['阻力'] = df['L1'] + df['P1'] * 7 / 8

    # 信号计算（严格对齐通达信逻辑）
    # 1. CROSS(支撑, 现价)：支撑上穿现价（前一周期支撑 < 现价，当前支撑 > 现价）= 现价下穿支撑（信号）
    # 这是通达信中黄色竖线的买入信号
    df['cross_support'] = ((df['支撑'].shift(1) < df['收盘'].shift(1)) & 
                          (df['支撑'] > df['收盘'])) & \
                          (abs(df['支撑'] - df['收盘']) > threshold)

    # 2. LONGCROSS(支撑, 现价, 2)：连续2周期支撑 < 现价，当前支撑 > 现价（买信号）
    # 通达信中的LONGCROSS(X,Y,N)函数表示X在N周期内都小于Y，本周期X上穿Y
    # 修复索引问题，使用正确的逐行计算方式
    df['longcross_support'] = ((df['支撑'].shift(2) < df['收盘'].shift(2)) & \
                               (df['支撑'].shift(1) < df['收盘'].shift(1)) & \
                               (df['支撑'] > df['收盘'])) & \
                              (abs(df['支撑'] - df['收盘']) > threshold)
    
    # 3. LONGCROSS(现价, 阻力, 2)：连续2周期现价 < 阻力，当前现价 > 阻力（卖信号）
    df['longcross_resistance'] = ((df['收盘'].shift(2) < df['阻力'].shift(2)) & \
                                  (df['收盘'].shift(1) < df['阻力'].shift(1)) & \
                                  (df['收盘'] > df['阻力'])) & \
                                 (abs(df['收盘'] - df['阻力']) > threshold)

    # 打印第一次买入信号的时间点
    first_buy_signal = df[df['longcross_support']].first_valid_index()
    if first_buy_signal is not None:
        first_buy_price = df.loc[first_buy_signal, '收盘']
        # 计算相对均线的涨跌幅
        if '均价' in df.columns:
            first_buy_avg_price = df.loc[first_buy_signal, '均价']
            if pd.notna(first_buy_avg_price) and first_buy_avg_price != 0:
                diff_pct = ((first_buy_price - first_buy_avg_price) / first_buy_avg_price) * 100
                print(f"阻力支撑：第一次买入信号时间点: {first_buy_signal.strftime('%Y-%m-%d %H:%M:%S')}, 价格: {first_buy_price:.2f}, 相对均线涨跌幅: {diff_pct:+.2f}%")
            else:
                print(f"阻力支撑：第一次买入信号时间点: {first_buy_signal.strftime('%Y-%m-%d %H:%M:%S')}, 价格: {first_buy_price:.2f}, 相对均线涨跌幅: N/A")
        else:
            print(f"阻力支撑：第一次买入信号时间点: {first_buy_signal.strftime('%Y-%m-%d %H:%M:%S')}, 价格: {first_buy_price:.2f}")
    else:
        print("未检测到买入信号")
    
    # 打印第一次卖出信号的时间点
    first_sell_signal = df[df['longcross_resistance']].first_valid_index()
    if first_sell_signal is not None:
        first_sell_price = df.loc[first_sell_signal, '收盘']
        # 计算相对均线的涨跌幅
        if '均价' in df.columns:
            first_sell_avg_price = df.loc[first_sell_signal, '均价']
            if pd.notna(first_sell_avg_price) and first_sell_avg_price != 0:
                diff_pct = ((first_sell_price - first_sell_avg_price) / first_sell_avg_price) * 100
                print(f"阻力支撑：第一次卖出信号时间点: {first_sell_signal.strftime('%Y-%m-%d %H:%M:%S')}, 价格: {first_sell_price:.2f}, 相对均线涨跌幅: {diff_pct:+.2f}%")
            else:
                print(f"阻力支撑：第一次卖出信号时间点: {first_sell_signal.strftime('%Y-%m-%d %H:%M:%S')}, 价格: {first_sell_price:.2f}, 相对均线涨跌幅: N/A")
        else:
            print(f"阻力支撑：第一次卖出信号时间点: {first_sell_signal.strftime('%Y-%m-%d %H:%M:%S')}, 价格: {first_sell_price:.2f}")
    else:
        print("未检测到卖出信号")

    return df


# ---------------------- 2. 昨收价获取（严格对应通达信 DYNAINFO(3)） ----------------------
# def get_prev_close(stock_code, trade_date):
#     daily_df = ak.stock_zh_a_daily(symbol=stock_code, start_date=trade_date, end_date=trade_date)
#     # daily_df = ak.stock_sz_a_spot_em()
#     print(daily_df)
#     close = daily_df['close'].iloc[-1]
#     print("close: ", close)

def get_prev_close(stock_code, trade_date):
    """从日线数据获取前一日收盘价，失败则用分时开盘价替代"""
    max_retries = 3
    for attempt in range(max_retries):
        try:
            trade_date_dt = datetime.strptime(trade_date, '%Y%m%d')
            
            # 如果是周末，获取上周五的收盘价
            weekday = trade_date_dt.weekday()  # 0=Monday, 6=Sunday
            if weekday == 5:  # Saturday
                trade_date_dt = trade_date_dt - timedelta(days=1)  # Friday
            elif weekday == 6:  # Sunday
                trade_date_dt = trade_date_dt - timedelta(days=2)  # Friday
            
            # 获取日线数据
            daily_df = ak.stock_zh_a_hist(
                symbol=stock_code,
                period="daily",
                adjust=""
            )


            if daily_df.empty:
                raise ValueError("无法获取日线数据")
                
            # 检查是否存在日期列
            if '日期' not in daily_df.columns:
                print(f"日线数据中缺少'日期'列，列名包括: {list(daily_df.columns)}")
                raise ValueError("日线数据格式错误，缺少日期列")

            # 转换日期列为datetime类型
            daily_df['日期'] = pd.to_datetime(daily_df['日期'])

            # 筛选出在交易日期之前的数据
            df_before = daily_df[daily_df['日期'] < trade_date_dt]

            if df_before.empty:
                raise ValueError("没有找到前一日数据")

            # 检查是否存在收盘列
            if '收盘' not in df_before.columns:
                print(f"日线数据中缺少'收盘'列，列名包括: {list(df_before.columns)}")
                raise ValueError("日线数据格式错误，缺少收盘列")

            # 获取最近的收盘价（上一个交易日）
            prev_close = df_before.iloc[-1]['收盘']
            return prev_close
        except Exception as e:
            if attempt == max_retries - 1:
                print(f"获取昨收价失败，最后一次尝试出错: {e}")
                return None
            else:
                print(f"获取昨收价时出错: {e}，正在重试... (第{attempt+1}次)")
                time.sleep(3)  # 等待3秒后重试


# ---------------------- 3. 缓存功能 ----------------------
def get_cached_data(stock_code, trade_date):
    """从缓存中获取数据"""
    cache_file = f"stock_data/{stock_code}_{trade_date}.csv"
    if os.path.exists(cache_file):
        try:
            df = pd.read_csv(cache_file)

            # 检查是否包含时间列
            if '时间' in df.columns:
                df['时间'] = pd.to_datetime(df['时间'])
                # 注意：缓存数据不设置时间列为索引，保持与网络获取数据一致的格式
                return df
            else:
                print("缓存文件中未找到时间列")
        except Exception as e:
            print(f"读取缓存文件失败: {e}")
    return None


def save_data_to_cache(df, stock_code, trade_date):
    """保存数据到缓存"""
    # 确保 stock_data 目录存在
    os.makedirs("stock_data", exist_ok=True)

    cache_file = f"stock_data/{stock_code}_{trade_date}.csv"
    try:
        df_reset = df.reset_index()
        df_reset.to_csv(cache_file, index=False)
    except Exception as e:
        print(f"保存缓存文件失败: {e}")


# ---------------------- 4. 绘图函数 ----------------------
def plot_tdx_intraday(stock_code, trade_date=None):
    try:
        # 1. 时间处理
        today = datetime.now().strftime('%Y%m%d')
        trade_date = trade_date or today

        # 2. 先尝试从缓存获取数据
        df = get_cached_data(stock_code, trade_date)

        # 3. 如果缓存没有数据，则从网络获取
        if df is None:
            df = ak.stock_zh_a_hist_min_em(
                symbol=stock_code,
                period="1",
                start_date=trade_date,
                end_date=trade_date,
                adjust=''
            )
            if df.empty:
                print("❌ 无分时数据")
                return None

            # 保存到缓存前确保列名正确
            if '时间' not in df.columns:
                # 查找实际的时间列
                time_col = None
                for col in df.columns:
                    if '时间' in col or 'date' in col.lower() or 'time' in col.lower():
                        time_col = col
                        break
                if time_col:
                    df.rename(columns={time_col: '时间'}, inplace=True)

            # 保存到缓存
            save_data_to_cache(df.copy(), stock_code, trade_date)
            data_from_cache = False
        else:
            data_from_cache = True

        # 如果数据来自缓存，则时间列已经是索引，否则需要转换时间列
        if not data_from_cache:
            # 强制转换为 datetime（AkShare 返回的时间已包含日期）
            df['时间'] = pd.to_datetime(df['时间'], errors='coerce')

        df = df[df['时间'].notna()]

        # 只保留指定日期的数据，不延伸到今天
        target_date = pd.to_datetime(trade_date, format='%Y%m%d')
        df_original = df.copy()  # 保存原始数据
        df = df[df['时间'].dt.date == target_date.date()]

        # 过滤掉 11:30 到 13:00 之间的数据
        df = df[~((df['时间'].dt.hour == 11) & (df['时间'].dt.minute >= 30)) & ~((df['时间'].dt.hour == 12))]
        if df.empty:
            print("❌ 所有时间数据均无效")
            return None

        # 分离上午和下午的数据
        morning_data = df[df['时间'].dt.hour < 12]
        afternoon_data = df[df['时间'].dt.hour >= 13]

        # 强制校准时间索引（只生成到指定日期的时间索引）
        morning_index = pd.date_range(
            start=f"{trade_date} 09:30:00",
            end=f"{trade_date} 11:30:00",
            freq='1min'
        )
        afternoon_index = pd.date_range(
            start=f"{trade_date} 13:00:00",
            end=f"{trade_date} 15:00:00",
            freq='1min'
        )

        # 合并索引
        full_index = morning_index.union(afternoon_index)
        df = df.set_index('时间').reindex(full_index)
        df.index.name = '时间'

        # 获取昨收（fallback到开盘价）
        prev_close = get_prev_close(stock_code, trade_date)
        if prev_close is None:
            prev_close = df['开盘'].dropna().iloc[0]

        # 计算指标
        df = df.ffill().bfill()  # 填充缺失值
        df = calculate_tdx_indicators(df, prev_close)

        # 计算均价
        df['均价'] = df['收盘'].expanding().mean()

        # 数据校验
        required_cols = ['开盘', '收盘', '最高', '最低', '支撑', '阻力']
        if not all(col in df.columns for col in required_cols):
            missing_cols = [col for col in required_cols if col not in df.columns]
            print(f"❌ 数据缺失关键列：{missing_cols}")
            return None

        if df['收盘'].isna().all():
            print("❌ 收盘价全为空")
            return None

        # 绘图设置（规范图形创建）
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

        # 绘制黄色柱状线（CROSS(支撑, 现价)）- 这是通达信中显示的买入信号（黄色竖线）
        cross_support_points = df_filtered[df_filtered['cross_support']]
        for idx in cross_support_points.index:
            x_pos = df_filtered.index.get_loc(idx)
            ax_price.plot([x_pos, x_pos],
                          [cross_support_points.loc[idx, '支撑'], cross_support_points.loc[idx, '阻力']],
                          color='yellow', linewidth=2, alpha=0.7, solid_capstyle='round')

        # 绘制买信号（红三角 + 竖线）- 这是LONGCROSS信号
        buy_signals = df_filtered[df_filtered['longcross_support']].dropna()
        
        # 重要提示：通达信中黄色竖线是CROSS(支撑,现价)信号，而红三角是LONGCROSS信号
        # 黄色竖线是更基础的买入信号，红三角是更严格的买入信号
        for idx, row in buy_signals.iterrows():
            x_pos = df_filtered.index.get_loc(idx)
            # 绘制红三角
            ax_price.scatter(x_pos, row['支撑'] * 1.001, marker='^', color='red', s=60, zorder=5)
            ax_price.text(x_pos, row['支撑'] * 1.001, '买',
                          color='red', fontsize=10, ha='center', va='bottom', fontweight='bold')
            # 绘制竖线信号
            ax_price.axvline(x=x_pos, color='red', linestyle='-', linewidth=2, alpha=0.7, zorder=4)

        # 绘制卖信号（绿三角 + 绿色竖线）
        sell_signals = df_filtered[df_filtered['longcross_resistance']].dropna()
        
        for idx, row in sell_signals.iterrows():
            x_pos = df_filtered.index.get_loc(idx)
            ax_price.scatter(x_pos, row['收盘'] * 0.999, marker='v', color='green', s=60, zorder=5)
            ax_price.text(x_pos, row['收盘'] * 0.999, '卖',
                          color='green', fontsize=10, ha='center', va='top', fontweight='bold')
            # 添加绿色竖线（与买入信号的黄色竖线相区分）
            ax_price.axvline(x=x_pos, color='green', linestyle='-', linewidth=2, alpha=0.7, zorder=4)

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

        # 使用 constrained_layout 替代 tight_layout 来避免警告
        plt.rcParams['figure.constrained_layout.use'] = True
        # plt.tight_layout()  # 移除这行以避免警告

        # 保存图表到output目录
        output_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'output', 'charts')
        os.makedirs(output_dir, exist_ok=True)
        chart_filename = os.path.join(output_dir, f'{stock_code}_{trade_date}_阻力支撑指标.png')
        
        # 直接保存，覆盖同名文件
        plt.savefig(chart_filename, dpi=300, bbox_inches='tight', format='png')

        # 关闭图形以避免阻塞
        plt.close(fig)

        return df

    except Exception as e:
        print(f"❌ 错误: {e}")
        import traceback
        traceback.print_exc()
        return None


# ---------------------- 5. 主程序（运行示例） ----------------------
if __name__ == "__main__":
    stock_code = '600030'  #
    trade_date = '20251017'  # 交易日期

    # pre = get_prev_close(stock_code, trade_date)
    # print(f"前收盘价: {pre}")

    # 绘制并获取结果
    result_df = plot_tdx_intraday(stock_code, trade_date)

    # 不再保存CSV文件，只生成图表
    if result_df is not None:
        print("图表已保存到output/charts目录")
    else:
        print("图表生成失败")
