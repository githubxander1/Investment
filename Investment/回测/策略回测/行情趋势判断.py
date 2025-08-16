import pandas as pd
import talib
"""
波动率 + ADX 指标（趋势强度）
原理：通过 Average True Range (ATR) 衡量波动率，ADX 判断趋势强度
阈值设定：
ADX < 25：震荡市
ADX ≥ 25：趋势市"""
def detect_market_state(df, window=14):
    df['ATR'] = talib.ATR(df['最高价'], df['最低价'], df['收盘价'], timeperiod=window)
    df['ADX'] = talib.ADX(df['最高价'], df['最低价'], df['收盘价'], timeperiod=window)

    df['MarketState'] = '震荡'
    df.loc[df['ADX'] >= 25, 'MarketState'] = '趋势'
    return df[['收盘价', 'ATR', 'ADX', 'MarketState']]
