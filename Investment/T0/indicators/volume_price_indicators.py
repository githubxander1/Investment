import os
import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import matplotlib.dates as mdates
from typing import Optional, Tuple, Dict, Any
import akshare as ak

# 添加项目根目录到系统路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# 设置matplotlib中文字体支持
plt.rcParams['font.sans-serif'] = ['SimHei', 'WenQuanYi Micro Hei', 'Heiti TC']
plt.rcParams['axes.unicode_minus'] = False

# 全局变量
CACHE_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'cache')
OUTPUT_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'output', 'charts')

# 确保目录存在
os.makedirs(CACHE_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

# 设置matplotlib后端，确保图表能正确显示
import matplotlib

matplotlib.use('Agg')  # 使用Agg后端，不显示图形界面


def calculate_volume_price_indicators(df, prev_close) -> Tuple[pd.DataFrame, float, float, float]:
    """
    计算量价指标：
    量价:=(VOL/CLOSE)/3;
    A2:=SUM((IF(((量价>0.20) AND (CLOSE>(REF(CLOSE,1)))),量价,0)),0);
    A3:=SUM((IF(((量价>0.20) AND (CLOSE< (REF(CLOSE,1)))),量价,0)),0);
    A6:=A2+A3;DD1:=1;
    比:=A2/A3;AAA1:=STRCAT(STRCAT('买: ',CON2STR((100*A2)/A6,0)),'%');
    AAA2:=STRCAT(STRCAT('卖: ',CON2STR((100*A3)/A6,0)),'%');
    AAA3:=STRCAT(STRCAT('差: ',CON2STR((100*(A2-A3))/A6,0)),'%');
    """
    # 计算量价指标
    df['量价'] = (df['成交量'] / df['收盘']) / 3
    
    # 计算A2（买方力量）
    condition_a2 = (df['量价'] > 0.20) & (df['收盘'] > df['收盘'].shift(1))
    df['A2'] = np.where(condition_a2, df['量价'], 0)
    
    # 计算A3（卖方力量）
    condition_a3 = (df['量价'] > 0.20) & (df['收盘'] < df['收盘'].shift(1))
    df['A3'] = np.where(condition_a3, df['量价'], 0)
    
    # 累计求和
    df['A2_cum'] = df['A2'].cumsum()
    df['A3_cum'] = df['A3'].cumsum()
    
    # 计算其他指标
    df['A6_cum'] = df['A2_cum'] + df['A3_cum']
    
    # 最新值
    latest_a2 = df['A2_cum'].iloc[-1] if len(df) > 0 else 0
    latest_a3 = df['A3_cum'].iloc[-1] if len(df) > 0 else 0
    latest_a6 = df['A6_cum'].iloc[-1] if len(df) > 0 else 0
    
    # 避免除零错误
    if latest_a6 != 0:
        buy_ratio = (100 * latest_a2) / latest_a6
        sell_ratio = (100 * latest_a3) / latest_a6
        diff_ratio = (100 * (latest_a2 - latest_a3)) / latest_a6
    else:
        buy_ratio = 0
        sell_ratio = 0
        diff_ratio = 0
    
    return df, buy_ratio, sell_ratio, diff_ratio


def calculate_support_resistance(df, prev_close) -> pd.DataFrame:
    """
    计算支撑和阻力位：
    H1:=MAX(DYNAINFO(3),DYNAINFO(5));
    L1:=MIN(DYNAINFO(3),DYNAINFO(6));P1:=H1-L1;
    支撑:L1+P1*1/8,POINTDOT,COLORMAGENTA;
    阻力:=L1+P1*7/8,COLORGREEN;
    章鱼底参考:L1+P1/3,POINTDOT,COLORBLUE;
    """
    # 获取当日最高价和最低价
    daily_high = df['最高'].max()
    daily_low = df['最低'].min()
    
    # 计算 H1、L1（昨收 vs 日内高低）
    df['H1'] = np.maximum(prev_close, daily_high)
    df['L1'] = np.minimum(prev_close, daily_low)
    
    # 支撑、阻力计算
    df['P1'] = df['H1'] - df['L1']
    df['支撑'] = df['L1'] + df['P1'] * 1 / 8
    df['阻力'] = df['L1'] + df['P1'] * 7 / 8
    df['章鱼底参考'] = df['L1'] + df['P1'] / 3
    
    return df


def calculate_fund_flow_indicators(df) -> pd.DataFrame:
    """
    计算资金流向指标：
    XX:=SUM(AMOUNT,BARSCOUNT(CLOSE))/SUM(V*100,BARSCOUNT(CLOSE));
    主力:=EXPMA(CLOSE/XX,20);
    大户:=EXPMA(CLOSE/XX,60);
    散户:=EXPMA(CLOSE/XX,120);
    """
    # 计算XX值
    df['XX'] = df['成交额'].cumsum() / (df['成交量'] * 100).cumsum()
    
    # 处理可能的除零情况
    df['CLOSE_XX'] = df['收盘'] / df['XX']
    df['CLOSE_XX'] = df['CLOSE_XX'].replace([np.inf, -np.inf], np.nan)
    df['CLOSE_XX'] = df['CLOSE_XX'].ffill().bfill()
    
    # 计算主力、大户、散户资金流向
    df['主力'] = df['CLOSE_XX'].ewm(span=20, adjust=False).mean()
    df['大户'] = df['CLOSE_XX'].ewm(span=60, adjust=False).mean()
    df['散户'] = df['CLOSE_XX'].ewm(span=120, adjust=False).mean()
    
    return df


def calculate_precise_lines(df) -> pd.DataFrame:
    """
    计算精准线：
    N01:=3;L00:=0.00;L01:=ABS(L-REF(L,1))<=L00;L02:=ABS(L-REF(L,2))<=L00;
    L03:=ABS(L-REF(L,3))<=L00;L04:=ABS(L-REF(L,4))<=L00;L05:=ABS(L-REF(L,5))<=L00;
    精准线首次:=L01 OR L02 OR L03 OR L04 OR L05;
    精准左:=FILTER(精准线首次,N01) ;
    """
    # 参数设置
    n01 = 3
    l00 = 0.00
    
    # 计算精准线条件
    df['L01'] = (df['最低'] - df['最低'].shift(1)).abs() <= l00
    df['L02'] = (df['最低'] - df['最低'].shift(2)).abs() <= l00
    df['L03'] = (df['最低'] - df['最低'].shift(3)).abs() <= l00
    df['L04'] = (df['最低'] - df['最低'].shift(4)).abs() <= l00
    df['L05'] = (df['最低'] - df['最低'].shift(5)).abs() <= l00
    
    # 精准线首次
    df['精准线首次'] = df['L01'] | df['L02'] | df['L03'] | df['L04'] | df['L05']
    
    # 精准左（FILTER函数模拟）
    df['精准左'] = df['精准线首次'].rolling(window=n01).apply(
        lambda x: x.iloc[-1] and not x.iloc[:-1].any(), raw=False
    ).fillna(0).astype(bool)
    
    # 高点精准线
    df['G1'] = (df['最高'] - df['最高'].shift(1)).abs() <= l00
    df['G2'] = (df['最高'] - df['最高'].shift(2)).abs() <= l00
    df['G3'] = (df['最高'] - df['最高'].shift(3)).abs() <= l00
    df['G4'] = (df['最高'] - df['最高'].shift(4)).abs() <= l00
    df['G5'] = (df['最高'] - df['最高'].shift(5)).abs() <= l00
    
    # 精准线首次（高点）
    df['精准线首次1'] = df['G1'] | df['G2'] | df['G3'] | df['G4'] | df['G5']
    
    # 精准左1（FILTER函数模拟）
    df['精准左1'] = df['精准线首次1'].rolling(window=n01).apply(
        lambda x: x.iloc[-1] and not x.iloc[:-1].any(), raw=False
    ).fillna(0).astype(bool)
    
    return df


def detect_signals(df) -> pd.DataFrame:
    """
    检测买卖信号
    """
    # 支撑位买入信号（LONGCROSS(支撑1,C,2)）
    df['支撑1'] = df['支撑']
    condition_buy = (
        (df['支撑1'].shift(2) < df['收盘'].shift(2)) &
        (df['支撑1'].shift(1) < df['收盘'].shift(1)) &
        (df['支撑1'] > df['收盘'])
    )
    df['买入信号'] = condition_buy
    
    # 阻力位卖出信号（LONGCROSS(C,阻力,2)）
    condition_sell = (
        (df['收盘'].shift(2) < df['阻力'].shift(2)) &
        (df['收盘'].shift(1) < df['阻力'].shift(1)) &
        (df['收盘'] > df['阻力'])
    )
    df['卖出信号'] = condition_sell
    
    # 主力资金信号
    df['主力>大户'] = df['主力'] > df['大户']
    df['大户>散户'] = df['大户'] > df['散户']
    df['C>EXPMA20'] = df['收盘'] > df['收盘'].ewm(span=20, adjust=False).mean()
    df['EXPMA10>EXPMA20'] = df['收盘'].ewm(span=10, adjust=False).mean() > df['收盘'].ewm(span=20, adjust=False).mean()
    df['EXPMA20>EXPMA60'] = df['收盘'].ewm(span=20, adjust=False).mean() > df['收盘'].ewm(span=60, adjust=False).mean()
    df['主力=HHV30'] = df['主力'] == df['主力'].rolling(window=30).max()
    df['CROSS主力1.003'] = (df['主力'].shift(1) <= 1.003) & (df['主力'] > 1.003)
    
    # 主力资金流入信号
    df['主力资金流入'] = (
        df['主力>大户'] & df['大户>散户'] & df['C>EXPMA20'] & 
        df['EXPMA10>EXPMA20'] & df['EXPMA20>EXPMA60'] & 
        df['主力=HHV30'] & df['CROSS主力1.003']
    )
    
    # 打印第一次买入信号的时间点
    first_buy_signal = df[df['买入信号']].first_valid_index()
    if first_buy_signal is not None:
        first_buy_price = df.loc[first_buy_signal, '收盘']
        # 计算相对均线的涨跌幅
        if '均价' in df.columns:
            first_buy_avg_price = df.loc[first_buy_signal, '均价']
            if pd.notna(first_buy_avg_price) and first_buy_avg_price != 0:
                diff_pct = ((first_buy_price - first_buy_avg_price) / first_buy_avg_price) * 100
                print(f"量价指标：第一次买入信号时间点: {first_buy_signal.strftime('%Y-%m-%d %H:%M:%S')}, 价格: {first_buy_price:.2f}, 相对均线涨跌幅: {diff_pct:+.2f}%")
            else:
                print(f"量价指标：第一次买入信号时间点: {first_buy_signal.strftime('%Y-%m-%d %H:%M:%S')}, 价格: {first_buy_price:.2f}, 相对均线涨跌幅: N/A")
        else:
            print(f"量价指标：第一次买入信号时间点: {first_buy_signal.strftime('%Y-%m-%d %H:%M:%S')}, 价格: {first_buy_price:.2f}")
    else:
        print("未检测到买入信号")
    
    # 打印第一次卖出信号的时间点
    first_sell_signal = df[df['卖出信号']].first_valid_index()
    if first_sell_signal is not None:
        first_sell_price = df.loc[first_sell_signal, '收盘']
        # 计算相对均线的涨跌幅
        if '均价' in df.columns:
            first_sell_avg_price = df.loc[first_sell_signal, '均价']
            if pd.notna(first_sell_avg_price) and first_sell_avg_price != 0:
                diff_pct = ((first_sell_price - first_sell_avg_price) / first_sell_avg_price) * 100
                print(f"量价指标：第一次卖出信号时间点: {first_sell_signal.strftime('%Y-%m-%d %H:%M:%S')}, 价格: {first_sell_price:.2f}, 相对均线涨跌幅: {diff_pct:+.2f}%")
            else:
                print(f"量价指标：第一次卖出信号时间点: {first_sell_signal.strftime('%Y-%m-%d %H:%M:%S')}, 价格: {first_sell_price:.2f}, 相对均线涨跌幅: N/A")
        else:
            print(f"量价指标：第一次卖出信号时间点: {first_sell_signal.strftime('%Y-%m-%d %H:%M:%S')}, 价格: {first_sell_price:.2f}")
    else:
        print("未检测到卖出信号")

    # plot_indicators(df, stock_code, trade_date, buy_ratio, sell_ratio, diff_ratio)
    
    return df


def plot_indicators(df, stock_code, trade_date, buy_ratio, sell_ratio, diff_ratio) -> str:
    """
    绘图量价指标图并返回图表保存路径
    """
    """
    绘图量价指标图
    """
    # 创建图形和子图
    fig = plt.figure(figsize=(16, 10))
    gs = fig.add_gridspec(3, 1, height_ratios=[1, 8, 1], hspace=0.1)
    
    ax_info = fig.add_subplot(gs[0])  # 顶部信息栏
    ax_price = fig.add_subplot(gs[1])  # 中部价格图
    ax_time = fig.add_subplot(gs[2])  # 底部时间轴
    
    # 顶部信息栏显示买卖比例
    ax_info.clear()
    ax_info.set_xlim(0, 1)
    ax_info.set_ylim(0, 1)
    ax_info.axis('off')
    
    info_text = f"买: {buy_ratio:.0f}%    卖: {sell_ratio:.0f}%    差: {diff_ratio:.0f}%"
    ax_info.text(0.5, 0.5, info_text, ha='center', va='center', fontsize=14, transform=ax_info.transAxes)
    
    # 使用数据点索引作为x轴坐标
    df_filtered = df.dropna(subset=['收盘'])
    x_values = list(range(len(df_filtered)))
    
    # 绘制收盘价曲线
    ax_price.plot(x_values, df_filtered['收盘'], marker='', linestyle='-', color='blue', linewidth=2, label='收盘价')
    
    # 绘制支撑线和阻力线
    ax_price.plot(x_values, df_filtered['支撑'], marker='', linestyle='--', color='magenta', linewidth=1, label='支撑')
    ax_price.plot(x_values, df_filtered['阻力'], marker='', linestyle='--', color='green', linewidth=1, label='阻力')
    ax_price.plot(x_values, df_filtered['章鱼底参考'], marker='', linestyle=':', color='blue', linewidth=1, label='章鱼底参考')
    
    # 绘制买入信号（红三角 + 红色文字 + 红色竖线）
    buy_signals = df_filtered[df_filtered['买入信号']].dropna()
    for idx in buy_signals.index:
        if idx in df_filtered.index:
            x_pos = df_filtered.index.get_loc(idx)
            ax_price.scatter(x_pos, buy_signals.loc[idx, '支撑'] * 0.999, marker='^', color='red', s=60, zorder=5)
            ax_price.text(x_pos, buy_signals.loc[idx, '支撑'] * 0.995, '买',
                          color='red', fontsize=10, ha='center', va='top', fontweight='bold')
            # 添加红色竖线
            ax_price.axvline(x=x_pos, color='red', linestyle='-', alpha=0.7, linewidth=2, zorder=3)
    
    # 绘制卖出信号（绿三角 + 绿色文字 + 绿色竖线）
    sell_signals = df_filtered[df_filtered['卖出信号']].dropna()
    for idx in sell_signals.index:
        if idx in df_filtered.index:
            x_pos = df_filtered.index.get_loc(idx)
            ax_price.scatter(x_pos, sell_signals.loc[idx, '阻力'] * 1.001, marker='v', color='green', s=60, zorder=5)
            ax_price.text(x_pos, sell_signals.loc[idx, '阻力'] * 1.002, '卖',
                          color='green', fontsize=10, ha='center', va='bottom', fontweight='bold')
            # 添加绿色竖线
            ax_price.axvline(x=x_pos, color='green', linestyle='-', alpha=0.7, linewidth=2, zorder=3)
    
    # 绘制主力资金流入信号
    fund_signals = df_filtered[df_filtered['主力资金流入']].dropna()
    for idx in fund_signals.index:
        if idx in df_filtered.index:
            x_pos = df_filtered.index.get_loc(idx)
            ax_price.scatter(x_pos, fund_signals.loc[idx, '收盘'] * 1.005, marker='*', color='purple', s=80, zorder=5)
    
    # 绘制精准线（底部支撑）
    precise_signals = df_filtered[df_filtered['精准左']].dropna()
    for idx in precise_signals.index:
        if idx in df_filtered.index:
            x_pos = df_filtered.index.get_loc(idx)
            support_val = precise_signals.loc[idx, '支撑']
            ax_price.plot([x_pos-2, x_pos+2], [support_val, support_val], color='magenta', linewidth=2)
    
    # 绘制精准线（顶部阻力）
    precise_signals1 = df_filtered[df_filtered['精准左1']].dropna()
    for idx in precise_signals1.index:
        if idx in df_filtered.index:
            x_pos = df_filtered.index.get_loc(idx)
            resistance_val = precise_signals1.loc[idx, '阻力']
            ax_price.plot([x_pos-2, x_pos+2], [resistance_val, resistance_val], color='cyan', linewidth=2)
    
    # 设置坐标轴标签
    ax_price.set_ylabel('价格', fontsize=12)
    
    # 设置网格
    ax_price.grid(True, linestyle='--', alpha=0.7)
    
    # 设置标题
    # 确保 trade_date 是正确的格式 (YYYY-MM-DD)
    if isinstance(trade_date, str):
        if '-' in trade_date:
            trade_date_formatted = trade_date
        else:
            trade_date_obj = datetime.strptime(trade_date, '%Y%m%d')
            trade_date_formatted = trade_date_obj.strftime('%Y-%m-%d')
    else:
        trade_date_formatted = trade_date.strftime('%Y-%m-%d')
        
    fig.suptitle(f'{stock_code} 量价指标 - {trade_date_formatted}', fontsize=14, y=0.98)
    
    # 添加图例
    ax_price.legend(loc='upper left', fontsize=10)
    
    # 设置x轴刻度
    total_points = len(df_filtered)
    if total_points > 0:
        step = max(1, total_points // 10)
        selected_indices = list(range(0, total_points, step))
        selected_times = df_filtered.index[selected_indices]
        
        ax_price.set_xticks(selected_indices)
        ax_price.set_xticklabels([t.strftime('%H:%M') if hasattr(t, 'strftime') else str(t) for t in selected_times])
        plt.setp(ax_price.get_xticklabels(), rotation=45, ha="right")
        
        # 底部时间轴
        ax_time.set_xlim(0, total_points - 1)
        ax_time.set_ylim(0, 1)
        ax_time.axis('off')
        ax_time.set_xticks(selected_indices)
        ax_time.set_xticklabels([t.strftime('%H:%M') if hasattr(t, 'strftime') else str(t) for t in selected_times])
    
    # 使用 constrained_layout 替代 tight_layout 来避免警告
    plt.rcParams['figure.constrained_layout.use'] = True
    
    # 保存图表到output目录
    output_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'output', 'charts')
    os.makedirs(output_dir, exist_ok=True)
    
    # 确保 trade_date 是正确的格式 (YYYY-MM-DD)
    if isinstance(trade_date, str):
        if '-' in trade_date:
            trade_date_formatted = trade_date
        else:
            trade_date_obj = datetime.strptime(trade_date, '%Y%m%d')
            trade_date_formatted = trade_date_obj.strftime('%Y-%m-%d')
    else:
        trade_date_formatted = trade_date.strftime('%Y-%m-%d')
        
    chart_filename = os.path.join(output_dir, f'{stock_code}_{trade_date_formatted}_量价指标.png')
    
    # 直接保存，覆盖同名文件
    plt.savefig(chart_filename, dpi=300, bbox_inches='tight', format='png')
    
    # 关闭图形以避免阻塞
    plt.close(fig)
    
    return fig


# ---------------------- 3. 缓存功能 ----------------------
def get_cached_data(stock_code: str, trade_date: str) -> Optional[pd.DataFrame]:
    """从缓存中获取数据"""
    cache_file = os.path.join(CACHE_DIR, f"{stock_code}_{trade_date}.csv")
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

def save_data_to_cache(df: pd.DataFrame, stock_code: str, trade_date: str) -> None:
    """保存数据到缓存"""
    """保存数据到缓存"""
    # 确保 stock_data 目录存在
    os.makedirs("stock_data", exist_ok=True)

    cache_file = f"stock_data/{stock_code}_{trade_date}.csv"
    try:
        df_reset = df.reset_index()
        df_reset.to_csv(cache_file, index=False)
    except Exception as e:
        print(f"保存缓存文件失败: {e}")

def analyze_volume_price(stock_code: str, trade_date: Optional[str] = None) -> Optional[pd.DataFrame]:
    """
    分析量价关系主函数
    
    Args:
        stock_code: 股票代码
        trade_date: 交易日期，格式为YYYY-MM-DD或YYYYMMDD，默认为昨天
    
    Returns:
        包含分析结果的DataFrame，如果失败则返回None
    """
    """
    分析量价关系主函数
    """
    try:
        import akshare as ak
        
        # 1. 时间处理
        # 如果没有提供交易日期，则使用昨天的日期
        if trade_date is None:
            # 获取昨天的日期（考虑到今天可能是周末或节假日，使用最近的交易日）
            yesterday = datetime.now() - timedelta(days=1)
            trade_date = yesterday.strftime('%Y-%m-%d')
        
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

        # 2. 获取数据
        df = ak.stock_zh_a_hist_min_em(
            symbol=stock_code,
            period="1",
            start_date=start_time,
            end_date=end_time,
            adjust=''
        )
        
        if df.empty:
            print("❌ 无分时数据")
            return None
        
        # 重命名列以匹配我们的代码
        df = df.rename(columns={
            '时间': '时间',
            '开盘': '开盘',
            '收盘': '收盘',
            '最高': '最高',
            '最低': '最低',
            '成交量': '成交量',
            '成交额': '成交额'
        })
        
        # 转换时间列为datetime类型
        df['时间'] = pd.to_datetime(df['时间'], errors='coerce')
        df = df[df['时间'].notna()]
        
        # 只保留指定日期的数据
        target_date = pd.to_datetime(trade_date_obj)
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
        
        # 强制校准时间索引
        morning_index = pd.date_range(
            start=f"{trade_date_obj.strftime('%Y-%m-%d')} 09:30:00",
            end=f"{trade_date_obj.strftime('%Y-%m-%d')} 11:30:00",
            freq='1min'
        )
        afternoon_index = pd.date_range(
            start=f"{trade_date_obj.strftime('%Y-%m-%d')} 13:00:00",
            end=f"{trade_date_obj.strftime('%Y-%m-%d')} 15:00:00",
            freq='1min'
        )
        
        # 合并索引
        full_index = morning_index.union(afternoon_index)
        df = df.set_index('时间').reindex(full_index)
        df.index.name = '时间'
        
        # 获取昨收（fallback到开盘价）
        try:
            daily_df = ak.stock_zh_a_hist(
                symbol=stock_code,
                period="daily",
                adjust=""
            )
            
            if not daily_df.empty:
                daily_df['日期'] = pd.to_datetime(daily_df['日期'])
                df_before = daily_df[daily_df['日期'] < target_date]
                if not df_before.empty:
                    prev_close = df_before.iloc[-1]['收盘']
                else:
                    prev_close = df['开盘'].dropna().iloc[0]
            else:
                prev_close = df['开盘'].dropna().iloc[0]
        except:
            prev_close = df['开盘'].dropna().iloc[0]
        
        # 填充缺失值
        df = df.ffill().bfill()
        
        # 计算各种指标
        df, buy_ratio, sell_ratio, diff_ratio = calculate_volume_price_indicators(df, prev_close)
        df = calculate_support_resistance(df, prev_close)
        df = calculate_fund_flow_indicators(df)
        df = calculate_precise_lines(df)
        df = detect_signals(df)
        
        # 绘图
        fig = plot_indicators(df, stock_code, trade_date, buy_ratio, sell_ratio, diff_ratio)
        
        return df
        
    except Exception as e:
        print(f"❌ 错误: {e}")
        import traceback
        traceback.print_exc()
        return None


def fetch_intraday_data(stock_code: str, trade_date: str) -> Optional[pd.DataFrame]:
    """
    获取股票分时数据
    
    Args:
        stock_code: 股票代码
        trade_date: 交易日期，格式为YYYY-MM-DD
    
    Returns:
        分时数据DataFrame，如果失败则返回None
    """
    try:
        # 尝试从缓存获取数据
        cached_df = get_cached_data(stock_code, trade_date)
        if cached_df is not None:
            print(f"从缓存加载{stock_code}在{trade_date}的分时数据")
            return cached_df
        
        # 构造 akshare 需要的时间格式
        trade_date_obj = datetime.strptime(trade_date, '%Y-%m-%d')
        start_time = f'{trade_date} 09:30:00'
        end_time = f'{trade_date} 15:00:00'

        # 获取数据
        df = ak.stock_zh_a_hist_min_em(
            symbol=stock_code,
            period="1",
            start_date=start_time,
            end_date=end_time,
            adjust=''  # 不复权
        )
        
        if df.empty:
            print(f"❌ {stock_code}在{trade_date}无分时数据")
            return None
        
        # 处理数据
        df = df.rename(columns={
            '时间': '时间',
            '开盘': '开盘',
            '收盘': '收盘',
            '最高': '最高',
            '最低': '最低',
            '成交量': '成交量',
            '成交额': '成交额'
        })
        
        # 转换时间列
        df['时间'] = pd.to_datetime(df['时间'], errors='coerce')
        df = df[df['时间'].notna()]
        
        # 过滤数据
        df = df[df['时间'].dt.date == trade_date_obj.date()]
        df = df[~((df['时间'].dt.hour == 11) & (df['时间'].dt.minute >= 30)) & ~((df['时间'].dt.hour == 12))]
        
        # 生成完整时间索引
        morning_index = pd.date_range(start=f"{trade_date} 09:30:00", end=f"{trade_date} 11:30:00", freq='1min')
        afternoon_index = pd.date_range(start=f"{trade_date} 13:00:00", end=f"{trade_date} 15:00:00", freq='1min')
        full_index = morning_index.union(afternoon_index)
        
        df = df.set_index('时间').reindex(full_index)
        df.index.name = '时间'
        df = df.ffill().bfill()
        
        # 保存到缓存
        save_data_to_cache(df, stock_code, trade_date)
        
        return df
    except Exception as e:
        print(f"获取{stock_code}在{trade_date}的分时数据失败: {e}")
        return None

def get_prev_close(stock_code: str, trade_date: str) -> float:
    """
    获取前一日收盘价
    
    Args:
        stock_code: 股票代码
        trade_date: 交易日期，格式为YYYY-MM-DD
    
    Returns:
        前一日收盘价，如果获取失败则返回当日开盘价
    """
    try:
        # 尝试获取日线数据
        daily_df = ak.stock_zh_a_hist(
            symbol=stock_code,
            period="daily",
            adjust=""
        )
        
        if not daily_df.empty:
            daily_df['日期'] = pd.to_datetime(daily_df['日期'])
            target_date = datetime.strptime(trade_date, '%Y-%m-%d')
            df_before = daily_df[daily_df['日期'] < target_date]
            if not df_before.empty:
                return df_before.iloc[-1]['收盘']
        
        # 如果无法获取前一日收盘价，尝试获取当日数据的开盘价作为备选
        df = fetch_intraday_data(stock_code, trade_date)
        if df is not None and not df['开盘'].dropna().empty:
            return df['开盘'].dropna().iloc[0]
            
        return 0.0
    except Exception as e:
        print(f"获取{stock_code}的前一日收盘价失败: {e}")
        return 0.0

def detect_trading_signals(df: pd.DataFrame) -> Dict[str, Any]:
    """
    检测交易信号
    
    Args:
        df: 包含指标的DataFrame
    
    Returns:
        包含信号信息的字典
    """
    signals = {
        'buy_signals': df[df['买入信号']].index.tolist() if '买入信号' in df.columns else [],
        'sell_signals': df[df['卖出信号']].index.tolist() if '卖出信号' in df.columns else [],
        'fund_signals': df[df['主力资金流入']].index.tolist() if '主力资金流入' in df.columns else []
    }
    
    # 打印信号信息
    if signals['buy_signals']:
        first_buy = signals['buy_signals'][0]
        price = df.loc[first_buy, '收盘']
        print(f"量价指标：第一次买入信号时间点: {first_buy.strftime('%Y-%m-%d %H:%M:%S')}, 价格: {price:.2f}")
    else:
        print("未检测到买入信号")
    
    if signals['sell_signals']:
        first_sell = signals['sell_signals'][0]
        price = df.loc[first_sell, '收盘']
        print(f"量价指标：第一次卖出信号时间点: {first_sell.strftime('%Y-%m-%d %H:%M:%S')}, 价格: {price:.2f}")
    else:
        print("未检测到卖出信号")
    
    return signals

def main(stock_code: str = '000333', trade_date: Optional[str] = None) -> None:
    """
    主函数，用于独立运行生成量价指标图表
    
    Args:
        stock_code: 股票代码
        trade_date: 交易日期，格式为YYYY-MM-DD或YYYYMMDD，默认为昨天
    """
    # 时间处理
    if trade_date is None:
        yesterday = datetime.now() - timedelta(days=1)
        trade_date = yesterday.strftime('%Y-%m-%d')
    
    # 标准化日期格式
    if isinstance(trade_date, str):
        if '-' not in trade_date:
            trade_date = datetime.strptime(trade_date, '%Y%m%d').strftime('%Y-%m-%d')
    
    print(f"开始分析{stock_code}在{trade_date}的量价指标")
    
    # 分析并绘图
    result_df = analyze_volume_price(stock_code, trade_date)
    
    if result_df is not None:
        print(f"图表已保存到{OUTPUT_DIR}目录")
    else:
        print("图表生成失败")

# 主程序入口
if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='量价指标分析工具')
    parser.add_argument('--code', type=str, default='000333', help='股票代码')
    parser.add_argument('--date', type=str, default=None, help='交易日期 (YYYY-MM-DD 或 YYYYMMDD)')
    
    args = parser.parse_args()
    main(stock_code=args.code, trade_date=args.date)
