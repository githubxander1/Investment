import akshare as ak
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime, timedelta
import os
from scipy.signal import argrelextrema

# 设置matplotlib后端，确保图表能正确显示
import matplotlib

matplotlib.use('Agg')  # 使用Agg后端，不显示图形界面
plt.rcParams.update({
    'font.sans-serif': ['SimHei'],
    'axes.unicode_minus': False
})


# ---------------------- 1. 指标计算（扩展通达信公式） ----------------------
def calculate_tdx_indicators(df, prev_close, daily_data, threshold=0.01):
    """
    扩展通达信公式实现：
    包含480日最高价、月内天数计算、特殊均线、MACD、量比分析等
    """
    # 获取当日最高价和最低价
    daily_high = df['最高'].max()
    daily_low = df['最低'].min()

    # 1. 计算480日最高价 (XG:HHV(H,480))
    if not daily_data.empty:
        # 使用480日最高值作为480日最高价
        df['XG_480'] = daily_data['最高'].rolling(window=480, min_periods=1).max().iloc[-1]
    else:
        df['XG_480'] = daily_high
    
    # 在分时图中显示480日最高价
    df['XG'] = df['XG_480']

    # 2. 计算今天是这个月的第几天 (RQ)
    # 转换时间为日期
    df['日期'] = df.index.date
    # 计算当月第一天
    df['月初'] = df['日期'].apply(lambda x: datetime(x.year, x.month, 1).date())
    # 计算是本月的第几天
    df['RQ'] = (pd.to_datetime(df['日期']) - pd.to_datetime(df['月初'])).dt.days + 1

    # 3. 计算自上次RQ变化以来经过的天数 (JY)
    # 计算RQ变化点
    df['RQ变化'] = df['RQ'] != df['RQ'].shift(1)
    # 计算距离上次变化的天数
    df['JY'] = 0
    current_jy = 0
    for i in range(len(df)):
        if df['RQ变化'].iloc[i]:
            current_jy = 1
        else:
            current_jy += 1
        df.at[df.index[i], 'JY'] = current_jy

    # 4. 计算特殊移动平均线 (MA1到MA9)
    # 由于JY是变化的，需要逐点计算
    ma_columns = []
    for i in range(1, 10):  # MA1到MA9
        col_name = f'MA{i}'
        ma_columns.append(col_name)
        df[col_name] = np.nan
        for j in range(len(df)):
            jy_value = df['JY'].iloc[j]
            if j - jy_value >= 0:
                df.at[df.index[j], col_name] = df['收盘'].iloc[j - jy_value]

    # 5. 计算阻力和支撑线（根据通达信公式调整比例）
    df['H1'] = np.maximum(prev_close, daily_high)
    df['L1'] = np.minimum(prev_close, daily_low)
    df['P1'] = df['H1'] - df['L1']
    df['阻力'] = df['L1'] + df['P1'] * 8 / 9  # 按照通达信公式
    df['支撑'] = df['L1'] + df['P1'] * 0.5 / 9  # 按照通达信公式

    # 6. 计算成交量加权平均价格均线
    # 确保有成交量数据
    if '成交量' in df.columns and '成交额' in df.columns:
        # 计算累计成交额和累计成交量
        df['累计成交额'] = df['成交额'].cumsum()
        df['累计成交量'] = df['成交量'].cumsum() * 100  # 转换为股数

        # 避免除零错误
        df['均价基础'] = np.where(df['累计成交量'] > 0, df['累计成交额'] / df['累计成交量'], 0)

        # 计算价格与均价基础的比率
        price_ratio = np.where(df['均价基础'] > 0, df['收盘'] / df['均价基础'], 0)

        # 计算均线 - 更精确地实现通达信公式
        df['均线'] = np.where(
            (price_ratio >= 0.95) & (price_ratio <= 1.05),
            df['均价基础'],
            df['收盘'].expanding().mean()
        )
    else:
        # 如果没有成交量数据，使用简单移动平均
        df['均线'] = df['收盘'].expanding().mean()

    # 7. 计算MACD指标
    # 计算EMA
    df['EMA12'] = df['收盘'].ewm(span=12, adjust=False).mean()
    df['EMA26'] = df['收盘'].ewm(span=26, adjust=False).mean()

    # 计算DIF和DEA - 严格按照通达信公式
    df['DIF'] = (df['EMA12'] - df['EMA26']) + prev_close
    df['DEA'] = df['DIF'].ewm(span=9, adjust=False).mean()

    # 计算MACD柱状线
    df['MACD1'] = 10 * (df['DIF'] - df['DEA'])
    df['MACD2'] = df['MACD1'].ewm(span=2, adjust=False).mean()

    # 8. 计算量比相关指标
    # 确保有成交量数据
    if '成交量' in df.columns and '成交额' in df.columns:
        # 计算XX - 严格按照通达信公式
        total_amount = df['成交额'].sum()
        total_volume = df['成交量'].sum() * 100  # 转换为股数
        df['XX'] = total_amount / total_volume if total_volume > 0 else 0

        # 计算主力、大户、散户线 - 修正计算方式
        df['主力'] = df['收盘'].div(df['XX'], fill_value=0).ewm(span=20, adjust=False).mean()
        df['大户'] = df['收盘'].div(df['XX'], fill_value=0).ewm(span=60, adjust=False).mean()
        df['散户'] = df['收盘'].div(df['XX'], fill_value=0).ewm(span=120, adjust=False).mean()

        # 9. 计算量价比
        df['A1'] = (df['成交量'] / df['收盘']) / 3

        # 计算A2到A5 - 修正累积计算
        df['A2'] = np.where((df['A1'] > 40) & (df['收盘'] > df['收盘'].shift(1)), df['A1'], 0).cumsum()
        df['A3'] = np.where((df['A1'] > 40) & (df['收盘'] < df['收盘'].shift(1)), df['A1'], 0).cumsum()
        df['A4'] = np.where((df['A1'] < 40) & (df['收盘'] > df['收盘'].shift(1)), df['A1'], 0).cumsum()
        df['A5'] = np.where((df['A1'] < 40) & (df['收盘'] < df['收盘'].shift(1)), df['A1'], 0).cumsum()

        # 计算A6
        df['A6'] = df['A2'] + df['A3'] + df['A4'] + df['A5']

        # 10. 计算机构和散户的买卖比例
        df['A7'] = np.where(df['A6'] > 0, (100 * df['A2']) / df['A6'], 0)
        df['A8'] = np.where(df['A6'] > 0, (100 * df['A3']) / df['A6'], 0)
        df['A9'] = np.where(df['A6'] > 0, (100 * df['A4']) / df['A6'], 0)
        df['A10'] = np.where(df['A6'] > 0, (100 * df['A5']) / df['A6'], 0)

        # 机构买盘、机构卖盘、散户买盘、散户卖盘
        df['机构买盘'] = df['A2']
        df['机构卖盘'] = df['A3']
        df['散户买盘'] = df['A4']
        df['散户卖盘'] = df['A5']
    else:
        # 如果没有成交量数据，初始化这些列为0
        for col in ['XX', '主力', '大户', '散户', 'A1', 'A2', 'A3', 'A4', 'A5',
                    'A6', 'A7', 'A8', 'A9', 'A10', '机构买盘', '机构卖盘', '散户买盘', '散户卖盘']:
            df[col] = 0

    # 11. 计算信号 - 修正信号计算逻辑以匹配通达信
    # 支撑上穿现价
    df['cross_support'] = ((df['支撑'].shift(1) < df['收盘'].shift(1)) & (df['支撑'] > df['收盘'])) & \
                          (abs(df['支撑'] - df['收盘']) > threshold)

    # 买信号 (LONGCROSS(支撑, 现价, 2)) - 优化计算逻辑
    df['longcross_support'] = ((df['支撑'].shift(2) < df['收盘'].shift(2)) & \
                               (df['支撑'].shift(1) < df['收盘'].shift(1)) & \
                               (df['支撑'] > df['收盘'])) 

    # 卖信号 (LONGCROSS(现价, 阻力, 2)) - 优化计算逻辑
    df['longcross_resistance'] = ((df['收盘'].shift(2) < df['阻力'].shift(2)) & \
                                  (df['收盘'].shift(1) < df['阻力'].shift(1)) & \
                                  (df['收盘'] > df['阻力']))

    # 主力相关信号 - 修正信号计算
    df['主力_拉信号'] = (df['主力'] > 1.02) & (df['主力'].shift(1) <= 1.02)
    df['主力_冲信号'] = (df['主力'] > 1.04) & (df['主力'].shift(1) <= 1.04)

    # 添加压信号
    df['压力信号'] = ((df['收盘'] > df['阻力']) & (df['收盘'].shift(1) <= df['阻力']))
    
    # 打印第一次买入信号的时间点
    first_buy_signal = df[df['longcross_support']].first_valid_index()
    if first_buy_signal is not None:
        first_buy_price = df.loc[first_buy_signal, '收盘']
        # 计算相对均线的涨跌幅
        if '均线' in df.columns:
            first_buy_avg_price = df.loc[first_buy_signal, '均线']
            if pd.notna(first_buy_avg_price) and first_buy_avg_price != 0:
                diff_pct = ((first_buy_price - first_buy_avg_price) / first_buy_avg_price) * 100
                print(f"扩展指标：第一次买入信号时间点: {first_buy_signal.strftime('%Y-%m-%d %H:%M:%S')}, 价格: {first_buy_price:.2f}, 相对均线涨跌幅: {diff_pct:+.2f}%")
            else:
                print(f"扩展指标：第一次买入信号时间点: {first_buy_signal.strftime('%Y-%m-%d %H:%M:%S')}, 价格: {first_buy_price:.2f}, 相对均线涨跌幅: N/A")
        else:
            print(f"扩展指标：第一次买入信号时间点: {first_buy_signal.strftime('%Y-%m-%d %H:%M:%S')}, 价格: {first_buy_price:.2f}")
    else:
        print("未检测到买入信号")
    
    # 打印第一次卖出信号的时间点
    first_sell_signal = df[df['longcross_resistance']].first_valid_index()
    if first_sell_signal is not None:
        first_sell_price = df.loc[first_sell_signal, '收盘']
        # 计算相对均线的涨跌幅
        if '均线' in df.columns:
            first_sell_avg_price = df.loc[first_sell_signal, '均线']
            if pd.notna(first_sell_avg_price) and first_sell_avg_price != 0:
                diff_pct = ((first_sell_price - first_sell_avg_price) / first_sell_avg_price) * 100
                print(f"扩展指标：第一次卖出信号时间点: {first_sell_signal.strftime('%Y-%m-%d %H:%M:%S')}, 价格: {first_sell_price:.2f}, 相对均线涨跌幅: {diff_pct:+.2f}%")
            else:
                print(f"扩展指标：第一次卖出信号时间点: {first_sell_signal.strftime('%Y-%m-%d %H:%M:%S')}, 价格: {first_sell_price:.2f}, 相对均线涨跌幅: N/A")
        else:
            print(f"扩展指标：第一次卖出信号时间点: {first_sell_signal.strftime('%Y-%m-%d %H:%M:%S')}, 价格: {first_sell_price:.2f}")
    else:
        print("未检测到卖出信号")

    return df


# ---------------------- 2. 数据获取函数 ----------------------
def get_prev_close(stock_code, trade_date):
    """从日线数据获取前一日收盘价，失败则用分时开盘价替代"""
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

        # 转换日期列为datetime类型
        daily_df['日期'] = pd.to_datetime(daily_df['日期'])

        # 筛选出在交易日期之前的数据
        df_before = daily_df[daily_df['日期'] < trade_date_dt]

        if df_before.empty:
            raise ValueError("没有找到前一日数据")

        # 获取最近的收盘价（上一个交易日）
        prev_close = df_before.iloc[-1]['收盘']
        return prev_close, daily_df
    except Exception as e:
        return None, pd.DataFrame()


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
                else:
                    print("❌ 未找到时间列")
                    return None

            # 保存到缓存
            save_data_to_cache(df.copy(), stock_code, trade_date)
            data_from_cache = False
        else:
            data_from_cache = True

        # 处理时间列
        if not data_from_cache:
            df['时间'] = pd.to_datetime(df['时间'], errors='coerce')

        df = df[df['时间'].notna()]

        # 只保留指定日期的数据
        target_date = pd.to_datetime(trade_date, format='%Y%m%d')
        df_original = df.copy()  # 保存原始数据
        df = df[df['时间'].dt.date == target_date.date()]

        # 过滤掉 11:30 到 13:00 之间的数据
        df = df[~((df['时间'].dt.hour == 11) & (df['时间'].dt.minute >= 30)) & ~((df['时间'].dt.hour == 12))]
        if df.empty:
            print("❌ 所有时间数据均无效")
            return None

        # 强制校准时间索引
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

        # 获取昨收和日线数据
        prev_close, daily_data = get_prev_close(stock_code, trade_date)
        if prev_close is None:
            prev_close = df['开盘'].dropna().iloc[0]

        # 计算指标
        df = df.ffill().bfill()  # 填充缺失值
        df = calculate_tdx_indicators(df, prev_close, daily_data)

        # 数据校验
        required_cols = ['开盘', '收盘', '最高', '最低', '支撑', '阻力']
        if not all(col in df.columns for col in required_cols):
            missing_cols = [col for col in required_cols if col not in df.columns]
            print(f"❌ 数据缺失关键列：{missing_cols}")
            return None

        if df['收盘'].isna().all():
            print("❌ 收盘价全为空")
            return None

        # 绘图设置
        plt.close('all')  # 关闭之前未关闭的图形

        # 创建图形和子图 - 调整布局使其更接近通达信风格
        fig = plt.figure(figsize=(14, 12))
        gs = fig.add_gridspec(3, 1, height_ratios=[5, 2, 1], hspace=0.2)

        ax_price = fig.add_subplot(gs[0])  # 价格图（包含所有指标）
        ax_macd = fig.add_subplot(gs[1])  # MACD图
        ax_info = fig.add_subplot(gs[2])  # 底部信息栏

        # 移除缺失数据的行
        # 只过滤掉收盘价为空的行，保留有信号的行
        df_filtered = df.copy()
        # 只过滤掉开盘、最高、最低、收盘都为空的行
        df_filtered = df_filtered.dropna(subset=['开盘', '最高', '最低', '收盘'], how='all')

        # 价格图绘制
        x_values = list(range(len(df_filtered)))

        # 绘制收盘价曲线
        ax_price.plot(x_values, df_filtered['收盘'], marker='', linestyle='-', color='blue', linewidth=2,
                      label='收盘价')

        # 绘制成交量加权平均价格均线
        if '均线' in df_filtered.columns and not df_filtered['均线'].isna().all():
            ax_price.plot(x_values, df_filtered['均线'], marker='', linestyle='-', color='yellow', linewidth=1.5,
                          label='成交量加权均价')

        # 绘制480日最高价 - 青色点线
        ax_price.axhline(df['XG_480'].iloc[0], color='cyan', linestyle=':', linewidth=1.5, label='480日最高价')

        # 绘制支撑线和阻力线
        ax_price.plot(x_values, df_filtered['支撑'], marker='', linestyle='--', color='green', linewidth=1,
                      label='支撑')
        ax_price.plot(x_values, df_filtered['阻力'], marker='', linestyle='--', color='red', linewidth=1,
                      label='阻力')

        # 绘制特殊移动平均线 (MA1到MA9)
        ma_colors = ['#FFA500', '#800080', '#00FFFF', '#008000', '#FFC0CB', '#0000FF', '#FF0000', '#808080', '#FFFF00']
        for i in range(1, 10):
            col_name = f'MA{i}'
            if col_name in df_filtered.columns and not df_filtered[col_name].isna().all():
                ax_price.plot(x_values, df_filtered[col_name], marker='', linestyle='-',
                              color=ma_colors[i - 1], linewidth=0.8, alpha=0.7, label=f'MA{i}')

        # 绘制橙色柱状线（CROSS(支撑, 现价)）
        cross_support_points = df_filtered[df_filtered['cross_support']]
        for idx in cross_support_points.index:
            x_pos = df_filtered.index.get_loc(idx)
            ax_price.plot([x_pos, x_pos],
                          [cross_support_points.loc[idx, '支撑'], cross_support_points.loc[idx, '阻力']],
                          color='orange', linewidth=2, alpha=0.7, solid_capstyle='round')

        # 绘制买信号（红三角）
        buy_signals = df_filtered[df_filtered['longcross_support'] == True]

        for idx, row in buy_signals.iterrows():
            x_pos = df_filtered.index.get_loc(idx)
            ax_price.scatter(x_pos, row['支撑'] * 1.01, marker='^', color='red', s=100, zorder=10)
            ax_price.text(x_pos, row['支撑'] * 1.02, '买',
                          color='red', fontsize=12, ha='center', va='bottom', fontweight='bold')

        # 绘制卖信号（绿三角）
        sell_signals = df_filtered[df_filtered['longcross_resistance'] == True]

        for idx, row in sell_signals.iterrows():
            x_pos = df_filtered.index.get_loc(idx)
            ax_price.scatter(x_pos, row['收盘'] * 0.99, marker='v', color='green', s=100, zorder=10)
            ax_price.text(x_pos, row['收盘'] * 0.98, '卖',
                          color='green', fontsize=12, ha='center', va='top', fontweight='bold')

        # 绘制主力相关信号
        pull_signals = df_filtered[df_filtered['主力_拉信号'] == True]

        for idx, row in pull_signals.iterrows():
            x_pos = df_filtered.index.get_loc(idx)
            ax_price.scatter(x_pos, row['收盘'] * 0.96, marker='^', color='magenta', s=100, zorder=10)
            ax_price.text(x_pos, row['收盘'] * 0.95, '拉',
                          color='magenta', fontsize=12, ha='center', va='top', fontweight='bold')

        rush_signals = df_filtered[df_filtered['主力_冲信号'] == True]

        for idx, row in rush_signals.iterrows():
            x_pos = df_filtered.index.get_loc(idx)
            ax_price.scatter(x_pos, row['收盘'] * 0.94, marker='^', color='purple', s=110, zorder=10)
            ax_price.text(x_pos, row['收盘'] * 0.93, '冲',
                          color='purple', fontsize=12, ha='center', va='top', fontweight='bold')

        # 绘制压力信号
        pressure_signals = df_filtered[df_filtered['压力信号'] == True]

        for idx, row in pressure_signals.iterrows():
            x_pos = df_filtered.index.get_loc(idx)
            ax_price.scatter(x_pos, row['收盘'] * 1.03, marker='v', color='orange', s=100, zorder=10)
            ax_price.text(x_pos, row['收盘'] * 1.04, '压',
                          color='orange', fontsize=12, ha='center', va='bottom', fontweight='bold')

        # 绘制主力、大户、散户线在价格图下方区域
        # 调整y轴范围以容纳这些指标
        y_min, y_max = ax_price.get_ylim()
        y_range = y_max - y_min
        ax_price.set_ylim(y_min - y_range * 0.2, y_max)  # 扩展下方空间

        # 在价格图下方绘制量比指标
        ax_price_twin = ax_price.twinx()
        ax_price_twin.set_ylim(0.95, 1.1)  # 设置量比指标的范围
        ax_price_twin.plot(x_values, df_filtered['主力'], color='red', linewidth=1, alpha=0.7, label='主力')
        ax_price_twin.plot(x_values, df_filtered['大户'], color='blue', linewidth=1, alpha=0.7, label='大户')
        ax_price_twin.plot(x_values, df_filtered['散户'], color='green', linewidth=1, alpha=0.7, label='散户')
        ax_price_twin.axhline(1.02, color='purple', linestyle=':', linewidth=1)
        ax_price_twin.axhline(1.04, color='purple', linestyle='--', linewidth=1)
        ax_price_twin.axhline(1.0, color='gray', linestyle='-', linewidth=1)
        ax_price_twin.set_ylabel('量比', fontsize=10)

        # 合并图例
        lines1, labels1 = ax_price.get_legend_handles_labels()
        lines2, labels2 = ax_price_twin.get_legend_handles_labels()
        ax_price.legend(lines1 + lines2, labels1 + labels2, loc='upper left', fontsize=8, ncol=2)

        # 设置价格图坐标轴
        ax_price.set_ylabel('价格', fontsize=12)
        ax_price.grid(True, linestyle='--', alpha=0.7)
        ax_price.axhline(prev_close, color='gray', linestyle='--', linewidth=1, alpha=0.7)

        # 设置x轴刻度
        total_points = len(df_filtered)
        step = max(1, total_points // 15)  # 控制刻度密度
        selected_indices = list(range(0, total_points, step))
        selected_times = df_filtered.index[selected_indices]

        ax_price.set_xticks(selected_indices)
        ax_price.set_xticklabels([t.strftime('%H:%M') for t in selected_times], rotation=45, ha="right")

        # 绘制MACD图
        if 'MACD1' in df_filtered.columns and 'MACD2' in df_filtered.columns:
            # 绘制MACD线
            ax_macd.plot(x_values, df_filtered['MACD1'], color='blue', linewidth=1.5, label='MACD')
            ax_macd.plot(x_values, df_filtered['MACD2'], color='orange', linewidth=1.5, label='MACD信号线')

            # 绘制MACD柱状图
            macd_bull = df_filtered[(df_filtered['MACD1'] >= df_filtered['MACD2']) & (df_filtered['MACD1'] >= 0)]
            macd_bear = df_filtered[(df_filtered['MACD1'] >= df_filtered['MACD2']) & (df_filtered['MACD1'] < 0)]

            ax_macd.bar(macd_bull.index.get_indexer(macd_bull.index), macd_bull['MACD1'],
                        color='red', alpha=0.5)
            ax_macd.bar(macd_bear.index.get_indexer(macd_bear.index), macd_bear['MACD1'],
                        color='green', alpha=0.5)

            ax_macd.axhline(0, color='gray', linestyle='--', linewidth=1)
            ax_macd.set_ylabel('MACD', fontsize=12)
            ax_macd.grid(True, linestyle='--', alpha=0.7)
            ax_macd.legend(loc='upper left', fontsize=10)
            ax_macd.set_xticks(selected_indices)
            ax_macd.set_xticklabels([t.strftime('%H:%M') for t in selected_times], rotation=45, ha="right")

        # 底部信息栏
        ax_info.clear()
        ax_info.set_xlim(0, 1)
        ax_info.set_ylim(0, 1)
        ax_info.axis('off')

        # 顶部信息栏
        latest_price = df_filtered['收盘'].iloc[-1] if not df_filtered.empty else 0
        avg_price = df_filtered['均线'].iloc[-1] if not df_filtered.empty and '均线' in df_filtered.columns else 0
        change = latest_price - prev_close
        change_pct = (change / prev_close) * 100 if prev_close != 0 else 0

        # 合并顶部信息为一个标题
        fig.suptitle(f'{stock_code} 分时图分析 - {trade_date} | 最新价: {latest_price:.2f} | 涨跌幅: {change:+.2f} ({change_pct:+.2f}%) | 480日最高: {df['XG_480'].iloc[0]:.2f}',
                     fontsize=12, y=0.98)

        # 获取最后一个有效数据点的买卖盘信息
        info_text_bottom = ""
        if not df_filtered.empty:
            last_data = df_filtered.iloc[-1]
            info_text_bottom = (f"机买: {last_data['机构买盘']:.2f}万    "
                                f"机卖: {last_data['机构卖盘']:.2f}万    "
                                f"散买: {last_data['散户买盘']:.2f}万    "
                                f"散卖: {last_data['散户卖盘']:.2f}万")

        # 在底部添加买卖盘信息
        ax_info.text(0.5, 0.5, info_text_bottom, ha='center', va='center', fontsize=12, transform=ax_info.transAxes)

        # 鼠标悬浮显示信息
        annotation = ax_price.annotate('', xy=(0, 0), xytext=(10, 10), textcoords='offset points',
                                       bbox=dict(boxstyle='round', fc='yellow', alpha=0.7),
                                       arrowprops=dict(arrowstyle='->'), fontsize=10)
        annotation.set_visible(False)

        # plt.tight_layout()
        # plt.subplots_adjust(top=0.95, bottom=0.1, left=0.1, right=0.9)
        
        # 使用 constrained_layout 替代 tight_layout 来避免警告
        plt.rcParams['figure.constrained_layout.use'] = True

        # 保存图表到output目录
        output_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'output', 'charts')
        os.makedirs(output_dir, exist_ok=True)
        chart_filename = os.path.join(output_dir, f'{stock_code}_{trade_date}_扩展指标.png')
        
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
    # 可以替换为其他股票代码
    stock_code = '000333'  # 美的集团
    trade_date = '20251010'  # 交易日期

    # 绘制并获取结果
    result_df = plot_tdx_intraday(stock_code, trade_date)

    # 保存结果（可选）
    if result_df is not None:
        result_df.to_csv(f'{stock_code}_{trade_date}_扩展指标分析.csv', encoding='utf-8-sig')
        print(f"结果已保存到: {stock_code}_{trade_date}_扩展指标分析.csv")