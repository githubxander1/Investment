import backtrader as bt
import pandas as pd

from trading_strategy import NationalTeamStrategy

def run_backtest(data, strategy_class=NationalTeamStrategy, start_date=None, end_date=None):
    """运行回测"""
    cerebro = bt.Cerebro()

    if start_date and end_date:
        data = data[(data.index >= start_date) & (data.index <= end_date)]

    # 确保日期列为 datetime 类型
    if 'date' in data.columns:
        data['date'] = pd.to_datetime(data['date'])
        data.set_index('date', inplace=True)
    else:
        data.index = pd.to_datetime(data.index)

    data_feed = bt.feeds.PandasData(dataname=data)
    cerebro.adddata(data_feed)

    # 添加策略
    cerebro.addstrategy(strategy_class)

    # 设置初始资金
    cerebro.broker.setcash(100000.0)

    # 设置佣金
    cerebro.broker.setcommission(
        commission=0.001,
        margin=1.0,
        leverage=1.0
    )

    # 设置滑点（示例：百分比滑点）
    cerebro.broker.set_slippage_perc(0.005)  # 0.5% 的滑点

    print('开始回测...')
    results = cerebro.run()
    print('回测完成')

    # 打印结果
    print('\n最终资产:', cerebro.broker.getvalue())

    # 绘制图表
    cerebro.plot()

    return results
