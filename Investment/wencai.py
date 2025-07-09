
#https://github.com/zsrl/pywencai

import pywencai

res = pywencai.get(query='退市股票', sort_key='退市@退市日期', perpage=10,query_type='stock',sort_order='asc', cookie='xxx')
print(res)