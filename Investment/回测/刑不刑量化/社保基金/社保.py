import time

import pandas as pd

import akshare as ak

# 获取所有股票的十大流通股东数据
stock_gdfx_free_holding_teamwork_em_df = ak.stock_gdfx_free_holding_teamwork_em(symbol="社保")
stock_gdfx_free_holding_teamwork_em_df = stock_gdfx_free_holding_teamwork_em_df.head(10)
print(stock_gdfx_free_holding_teamwork_em_df)

# 保存到CSV文件
stock_gdfx_free_holding_teamwork_em_df.to_csv('social_security_holdings.csv', index=False)

# 等待运行
time.sleep(5)
# 假设已经获取到社保基金持仓数据，格式为DataFrame，包含股票代码、持股市值等列
social_security_holdings = pd.read_csv('social_security_holdings.csv')

def social_security_strategy():
    trading_dates = ['2022-10-31', '2023-04-30', '2023-08-31', '2024-08-31']  # 示例交易日期，实际应根据财报披露时间确定
    for i in range(len(trading_dates) - 1):
        current_date = trading_dates[i]
        next_date = trading_dates[i + 1]
        # 筛选出当前日期的持仓数据
        current_holdings = social_security_holdings[social_security_holdings['报告期'] == current_date]
        # 剔除退市停牌和上市不满一年新股（假设已有相应判断函数）
        current_holdings = current_holdings[~is_delisted_or_new_stock(current_holdings)]
        # 按持股市值排序
        current_holdings = current_holdings.sort_values(by='持股市值', ascending=False)
        # 选择市值最大的100只股票
        selected_stocks = current_holdings.head(100)
        # 在此处添加买入和卖出操作的代码，例如使用交易接口进行下单等
        buy_stocks(selected_stocks, next_date)
        sell_stocks(current_holdings, next_date)

def is_delisted_or_new_stock(holdings):
    # 假设这里有判断股票是否退市停牌或上市不满一年新股的逻辑
    return holdings['退市停牌判断'] | holdings['上市不满一年判断']

def buy_stocks(selected_stocks, date):
    # 实现买入股票的逻辑，例如通过交易接口下单
    print(f"在{date}买入股票：{selected_stocks['股票代码'].tolist()}")

def sell_stocks(current_holdings, date):
    # 实现卖出股票的逻辑，例如通过交易接口下单
    print(f"在{date}卖出股票：{current_holdings['股票代码'].tolist()}")

if __name__ == "__main__":
    social_security_strategy()