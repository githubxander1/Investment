import akshare as ak
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime, timedelta

import matplotlib

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


# ---------------------- 3. 绘图函数（严格模仿通达信分时风格） ----------------------
def plot_tdx_intraday(stock_code, trade_date=None):
    try:
        # 1. 时间处理
        today = datetime.now().strftime('%Y%m%d')
        trade_date = trade_date or today

        # 2. 获取分时数据（1分钟周期）
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

        fig, ax = plt.subplots(figsize=(12, 8))  # 增大图表尺寸

        # 设置默认的纵轴范围
        price_min = df['收盘'].min()
        price_max = df['收盘'].max()
        default_margin = 0.2  # 默认裕量比例
        ax.set_ylim(price_min - (price_max - price_min) * default_margin,
                    price_max + (price_max - price_min) * default_margin)

        # 过滤掉 11:30 到 13:00 之间的数据
        df_filtered = df[~((df.index.hour == 11) & (df.index.minute >= 30)) & ~((df.index.hour == 12))]

        # 绘制价格线
        ax.plot(
            df_filtered.index,
            df_filtered['收盘'],
            color='crimson',
            linewidth=2,
            label='现价',
            antialiased=True
        )

        # # 手动连接 11:30 和 13:01 的数据
        # if not df.empty:
        #     # 获取 11:30 的最后一个数据点和 13:01 的第一个数据点
        #     idx_11_30 = df.index.asof(pd.Timestamp(f"{trade_date} 11:30:00"))
        #     idx_13_01 = df.index.asof(pd.Timestamp(f"{trade_date} 13:01:00"))
        #
        #     if idx_11_30 and idx_13_01:
        #         value_11_30 = df.loc[idx_11_30, '收盘']
        #         value_13_01 = df.loc[idx_13_01, '收盘']
        #
        #         # 连接这两个点
        #         ax.plot([idx_11_30, idx_13_01], [value_11_30, value_13_01], color='crimson', linewidth=2, antialiased=True)

        # 9. 绘制支撑、阻力线
        ax.plot(df.index, df['支撑'], color='#00DD00', linestyle='--', linewidth=1.2, label='支撑')
        ax.plot(df.index, df['阻力'], color='#ff0000', linestyle='--', linewidth=1.2, label='阻力')

        # 10. 绘制黄色柱状线（CROSS(支撑, 现价)）
        for idx in df[df['cross_support']].index:
            ax.plot([idx, idx], [df['支撑'][idx], df['阻力'][idx]],
                    'yellow', linewidth=3, alpha=0.7, solid_capstyle='round')

        # 绘制买信号（红三角）
        buy_signals = df[df['longcross_support']].dropna()
        for idx, row in buy_signals.iterrows():
            ax.scatter(idx, row['支撑'] * 1.001, marker='^', color='red', s=80, zorder=5)
            ax.text(idx, row['支撑'] * 1.001, '买',
                    color='red', fontsize=12, ha='center', va='bottom', fontweight='bold')

        # 绘制卖信号（绿三角）
        sell_signals = df[df['longcross_resistance']].dropna()
        for idx, row in sell_signals.iterrows():
            ax.scatter(idx, row['收盘'] * 0.999, marker='v', color='green', s=80, zorder=5)
            ax.text(idx, row['收盘'] * 0.999, '卖',
                    color='green', fontsize=12, ha='center', va='top', fontweight='bold')

        # 13. 时间轴设置（每1分钟间隔，模仿通达信）
        ax.xaxis.set_major_locator(mdates.MinuteLocator(byminute=range(0, 60), interval=1))

        # 条件性地显示时间刻度（每 5 分钟显示一次）
        # def custom_time_labels(x, pos):
        #     time_str = mdates.num2date(x).strftime('%H:%M')
        #     minute = int(time_str[-2:])
        #     if minute % 5 == 0:
        #         return time_str
        #     return ''
        # 排除 11:30 到 13:00 之间的刻度
        def exclude_break_time_labels(x, pos):
            time_str = mdates.num2date(x).strftime('%H:%M')
            if '11:30' <= time_str < '13:00':
                return ''
            return time_str

        ax.xaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(exclude_break_time_labels))
        plt.xticks(rotation=45, ha='center', fontsize=5)  # 调整 x 轴标签旋转角度
        plt.xlabel('时间', fontsize=12)

        # 14. 价格轴与网格
        plt.ylabel('价格', fontsize=12)
        plt.grid(True, linestyle='--', alpha=0.5, color='gray')  # 美化网格线

        # 15. 昨收价参考线
        ax.axhline(prev_close, color='gray', linestyle='--', linewidth=1, alpha=0.7)
        ax.text(df.index[0], prev_close * 1.0015, f'昨收: {prev_close:.2f}',
                color='gray', fontsize=10, ha='left', va='bottom')

        # 添加指标显示面板（固定显示最新值）
        latest = df.iloc[-1]  # 获取最新数据点
        panel_text = (
            f'昨收: {prev_close:.2f} '
            f"支撑: {latest['支撑']:.2f} "
            f"阻力: {latest['阻力']:.2f} "
            f"现价: {latest['收盘']:.2f}"
        )

        # 绘制指标面板（半透明背景）
        props = dict(boxstyle='round', facecolor='white', alpha=0.7)
        ax.text(
            0.95, 0.95,  # 调整位置到右上角
            panel_text,
            transform=ax.transAxes,
            fontsize=12,
            verticalalignment='top',
            horizontalalignment='right',  # 调整为右对齐
            bbox=props
        )

        # 调整标题位置
        plt.title(f'{stock_code} - {trade_date}', fontsize=14, pad=20)

        # 调整图例位置
        plt.legend(loc='upper left', bbox_to_anchor=(1, 1), fontsize=10)
        # 确保 annotation 在函数外部正确初始化
        annotation = None

        def on_move(event):
            nonlocal annotation  # 使用 nonlocal 关键字来引用外部的 annotation 变量
            if event.inaxes == ax:
                x = mdates.num2date(event.xdata)
                x = x.replace(tzinfo=None)
                closest_idx = df.index.get_indexer([x], method='nearest')[0]
                if 0 <= closest_idx < len(df):
                    data_point = df.iloc[closest_idx]
                    if annotation:
                        annotation.remove()
                    annotation = ax.annotate(
                        f"价格: {data_point['收盘']:.2f}",
                        xy=(event.xdata, event.ydata),
                        xytext=(10, 10),
                        textcoords='offset points',
                        bbox=dict(boxstyle="round", fc="w"),
                        arrowprops=dict(arrowstyle="->")
                    )
                    fig.canvas.draw_idle()
            else:
                if annotation:
                    annotation.remove()
                    annotation = None  # 重置 annotation 为 None
                    fig.canvas.draw_idle()

        fig.canvas.mpl_connect('motion_notify_event', on_move)

        plt.title(f'{stock_code}- {trade_date}', fontsize=12)
        plt.legend(loc='upper left', fontsize=10)
        plt.tight_layout()

        # 强制显示（解决后端静默问题）
        plt.show(block=True)

        return df

    except Exception as e:
        print(f"❌ 错误: {e}")
        import traceback
        traceback.print_exc()
        return None


# ---------------------- 4. 主程序（运行示例） ----------------------
if __name__ == "__main__":
    # stock_code = '516780'  # 长江电力
    stock_code = '601728'  # 中国电信
    # stock_code = '601398'  # 工商银行
    trade_date = '20250613'  # 交易日期

    # 绘制并获取结果
    result_df = plot_tdx_intraday(stock_code, trade_date)
    get_prev_close(stock_code, trade_date)
    df = ak.stock_zh_a_hist_min_em(
        symbol=stock_code,
        period="1",
        start_date=trade_date,
        end_date=trade_date,
        adjust=''
    )
    print(df)

    # 保存结果（可选）
    # if result_df is not None:
    #     result_df.to_csv(f'{stock_code}_{trade_date}_通达信分时信号.csv', encoding='utf-8-sig')
    #     print(f"结果已保存到: {stock_code}_{trade_date}_通达信分时信号.csv")