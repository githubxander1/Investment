# five_ma_backtest.py
import os

import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import pandas as pd

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei']  # 使用黑体显示中文
plt.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题

pd.set_option('expand_frame_repr', False)  # 当列太多时不换行
pd.set_option('display.max_rows', 5000)  # 最多显示数据的行数

# ====设定测试参数，可以自行修改
# 移动平均线周期
window = 5
# 测试时间段，可根据数据时间更改
start_time = '20230531'
end_time = '20240424'

# ====获取所有股票数据的股票代码
# 获取股票文件夹路径
file_path = os.path.abspath(os.path.dirname(__file__)) + '/股票数据/'  # 返回当前文件路径
# 获取文件夹下的所有csv文件的文件路径
file_list = os.listdir(file_path)
file_list = [f for f in file_list if '.csv' in f]

# ====遍历每个股票
tables = []
for f in file_list:
    print(f"正在处理股票: {f}")
    # 读取这个数据的数据
    table = pd.read_csv(os.path.join(file_path, f), encoding='gbk', parse_dates=['交易日期'])
    table['股票代码'] = f.split('.')[0]  # 假设文件名是股票代码.csv

    # 打印数据的前几行，检查数据是否正确加载
    print(table.head())

    # 计算5日移动平均线
    table['5日均线'] = table['收盘价_复权'].rolling(window=window).mean()
    print(table[['交易日期', '收盘价_复权', '5日均线']].head())

    # 生成交易信号
    table['signal'] = 0
    table.loc[table['5日均线'] > table['收盘价_复权'], 'signal'] = 1  # 买入信号
    table.loc[table['5日均线'] < table['收盘价_复权'], 'signal'] = 0  # 卖出信号

    # 打印信号列的前几行，检查信号是否正确生成
    print(table[['交易日期', '收盘价_复权', '5日均线', 'signal']].head(10))

    # 选取指定时间范围内的股票
    table = table[(table['交易日期'] >= pd.to_datetime(start_time)) & (table['交易日期'] <= pd.to_datetime(end_time))]

    # 打印筛选后的数据，检查是否为空
    print(f"筛选后的数据行数: {len(table)}")
    if table.empty:
        print(f"警告: 股票 {f} 的数据为空，跳过该股票。")
    else:
        tables.append(table)

all_table = pd.concat(tables, ignore_index=True)

# =====模拟交易
def backtest(table, initial_capital=100000.0):
    table['持有'] = 0  # 初始化持有状态
    table['持仓成本'] = 0.0  # 初始化持仓成本为浮点数
    table['现金'] = initial_capital  # 初始化现金为浮点数
    table['总资产'] = initial_capital  # 初始化总资产为浮点数
    table['累计收益'] = 0.0  # 初始化累计收益为浮点数

    # 记录买入和卖出操作
    transactions = []

    for i in range(1, len(table)):
        if table.loc[i, 'signal'] == 1 and table.loc[i-1, '持有'] == 0:
            # 买入信号
            table.loc[i, '持有'] = 1
            table.loc[i, '持仓成本'] = table.loc[i, '收盘价_复权']
            table.loc[i, '现金'] = table.loc[i-1, '现金'] - table.loc[i, '持仓成本']
            table.loc[i, '总资产'] = table.loc[i, '现金'] + table.loc[i, '持仓成本']
            transactions.append({
                '日期': table.loc[i, '交易日期'],
                '价格': table.loc[i, '收盘价_复权'],
                '操作': '买入'
            })
            # print(f"买入信号: 日期: {table.loc[i, '交易日期']}, 价格: {table.loc[i, '收盘价_复权']}")
        elif table.loc[i, 'signal'] == 0 and table.loc[i-1, '持有'] == 1:
            # 卖出信号
            table.loc[i, '持有'] = 0
            table.loc[i, '现金'] = table.loc[i-1, '现金'] + table.loc[i, '收盘价_复权']
            table.loc[i, '总资产'] = table.loc[i, '现金']
            table.loc[i, '累计收益'] = table.loc[i, '总资产'] - initial_capital
            transactions.append({
                '日期': table.loc[i, '交易日期'],
                '价格': table.loc[i, '收盘价_复权'],
                '操作': '卖出'
            })
            # print(f"卖出信号: 日期: {table.loc[i, '交易日期']}, 价格: {table.loc[i, '收盘价_复权']}")

    table['transactions'] = [transactions] * len(table)  # 将交易记录添加到表格中
    return table

# =====回测每个股票
backtest_results = []
for f in file_list:
    table = tables[file_list.index(f)]
    result = backtest(table)
    if not result.empty:
        backtest_results.append(result)
    else:
        print(f"警告: 股票 {f} 的回测结果为空，跳过该股票。")

# =====合并所有股票的回测结果
if backtest_results:
    all_backtest_results = pd.concat(backtest_results, ignore_index=True)
else:
    print("所有股票的回测结果都为空，无法进行分析。")
    exit(1)

# =====分析回测结果
def analyze_backtest(results):
    if results.empty:
        print("回测结果为空，无法进行分析。")
        return

    # 计算总收益
    total_return = results['累计收益'].iloc[-1]
    # 计算平均收益
    average_return = results['累计收益'].mean()
    # 计算最大回撤
    cumulative_returns = results['总资产'] / results['总资产'].iloc[0]
    drawdown = cumulative_returns / cumulative_returns.cummax() - 1
    max_drawdown = drawdown.min()

    print(f'\n总收益: {total_return}')
    print(f'平均收益: {average_return}')
    print(f'最大回撤: {max_drawdown}')

    # 绘制收盘价曲线和均线
    def plot_kline_with_ma(df):
        plt.figure(figsize=(14, 7))
        plt.plot(df['交易日期'], df['收盘价_复权'], label='收盘价')
        plt.plot(df['交易日期'], df['5日均线'], label='5日均线')
        buy_signals = df[df['signal'] == 1]
        sell_signals = df[df['signal'] == 0]
        plt.scatter(buy_signals['交易日期'], buy_signals['收盘价_复权'], color='red', marker='^', label='买入信号')
        plt.scatter(sell_signals['交易日期'], sell_signals['收盘价_复权'], color='green', marker='v', label='卖出信号')
        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
        plt.gcf().autofmt_xdate()
        plt.title('K线图+均线')
        plt.xlabel('交易日期')
        plt.ylabel('价格')
        plt.legend()
        plt.show()

    # 绘制总资产和收益情况
    def plot_assets_and_returns(df):
        plt.figure(figsize=(14, 7))
        plt.plot(df['交易日期'], df['总资产'], label='总资产')
        plt.title('总资产和收益情况')
        plt.xlabel('交易日期')
        plt.ylabel('总资产')
        plt.legend()
        plt.grid(True)
        plt.show()

    # 展示每个股票的买入和卖出操作
    for stock in file_list:
        stock_results = results[results['股票代码'] == stock]
        if stock_results.empty:
            print(f"\n股票代码: {stock} 的回测结果为空，跳过该股票。")
            continue
        plot_kline_with_ma(stock_results)
        plot_assets_and_returns(stock_results)
        transactions = stock_results['transactions'].iloc[0]
        print(f'\n股票代码: {stock}')
        for transaction in transactions:
            print(f"日期: {transaction['日期']}, 价格: {transaction['价格']}, 操作: {transaction['操作']}")

analyze_backtest(all_backtest_results)
