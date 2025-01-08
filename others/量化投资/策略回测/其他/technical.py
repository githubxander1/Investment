def technical_indicator(table):

    # =======以下计算指标的公式，可以修改
    # 计算过去40个交易日的最低价_复权的最小值
    table['LOW_N'] = table['最低价_复权'].rolling(40).min()
    # 计算过去40个交易日的最高价_复权的最大值
    table['HIGH_N'] = table['最高价_复权'].rolling(40).max()
    # 计算相对强弱指数 (RSV)
    table['RSV'] = (table['收盘价_复权'] - table['LOW_N']) / (table['HIGH_N'] - table['LOW_N']) * 100
    # 计算K值，使用指数加权移动平均，span=2
    table['K'] = table['RSV'].ewm(span=(3-1), adjust=False).mean()
    # 计算D值，使用指数加权移动平均，span=2
    table['D'] = table['K'].ewm(span=(3-1), adjust=False).mean()

    # =======以下计算交易信号，可以修改
    # 金叉信号：当前K值大于D值，且前一天K值小于等于D值时，生成买入信号（signal = 1）
    table.loc[(table['K'].shift(1) <= table['D'].shift(1)) & (table['K'] > table['D']), 'signal'] = 1
    # 死叉信号：当前K值小于D值，且前一天K值大于等于D值时，生成卖出信号（signal = 0）
    table.loc[(table['K'].shift(1) >= table['D'].shift(1)) & (table['K'] < table['D']), 'signal'] = 0

    return table
