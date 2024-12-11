import akshare as ak

'''https://zhuanlan.zhihu.com/p/715128889
获取历史行情数据
接口: fund_etf_hist_em
描述: 东方财富-ETF行情; 历史数据按日频率更新, 当日收盘价请在收盘后获取
限量: 单次返回指定ETF、指定周期和指定日期间的历史行情日频率数据
文档: https://akshare.akfamily.xyz/da
前复权adjust="qfq"
后复权adjust="hfq"
'''
# 不复权
fund_etf_hist_em_df = ak.fund_etf_hist_em(symbol="510760", period="daily", start_date="20241201", end_date="20241211", adjust="hfq")
# print(fund_etf_hist_em_df)

'''
金持仓比例
接口: fund_portfolio_hold_em
描述: 天天基金网-基金档案-投资组合-基金持仓
限量: 单次返回指定 symbol 和 date 的所有持仓数据
'''
fund_portfolio_hold_em_df = ak.fund_portfolio_hold_em(symbol="510760", date="2024")
fund_portfolio_hold_em_df = fund_portfolio_hold_em_df.head(10)
# print(fund_portfolio_hold_em_df)

'''
获取实时行情数据-所有基金列表
接口: fund_etf_spot_em
描述: 东方财富-ETF 实时行情
限量: 单次返回所有数据

按成交额排序
df_sorted = fund_etf_spot_simple.sort_values(by='成交额', ascending=False)
# 成交量最大的10个etf基金
df_sorted[:10]'''
# import akshare as ak
fund_etf_spot_em_df = ak.fund_etf_spot_em()
fund_etf_spot_simple = fund_etf_spot_em_df[["代码","名称","最新价","涨跌幅","成交量","成交额"]]
# print(fund_etf_spot_simple)

'''基金持股
接口: stock_fund_stock_holder

目标地址: https://vip.stock.finance.sina.com.cn/corp/go.php/vCI_FundStockHolder/stockid/600004.phtml

描述: 获取新浪财经-股本股东-基金持股

限量: 单次获取新浪财经-股本股东-基金持股所有历史数据

输入参数

名称类型必选描述stockstrYstock="600004"; 股票代码'''
# import akshare as ak
# stock_fund_stock_holder_df = ak.stock_fund_stock_holder(stock="600004")
# print(stock_fund_stock_holder_df)

'''作者：搏击长空
链接：https://zhuanlan.zhihu.com/p/163224286
来源：知乎
著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。

基金持股接口: stock_report_fund_hold目标地址: http://data.eastmoney.com/zlsj/2020-06-30-1-2.html
描述: 获取个股的基金持股数据限量: 单次返回指定 symbol 和 date 的所有历史数据输入参数名称类型必选描述symbolstrYsymbol="基金持仓"; 
choice of {"基金持仓", "QFII持仓", "社保持仓", "券商持仓", "保险持仓", "信托持仓"}datestrYdate="20200630"; 
财报发布日期, xxxx-03-31, xxxx-06-30, xxxx-09-30, 
xxxx-12-31输出参数名称类型默认显示描述stock_codedatetimeY股票代码stock_namefloatY股票简称pub_datefloatY发布时间hold_numfloatY持有基金家数(家)hold_changefloatY持股变化share_hold_numfloatY持股总数(股)value_positionfloatY持股市值(元)hold_value_changefloatY持股变动数值(元)hold_rate_changefloatY持股变动比例(%)
接口示例import akshare as ak'''
stock_report_fund_hold_df = ak.stock_report_fund_hold(symbol="基金持仓", date="20200630")
# print(stock_report_fund_hold_df)

'''获取基金分析数据
雪球基金分析
接口: fund_individual_analysis_xq
目标地址: https://danjuanfunds.com/funding/000001
描述: 雪球基金-基金详情-数据分析
限量: 返回单只基金历史表现分析数据'''
fund_individual_analysis_xq_df = ak.fund_individual_analysis_xq(symbol="159915")
# print(fund_individual_analysis_xq_df)

'''基金盈利概率
接口: fund_individual_profit_probability_xq
描述: 雪球基金-基金详情-盈利概率；历史任意时点买入，持有满X时间，盈利概率，以及平均收益
限量: 单次返回单只基金历史任意时点买入，持有满 X 时间，盈利概率，以及平均收益'''
fund_individual_profit_probability_xq_df = ak.fund_individual_profit_probability_xq(symbol="159915")
# print(fund_individual_profit_probability_xq_df)

'''
开放式基金接口: fund_scale_open_sina目标地址: https://vip.stock.finance.sina.com.cn/fund_center/index.html#jjhqetf描述: 基金数据中心-基金规模-开放式基金限量: 单次返回指定 symbol 的基金规模数据输入参数名称类型描述symbolstrsymbol="股票型基金"; choice of {"股票型基金", "混合型基金", "债券型基金", "货币型基金", "QDII基金"}

作者：搏击长空
链接：https://zhuanlan.zhihu.com/p/717679707
来源：知乎
著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。'''
fund_scale_open_sina_df = ak.fund_scale_open_sina(symbol='股票型基金')
# print(fund_scale_open_sina_df)

'''ETF基金实时行情-同花顺接口: fund_etf_spot_ths目标地址: https://fund.10jqka.com.cn/datacenter/jz/kfs/etf/描述: 同花顺理财-基金数据-每日净值-ETF-实时行情限量: 单次返回指定 date 的所有数据输入参数名称类型描述datestrdate=""; 默认返回当前最新的数据

作者：搏击长空
链接：https://zhuanlan.zhihu.com/p/704731467
来源：知乎
著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。'''
fund_etf_spot_ths_df = ak.fund_etf_spot_ths(date="20240620")
# print(fund_etf_spot_ths_df)

'''基金基本信息-雪球接口: fund_individual_basic_info_xq目标地址: https://danjuanfunds.com/funding/000001描述: 雪球基金-基金详情限量: 单次返回单只基金基本信息输入参数名称类型描述symbolstrsymbol="000001"; 基金代码timeoutfloattimeout=None; 默认不设置超时参数

作者：搏击长空
链接：https://zhuanlan.zhihu.com/p/675891447
来源：知乎
著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。'''
fund_individual_basic_info_xq_df = ak.fund_individual_basic_info_xq(symbol="510310")
print(fund_individual_basic_info_xq_df)

'''
基金评级-基金评级总汇
接口: fund_rating_all

目标地址: https://fund.eastmoney.com/data/fundrating.html

描述: 天天基金网-基金评级-基金评级总汇

限量: 单次返回所有基金评级数据'''
fund_rating_all_df = ak.fund_rating_all()
print(fund_rating_all_df)

'''重大变动接口: fund_portfolio_change_em目标地址: https://fundf10.eastmoney.com/ccbd_000001.html描述: 天天基金网-基金档案-投资组合-重大变动限量: 单次返回指定 symbol、indicator 和 date 的所有重大变动数据输入参数名称类型描述symbolstrsymbol="003567"; 基金代码, 可以通过调用 ak.fund_name_em() 接口获取indicatorstrindicator="累计买入"; choice of {"累计买入", "累计卖出"}datestrdate="2023"; 指定年份

作者：搏击长空
链接：https://zhuanlan.zhihu.com/p/665075502
来源：知乎
著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。'''
fund_portfolio_change_em_df = ak.fund_portfolio_change_em(symbol="003567", indicator="累计买入", date="2023")
print(fund_portfolio_change_em_df)