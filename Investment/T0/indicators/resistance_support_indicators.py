import akshare as ak
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime, timedelta
import os
import sys
from typing import Dict, List, Tuple, Optional, Any

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# 设置matplotlib后端，确保图表能正确显示
import matplotlib
matplotlib.use('Agg')  # 使用Agg后端，不显示图形界面
plt.rcParams.update({
    'font.sans-serif': ['SimHei'],
    'axes.unicode_minus': False
})

# 全局变量定义
CHART_OUTPUT_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'output', 'charts')
CACHE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'stock_data')

# 确保输出目录存在
os.makedirs(CHART_OUTPUT_DIR, exist_ok=True)
os.makedirs(CACHE_DIR, exist_ok=True)

# ---------------------- 1. 指标计算 ----------------------
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

    # 改进：增加趋势确认机制，避免虚假信号
    # 计算短期均线和长期均线
    df['short_ma'] = df['收盘'].rolling(window=5, min_periods=1).mean()
    df['long_ma'] = df['收盘'].rolling(window=20, min_periods=1).mean()
    
    # 增加趋势过滤条件：买入信号需要短期均线上穿长期均线或处于上升趋势
    df['trend_filter_buy'] = (df['short_ma'] > df['long_ma']) | (df['short_ma'] > df['short_ma'].shift(1))
    
    # 增加趋势过滤条件：卖出信号需要短期均线下穿长期均线或处于下降趋势
    df['trend_filter_sell'] = (df['short_ma'] < df['long_ma']) | (df['short_ma'] < df['short_ma'].shift(1))
    
    # 应用趋势过滤器到买卖信号
    df['longcross_support_filtered'] = df['longcross_support'] & df['trend_filter_buy']
    df['longcross_resistance_filtered'] = df['longcross_resistance'] & df['trend_filter_sell']

    # 改进：收集所有信号而非仅第一次信号
    buy_signals = df[df['longcross_support_filtered']]
    sell_signals = df[df['longcross_resistance_filtered']]
    
    print(f"阻力支撑：共检测到 {len(buy_signals)} 个买入信号和 {len(sell_signals)} 个卖出信号")
    
    for idx, row in buy_signals.iterrows():
        buy_time = idx
        buy_price = row['收盘']
        # 计算相对均线的涨跌幅
        if '均价' in df.columns:
            buy_avg_price = row['均价']
            if pd.notna(buy_avg_price) and buy_avg_price != 0:
                diff_pct = ((buy_price - buy_avg_price) / buy_avg_price) * 100
                # 确保 idx 是 datetime 对象
                if isinstance(idx, str):
                    buy_time = pd.to_datetime(idx)
                print(f"阻力支撑：买入信号时间点: {buy_time.strftime('%Y-%m-%d %H:%M:%S')}, 价格: {buy_price:.2f}, 相对均线涨跌幅: {diff_pct:+.2f}%")
            else:
                # 确保 idx 是 datetime 对象
                if isinstance(idx, str):
                    buy_time = pd.to_datetime(idx)
                print(f"阻力支撑：买入信号时间点: {buy_time.strftime('%Y-%m-%d %H:%M:%S')}, 价格: {buy_price:.2f}, 相对均线涨跌幅: N/A")
        else:
            # 确保 idx 是 datetime 对象
            if isinstance(idx, str):
                buy_time = pd.to_datetime(idx)
            print(f"阻力支撑：买入信号时间点: {buy_time.strftime('%Y-%m-%d %H:%M:%S')}, 价格: {buy_price:.2f}")
    
    for idx, row in sell_signals.iterrows():
        sell_time = idx
        sell_price = row['收盘']
        # 计算相对均线的涨跌幅
        if '均价' in df.columns:
            sell_avg_price = row['均价']
            if pd.notna(sell_avg_price) and sell_avg_price != 0:
                diff_pct = ((sell_price - sell_avg_price) / sell_avg_price) * 100
                # 确保 idx 是 datetime 对象
                if isinstance(idx, str):
                    sell_time = pd.to_datetime(idx)
                print(f"阻力支撑：卖出信号时间点: {sell_time.strftime('%Y-%m-%d %H:%M:%S')}, 价格: {sell_price:.2f}, 相对均线涨跌幅: {diff_pct:+.2f}%")
            else:
                # 确保 idx 是 datetime 对象
                if isinstance(idx, str):
                    sell_time = pd.to_datetime(idx)
                print(f"阻力支撑：卖出信号时间点: {sell_time.strftime('%Y-%m-%d %H:%M:%S')}, 价格: {sell_price:.2f}, 相对均线涨跌幅: N/A")
        else:
            # 确保 idx 是 datetime 对象
            if isinstance(idx, str):
                sell_time = pd.to_datetime(idx)
            print(f"阻力支撑：卖出信号时间点: {sell_time.strftime('%Y-%m-%d %H:%M:%S')}, 价格: {sell_price:.2f}")

    if len(buy_signals) == 0 and len(sell_signals) == 0:
        print("未检测到任何信号")

    return df


# ---------------------- 3. 数据获取函数 ----------------------
def fetch_intraday_data(stock_code: str, trade_date: str) -> Optional[pd.DataFrame]:
    """
    获取分时数据
    """
    try:
        # 确保 trade_date 是正确的格式
        if isinstance(trade_date, str):
            if '-' in trade_date:
                trade_date_obj = datetime.strptime(trade_date, '%Y-%m-%d')
            else:
                trade_date_obj = datetime.strptime(trade_date, '%Y%m%d')
        else:
            trade_date_obj = trade_date
            
        # 格式化为 akshare 接口需要的日期格式
        trade_date_str = trade_date_obj.strftime('%Y%m%d')
        
        # 构造 akshare 需要的时间格式 (YYYY-MM-DD HH:MM:SS)
        start_time = f'{trade_date_obj.strftime("%Y-%m-%d")} 09:30:00'
        end_time = f'{trade_date_obj.strftime("%Y-%m-%d")} 15:00:00'

        # 如果缓存没有数据，则从网络获取
        df = ak.stock_zh_a_hist_min_em(
            symbol=stock_code,
            period="1",
            start_date=start_time,
            end_date=end_time,
            adjust=''
        )

        if df.empty:
            print(f"❌ {stock_code} 在 {trade_date} 无分时数据")
            return None
            
        return df
    except Exception as e:
        print(f"❌ 获取分时数据失败: {e}")
        return None

# ---------------------- 4. 交易信号检测函数 ----------------------
def detect_trading_signals(df: pd.DataFrame) -> Dict[str, List[Tuple[datetime, float]]]:
    """
    检测交易信号
    """
    signals = {
        'buy_signals': [],
        'sell_signals': []
    }
    
    # 检测买入信号（使用过滤后的信号）
    buy_signals = df[df['longcross_support_filtered']]
    for idx, row in buy_signals.iterrows():
        if isinstance(idx, str):
            signal_time = pd.to_datetime(idx)
        else:
            signal_time = idx
        signals['buy_signals'].append((signal_time, row['收盘']))
    
    # 检测卖出信号（使用过滤后的信号）
    sell_signals = df[df['longcross_resistance_filtered']]
    for idx, row in sell_signals.iterrows():
        if isinstance(idx, str):
            signal_time = pd.to_datetime(idx)
        else:
            signal_time = idx
        signals['sell_signals'].append((signal_time, row['收盘']))
    
    return signals

# ---------------------- 5. 主分析函数 ----------------------
def analyze_resistance_support(stock_code: str, trade_date: Optional[str] = None) -> Optional[Tuple[pd.DataFrame, Dict[str, List[Tuple[datetime, float]]]]]:
    """
    阻力支撑指标分析主函数
    
    Args:
        stock_code: 股票代码
        trade_date: 交易日期，默认为今天
    
    Returns:
        (数据框, 信号字典) 或 None
    """
    try:
        # 时间处理
        if trade_date is None:
            # 获取今天的日期
            today = datetime.now()
            trade_date = today.strftime('%Y-%m-%d')

        # 获取分时数据
        df = fetch_intraday_data(stock_code, trade_date)
        if df is None:
            return None
        
        df = df[df['时间'].notna()]
        
        # 只保留指定日期的数据
        target_date = pd.to_datetime(trade_date, format='%Y%m%d')
        df = df[df['时间'].str.split(' ', expand=True)[0] == target_date.strftime('%Y-%m-%d')]
        
        # 分离上午和下午的数据
        time_series = df['时间'].str.split(' ', expand=True)[1]
        hour_parts = time_series.str.split(':', expand=True)[0].astype(int)
        morning_data = df[hour_parts < 12]
        afternoon_data = df[hour_parts >= 13]
        
        # 设置时间索引
        df = df.set_index('时间')
        df.index.name = '时间'
        
        # 获取昨收
        from Investment.T0.utils.get_pre_close import get_prev_close
        prev_close = get_prev_close(stock_code, trade_date)
        if prev_close is None:
            prev_close = df['开盘'].dropna().iloc[0]
        
        # 计算指标
        df = df.ffill().bfill()
        df = calculate_tdx_indicators(df, prev_close)
        
        # 计算均价
        df['均价'] = df['收盘'].expanding().mean()
        
        # 数据校验
        required_cols = ['开盘', '收盘', '最高', '最低', '支撑', '阻力']
        if not all(col in df.columns for col in required_cols):
            missing_cols = [col for col in required_cols if col not in df.columns]
            print(f"❌ 数据缺失关键列：{missing_cols}")
            return None
        
        # 检测交易信号
        signals = detect_trading_signals(df)
        
        return df, signals
        
    except Exception as e:
        print(f"❌ 分析失败: {e}")
        import traceback
        traceback.print_exc()
        return None

# ---------------------- 6. 绘图函数 ----------------------
def plot_tdx_intraday(stock_code: str, trade_date: Optional[str] = None, df: Optional[pd.DataFrame] = None) -> Optional[str]:
    """
    绘制阻力支撑指标分时图
    
    Args:
        stock_code: 股票代码
        trade_date: 交易日期，默认为昨天
        df: 可选，已计算的数据框
    
    Returns:
        图表文件路径或 None
    """
    try:
        # 如果没有提供数据框，执行完整分析
        if df is None:
            result = analyze_resistance_support(stock_code, trade_date)
            if result is None:
                return None
            df, _ = result

        # 获取交易日期
        if trade_date is None:
            yesterday = datetime.now() - timedelta(days=1)
            trade_date = yesterday.strftime('%Y-%m-%d')
        
        # 确保 trade_date 是正确的格式
        if isinstance(trade_date, str):
            if '-' in trade_date:
                trade_date_formatted = trade_date
            else:
                trade_date_obj = datetime.strptime(trade_date, '%Y%m%d')
                trade_date_formatted = trade_date_obj.strftime('%Y-%m-%d')
        else:
            trade_date_formatted = trade_date.strftime('%Y-%m-%d')

        # 获取昨收
        from Investment.T0.utils.get_pre_close import get_prev_close
        prev_close = get_prev_close(stock_code, trade_date_formatted)
        if prev_close is None:
            prev_close = df['开盘'].dropna().iloc[0]

        # 1. 时间处理
        # 如果没有提供交易日期，则使用昨天的日期
        if trade_date is None:
            # 获取昨天的日期（考虑到今天是周六，昨天是周五）
            yesterday = datetime.now() - timedelta(days=1)
            trade_date = yesterday.strftime('%Y-%m-%d')

        # 确保 trade_date 是正确的格式
        if isinstance(trade_date, str):
            try:
                # 尝试使用 YYYY-MM-DD 格式解析
                trade_date_obj = datetime.strptime(trade_date, '%Y-%m-%d')
            except ValueError:
                try:
                    # 如果失败，尝试使用 YYYYMMDD 格式解析
                    trade_date_obj = datetime.strptime(trade_date, '%Y%m%d')
                except ValueError:
                    raise ValueError(f"无法解析日期格式: {trade_date}")
        else:
            trade_date_obj = trade_date
            
        # 格式化为 akshare 接口需要的日期格式
        trade_date_str = trade_date_obj.strftime('%Y%m%d')
        
        # 构造 akshare 需要的时间格式 (YYYY-MM-DD HH:MM:SS)
        start_time = f'{trade_date_obj.strftime("%Y-%m-%d")} 09:30:00'
        end_time = f'{trade_date_obj.strftime("%Y-%m-%d")} 15:00:00'

        df_resouce = ak.stock_zh_a_hist_min_em(
            symbol=stock_code,
            period="1",
            start_date=start_time,
            end_date=end_time,
            adjust=''
        )
        if df_resouce.empty:
            print("❌ 无分时数据")
            return None

        df_resouce = df_resouce[df_resouce['时间'].notna()]

        # 只保留指定日期的数据，不延伸到今天
        target_date = pd.to_datetime(trade_date, format='%Y-%m-%d')
        df = df_resouce.copy()  # 保存原始数据
        df = df[df['时间'].str.split(' ', expand=True)[0] == target_date.strftime('%Y-%m-%d')]

        # 分离上午和下午的数据
        # 修复时间比较逻辑，正确提取小时部分并转换为整数进行比较
        time_series = df['时间'].str.split(' ', expand=True)[1]
        hour_parts = time_series.str.split(':', expand=True)[0].astype(int)
        morning_data = df[hour_parts < 12]
        afternoon_data = df[hour_parts >= 13]

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
        df = df.set_index('时间')
        # 先前的 reindex 操作可能会引入大量 NaN 值，我们只保留原始数据中的时间点
        # df = df.reindex(full_index)
        df.index.name = '时间'

        # 获取昨收（fallback到开盘价）
        try:
            from Investment.T0.utils.get_pre_close import get_prev_close
            prev_close = get_prev_close(stock_code, trade_date)
        except ImportError:
            # 如果导入失败，尝试另一种导入方式
            import sys
            sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
            try:
                from utils.get_pre_close import get_prev_close
                prev_close = get_prev_close(stock_code, trade_date)
            except ImportError:
                prev_close = None
        
        if prev_close is None:
            prev_close = df['开盘'].dropna().iloc[0]

        # 计算指标
        # 在计算指标前，先确保数据没有被错误地填充为 NaN
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
        
        # 确保 selected_times 中的时间是 datetime 对象
        if len(selected_times) > 0 and isinstance(selected_times[0], str):
            selected_times = [pd.to_datetime(t) for t in selected_times]

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
        chart_filename = os.path.join(CHART_OUTPUT_DIR, f'{stock_code}_{trade_date_formatted}_阻力支撑指标.png')
        
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


# ---------------------- 7. 命令行接口 ----------------------
def main():
    """
    命令行运行入口
    """
    import argparse
    
    parser = argparse.ArgumentParser(description='阻力支撑指标分析工具')#000333
    parser.add_argument('--stock', type=str, default='600030', help='股票代码')
    parser.add_argument('--date', type=str, default=datetime.now().strftime('%Y-%m-%d'), help='交易日期 (YYYY-MM-DD)')
    # parser.add_argument('--stock', type=str, default='600030', help='股票代码')
    # parser.add_argument('--date', type=str, default=None, help='交易日期 (YYYY-MM-DD)')

    args = parser.parse_args()
    
    # 分析并绘图
    result = plot_tdx_intraday(args.stock, args.date)
    
    if result is not None:
        # 获取交易日期
        # trade_date = args.date if args.date else (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
        # 今天的 日期
        trade_date = datetime.now().strftime('%Y-%m-%d')
        if isinstance(trade_date, str):
            if '-' in trade_date:
                trade_date_formatted = trade_date
            else:
                trade_date_obj = datetime.strptime(trade_date, '%Y%m%d')
                trade_date_formatted = trade_date_obj.strftime('%Y-%m-%d')
        else:
            trade_date_formatted = trade_date.strftime('%Y-%m-%d')
            
        chart_path = os.path.join(CHART_OUTPUT_DIR, f'{args.stock}_{trade_date_formatted}_阻力支撑指标.png')
        print(f"🎉 阻力支撑指标分析完成！图表已保存到: {chart_path}")
    else:
        print("❌ 分析失败！")


# ---------------------- 8. 主程序入口 ----------------------
if __name__ == "__main__":
    main()