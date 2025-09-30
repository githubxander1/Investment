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


# ---------------------- 1. 指标计算（量价关系指标） ----------------------
def calculate_volume_price_indicators(df, prev_close, threshold=0.01):
    """
    量价关系指标计算（严格还原通达信公式）：
    量价:=(VOL/CLOSE)/3;
    A2:=SUM((IF(((量价>0.20) AND (CLOSE>(REF(CLOSE,1)))),量价,0)),0);
    A3:=SUM((IF(((量价>0.20) AND (CLOSE< (REF(CLOSE,1)))),量价,0)),0);
    A6:=A2+A3;DD1:=1;
    比:=A2/A3;
    AAA1:=STRCAT(STRCAT('买: ',CON2STR((100*A2)/A6,0)),'%');
    AAA2:=STRCAT(STRCAT('卖: ',CON2STR((100*A3)/A6,0)),'%');
    AAA3:=STRCAT(STRCAT('差: ',CON2STR((100*(A2-A3))/A6,0)),'%');
    
    H1:=MAX(DYNAINFO(3),DYNAINFO(5));  # 昨收，当日最高
    L1:=MIN(DYNAINFO(3),DYNAINFO(6));  # 昨收，当日最低
    P1:=H1-L1;
    支撑:L1+P1*1/8;
    阻力:L1+P1*7/8;
    章鱼底参考:L1+P1/3;
    
    DRAWTEXT(LONGCROSS(支撑,C,2),C,'买'),COLORYELLOW;
    DRAWTEXT(LONGCROSS(C,阻力,2),C,'卖'),COLOR70DB93;
    DRAWICON(LONGCROSS(支撑,C,2),C,1);  { 买入箭头 }
    DRAWICON(LONGCROSS(C,阻力,2),C,2);  { 卖出箭头 }
    """
    # 计算量价指标
    df['量价'] = (df['成交量'] / df['收盘']) / 3
    
    # 计算A2和A3
    condition_buy = (df['量价'] > 0.20) & (df['收盘'] > df['收盘'].shift(1))
    condition_sell = (df['量价'] > 0.20) & (df['收盘'] < df['收盘'].shift(1))
    
    df['A2_component'] = np.where(condition_buy, df['量价'], 0)
    df['A3_component'] = np.where(condition_sell, df['量价'], 0)
    
    # 计算当日最高价和最低价
    daily_high = df['最高'].max()
    daily_low = df['最低'].min()
    
    # 计算H1, L1, P1
    df['H1'] = np.maximum(prev_close, daily_high)
    df['L1'] = np.minimum(prev_close, daily_low)
    df['P1'] = df['H1'] - df['L1']
    
    # 计算支撑、阻力和章鱼底参考线
    df['支撑'] = df['L1'] + df['P1'] * 1 / 8
    df['阻力'] = df['L1'] + df['P1'] * 7 / 8
    df['章鱼底参考'] = df['L1'] + df['P1'] / 3
    
    # 计算买入和卖出信号
    df['cross_support_buy'] = (df['支撑'].shift(1) >= df['收盘'].shift(1)) & (df['支撑'] < df['收盘'])
    df['longcross_support_buy'] = (df['支撑'].shift(2) >= df['收盘'].shift(2)) & \
                                  (df['支撑'].shift(1) >= df['收盘'].shift(1)) & \
                                  (df['支撑'] < df['收盘'])
    
    df['cross_resistance_sell'] = (df['阻力'].shift(1) <= df['收盘'].shift(1)) & (df['阻力'] > df['收盘'])
    df['longcross_resistance_sell'] = (df['阻力'].shift(2) <= df['收盘'].shift(2)) & \
                                      (df['阻力'].shift(1) <= df['收盘'].shift(1)) & \
                                      (df['阻力'] > df['收盘'])
    
    # 计算均价线
    df['均价'] = (df['收盘'] * df['成交量']).expanding().sum() / df['成交量'].expanding().sum()
    
    return df


# ---------------------- 2. 昨收价获取 ----------------------
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

        if daily_df.empty or prev_date not in daily_df['日期'].values:
            raise ValueError("前一日数据缺失")

        prev_close = daily_df[daily_df['日期'] == prev_date]['收盘'].values[0]
        return prev_close
    except Exception as e:
        print(f"昨收获取失败: {e}，将使用分时开盘价替代")
        return None


# ---------------------- 3. 缓存功能 ----------------------
def get_cached_data(stock_code, trade_date):
    """从缓存中获取数据"""
    cache_file = f"stock_data/{stock_code}.csv"
    if os.path.exists(cache_file):
        try:
            df = pd.read_csv(cache_file)
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
    os.makedirs("../stock_data", exist_ok=True)
    cache_file = f"stock_data/{stock_code}.csv"
    try:
        df_reset = df.reset_index()
        df_reset.to_csv(cache_file, index=False)
        print(f"数据已保存到缓存: {cache_file}")
    except Exception as e:
        print(f"保存缓存文件失败: {e}")


# ---------------------- 4. 绘图函数 ----------------------
def plot_volume_price_indicators(stock_code, trade_date=None):
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

            # 保存到缓存前确保列名正确
            if '时间' not in df.columns:
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
            print("使用缓存数据")
            data_from_cache = True

        if not data_from_cache:
            df['时间'] = pd.to_datetime(df['时间'], errors='coerce')

        df = df[df['时间'].notna()]
        target_date = pd.to_datetime(trade_date, format='%Y%m%d')
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

        full_index = morning_index.union(afternoon_index)
        df = df.set_index('时间').reindex(full_index)
        df.index.name = '时间'

        # 获取昨收
        prev_close = get_prev_close(stock_code, trade_date)
        if prev_close is None:
            prev_close = df['开盘'].dropna().iloc[0]
            print(f"⚠️ 使用分时开盘价替代昨收: {prev_close:.2f}")

        # 计算指标
        df = df.ffill().bfill()  # 填充缺失值
        df = calculate_volume_price_indicators(df, prev_close)

        # 数据校验
        required_cols = ['开盘', '收盘', '最高', '最低', '成交量']
        if not all(col in df.columns for col in required_cols):
            missing_cols = [col for col in required_cols if col not in df.columns]
            print(f"❌ 数据缺失关键列：{missing_cols}")
            return None

        # 调试信息
        print("✅ 过滤后数据概览：")
        print(df[['开盘', '收盘', '最高', '最低']].head())
        print(f"数据时间范围：{df.index.min()} ~ {df.index.max()}")
        print(f"有效数据量：{len(df)} 条")

        # 计算统计信息
        A2 = df['A2_component'].sum()
        A3 = df['A3_component'].sum()
        A6 = A2 + A3
        
        if A6 > 0:
            buy_ratio = (100 * A2) / A6
            sell_ratio = (100 * A3) / A6
            diff_ratio = (100 * (A2 - A3)) / A6
        else:
            buy_ratio = sell_ratio = diff_ratio = 0

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

        # 顶部信息栏显示最新价、涨跌幅
        latest_price = df_filtered['收盘'].iloc[-1]
        change = latest_price - prev_close
        change_pct = (change / prev_close) * 100

        ax_info.clear()
        ax_info.set_xlim(0, 1)
        ax_info.set_ylim(0, 1)
        ax_info.axis('off')

        info_text = f"最新: {latest_price:.2f}    涨跌幅: {change:+.2f} ({change_pct:+.2f}%)"
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

        # 绘制支撑线、阻力线和章鱼底参考线
        ax_price.plot(x_values, df_filtered['支撑'], marker='', linestyle='--', color='magenta', linewidth=1,
                      label='支撑')
        ax_price.plot(x_values, df_filtered['阻力'], marker='', linestyle='--', color='green', linewidth=1,
                      label='阻力')
        ax_price.plot(x_values, df_filtered['章鱼底参考'], marker='', linestyle='-.', color='cyan', linewidth=1,
                      label='章鱼底参考')

        # 绘制买入信号（红三角）
        buy_signals = df_filtered[df_filtered['longcross_support_buy']].dropna()
        for idx, row in buy_signals.iterrows():
            x_pos = df_filtered.index.get_loc(idx)
            ax_price.scatter(x_pos, row['支撑'] * 0.999, marker='^', color='red', s=60, zorder=5)
            ax_price.text(x_pos, row['支撑'] * 0.999, '买',
                          color='red', fontsize=10, ha='center', va='top', fontweight='bold')

        # 绘制卖出信号（绿三角）
        sell_signals = df_filtered[df_filtered['longcross_resistance_sell']].dropna()
        for idx, row in sell_signals.iterrows():
            x_pos = df_filtered.index.get_loc(idx)
            ax_price.scatter(x_pos, row['阻力'] * 1.001, marker='v', color='green', s=60, zorder=5)
            ax_price.text(x_pos, row['阻力'] * 1.001, '卖',
                          color='green', fontsize=10, ha='center', va='bottom', fontweight='bold')

        # 绘制支撑下方的红色柱状线
        below_support = df_filtered[df_filtered['收盘'] < df_filtered['支撑']]
        for idx, row in below_support.iterrows():
            x_pos = df_filtered.index.get_loc(idx)
            ax_price.plot([x_pos, x_pos], [row['支撑'], row['收盘']], color='red', linewidth=2)

        # 绘制阻力上方的绿色柱状线
        above_resistance = df_filtered[df_filtered['收盘'] > df_filtered['阻力']]
        for idx, row in above_resistance.iterrows():
            x_pos = df_filtered.index.get_loc(idx)
            ax_price.plot([x_pos, x_pos], [row['阻力'], row['收盘']], color='green', linewidth=2)

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

        # 添加统计信息文本
        ax_price.text(0.5, 0.98, f"买: {buy_ratio:.0f}%", transform=ax_price.transAxes, fontsize=10,
                      verticalalignment='top', horizontalalignment='center',
                      bbox=dict(boxstyle='round,pad=0.3', facecolor='red', alpha=0.7))
        
        ax_price.text(0.7, 0.98, f"卖: {sell_ratio:.0f}%", transform=ax_price.transAxes, fontsize=10,
                      verticalalignment='top', horizontalalignment='center',
                      bbox=dict(boxstyle='round,pad=0.3', facecolor='green', alpha=0.7))
        
        ax_price.text(0.9, 0.98, f"差: {diff_ratio:.0f}%", transform=ax_price.transAxes, fontsize=10,
                      verticalalignment='top', horizontalalignment='center',
                      bbox=dict(boxstyle='round,pad=0.3', facecolor='cyan', alpha=0.7))

        # 添加右侧纵轴显示当前价格相对于均线的涨跌幅
        ax_diff = ax_price.twinx()
        if '均价' in df_filtered.columns and not df_filtered['均价'].isna().all():
            latest_avg_price = df_filtered['均价'].iloc[-1]
            diff_pct = ((latest_price - latest_avg_price) / latest_avg_price) * 100
            
            # 在右侧纵轴上显示涨跌幅信息
            ax_diff.text(0.98, 0.94, f"相对均线: {diff_pct:+.2f}%", transform=ax_diff.transAxes, fontsize=10,
                         verticalalignment='top', horizontalalignment='right',
                         bbox=dict(boxstyle='round,pad=0.5', facecolor='yellow', alpha=0.7))
            
            # 设置右侧纵轴的标签
            ax_diff.set_ylabel('相对均线涨跌幅 (%)', fontsize=10)
            
            # 设置右侧纵轴的刻度
            ax_diff.set_yticks([-2, -1, 0, 1, 2])
            ax_diff.set_yticklabels(['-2%', '-1%', '0%', '1%', '2%'])
            
            # 设置右侧纵轴的范围
            ax_diff.set_ylim(-3, 3)

        # 设置图表标题
        fig.suptitle(f'{stock_code} 量价关系图 - {trade_date}', fontsize=14, y=0.98)

        # 添加图例到价格图
        ax_price.legend(loc='upper left', fontsize=10)

        # 鼠标悬浮显示价格和时间
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
                        annotation.xy = (x_index, event.ydata)
                        annotation.set_text(f"时间: {time_str}\n价格: {data_point['收盘']:.2f}")
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

        # 强制显示（解决后端静默问题）
        plt.show(block=True)

        return df

    except Exception as e:
        print(f"❌ 错误: {e}")
        import traceback
        traceback.print_exc()
        return None


# ---------------------- 5. 主程序 ----------------------
if __name__ == "__main__":
    stock_code = '601398'  # 工商银行
    trade_date = '20250926'  # 交易日期

    # 绘制并获取结果
    result_df = plot_volume_price_indicators(stock_code, trade_date)