import akshare as ak

# 分时数据
# 接口: stock_zh_a_minute
# 目标地址: http://finance.sina.com.cn/realstock/company/sh600519/nc.shtml
# 描述: 新浪财经获取分时数据，目前可以获取 1, 5, 15, 30, 60 分钟的数据频率
# 限量: 单次返回指定公司的指定频率的所有历史分时行情数据
stock_zh_a_minute_df = ak.stock_zh_a_minute(symbol='sh000300', period='1')
# print(stock_zh_a_minute_df)

# 电报-财联社
# 接口：stock_info_global_cls
# 目标地址：https://www.cls.cn/telegraph
# 描述：财联社-电报
# 限量：单次返回指定 symbol 的最近 20 条财联社-电报的数据
stock_info_global_cls_df = ak.stock_info_global_cls(symbol="sh000300")
# print(stock_info_global_cls_df)

# 个股估值
# 接口: stock_value_em
# 目标地址: https://data.eastmoney.com/gzfx/detail/300766.html
# 描述: 东方财富网-数据中心-估值分析-每日互动-每日互动-估值分析
# 限量: 单次获取指定 symbol 的所有历史数据
stock_value_em_df = ak.stock_value_em(symbol="300766")
# print(stock_value_em_df)

# 主要股东
# 接口: stock_main_stock_holder
# 目标地址: https://vip.stock.finance.sina.com.cn/corp/go.php/vCI_StockHolder/stockid/600004.phtml
# 描述: 获取新浪财经-股本股东-主要股东
# 限量: 单次获取新浪财经-股本股东-主要股东所有历史数据
stock_main_stock_holder_df = ak.stock_main_stock_holder(stock="600004")
# print(stock_main_stock_holder_df)

# 机构持股一览表
# 接口: stock_institute_hold
# 目标地址: http://vip.stock.finance.sina.com.cn/q/go.php/vComStockHold/kind/jgcg/index.phtml
# 描述: 获取新浪财经-机构持股-机构持股一览表
# 限量: 单次获取新浪财经-机构持股-机构持股一览表所有数据
# stock_institute_hold_df = ak.stock_institute_hold(quarter="20201")
# print(stock_institute_hold_df)

# 机构持股详情
# 接口: stock_institute_hold_detail
# 目标地址: http://vip.stock.finance.sina.com.cn/q/go.php/vComStockHold/kind/jgcg/index.phtml
# 描述: 获取新浪财经-机构持股-机构持股详情
# 限量: 单次获取新浪财经-机构持股-机构持股详情所有数据
stock_institute_hold_detail_df = ak.stock_institute_hold_detail(stock="300003", quarter="20201")
# print(stock_institute_hold_detail_df)

# 股东持股变动统计
# 接口: stock_shareholder_change_ths
# 目标地址: https://basic.10jqka.com.cn/new/688981/event.html
# 描述: 同花顺-公司大事-股东持股变动
# 限量: 单次返回所有数据
stock_shareholder_change_ths_df = ak.stock_shareholder_change_ths(symbol="688981")
# print(stock_shareholder_change_ths_df)

# 公司股本变动-巨潮资讯
# 接口: stock_share_change_cninfo
# 目标地址: https://webapi.cninfo.com.cn/#/apiDoc
# 描述: 巨潮资讯-数据-公司股本变动
# 限量: 单次获取指定 symbol 在 start_date 和 end_date 之间的公司股本变动数据
stock_share_change_cninfo_df = ak.stock_share_change_cninfo(symbol="002594", start_date="20091227", end_date="20241021")
# print(stock_share_change_cninfo_df)

# 实时行情数据-雪球
# 接口: stock_individual_spot_xq
# 目标地址: https://xueqiu.com/S/SH513520
# 描述: 雪球-行情中心-个股
# 限量: 单次获取指定 symbol 的最新行情数据
stock_individual_spot_xq_df = ak.stock_individual_spot_xq(symbol="SPY")
# print(stock_individual_spot_xq_df.dtypes)

# 信息披露调研-巨潮资讯
# 接口: stock_zh_a_disclosure_relation_cninfo
# 目标地址: http://www.cninfo.com.cn/new/commonUrl/pageOfSearch?url=disclosure/list/search
# 描述: 巨潮资讯-首页-公告查询-信息披露调研-沪深京
# 限量: 单次获取指定 symbol 的信息披露调研数据
stock_zh_a_disclosure_relation_cninfo_df = ak.stock_zh_a_disclosure_relation_cninfo(symbol="000001", market="沪深京", start_date="20230619", end_date="20231220")
# print(stock_zh_a_disclosure_relation_cninfo_df)

# 股东持股明细-十大股东
# 接口: stock_gdfx_holding_detail_em
# 目标地址: https://data.eastmoney.com/gdfx/HoldingAnalyse.html
# 描述: 东方财富网-数据中心-股东分析-股东持股明细-十大股东
# 限量: 单次返回指定参数的所有数据
stock_gdfx_holding_detail_em_df = ak.stock_gdfx_holding_detail_em(date="20230331", indicator="个人", symbol="新进")
# print(stock_gdfx_holding_detail_em_df)

# 股东持股明细-十大流通股东
# 接口: stock_gdfx_free_holding_detail_em
# 目标地址: https://data.eastmoney.com/gdfx/HoldingAnalyse.html
# 描述: 东方财富网-数据中心-股东分析-股东持股明细-十大流通股东
# 限量: 单次返回指定 date 的所有数据
stock_gdfx_free_holding_detail_em_df = ak.stock_gdfx_free_holding_detail_em(date="20210930")
print(stock_gdfx_free_holding_detail_em_df)
