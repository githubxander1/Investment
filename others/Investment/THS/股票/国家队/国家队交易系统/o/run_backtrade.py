import backtrader as bt
import pandas as pd

def run_backtest(data_path, strategy_class=DualMA Strategy):
    cerebro = bt.Cerebro()

    # 加载数据
    data = bt.feeds.GenericCSVData(
        dataname=data_path,
        fromdate=datetime.datetime(2022, 6, 15),
        todate=datetime.datetime(2023, 6, 15),
        datetime=1,
        open=2,
        high=3,
        low=4,
        close=5,
        volume=6,
        openinterest=-1
    )
    cerebro.adddata(data)

    # 添加策略
    cerebro.addstrategy(strategy_class)

    # 设置初始资金
    cerebro.broker.setcash(100000.0)

    # 设置佣金
    cerebro.broker.setcommission(commission=0.001)

    print('开始回测...')
    results = cerebro.run()
    print('回测完成')

    # 打印结果
    print('\n最终资产:', cerebro.broker.getvalue())

    # 绘制图表
    cerebro.plot()

    return results

# 示例：运行双均线策略回测
data_path = 'stock_data/601800.csv'  # 替换为实际的股票数据路径
run_backtest(data_path, strategy_class=DualMA Strategy)

# 示例：运行不同持有期策略回测
run_backtest(data_path, strategy_class=HoldingPeriodStrategy)
