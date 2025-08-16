"""
震荡市策略：布林带 + 均线共振（低买高卖）
趋势市策略：均线交叉（如 MA20 上穿 MA50）+ MACD 过滤

"""
def bollinger_band_strategy(df, window=20, num_std=2):
    df['MA20'] = df['收盘价'].rolling(window=window).mean()
    df['STD'] = df['收盘价'].rolling(window=window).std()
    df['Upper'] = df['MA20'] + (num_std * df['STD'])
    df['Lower'] = df['MA20'] - (num_std * df['STD'])

    df['Signal'] = 0
    df.loc[df['收盘价'] < df['Lower'], 'Signal'] = 1  # 买入
    df.loc[df['收盘价'] > df['Upper'], 'Signal'] = -1  # 卖出
    return df

def reits_strategy(df):
    # 1. 判断市场状态
    df = detect_market_state(df)

    # 2. 计算技术指标
    df['MA20'] = df['收盘价'].rolling(20).mean()
    df['MA50'] = df['收盘价'].rolling(50).mean()
    df['RSI'] = talib.RSI(df['收盘价'], timeperiod=14)

    # 3. 识别蜡烛形态
    df = detect_candlestick_patterns(df)

    # 4. 策略信号生成
    df['Signal'] = 0

    # 震荡市：布林带低买高卖
    df.loc[(df['MarketState'] == '震荡') & (df['收盘价'] < df['Lower']), 'Signal'] = 1
    df.loc[(df['MarketState'] == '震荡') & (df['收盘价'] > df['Upper']), 'Signal'] = -1

    # 趋势市：均线交叉 + MACD 过滤
    df['MACD'], df['Signal_Line'], _ = talib.MACD(df['收盘价'])
    df.loc[(df['MarketState'] == '趋势') & (df['MA20'] > df['MA50']) & (df['MACD'] > df['Signal_Line']), 'Signal'] = 1
    df.loc[(df['MarketState'] == '趋势') & (df['MA20'] < df['MA50']) & (df['MACD'] < df['Signal_Line']), 'Signal'] = -1

    return df[['收盘价', 'Signal']]
