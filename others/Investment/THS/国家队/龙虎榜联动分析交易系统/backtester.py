import backtrader as bt

class LHBStrategy(bt.Strategy):
    params = (
        ('print_log', True),
    )

    def log(self, txt, dt=None):
        if self.params.print_log:
            dt = dt or self.datas[0].datetime.date(0)
            print(f'{dt.isoformat()} {txt}')

    def __init__(self):
        self.data_close = self.datas[0].close
        self.order = None
        self.buy_price = None
        self.buy_comm = None

    def notify_order(self, order):
        if order.status in [order.Submitted, order.Accepted]:
            return
        if order.status in [order.Completed]:
            if order.isbuy():
                self.log(
                    f'BUY EXECUTED, Price: {order.executed.price:.2f}, Cost: {order.executed.value:.2f}, Comm: {order.executed.comm:.2f}'
                )
                self.buy_price = order.executed.price
                self.buy_comm = order.executed.comm
            else:
                self.log(
                    f'SELL EXECUTED, Price: {order.executed.price:.2f}, Cost: {order.executed.value:.2f}, Comm: {order.executed.comm:.2f}'
                )
            self.bar_executed = len(self)
        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            self.log('Order Canceled/Margin/Rejected')
        self.order = None

    def next(self):
        if not self.position:
            if self.data_close[0] > self.data_close[-1]:  # 红K线
                self.buy(size=100)  # 买入100股
        else:
            if len(self) >= self.bar_executed + 5:  # 持有5天后卖出
                self.sell(size=100)

# 使用示例
cerebro = bt.Cerebro()
data = bt.feeds.PandasData(dataname=your_df)  # 替换为你的历史数据
cerebro.adddata(data)
cerebro.addstrategy(LHBStrategy)
cerebro.broker.setcash(100000.0)
cerebro.run()

# 输出结果
print(f"初始资金: 100000.00")
print(f"最终资金: {cerebro.broker.getvalue():.2f}")
