import backtrader as bt
import pandas as pd

class SingleHoldingPeriodStrategy(bt.Strategy):
    """单个持有期策略"""
    params = (
        ('holding_period', None),  # 单个持有期
        ('print_log', False),
        ('stock_name', ''),
        ('buy_date', None)
    )

    def __init__(self):
        self.data_close = self.datas[0].close
        self.order = None
        self.buy_price = None
        self.buy_executed = False
        self.sell_executed = False
        self.buy_bar_index = None
        self.result = None

    def next(self):
        if self.sell_executed:
            return

        current_date = self.datas[0].datetime.date(0)

        # 确保买入日期是datetime.date类型
        if isinstance(self.params.buy_date, pd.Timestamp):
            buy_date = self.params.buy_date.date()
        else:
            buy_date = self.params.buy_date

        # 如果是买入日（选股日+1）
        if current_date == buy_date and not self.buy_bar_index:
            self.log(f'到达买入日: {current_date}, 准备买入')
            self.buy_bar_index = len(self)
            if not self.buy_executed:
                self.log(f'BUY CREATE for {self.params.holding_period} days, {self.data_close[0]:.2f}')
                self.buy()
                self.buy_executed = True
                self.buy_price = self.data_close[0]

        # 检查卖出条件
        if self.buy_bar_index is not None and not self.sell_executed:
            if len(self) >= (self.buy_bar_index + self.params.holding_period):
                self.log(f'SELL CREATE after {self.params.holding_period} days, {self.data_close[0]:.2f}')
                self.sell()
                self.sell_executed = True
                self.sell_price = self.data_close[0]

    def stop(self):
        # 计算收益
        if self.buy_executed and self.sell_executed:
            profit = (self.sell_price - self.buy_price) / self.buy_price
            self.result = {
                'holding_period': self.params.holding_period,
                'buy_price': self.buy_price,
                'sell_price': self.sell_price,
                'profit': profit
            }
        else:
            self.result = None

    def log(self, txt, dt=None):
        if self.params.print_log:
            dt = dt or self.datas[0].datetime.date(0)
            print(f'{dt.isoformat()} {txt}')

    def notify_order(self, order):
        if order.status in [order.Submitted, order.Accepted]:
            return

        # 订单完成状态
        if order.status in [order.Completed]:
            if order.isbuy():
                self.log(f'BUY EXECUTED, {order.executed.price:.2f}')
            elif order.issell():
                self.log(f'SELL EXECUTED, {order.executed.price:.2f}')

        # 重置订单状态
        self.order = None
