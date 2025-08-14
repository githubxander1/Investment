def detect_candlestick_patterns(df):
    # 锤子线：下影线长，实体小
    df['LowerShadow'] = df['最低价'] / df['开盘价'] - 1
    df['Hammer'] = (df['LowerShadow'] > 0.02) & (abs(df['收盘价'] - df['开盘价']) / (df['最高价'] - df['最低价']) < 0.3)

    # 吞没形态：前K线被后K线完全覆盖
    df['Engulfing'] = (df['收盘价'].shift(1) < df['开盘价'].shift(1)) & \
                      (df['收盘价'] > df['开盘价']) & \
                      (df['收盘价'] > df['开盘价'].shift(1)) & \
                      (df['开盘价'] < df['收盘价'].shift(1))

    return df[['Hammer', 'Engulfing']]
