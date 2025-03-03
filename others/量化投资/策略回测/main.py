# generate_test_case.py
import os
import sys

import pandas as pd
from matplotlib import pyplot as plt

from backtest import backtest
from data_loader import load_data
from plotter import plot_kline_with_ma, plot_assets_and_cumulative_returns

# from strategy import calculate_ma, generate_signals  # 导入新的策略函数

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei']  # 使用黑体显示中文
plt.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题

# 配置 pandas 显示选项
pd.set_option('expand_frame_repr', False)  # 当列太多时不换行
pd.set_option('display.max_rows', 5000)  # 最多显示数据的行数


# 时间段
start_time = '20230531'
end_time = '20240424'

# 获取股票文件夹路径
file_path = os.path.abspath(os.path.dirname(__file__)) + '/股票数据/'  # 返回当前文件路径
# 获取文件夹下的所有csv文件的文件路径
file_list = os.listdir(file_path)
file_list = [f for f in file_list if '.csv' in f]

def load_strategy(strategy_file):
    """
    加载策略文件并返回其中的 calculate_ma 和 generate_signals 函数
    """
    # 将策略文件所在的目录添加到 sys.path
    strategy_dir = os.path.dirname(strategy_file)
    if strategy_dir not in sys.path:
        sys.path.append(strategy_dir)

    strategy_module_name = os.path.splitext(os.path.basename(strategy_file))[0]
    strategy_module = __import__(strategy_module_name)
    return strategy_module.calculate_ma, strategy_module.generate_signals

def generate_report(df, stock_name, final_total_asset, total_profit):
    """
    生成回测报告
    """
    report = {
        '操作股票': stock_name,
        '总信号数': len(df[df['信号'].isin(['买入', '卖出'])]),  # 计算总信号数
        '买入次数': len(df[df['信号'] == '买入']),
        '卖出次数': len(df[df['信号'] == '卖出']),
        '收益为正次数': len(df[df['收益'] > 0]),
        '收益为负次数': len(df[df['收益'] < 0]),
        # '总收益': df['收益'].sum(),
        '累计收益': total_profit,
        '最终总资产': final_total_asset
    }
    return report

def analyze_data(df, stock_name):
    """
    分析数据
    """
    # 计算累计收益的统计量
    cumulative_returns = df['累计收益']
    # print(f"\n{stock_name} 累计收益统计量:")
    # print(cumulative_returns.describe())

    # 结论和建议
    print(f"\n{stock_name} 结论和建议:")
    if cumulative_returns.iloc[-1] > 0:
        print(f"该策略在 {stock_name} 上实现了正的累计收益，最终总资产为 {df['总资产'].iloc[-1]:.2f}。")
    else:
        print(f"该策略在 {stock_name} 上未能实现正的累计收益，最终总资产为 {df['总资产'].iloc[-1]:.2f}。")

    if len(df[df['信号'] == '买入']) > len(df[df['信号'] == '卖出']):
        print(f"买入次数 ({len(df[df['信号'] == '买入'])}) 多于卖出次数 ({len(df[df['信号'] == '卖出'])})，可能需要调整卖出策略。")
    elif len(df[df['信号'] == '买入']) < len(df[df['信号'] == '卖出']):
        print(f"卖出次数 ({len(df[df['信号'] == '卖出'])}) 多于买入次数 ({len(df[df['信号'] == '买入'])})，可能需要调整买入策略。")
    else:
        print(f"买入次数 ({len(df[df['信号'] == '买入'])}) 等于卖出次数 ({len(df[df['信号'] == '卖出'])})，策略较为均衡。")

def main(strategy_file):
    """
    主函数，执行策略回测
    """
    calculate_ma, generate_signals = load_strategy(strategy_file)

    strategy_module_name = os.path.splitext(os.path.basename(strategy_file))[0]
    # 获取策略文件所在目录
    strategy_dir = os.path.dirname(strategy_file)

    # 遍历每个股票
    tables = []
    all_transactions = []

    for f in file_list:
        print(f"正在处理股票: {f}")
        table = load_data(f)

        table = calculate_ma(table)
        table = generate_signals(table)
        table = table[(table['交易日期'] >= pd.to_datetime(start_time)) & (table['交易日期'] <= pd.to_datetime(end_time))]

        if table.empty:
            print(f"警告: 股票 {f} 的数据为空，跳过该股票。")
        else:
            tables.append(table)

    all_table = pd.concat(tables, ignore_index=True)

    # 用于存储所有股票的交易记录
    all_transactions = {}
    reports = []

    for stock in file_list:
        stock_results = all_table[all_table['股票代码'] == stock.split('.')[0]].copy()  # 使用 .copy() 确保是原始 DataFrame 的副本
        if stock_results.empty:
            print(f"\n股票代码: {stock} 的回测结果为空，跳过该股票。")
            continue

        # 确保 '交易日期' 列存在并且格式正确
        stock_results.loc[:, '交易日期'] = pd.to_datetime(stock_results['交易日期'])

        # 重置索引以确保索引从 0 开始
        stock_results.reset_index(drop=True, inplace=True)

        # 修改解包语句以匹配 backtest 函数的返回值数量
        stock_results, final_total_asset, total_profit, transaction_df = backtest(stock_results)

        # 提取交易记录
        transactions = stock_results['transactions'].iloc[0]
        all_transactions[stock] = transactions

        # 获取股票名称
        stock_name = stock_results['股票名称'].unique()[0]

        # 生成并打印回测报告
        report = generate_report(stock_results, stock_name, final_total_asset, total_profit)
        reports.append(report)

        # 数据分析
        # analyze_data(stock_results, stock_name)

        # 显示K线图和均线图
        plot_kline_with_ma(stock_results, stock_name, strategy_dir, strategy_module_name)

        # 显示累计收益图和收益图
        plot_assets_and_cumulative_returns(stock_results, stock_name, strategy_dir, strategy_module_name)

    # 使用 ExcelWriter 将每个股票的交易记录保存到不同的工作表中
    with pd.ExcelWriter('记录/all_transactions.xlsx') as writer:
        for stock, transactions in all_transactions.items():
            stock_transactions = pd.DataFrame(transactions)
            stock_transactions['股票代码'] = stock.split('.')[0]
            stock_transactions.to_excel(writer, sheet_name=stock.split('.')[0], index=False)

    print(f"所有交易记录已保存到 all_transactions.xlsx")

    # 统计汇总
    reports_df = pd.DataFrame(reports)
    print("\n所有股票的统计汇总:")
    print(reports_df)

    # 计算策略的整体表现
    average_profit = reports_df['累计收益'].mean()
    win_rate = (reports_df['累计收益'] > 0).mean()  # 修改胜率计算方式
    num_positive_assets = (reports_df['最终总资产'] > 100000).sum()
    num_negative_assets = (reports_df['最终总资产'] <= 100000).sum()

    print("\n整体表现:")
    print(f"平均累计收益: {average_profit:.2f}")
    print(f"胜率: {win_rate:.2%}")
    print(f"最终总资产大于初始资产的数量: {num_positive_assets}")
    print(f"最终总资产小于等于初始资产的数量: {num_negative_assets}")

# 运行主函数
if __name__ == "__main__":
    # 自定义要测试的策略文件路径
    strategy_file = r'D:\1document\1test\PycharmProject_gitee\others\量化投资\策略回测\策略\双均线策略.py'  # 这里可以修改为你想要测试的策略文件路径
    # strategy_file = r'D:\1document\1test\PycharmProject_gitee\others\量化投资\策略回测\策略\5日优化1.py'  # 这里可以修改为你想要测试的策略文件路径
    # strategy_file = r'D:\1document\1test\PycharmProject_gitee\others\量化投资\策略回测\策略\五日均线策略.py'  # 这里可以修改为你想要测试的策略文件路径

    main(strategy_file)
