import backtrader as bt

class DualMAStrategy(bt.Strategy):
    params = (
        ('short_window', 10),
        ('long_window', 30),
        ('print_log', True)
    )

    def __init__(self):
        self.data_close = self.datas[0].close
        self.short_ma = bt.indicators.SimpleMovingAverage(self.datas[0], period=self.params.short_window)
        self.long_ma = bt.indicators.SimpleMovingAverage(self.datas[0], period=self.params.long_window)
        self.order = None

    def next(self):
        if self.order:
            return

        if not self.position:
            if self.short_ma[0] > self.long_ma[0]:
                self.log(f'BUY CREATE, {self.data_close[0]:.2f}')
                self.order = self.buy()
        else:
            if self.short_ma[0] < self.long_ma[0]:
                self.log(f'SELL CREATE, {self.data_close[0]:.2f}')
                self.order = self.sell()

    def log(self, txt, dt=None):
        if self.params.print_log:
            dt = dt or self.datas[0].datetime.date(0)
            print(f'{dt.isoformat()} {txt}')

    def notify_order(self, order):
        if order.status in [order.Submitted, order.Accepted]:
            return

        if order.status in [order.Completed]:
            if order.isbuy():
                self.log(f'BUY EXECUTED, {order.executed.price:.2f}')
            elif order.issell():
                self.log(f'SELL EXECUTED, {order.executed.price:.2f}')

            self.bar_executed = len(self)

        self.order = None
