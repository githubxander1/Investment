from tqsdk import TqApi, TqSimfrom tqsdk.ta import BOLL
# 初始化 API 和模拟账户api = TqApi(TqSim())
# 订阅行情quote = api.get_quote("SHFE.au2306")
# 获取 K 线数据klines = api.get_kline_serial("SHFE.au2306", 60)
while True:    api.wait_update()  # 等待数据更新    boll = BOLL(klines, 20)  # 计算布林带指标
    # 策略逻辑：价格突破布林带上下轨    if klines.close.iloc[-1] > boll["upper"].iloc[-1]:        print("做多信号触发！")    elif klines.close.iloc[-1] < boll["lower"].iloc[-1]:        print("做空信号触发！")


from tqsdk import TqApi, TqBacktest, TqSim
api = TqApi(TqSim(), backtest=TqBacktest(start_dt="2023-01-01", end_dt="2023-03-01"))klines = api.get_kline_serial("SHFE.au2306", 60)
while True:    api.wait_update()    print(klines.close.iloc[-1])  # 打印回测期间的最新收盘价