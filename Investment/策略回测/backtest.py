# backtest.py
import logging
from decimal import Decimal, getcontext

import pandas as pd

getcontext().prec = 10
logging.basicConfig(filename='记录/回测log.log',
                    level=logging.INFO,
                    encoding='utf-8',
                    format='%(asctime)s - %(levelname)s - %(message)s')

def backtest(df, initial_capital=Decimal('100000.0')):
    # 复制 DataFrame 以避免 SettingWithCopyWarning
    df = df.copy()

    # 初始化必要的列
    df['持有'] = 0  # 是否持有股票
    df['买入价'] = Decimal('0.0')  # 最近一次买入的价格
    df['持有数量'] = 0  # 当前持有的股票数量
    df['总资产'] = initial_capital  # 初始化总资产
    df['余额'] = initial_capital  # 初始化现金余额
    df['持有金额'] = Decimal('0.0')  # 持仓成本
    df['收益'] = Decimal('0.0')  # 收益
    df['累计收益'] = Decimal('0.0')  # 累计收益

    transactions = []  # 存储交易记录

    lot_size = 100  # 手数
    commission_rate = Decimal('0.0001')  # 手续费率
    stamp_tax_rate = Decimal('0.00005')  # 印花税率

    last_balance = initial_capital  # 上一次操作后的余额
    last_holding_quantity = 0  # 上次买入操作后的持有数量
    last_total_cost = 0  # 上次买入操作后的总成本
    last_buy_index = None  # 记录上次买入的索引

    # 初始化变量来存储最后一次操作后的总资产和累计收益
    last_total_asset = initial_capital
    last_cumulative_profit = Decimal('0.0')

    for i in range(1, len(df)):
        if df.loc[i, '信号'] == '买入':
            # 买入信号
            try:
                price = round(Decimal(df.loc[i, '收盘价_复权']), 3)  # 价格保留3位小数
            except Exception as e:
                logging.error(f"Invalid value for conversion to Decimal: {df.loc[i, '收盘价_复权']}")
                continue

            available_cash = last_balance  # 使用上一次的余额
            max_quantity = int(available_cash / price)  # 根据余额计算最大可买股数
            quantity = max_quantity - (max_quantity % lot_size)  # 调整为整数手
            total_cost = price * quantity * (1 + commission_rate)  # 总成本
            # total_cost_with_commission = total_cost + stamp_tax_rate * (price * quantity)  # 总成本加上印花税

            if available_cash >= price * lot_size:
                df.at[i, '持有'] = 1
                df.at[i, '买入价'] = price
                df.at[i, '持有数量'] = quantity
                df.at[i, '持有金额'] = price * quantity
                df.at[i, '余额'] = available_cash - total_cost
                df.at[i, '总资产'] = df.at[i, '余额'] + df.at[i, '持有金额']
                df.at[i, '累计收益'] = df.at[i, '总资产'] - initial_capital
                transactions.append({
                    '日期': df.loc[i, '交易日期'],
                    '操作': '买入',
                    '价格': price,
                    '数量': quantity,
                    '持有金额': round(df.at[i, '持有金额'], 3),
                    '总成本': round(total_cost, 3),
                    '余额': round(df.at[i, '余额'], 3),
                    '总资产': round(df.at[i, '总资产'], 3)
                })
                last_balance = df.at[i, '余额']
                last_holding_quantity = quantity
                last_total_cost = round(total_cost, 3)
                last_buy_index = i  # 更新上次买入的索引
                last_total_asset = df.at[i, '总资产']
                last_cumulative_profit = df.at[i, '累计收益']

                logging.info(f"买入: 日期: {df.loc[i, '交易日期']}, 价格: {price}, 数量: {quantity}, 总成本: {round(total_cost, 3)}, 余额: {round(df.at[i, '余额'], 3)} , 总资产: {round(df.at[i, '总资产'], 3)}")
            else:
                df.at[i, '持有'] = 0  # 如果无法买入，保持持有状态不变
                df.at[i, '买入价'] = Decimal('0.0')
                df.at[i, '持有数量'] = 0
                df.at[i, '持有金额'] = Decimal('0.0')
                df.at[i, '余额'] = available_cash
                df.at[i, '总资产'] = available_cash
                df.at[i, '累计收益'] = available_cash - initial_capital
                transactions.append({
                    '日期': df.loc[i, '交易日期'],
                    '操作': '买入失败',
                    '价格': price,
                    '数量': quantity,
                    '持有金额': 0,
                    '总成本': 0,
                    '余额': round(available_cash, 3),
                    '总资产': round(available_cash, 3)
                })
                logging.warning(f"警告: 余额不足，无法买入。日期: {df.loc[i, '交易日期']}, 价格: {price}, 需要: {total_cost}, 当前余额: {available_cash}")

        elif df.loc[i, '信号'] == '卖出':
            # 卖出信号
            price = round(Decimal(df.loc[i, '收盘价_复权']), 3)  # 价格保留3位小数
            quantity = last_holding_quantity  # 使用上次买入操作后的持有数量
            total_sell = price * quantity
            commission = total_sell * commission_rate
            stamp_tax = total_sell * stamp_tax_rate
            total_sell_with_fees = total_sell - (commission + stamp_tax)

            if last_buy_index is not None:
                df.at[i, '持有'] = 0
                df.at[i, '买入价'] = 0.0
                df.at[i, '持有数量'] = 0
                df.at[i, '持有金额'] = 0.0
                df.at[i, '余额'] = df.loc[last_buy_index, '余额'] + total_sell_with_fees
                df.at[i, '总资产'] = df.at[i, '余额']
                df.at[i, '收益'] = round(total_sell_with_fees, 3) - last_total_cost
                df.at[i, '累计收益'] = round(df.at[i, '总资产'] - initial_capital, 3)
                transactions.append({
                    '日期': df.loc[i, '交易日期'],
                    '操作': '卖出',
                    '价格': price,
                    '数量': quantity,
                    # '卖出收入': round(total_sell_with_fees, 3),
                    '余额': round(df.at[i, '余额'], 3),
                    '总资产': round(df.at[i, '总资产'], 3),
                    '收益': round(df.at[i, '收益'], 3)
                })
                last_balance = df.at[i, '余额']
                last_holding_quantity = quantity
                last_buy_index = None  # 重置上次买入的索引
                last_total_asset = df.at[i, '总资产']
                last_cumulative_profit = df.at[i, '累计收益']

                logging.info(f"卖出: 日期: {df.loc[i, '交易日期']}, 价格: {price}, 数量: {quantity}, 收益: {round(df.at[i, '收益'], 3)}, 余额: {round(df.at[i, '余额'], 3)}, 总资产: {round(df.at[i, '总资产'], 3)}")

            else:
                df.at[i, '持有'] = 0  # 如果没有之前的买入操作，保持持有状态不变
                df.at[i, '买入价'] = Decimal('0.0')
                df.at[i, '持有数量'] = 0
                df.at[i, '持有金额'] = Decimal('0.0')
                df.at[i, '余额'] = last_balance
                df.at[i, '总资产'] = last_balance

                df.at[i, '累计收益'] = last_balance - initial_capital
                transactions.append({
                    '日期': df.loc[i, '交易日期'],
                    '操作': '卖出失败',
                    '价格': price,
                    '数量': quantity,
                    # '卖出收入': 0,
                    '余额': round(last_balance, 3),
                    '总资产': round(last_balance, 3),
                    '收益': 0
                })
                logging.warning(f"警告: 没有之前的买入操作，无法卖出。日期: {df.loc[i, '交易日期']}")

    # 将最后一次操作后的总资产和累计收益赋值给最终变量
    final_total_asset = last_total_asset
    total_profit = last_cumulative_profit

    # 将 `transactions` 添加到表格中
    file_path = '记录/transactions.xlsx'
    # df['transactions'] = [transactions] * len(df)
    df['transactions'].to_excel(file_path, index=False)
    # df.to_excel('output.xlsx', index=False)

    # 创建一个新的 DataFrame 来存储交易记录
    transaction_df = pd.DataFrame(transactions)

    # 返回原始的 df、最终总资产和总利润
    return df, final_total_asset, total_profit, transactions
