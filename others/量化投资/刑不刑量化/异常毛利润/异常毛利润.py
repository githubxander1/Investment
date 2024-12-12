import akshare as ak
import pandas as pd
import numpy as np

import akshare as ak
import pandas as pd

def calculate_abnormal_gross_profit(symbol):
    try:
        # 获取股票财务数据
        stock_financial_data = ak.stock_financial_analysis_indicator(symbol)
        stock_financial_data['date'] = pd.to_datetime(stock_financial_data['date'])
        stock_financial_data.set_index('date', inplace=True)

        # 计算毛利润增长
        stock_financial_data['gross_profit_growth'] = (stock_financial_data['gross_profit'].diff() / stock_financial_data['gross_profit'].shift(1))
        # 计算销售额增长
        stock_financial_data['sales_growth'] = (stock_financial_data['operating_revenue'].diff() / stock_financial_data['operating_revenue'].shift(1))
        # 计算异常毛利润
        stock_financial_data['abnormal_gross_profit'] = stock_financial_data['gross_profit_growth'] - stock_financial_data['sales_growth']

        return stock_financial_data
    except:
        print(f"获取股票 {symbol} 数据失败")
        return None

def stock_selection_strategy(start_date, end_date):
    all_stocks = []
    for symbol in ak.stock_zh_a_spot_em().index:
        try:
            # 获取股票财务数据
            stock_financial_data = ak.stock_financial_analysis_indicator(symbol)
            stock_financial_data['date'] = pd.to_datetime(stock_financial_data['date'])
            stock_financial_data.set_index('date', inplace=True)
            # 计算异常毛利润
            stock_financial_data = calculate_abnormal_gross_profit(stock_financial_data)
            # 合并到总数据中
            all_stocks.append(stock_financial_data)
        except:
            continue
    all_stocks_df = pd.concat(all_stocks, axis=1)
    all_stocks_df.columns = pd.MultiIndex.from_product([all_stocks_df.columns.levels[0], all_stocks_df.columns.levels[1]])
    # 每月最后一个交易日进行选股
    trading_dates = pd.date_range(start_date, end_date, freq='M')
    portfolio = []
    for i in range(len(trading_dates) - 1):
        current_date = trading_dates[i]
        next_date = trading_dates[i + 1]
        # 筛选当前月的数据
        monthly_data = all_stocks_df.loc[current_date.strftime('%Y-%m')]
        # 按异常毛利润排序
        monthly_data.sort_values(by=('abnormal_gross_profit', 'abnormal_gross_profit'), ascending=False, inplace=True)
        # 选择前5%的股票
        top_stocks = monthly_data.index[:int(len(monthly_data) * 0.05)]
        portfolio.append(top_stocks)
    return portfolio


def simulate_trading(portfolio):
    initial_capital = 1000000
    capital = initial_capital
    positions = {}
    for i in range(len(portfolio)):
        if i > 0:
            # 卖出上一期持有的股票
            for stock in positions:
                current_price = ak.stock_zh_a_hist(symbol=stock, period="daily", start_date=portfolio[i - 1][0], end_date=portfolio[i][0])['close'].iloc[-1]
                capital += positions[stock] * current_price
                del positions[stock]
        # 买入本期选中的股票
        for stock in portfolio[i]:
            current_price = ak.stock_zh_a_hist(symbol=stock, period="daily", start_date=portfolio[i][0], end_date=portfolio[i][0])['close'].iloc[-1]
            positions[stock] = capital / (len(portfolio[i]) * current_price)
    # 最后一期卖出股票
    for stock in positions:
        current_price = ak.stock_zh_a_hist(symbol=stock, period="daily", start_date=portfolio[-1][0], end_date=portfolio[-1][0])['close'].iloc[-1]
        capital += positions[stock] * current_price
    return capital / initial_capital

if __name__ == "__main__":
    start_date = '2010-01-01'
    end_date = '2023-12-31'
    portfolio = stock_selection_strategy(start_date, end_date)
    final_value = simulate_trading(portfolio)
    print(f"最终资金变为初始资金的{final_value}倍")