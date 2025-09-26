import akshare as ak
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime, timedelta
import os

# 设置matplotlib后端，确保图表能正确显示
import matplotlib
matplotlib.use('TkAgg')  # 使用TkAgg后端，适用于大多数环境
plt.rcParams.update({
    'font.sans-serif': ['SimHei'],
    'axes.unicode_minus': False
})

# ---------------------- 1. 指标计算（严格还原通达信公式） ----------------------
def calculate_tdx_indicators(df, prev_close, threshold=0.01):
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
    # 动态计算日内到当前时刻的最高/最低价（随时间推移更新）
    df['日内最高'] = df['最高'].cummax()  # 累积最高（到当前K线的最高）
    df['日内最低'] = df['最低'].cummin()  # 累积最低（到当前K线的最低）

    # 计算 H1、L1（昨收 vs 日内高低）
    df['H1'] = np.maximum(prev_close, df['日内最高'])
    df['L1'] = np.minimum(prev_close, df['日内最低'])

    # 支撑、阻力计算（严格按公式 0.5/8 和 7/8）
    df['P1'] = df['H1'] - df['L1']
    df['支撑'] = df['L1'] + df['P1'] * 0.5 / 8
    df['阻力'] = df['L1'] + df['P1'] * 7 / 8

    # 信号计算（严格对齐通达信逻辑）
    # 1. CROSS(支撑, 现价)：支撑上穿现价（前一周期支撑 < 现价，当前支撑 > 现价）= 现价下穿支撑（信号）
    df['cross_support'] = ((df['支撑'].shift(1) < df['收盘'].shift(1)) & (df['支撑'] > df['收盘'])) & \
                          (abs(df['支撑'] - df['收盘']) > threshold)

    # 2. LONGCROSS(支撑, 现价, 2)：连续2周期支撑 < 现价，当前支撑 > 现价（买信号）
    df['longcross_support'] = ((df['支撑'].shift(2) < df['收盘'].shift(2)) & \
                               (df['支撑'].shift(1) < df['收盘'].shift(1)) & \
                               (df['支撑'] > df['收盘'])) & \
                              (abs(df['支撑'] - df['收盘']) > threshold)

    # 3. LONGCROSS(现价, 阻力, 2)：连续2周期现价 < 阻力，当前现价 > 阻力（卖信号）
    df['longcross_resistance'] = ((df['收盘'].shift(2) < df['阻力'].shift(2)) & \
                                  (df['收盘'].shift(1) < df['阻力'].shift(1)) & \
                                  (df['收盘'] > df['阻力']))
                                 # (abs(df['收盘'] - df['阻力']) > threshold)

    return df


# ---------------------- 2. 昨收价获取（严格对应通达信 DYNAINFO(3)） ----------------------
def get_prev_close(stock_code, trade_date):
    """从日线数据获取前一日收盘价，失败则用分时开盘价替代"""
    try:
        trade_date_dt = datetime.strptime(trade_date, '%Y%m%d')
        prev_date = (trade_date_dt - timedelta(days=1)).strftime('%Y%m%d')

        # 获取日线数据（前一日 + 当日）
        daily_df = ak.stock_zh_a_hist(
            symbol=stock_code,
            period="daily",
            start_date=prev_date,
            end_date=trade_date,
            adjust=""
        )
        print(f"获取日线数据成功，日期: {daily_df['日期'].values[0]}")

        # 确保格式一致：把日期列也转为 'YYYYMMDD' 格式
        daily_df['日期'] = pd.to_datetime(daily_df['日期']).dt.strftime('%Y%m%d')
        print(daily_df)

        if daily_df.empty or prev_date not in daily_df['日期'].values:
            raise ValueError("前一日数据缺失")

        prev_close = daily_df[daily_df['日期'] == prev_date]['收盘'].values[0]
        print(f"昨收价: {prev_close:.2f}")
        return prev_close
    except Exception as e:
        print(f"昨收获取失败: {e}，将使用分时开盘价替代")
        return None

# ---------------------- 3. 缓存功能 ----------------------
def get_cached_data(stock_code, trade_date):
    """从缓存中获取数据"""
    cache_file = f"stock_data/{stock_code}_{trade_date}.csv"
    if os.path.exists(cache_file):
        try:
            df = pd.read_csv(cache_file)
            # 检查列名，修复可能的编码问题
            time_col = None
            for col in df.columns:
                if '时间' in col:
                    time_col = col
                    break

            if time_col:
                df['时间'] = pd.to_datetime(df[time_col])
                df = df.drop(columns=[time_col])
                df = df.set_index('时间')
                print(f"从缓存加载数据: {cache_file}")
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
        print(f"数据已保存到缓存: {cache_file}")
    except Exception as e:
        print(f"保存缓存文件失败: {e}")

# ---------------------- 4. 绘图函数（严格模仿通达信分时风格） ----------------------
def plot_tdx_intraday(stock_code, trade_date=None):
    try:
        # 1. 时间处理
        today = datetime.now().strftime('%Y%m%d')
        trade_date = trade_date or today

        # 2. 先尝试从缓存获取数据
        df = get_cached_data(stock_code, trade_date)
        
        # 3. 如果缓存没有数据，则从网络获取
        if df is None:
            print("缓存中无数据，从网络获取...")
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
            
            # 保存到缓存
            save_data_to_cache(df.copy(), stock_code, trade_date)
        else:
            print("使用缓存数据")

        # 打印原始时间列（调试用）
        # print("📅 分时数据原始时间列（前5行）：")
        # print(df['时间'].head())
        # print("🕒 时间列原始类型：", df['时间'].dtype)

        # 强制转换为 datetime（AkShare 返回的时间已包含日期）
        df['时间'] = pd.to_datetime(df['时间'], errors='coerce')

        df = df[df['时间'].notna()]
        df = df[~((df['时间'].dt.hour == 11) & (df['时间'].dt.minute >= 30)) & ~((df['时间'].dt.hour == 12))]
        if df.empty:
            print("❌ 所有时间数据均无效")
            return None

        # 强制校准时间索引（只生成到当前时间的索引）
        current_time = datetime.now().strftime('%Y%m%d %H:%M:%S')
        full_index = pd.date_range(
            start=f"{trade_date} 09:30:00",
            end=current_time,
            freq='1min'
        )
        full_index = full_index[
            ((full_index.hour == 9) & (full_index.minute >= 30)) |
            ((full_index.hour >= 10) & (full_index.hour <= 11) & (full_index.minute < 30)) |
            ((full_index.hour >= 13) & (full_index.hour <= 14))
            ]
        df = df.set_index('时间').reindex(full_index)
        df.index.name = '时间'

        # 获取昨收（fallback到开盘价）
        prev_close = get_prev_close(stock_code, trade_date)
        if prev_close is None:
            prev_close = df['开盘'].dropna().iloc[0]
            print(f"⚠️ 使用分时开盘价替代昨收: {prev_close:.2f}")

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

        # 调试信息
        print("✅ 过滤后数据概览：")
        print(df[['开盘', '收盘', '最高', '最低']].head())
        print(f"数据时间范围：{df.index.min()} ~ {df.index.max()}")
        print(f"有效数据量：{len(df)} 条")

        # 绘图设置（规范图形创建）
        plt.close('all')  # 关闭之前未关闭的图形，释放资源

        # 创建三个子图，按照要求布局（顶部信息栏、中部价格图、底部时间轴）
        fig = plt.figure(figsize=(12, 10))
        gs = fig.add_gridspec(3, 1, height_ratios=[1, 8, 1], hspace=0.1)
        
        ax_info = fig.add_subplot(gs[0])      # 顶部信息栏
        ax_price = fig.add_subplot(gs[1])     # 中部价格图
        ax_time = fig.add_subplot(gs[2])      # 底部时间轴

        # 过滤掉 11:30 到 13:00 之间的数据
        df_filtered = df[~((df.index.hour == 11) & (df.index.minute >= 30)) & ~((df.index.hour == 12))]

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
        
        # 中部价格图
        price_min = df_filtered['收盘'].min()
        price_max = df_filtered['收盘'].max()
        margin = (price_max - price_min) * 0.1
        if margin == 0:
            margin = 0.01
        ax_price.set_ylim(price_min - margin, price_max + margin)
        
        # 绘制价格线
        ax_price.plot(
            df_filtered.index,
            df_filtered['收盘'],
            color='crimson',
            linewidth=1.5,
            label='现价',
            antialiased=True
        )
        
        # 绘制均价线（黄线）
        ax_price.plot(
            df_filtered.index,
            df_filtered['均价'],
            color='yellow',
            linewidth=1.5,
            label='均价',
            antialiased=True
        )

        # 9. 绘制支撑、阻力线
        ax_price.plot(df_filtered.index, df_filtered['支撑'], color='#00DD00', linestyle='--', linewidth=1, label='支撑')
        ax_price.plot(df_filtered.index, df_filtered['阻力'], color='#ff0000', linestyle='--', linewidth=1, label='阻力')

        # 10. 绘制黄色柱状线（CROSS(支撑, 现价)）
        for idx in df_filtered[df_filtered['cross_support']].index:
            ax_price.plot([idx, idx], [df_filtered['支撑'][idx], df_filtered['阻力'][idx]],
                    'yellow', linewidth=2, alpha=0.7, solid_capstyle='round')

        # 绘制买信号（红三角）
        buy_signals = df_filtered[df_filtered['longcross_support']].dropna()
        for idx, row in buy_signals.iterrows():
            ax_price.scatter(idx, row['支撑'] * 1.001, marker='^', color='red', s=60, zorder=5)
            ax_price.text(idx, row['支撑'] * 1.001, '买',
                    color='red', fontsize=10, ha='center', va='bottom', fontweight='bold')

        # 绘制卖信号（绿三角）
        sell_signals = df_filtered[df_filtered['longcross_resistance']].dropna()
        for idx, row in sell_signals.iterrows():
            ax_price.scatter(idx, row['收盘'] * 0.999, marker='v', color='green', s=60, zorder=5)
            ax_price.text(idx, row['收盘'] * 0.999, '卖',
                    color='green', fontsize=10, ha='center', va='top', fontweight='bold')

        # 设置价格图的网格
        ax_price.grid(True, linestyle='--', alpha=0.5, color='gray')
        ax_price.set_ylabel('价格', fontsize=12)
        
        # 昨收价参考线
        ax_price.axhline(prev_close, color='gray', linestyle='--', linewidth=1, alpha=0.7)
        
        # 隐藏中部图表的x轴标签
        ax_price.set_xticklabels([])
        
        # 底部时间轴
        ax_time.set_xlim(df_filtered.index.min(), df_filtered.index.max())
        ax_time.set_ylim(0, 1)
        ax_time.axis('off')
        
        # 设置时间轴刻度
        time_ticks = []
        time_labels = []
        
        # 添加上午时间刻度 (9:30 - 11:30)
        morning_times = pd.date_range(start=f"{trade_date} 09:30", end=f"{trade_date} 11:30", freq='30min')
        for time in morning_times:
            if time in df_filtered.index or True:  # 总是添加主要时间点
                time_ticks.append(time)
                time_labels.append(time.strftime('%H:%M'))
        
        # 添加下午时间刻度 (13:00 - 15:00)
        afternoon_times = pd.date_range(start=f"{trade_date} 13:00", end=f"{trade_date} 15:00", freq='30min')
        for time in afternoon_times:
            if time in df_filtered.index or True:  # 总是添加主要时间点
                time_ticks.append(time)
                time_labels.append(time.strftime('%H:%M'))
        
        # 在时间轴上显示时间标签
        for i, (tick, label) in enumerate(zip(time_ticks, time_labels)):
            ax_time.text(tick, 0.5, label, ha='center', va='center', fontsize=10)
            # 添加时间刻度线
            ax_price.axvline(tick, color='gray', linestyle='-', linewidth=0.5, alpha=0.5)
        
        ax_time.set_xticks(time_ticks)
        ax_time.set_xticklabels(time_labels)
        
        # 鼠标悬浮显示价格和时间
        annotation = ax_price.annotate('', xy=(0,0), xytext=(10, 10), textcoords='offset points',
                                      bbox=dict(boxstyle='round', fc='yellow', alpha=0.7),
                                      arrowprops=dict(arrowstyle='->'), fontsize=10)
        annotation.set_visible(False)

        def on_move(event):
            if event.inaxes == ax_price:
                if event.xdata is not None and event.ydata is not None:
                    # 找到最近的时间点
                    x_date = mdates.num2date(event.xdata)
                    x_date = x_date.replace(tzinfo=None)
                    closest_idx = df_filtered.index.get_indexer([x_date], method='nearest')[0]
                    if 0 <= closest_idx < len(df_filtered):
                        data_point = df_filtered.iloc[closest_idx]
                        time_str = df_filtered.index[closest_idx].strftime('%H:%M')
                        annotation.xy = (event.xdata, event.ydata)
                        annotation.set_text(f"时间: {time_str}\n价格: {data_point['收盘']:.2f}")
                        annotation.set_visible(True)
                        fig.canvas.draw_idle()
            else:
                if annotation.get_visible():
                    annotation.set_visible(False)
                    fig.canvas.draw_idle()

        fig.canvas.mpl_connect('motion_notify_event', on_move)

        # 设置图表标题
        fig.suptitle(f'{stock_code} 分时图 - {trade_date}', fontsize=14, y=0.98)
        
        # 添加图例到价格图
        ax_price.legend(loc='upper left', fontsize=10)

        plt.tight_layout()
        plt.subplots_adjust(top=0.95)
        
        # 强制显示（解决后端静默问题）
        plt.show(block=True)

        return df

    except Exception as e:
        print(f"❌ 错误: {e}")
        import traceback
        traceback.print_exc()
        return None


# ---------------------- 5. 主程序（运行示例） ----------------------
if __name__ == "__main__":
    # stock_code = '516780'  # 长江电力
    stock_code = '601728'  # 中国电信
    # stock_code = '601766'  # 中国中车
    # stock_code = '601398'  # 工商银行
    trade_date = '20250926'  # 交易日期

    # 绘制并获取结果
    result_df = plot_tdx_intraday(stock_code, trade_date)
    # get_prev_close(stock_code, trade_date)
    # df = ak.stock_zh_a_hist_min_em(
    #     symbol=stock_code,
    #     period="1",
    #     start_date=trade_date,
    #     end_date=trade_date,
    #     adjust=''
    # )
    # print(df)

    # 保存结果（可选）
    # if result_df is not None:
    #     result_df.to_csv(f'{stock_code}_{trade_date}_通达信分时信号.csv', encoding='utf-8-sig')
    #     print(f"结果已保存到: {stock_code}_{trade_date}_通达信分时信号.csv")