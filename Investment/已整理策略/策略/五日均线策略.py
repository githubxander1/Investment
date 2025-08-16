# 五日均线策略.py

def calculate_ma(df):
    df['5日均线'] = df['收盘价_复权'].rolling(window=5).mean()
    # df['10日均线'] = df['收盘价_复权'].rolling(window=window).mean()
    # df['20日均线'] = df['收盘价_复权'].rolling(window=window).mean()
    return df

def generate_signals(df):
    df['信号'] = '无'
    df['信号'] = df['信号'].astype(str)  # 确保 '信号' 列是字符串类型
    # 金叉：5日均线 > 收盘价_复权且前一日5日均线 < 收盘价_复权
    df.loc[(df['5日均线'] > df['收盘价_复权']) & (df['5日均线'].shift(1) < df['收盘价_复权'].shift(1)), '信号'] = '买入'  # 买入信号
    # 死叉：5日均线 < 收盘价_复权且前一日5日均线 > 收盘价_复权
    df.loc[(df['5日均线'] < df['收盘价_复权']) & (df['5日均线'].shift(1) > df['收盘价_复权'].shift(1)), '信号'] = '卖出'  # 卖出信号
    return df
