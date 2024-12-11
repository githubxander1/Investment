import tushare as ts

#设置你的token，登录tushare在个人用户中心里拷贝
ts.set_token('2e9a7a0827b4c655aa6c267dc00484c6e76ab1022b5717092b44573e')

#sina数据
df = ts.realtime_tick(ts_code='600000.SH')
df = df.head(100)
print(df)

# #东财数据
# df = ts.realtime_tick(ts_code='600000.SH', src='dc')