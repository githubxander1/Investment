# from tqsdk import TqApi, TqSim
# api = TqApi(TqSim())
# quote = api.get_quote("SHFE.au2306")
# whileTrue:  api.wait_update()
# print(quote.last_price)

from tqsdk import TqApi, TqAuth

# 创建 API 实例
api = TqApi(auth=TqAuth("19918754473", "TQsdk0520@xl"))
# 获取指定合约的行情对象
quote = api.get_quote("SHFE.cu2403")

while True:
    api.wait_update()
    print(f"最新价: {quote.last_price}")
# from tqsdk.taimportBOLL
# 初始化 API 和模拟账户
# api = TqApi(TqSim())
# 订阅行情
# quote = api.get_quote("SHFE.au2306")
# 获取 K 线数据
# klines = api.get_kline_serial("SHFE.au2306",60)
# while True:  api.wait_update()
# 等待数据更新
# boll = BOLL(klines,20)
# 计算布林带指标
  # 策略逻辑：价格突破布林带上下轨
# if klines.close.iloc[-1] > boll["upper"].iloc[-1]:
# print("做多信号触发！")
# elif klines.close.iloc[-1] < boll["lower"].iloc[-1]:
# print("做空信号触发！")


# from tqsdk import TqApi, TqBacktest, TqSim
# api = TqApi(TqSim(), backtest=TqBacktest(start_dt="2023-01-01", end_dt="2023-03-01"))
# klines = api.get_kline_serial("SHFE.au2306",60)
# whileTrue:  api.wait_update()
# print(klines.close.iloc[-1]) # 打印回测期间的最新收盘价