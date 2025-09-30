

import akshare

#获取日线数据
# df = akshare.stock_zh_a_hist(symbol='000001', start_date='2026-05-01', end_date='2026-06-05', adjust='qfq')
df = akshare.stock_zh_a_hist_tx(symbol='sz000001', start_date='20250501', end_date='20250605', adjust='qfq')
# df = akshare.stock_zh_a_daily(symbol='sz000001', start_date='20250501', end_date='20250605', adjust='qfq')
# df = akshare.stock_zh_a_tick_tx_js(symbol='sz000001')
# df = akshare.stock_zh_a_hist(symbol='sz000001',start_date='20250501', end_date='20250605', adjust='qfq')
# df = akshare.stock_zh_a_spot_em()

print(df)