import akshare as ak

# 获取指定 ETF 的历史行情数据
fund_etf_hist_em_df = ak.fund_etf_hist_em(symbol="510760", period="daily", start_date="20241201", end_date="20241211", adjust="hfq")
print("ETF 历史行情数据:")
print(fund_etf_hist_em_df)

# 获取指定 ETF 的持仓比例
fund_portfolio_hold_em_df = ak.fund_portfolio_hold_em(symbol="510760", date="2024")
print("\nETF 持仓比例:")
print(fund_portfolio_hold_em_df.head(10))

# 获取所有 ETF 的实时行情数据
fund_etf_spot_em_df = ak.fund_etf_spot_em()
fund_etf_spot_simple = fund_etf_spot_em_df[["代码", "名称", "最新价", "涨跌幅", "成交量", "成交额"]]
print("\nETF 实时行情数据:")
print(fund_etf_spot_simple)

# 获取指定股票的基金持股数据
# stock_fund_stock_holder_df = ak.stock_fund_stock_holder(stock="600004")
# print("\n股票基金持股数据:")
# print(stock_fund_stock_holder_df)

# 获取个股的基金持股数据
stock_report_fund_hold_df = ak.stock_report_fund_hold(symbol="基金持仓", date="20200630")
print("\n个股基金持股数据:")
print(stock_report_fund_hold_df)

# 获取指定基金的历史表现分析数据
fund_individual_analysis_xq_df = ak.fund_individual_analysis_xq(symbol="159915")
print("\n基金历史表现分析数据:")
print(fund_individual_analysis_xq_df)

# 获取指定基金的盈利概率及平均收益
fund_individual_profit_probability_xq_df = ak.fund_individual_profit_probability_xq(symbol="159915")
print("\n基金盈利概率及平均收益:")
print(fund_individual_profit_probability_xq_df)

# 获取指定类型的开放式基金规模数据
fund_scale_open_sina_df = ak.fund_scale_open_sina(symbol='股票型基金')
print("\n开放式基金规模数据:")
print(fund_scale_open_sina_df)

# 获取指定日期的 ETF 实时行情数据
fund_etf_spot_ths_df = ak.fund_etf_spot_ths(date="20240620")
print("\nETF 实时行情数据 (同花顺):")
print(fund_etf_spot_ths_df)

# 获取指定基金的基本信息
fund_individual_basic_info_xq_df = ak.fund_individual_basic_info_xq(symbol="510310")
print("\n基金基本信息:")
print(fund_individual_basic_info_xq_df)

# 获取所有基金的评级数据
fund_rating_all_df = ak.fund_rating_all()
print("\n基金评级数据:")
print(fund_rating_all_df)

# 获取指定基金的重大变动数据
fund_portfolio_change_em_df = ak.fund_portfolio_change_em(symbol="003567", indicator="累计买入", date="2023")
print("\n基金重大变动数据:")
print(fund_portfolio_change_em_df)
