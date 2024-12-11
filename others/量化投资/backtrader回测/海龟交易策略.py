import backtrader as bt
import pandas as pd
import akshare as ak
from backtrader.feeds import PandasData
import warnings
import quantstats as qs

warnings.filterwarnings('ignore')

# 常量定义
SYMBOL = "510310"
START_DATE = "20210101"
END_DATE = "20241211"
ADJUST = "hfq"
START_CASH = 20000
COMMISSION = 0.0001

# 数据获取
def get_data(symbol, start_date, end_date, adjust):
    fund_etf_hist_em_df = ak.fund_etf_hist_em(symbol=symbol, period="daily", start_date=start_date, end_date=end_date, adjust=adjust)
    fund_etf_hist_em_df['date'] = pd.to_datetime(fund_etf_hist_em_df["日期"])
    fund_etf_hist_em_df.set_index('date', inplace=True)
    return fund_etf_hist_em_df

# 策略定义
class TurtleStrategy(bt.Strategy):
    params = (
        ('H_period', 20),   # 唐奇安通道上轨周期
        ('L_period', 10),   # 唐奇安通道下轨周期
        ('ATRPeriod', 14),  # 平均真实波幅ATR周期
    )

    def log(self, txt, dt=None, doprint=False):
        if doprint:
            dt = dt or self.datetime.date(0)
            print(f'{dt.isoformat()},{txt}')

    def __init__(self):
        self.order = None
        self.buyprice = 0
        self.buycomm = 0
        self.buy_size = 0
        self.buy_count = 0

        self.H_line = bt.indicators.Highest(self.data.high(-1), period=self.p.H_period)
        self.L_line = bt.indicators.Lowest(self.data.low(-1), period=self.p.L_period)
        self.ATR = bt.indicators.AverageTrueRange(self.data, period=self.p.ATRPeriod)

        self.buy_signal = bt.ind.CrossOver(self.data.close(0), self.H_line)
        self.sell_signal = bt.ind.CrossDown(self.data.close(0), self.L_line)

    def next(self):
        if self.order:
            return

        if self.buy_signal and self.buy_count == 0:
            self.buy_size = self.broker.getvalue() * 0.01 / self.ATR
            self.buy_size = int(self.buy_size / 100) * 100

            self.buy_count += 1
            self.log('创建买单')
            self.order = self.buy(size=self.buy_size)

        elif self.data.close > self.buyprice + 0.5 * self.ATR[0] and self.buy_count > 0 and self.buy_count <= 4:
            self.buy_size = self.broker.getvalue() * 0.01 / self.ATR
            self.buy_size = int(self.buy_size / 100) * 100

            self.log('创建买单')
            self.order = self.buy(size=self.buy_size)
            self.buy_count += 1

        elif self.position:
            if self.sell_signal or self.data.close < (self.buyprice - 2 * self.ATR[0]):
                self.log('创建卖单')
                self.order = self.close()
                self.buy_count = 0

    def notify_order(self, order):
        if order.status in [order.Submitted, order.Accepted]:
            return

        if order.status in [order.Completed]:
            if order.isbuy():
                self.log(f'买入:价格:{order.executed.price}, 成本:{order.executed.value}, 手续费:{order.executed.comm}')
                self.buyprice = order.executed.price
                self.buycomm = order.executed.comm
            else:
                self.log(f'卖出:价格:{order.executed.price}, 成本:{order.executed.value}, 手续费:{order.executed.comm}')
        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            self.log('交易失败%s' % order.getstatusname())
        self.order = None

    def notify_trade(self, trade):
        if not trade.isclosed:
            return
        self.log(f'策略收益：\n毛收益 {trade.pnl:.2f}, 净收益 {trade.pnlcomm:.2f}')

    def stop(self):
        self.log(f'(组合线：{self.p.H_period},{self.p.L_period}); 期末总资金: {self.broker.getvalue():.2f}', doprint=True)

# 主函数
def main():
    # 获取数据
    data = get_data(SYMBOL, START_DATE, END_DATE, ADJUST)

    # 创建Cerebro实例
    cerebro = bt.Cerebro()
    data_feed = PandasData(dataname=data,
                           datetime=None,
                           open='开盘',
                           high='最高',
                           low='最低',
                           close='收盘',
                           volume='成交量',
                           openinterest=None)
    cerebro.adddata(data_feed)

    # 设置策略
    cerebro.addstrategy(TurtleStrategy)

    # 设置资金和佣金
    cerebro.broker.setcash(START_CASH)
    cerebro.broker.setcommission(commission=COMMISSION)

    # 添加分析器
    cerebro.addanalyzer(bt.analyzers.PyFolio, _name="PyFolio")

    # 运行回测
    results = cerebro.run()

    # 获取回测结果
    portvalue = cerebro.broker.getvalue()
    pnl = portvalue - START_CASH
    print(f'初始资金：{START_CASH}')
    print(f'总资金: {round(portvalue, 2)}')
    print(f'净收益: {round(pnl, 2)}')

    # 内置画图
    cerebro.plot(iplot=False)

    # Quantstats分析
    pyfolio = results[0].analyzers.PyFolio
    returns, positions, transactions, gross_lev = pyfolio.get_pf_items()

    # 打印详细的性能指标
    try:
        qs_stats = qs.stats.compsum(returns)
        print(f"Cumulative Return: {qs_stats['total']:.2%}")
    except KeyError:
        print("Cumulative Return: N/A")

    print(f"CAGR: {qs.stats.cagr(returns):.2%}")
    print(f"Sharpe Ratio: {qs.stats.sharpe(returns):.2f}")
    print(f"Sortino Ratio: {qs.stats.sortino(returns):.2f}")
    print(f"Max Drawdown: {qs.stats.max_drawdown(returns):.2%}")
    print(f"Volatility (annualized): {qs.stats.volatility(returns):.2%}")
    print(f"Calmar Ratio: {qs.stats.calmar(returns):.2f}")
    print(f"Skew: {qs.stats.skew(returns):.2f}")
    print(f"Kurtosis: {qs.stats.kurtosis(returns):.2f}")
    print(f"Kelly Criterion: {qs.stats.kelly_criterion(returns):.2f}")
    print(f"Best Day: {qs.stats.best(returns):.2%}")
    print(f"Worst Day: {qs.stats.worst(returns):.2%}")
    print(f"Best Month: {qs.stats.best(returns, 'M'):.2%}")
    print(f"Worst Month: {qs.stats.worst(returns, 'M'):.2%}")
    print(f"Best Year: {qs.stats.best(returns, 'Y'):.2%}")
    print(f"Worst Year: {qs.stats.worst(returns, 'Y'):.2%}")

    # 生成quantstats报告
    qs.reports.full(returns)

if __name__ == "__main__":
    main()
