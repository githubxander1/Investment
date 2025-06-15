import backtrader as bt

class HoldingPeriodStrategy(bt.Strategy):
    params = (
        ('holding_periods', [5, 10, 20]),  # 短期、中期、长期持有期（单位：天）
        ('print_log', True)
    )

    def __init__(self):
        self.data_close = self.datas[0].close
        self.order = None
        self.buy_date = None

    def next(self):
        if self.order:
            return

        if not self.position:
            self.log(f'BUY CREATE, {self.data_close[0]:.2f}')
            self.order = self.buy()
            self.buy_date = len(self)
        else:
            for period in self.params.holding_periods:
                if len(self) >= (self.buy_date + period):
                    self.log(f'SELL CREATE after {period} days, {self.data_close[0]:.2f}')
                    self.order = self.sell()
                    self.buy_date = None
                    break

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
