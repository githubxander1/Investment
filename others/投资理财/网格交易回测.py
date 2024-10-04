import qstock as qs

import pandas as pd

import backtrader as bt

# 创建自定义网格交易策略

class GridStrategy(bt.Strategy):

    params =(

        ('grid_size',0.03),  # 网格间距

        ('grid_min',2.23),  # 网格最低价

        ('grid_max',3.89),  # 网格最高价

        ('order_pct',0.1),  # 每次买入卖出的仓位比例

    )

    def __init__(self):

        self.buy_orders =[]

        self.sell_orders =[]

        self.grid_levels =[]

        # 生成网格层次

        self.grid_levels =[self.p.grid_min + i * self.p.grid_size for i in range(int((self.p.grid_max - self.p.grid_min)/ self.p.grid_size)+1)]

    def next(self):

        current_price = self.data.close[0]

        # 买入条件：当前价格低于某个网格层次且未持有该层次买单

        for level in self.grid_levels:

            if current_price <= level and not any([order for order in self.buy_orders if order.price == level]):

                size = self.broker.getcash()* self.p.order_pct / current_price

                order = self.buy(price=level, size=size)

                self.buy_orders.append(order)

        # 卖出条件：当前价格高于某个网格层次且未持有该层次卖单

        for level in self.grid_levels:

            if current_price >= level and not any([order for order in self.sell_orders if order.price == level]):

                size = self.broker.getvalue()* self.p.order_pct / current_price

                order = self.sell(price=level, size=size)

                self.sell_orders.append(order)

qs.bt_result(code='沪深300',

    start='20200101',

    end='20240927',

    strategy=GridStrategy,

    startcash=1000000.0,

    commission=0.0001,

)