'''
均线计算：
计算5日均线 (MA5)、10日均线 (MA10) 和20日均线 (MA20)。
选股条件：
TREND_UP：5日均线和20日均线均呈上升趋势。
CROSS_UP：收盘价高于5日均线和10日均线，并且开盘价高于收盘价（即阴线）。
VBR：成交量比5日平均成交量高1.3倍。
VOL_UP：成交量高于5日平均成交量。
MAV_WEEK 和 MAV10W：计算5日和10日的平均成交量。
VOL_WEEK_UP：成交量高于5日和10日平均成交量的两倍。
SELECTION：综合上述条件，选择符合条件的股票。
操作信号：
BUY_SIG：买入信号，满足 SELECTION 条件。
SELL_SIG1：卖出信号1，满足以下条件：
5日均线高于收盘价。
过去30天内收盘价低于5日均线的天数至少为1天。
收盘价相对于5日均线的跌幅超过2%。
SELL_SIG2：卖出信号2，满足以下条件：
收盘价高于5日均线的1.2倍。
过去5天内收盘价高于5日均线的天数为5天。
过去3天内收盘价相对于前一天的涨幅超过10%的天数至少为1天。
SELL_SIG3：卖出信号3，满足以下条件：
前一天为买入信号。
5日均线高于收盘价。
收盘价低于前一天的收盘价。
收盘价相对于前一天的跌幅超过3%。
SELL_SIG：综合卖出信号，满足 SELL_SIG1、SELL_SIG2 或 SELL_SIG3 中的任意一个。
生成最终的交易信号：
signal 列：0 表示卖出信号，1 表示买入信号。
'''


def calculate_ma(data):
    """
    计算均线
    """
    data['MA5'] = data['收盘价_复权'].rolling(window=5).mean()
    data['MA10'] = data['收盘价_复权'].rolling(window=10).mean()
    data['MA20'] = data['收盘价_复权'].rolling(window=20).mean()
    return data

def generate_signals(data):
    """
    生成买入和卖出信号
    """
    # 选股条件
    data['TREND_UP'] = (data['MA5'] >= data['MA5'].shift(1)) & (data['MA20'] >= data['MA20'].shift(1))
    data['CROSS_UP'] = (data['收盘价_复权'] > data['MA5']) & (data['收盘价_复权'] > data['MA10']) & (data['开盘价_复权'] > data['收盘价_复权'])
    data['VBR'] = data['成交量'] / data['成交量'].rolling(window=5).mean()
    data['VOL_UP'] = (data['VBR'] > 1.3) & (data['成交量'] > data['成交量'].rolling(window=5).mean())
    data['MAV_WEEK'] = data['成交量'].rolling(window=5).mean()
    data['MAV10W'] = data['成交量'].rolling(window=10).mean()
    data['VOL_WEEK_UP'] = (data['成交量'] > 2 * data['MAV_WEEK']) & (data['成交量'] > data['MAV10W'])
    data['SELECTION'] = data['TREND_UP'] & data['CROSS_UP'] & data['VOL_UP'] & data['VOL_WEEK_UP']

    # 操作信号
    data['BUY_SIG'] = data['SELECTION']
    data['SELL_SIG1'] = (data['MA5'] > data['收盘价_复权']) & ((data['收盘价_复权'] < data['MA5']).rolling(window=30).sum() >= 1) & (
            (data['收盘价_复权'] - data['MA5']) / data['MA5'] < -0.02)
    data['SELL_SIG2'] = (data['收盘价_复权'] > 1.2 * data['MA5']) & (((data['收盘价_复权'] > data['MA5']).rolling(window=5).sum() == 5) & ((data['收盘价_复权'] - data['收盘价_复权'].shift(1)) / data['收盘价_复权'].shift(1) > 0.1).rolling(window=3).sum() >= 1)
    # data['SELL_SIG3'] = data['BUY_SIG'].shift(1) & (data['MA5'] > data['收盘价_复权']) & (data['收盘价_复权'] < data['收盘价_复权'].shift(1)) & (
    #         (data['收盘价_复权'] - data['收盘价_复权'].shift(1)) / data['收盘价_复权'].shift(1) < -0.03)

    # 综合卖出信号
    data['SELL_SIG'] = data['SELL_SIG2']
                       # | data['SELL_SIG3']

    # 生成最终的交易信号
    data['signal'] = 0
    data.loc[data['BUY_SIG'], 'signal'] = 1  # 买入信号
    data.loc[data['SELL_SIG'], 'signal'] = 0  # 卖出信号

    # 将 signal 列转换为 信号 列
    data['信号'] = data['signal'].map({1: '买入', 0: '卖出'})

    return data
