def zhangting_relay_strategy(stock_df):
    """
    涨停接力策略：昨日涨停，今日红盘，成交量放大
    """
    stock_df['zt'] = (stock_df['close'] / stock_df['open'] - 1) >= 0.098
    stock_df['volume_increase'] = stock_df['volume'].pct_change() > 0.3

    buy_signal = stock_df[(stock_df['zt'].shift(1)) & (stock_df['close'] > stock_df['open']) & (stock_df['volume_increase'])]
    return buy_signal
