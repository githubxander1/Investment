import akshare as ak
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import Formatter

plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

# ---------------------- 1. 获取日线数据 ----------------------
def get_daily_data(stock_code, start_date, end_date):
    """获取股票日线数据（AkShare）"""
    df = ak.stock_zh_a_hist_tx(stock_code, start_date, end_date)
    print(df)
    # 处理时间索引
    df['date'] = pd.to_datetime(df['date'])
    df.set_index('date', inplace=True)
    # 打印index检查时间格式
    print("index", df.index)
    return df

# ---------------------- 2. 计算通达信指标 ----------------------
def calculate_tdx_indicator(df):
    """还原通达信指标逻辑：
    VAR1:=(2*CLOSE+HIGH+LOW)/4;
    VAR2:=LLV(LOW,34);
    VAR3:=HHV(HIGH,34);
    AA: EMA((VAR1-VAR2)/(VAR3-VAR2)*100,13);
    BB: EMA(0.667*REF(AA,1)+0.333*AA,2);
    XG: CROSS(AA,BB) AND AA<20 → 标记30
    黄柱: CROSS(AA,22) AND BB<AA
    速顶: FILTER(CROSS(BB,AA) AND AA>80.3,3)
    """
    high = df['high']
    low = df['low']
    close = df['close']

    # 计算基础变量
    VAR1 = (2 * close + high + low) / 4
    VAR2 = low.rolling(34).min()  # LLV(LOW,34)
    VAR3 = high.rolling(34).max()  # HHV(HIGH,34)

    # 避免除零错误
    denominator = VAR3 - VAR2
    denominator = np.where(denominator == 0, 1e-10, denominator)  # 极小值替代0
    AA_raw = (VAR1 - VAR2) / denominator * 100

    # EMA计算（通达信默认adjust=False，递归计算）
    AA = AA_raw.ewm(span=13, adjust=False).mean()  # AA: EMA(13)
    BB = (0.667 * AA.shift(1) + 0.333 * AA).ewm(span=2, adjust=False).mean()  # BB: EMA(2)

    # 检查 AA 和 BB 是否有 NaN 值
    if AA.isnull().any():
        print("Warning: AA contains NaN values.")
    if BB.isnull().any():
        print("Warning: BB contains NaN values.")

    # 信号计算
    # 1. 金叉 CROSS(AA, BB)：前一周期AA<BB，当前AA>BB
    cross_aa_bb = (AA.shift(1) < BB.shift(1)) & (AA > BB)
    # XG: 金叉且AA<20 → 标记30
    df['XG'] = np.where(cross_aa_bb & (AA < 20), 30, 0)

    # 2. 黄柱条件：CROSS(AA,22) 且 BB<AA
    cross_aa_22 = (AA.shift(1) < 22) & (AA > 22)  # AA上穿22
    df['黄柱'] = cross_aa_22 & (BB < AA)

    # 3. 速顶条件：CROSS(BB,AA) 且 AA>80.3，过滤3周期内重复信号
    cross_bb_aa = (BB.shift(1) < AA.shift(1)) & (BB > AA)  # BB上穿AA
    top_condition = cross_bb_aa & (AA > 80.3)
    # FILTER函数：3周期内只保留第一次信号
    top_filter = top_condition & (top_condition.rolling(3).sum() == 1)
    df['速顶'] = top_filter

    # 保存指标
    df['AA'] = AA
    df['BB'] = BB
    print("AA值", df["AA"])
    print("BB值", df["BB"])

    return df

# ---------------------- 3. 可视化指标（还原通达信风格） ----------------------
class DateFormatter(Formatter):
    """自定义时间轴格式化，适配Matplotlib"""

    def __init__(self, dates):
        self.dates = dates

    def __call__(self, x, pos=None):
        if x < 0 or x >= len(self.dates):
            return ''
        return self.dates[int(x)].strftime('%Y-%m-%d')

def plot_tdx_indicator(df):
    """绘制指标图：价格+AA/BB曲线+信号标记"""
    fig, (ax_price, ax_indicator) = plt.subplots(
        2, 1, figsize=(12, 8),
        gridspec_kw={'height_ratios': [3, 1]}
    )

    # -------------- 绘制价格曲线（简化为收盘价） --------------
    ax_price.plot(df.index, df['close'], label='close', color='blue')
    ax_price.set_ylabel('价格', fontsize=12)
    ax_price.legend(loc='upper left')
    ax_price.grid(alpha=0.3)

    # -------------- 绘制AA/BB曲线 --------------
    ax_indicator.plot(df.index, df['AA'], label='AA', color='red', linewidth=1.5)
    ax_indicator.plot(df.index, df['BB'], label='BB', color='green', linewidth=1.5)
    ax_indicator.set_ylabel('指标值', fontsize=12)
    ax_indicator.set_ylim(0, 100)  # 指标值域0-100
    ax_indicator.legend(loc='upper left')
    ax_indicator.grid(alpha=0.3)

    # -------------- 绘制红柱（BB < AA时填充） --------------
    red_bar_mask = df['BB'] < df['AA']
    ax_indicator.fill_between(
        df[red_bar_mask].index,
        df[red_bar_mask]['BB'],
        df[red_bar_mask]['AA'],
        color='red', alpha=0.3
    )

    # -------------- 绘制XG信号（金叉+AA<20 → 紫色三角） --------------
    xg_mask = df['XG'] == 30
    ax_indicator.scatter(
        df[xg_mask].index, df[xg_mask]['XG'],
        color='magenta', label='XG',
        s=100, marker='^', zorder=5
    )

    # -------------- 绘制黄柱（AA上穿22+BB<AA → 黄色填充+文字） --------------
    yellow_bar_mask = df['黄柱']
    ax_indicator.fill_between(
        df[yellow_bar_mask].index,
        df[yellow_bar_mask]['AA'] - 5,
        df[yellow_bar_mask]['AA'] + 5,
        color='yellow', alpha=0.5
    )
    for date in df[yellow_bar_mask].index:
        ax_indicator.text(
            date, df.loc[date, 'AA'] - 12,
            '底部参与', color='white',
            ha='center', va='top', fontsize=9
        )

    # -------------- 绘制速顶（BB上穿AA+AA>80.3 → 绿色填充+图标） --------------
    top_mask = df['速顶']
    ax_indicator.fill_between(
        df[top_mask].index,
        96, 100,  # 高度96-100
        color='green', alpha=0.5
    )
    for date in df[top_mask].index:
        ax_indicator.scatter(
            date, 95,  # 图标位置
            color='green', marker=15,  # 15=向上箭头图标
            s=200, zorder=6
        )

    # -------------- 时间轴格式化 --------------
    dates = df.index.tolist()
    ax_price.xaxis.set_major_formatter(DateFormatter(dates))  # 为价格图也设置时间格式化
    ax_indicator.xaxis.set_major_formatter(DateFormatter(dates))
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.show()

# ---------------------- 4. 主程序运行 ----------------------
if __name__ == "__main__":
    # 股票代码与时间范围
    stock_code = "sz000001"  # 长江电力
    start_date = "2025-04-01"
    end_date = "2025-06-05"

    # 1. 获取日线数据
    df = get_daily_data(stock_code, start_date, end_date)
    # 打印 DataFrame 以检查数据时间范围
    print("Data time range:", df.index.min(), "to", df.index.max())

    # 2. 计算通达信指标
    df = calculate_tdx_indicator(df)

    # 3. 可视化指标
    plot_tdx_indicator(df)
