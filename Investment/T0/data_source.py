from pprint import pprint

import requests
from efinance.bond import get_quote_history
from efinance.stock import get_realtime_quotes


# # 获取贵州茅台（600519.SH）的当日1分钟K线
# url = 'http://push2his.eastmoney.com/api/qt/stock/kline/get?secid=1.600519&klt=101&fqt=0'
# response = requests.get(url)
# data = response.json()
# pprint(data)
#
# # from efinance import get_quote_history
# # 获取腾讯控股（00700.HK）的5分钟K线
# # df = get_quote_history('600030', beg='20251023', end='20251023', klt=1, fqt=1)
# # df.to_csv('600030.csv', index=False)
# # print(df)
#
# import requests
# # 获取宁德时代（300750.SZ）的当日分时成交数据
# url = 'http://api.mairuiapi.com/hsrl/fscj/300750.SZ'
# response = requests.get(url)
# data = response.json()
# pprint(data)
import requests

def get_realtime_data(stock_code):
    url = f"http://hq.sinajs.cn/list=sh{stock_code}"
    response = requests.get(url)
    data = response.text.split('=')[1].split(',')
    return {
        'date': data[30],
        'time': data[31],
        'price': data[32],
        'volume': data[33]
    }

stock_code = '600519'  # 示例股票代码，上证指数
data = get_realtime_data(stock_code)
print(data)
