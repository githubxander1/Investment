# 五日均线策略.py

def calculate_ma(df, short_window=5, long_window=20):
    """
    计算短期和长期均线。

    参数:
    df (pd.DataFrame): 包含收盘价数据的数据框。
    short_window (int): 短期均线窗口大小，默认为5。
    long_window (int): 长期均线窗口大小，默认为20。

    返回:
    pd.DataFrame: 包含短期和长期均线的数据框。
    """
    df[f'{short_window}日均线'] = df['收盘价_复权'].rolling(window=short_window).mean()
    df[f'{long_window}日均线'] = df['收盘价_复权'].rolling(window=long_window).mean()
    return df

def generate_signals(df, short_window=5, long_window=20):
    """
    生成交易信号，基于短期和长期均线的金叉和死叉。

    参数:
    df (pd.DataFrame): 包含短期和长期均线的数据框。
    short_window (int): 短期均线窗口大小，默认为5。
    long_window (int): 长期均线窗口大小，默认为20。

    返回:
    pd.DataFrame: 包含交易信号的数据框。
    """
    df['信号'] = '无'
    df['信号'] = df['信号'].astype(str)  # 确保 '信号' 列是字符串类型

    # 金叉：短期均线 > 长期均线且前一日短期均线 < 前一日长期均线
    df.loc[(df[f'{short_window}日均线'] > df[f'{long_window}日均线']) &
           (df[f'{short_window}日均线'].shift(1) < df[f'{long_window}日均线'].shift(1)), '信号'] = '买入'

    # 死叉：短期均线 < 长期均线且前一日短期均线 > 前一日长期均线
    df.loc[(df[f'{short_window}日均线'] < df[f'{long_window}日均线']) &
           (df[f'{short_window}日均线'].shift(1) > df[f'{long_window}日均线'].shift(1)), '信号'] = '卖出'

    return df
