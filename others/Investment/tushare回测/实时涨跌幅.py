import pandas as pd
import tushare as ts
from datetime import datetime, timedelta

# 设置Tushare Pro的API Token
ts.set_token('2e9a7a0827b4c655aa6c267dc00484c6e76ab1022b5717092b44573e')

# 初始化Tushare API
pro = ts.pro_api()

# 获取当前日期
current_date = datetime.now().date()

# 东财数据
df = ts.realtime_list(src='dc')

# 限制只查询前100条数据
df = df.head(100)

# 将输出的列名从英文替换为中文
column_mapping = {
    'ts_code': '股票代码',
    'name': '股票名称',
    'price': '当前价格',
    'pct_change': '涨跌幅',
    'change': '涨跌额',
    'volume': '成交量（单位：手）',
    'amount': '成交金额（元）',
    'swing': '振幅',
    'low': '今日最低价',
    'high': '今日最高价',
    'open': '今日开盘价',
    'close': '今日收盘价',
    'vol_ratio': '量比',
    'turnover_rate': '换手率',
    'pe': '市盈率PE',
    'pb': '市净率PB',
    'total_mv': '总市值（元）',
    'float_mv': '流通市值（元）',
    'rise': '涨速',
    '5min': '5分钟涨幅',
    '60day': '60天涨幅',
    '1tyear': '1年涨幅'
}

df.rename(columns=column_mapping, inplace=True)

# 打印结果
print(df)

# 保存到CSV文件
# df.to_csv('D:\\stock_list.csv', index=False, encoding='utf-8-sig')
