# backtester.py
import backtrader as bt
import pandas as pd
from src.data.data_loader import DataLoader
from src.strategy.pajing_strategy import PajingStrategy

class Backtester:
    def __init__(self, config):
        self.config = config
        self.cerebro = bt.Cerebro()
        self._setup_data()
        self._setup_strategy()

    def _setup_data(self):
        """加载并添加数据到Cerebro"""
        # 加载数据
        data_loader = DataLoader(self.config)
        stock_data = data_loader.load_local_data(
            self.config['data']['file_path']
        )

        # 转换为Cerebro数据格式
        for _, row in stock_data.iterrows():
            data = bt.feeds.PandasData(dataname=row)
            self.cerebro.adddata(data)

    def _setup_strategy(self):
        """配置策略"""
        self.cerebro.addstrategy(
            PajingStrategy,
            pb_threshold=self.config['strategy']['pb_threshold'],
            hold_days=self.config['strategy']['hold_days'],
            factor_weights=self.config['strategy']['factor_weights'],
            sector_weights=self.config['strategy']['sector_weights']
        )

    def run_backtest(self):
        """运行回测"""
        # 设置初始资金
        self.cerebro.broker.setcash(self.config['backtest']['initial_capital'])

        # 添加分析器
        self.cerebro.addanalyzer(bt.analyzers.SharpeRatio, _name='sharpe')
        self.cerebro.addanalyzer(bt.analyzers.DrawDown, _name='drawdown')

        # 运行回测
        results = self.cerebro.run()

        # 保存结果
        self._save_results(results)

        return results

    def _save_results(self, results):
        """保存回测结果"""
        # 保存策略结果
        strategy_results = {
            'final_value': self.cerebro.broker.getvalue(),
            'sharpe_ratio': results[0].analyzers.sharpe.get_analysis(),
            'drawdown': results[0].analyzers.drawdown.get_analysis()
        }

        # 保存详细交易记录
        trade_records = results[0].analyzers.getbyname('trade_list').get_analysis()

        # 生成图表
        self._generate_charts()

    def _generate_charts(self):
        """生成回测图表"""
        fig = self.cerebro.plot(style='candlestick')
        fig.savefig('reports/results/backtest_chart.png')
