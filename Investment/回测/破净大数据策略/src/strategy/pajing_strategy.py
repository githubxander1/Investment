# pajing_strategy.py
import backtrader as bt
import numpy as np
import pandas as pd
from src.strategy.base_strategy import BaseStrategy

class PajingStrategy(BaseStrategy):
    params = (
        ('pb_threshold', 1.0),
        ('hold_days', 60),
        ('sector_weights', {}),
        ('dynamic_weight', True)
    )

    def __init__(self):
        super().__init__()
        # 添加技术指标
        self.sma20 = bt.indicators.SimpleMovingAverage(
            self.data.close, period=20)

        self.sma60 = bt.indicators.SimpleMovingAverage(
            self.data.close, period=60)

        self.volume_sma20 = bt.indicators.SimpleMovingAverage(
            self.data.volume, period=20)

    def prenext(self):
        # 初始化持仓记录
        self.log('策略预热阶段')

    def next(self):
        current_date = self.datas[0].datetime.date(0)

        # 动态调仓
        if self._should_rebalance(current_date):
            self._dynamic_rebalance(current_date)

        # 止损检查
        self._check_stop_loss(current_date)

    def _should_rebalance(self, current_date):
        """判断是否需要调仓"""
        # 每月最后一个交易日调仓
        if current_date.day >= 28:
            return True

        # 突发事件检查
        if self._check_event_alerts():
            return True

        return False

    def _dynamic_rebalance(self, current_date):
        """动态调仓逻辑"""
        # 获取最新分析数据
        df_analysis = pd.read_excel('data/raw/破净股票数据_*.xlsx')

        # 计算综合评分
        df_analysis = self._calculate_composite_score(df_analysis)

        # 获取有效标的
        valid_stocks = df_analysis[
            df_analysis['composite_score'] > self.p.score_threshold
        ]['股票代码'].tolist()

        # 执行调仓
        self._execute_rebalance(valid_stocks)

    def _calculate_composite_score(self, df):
        """多因子综合评分"""
        # 行业景气度映射
        sector_map = {
            '银行': 0.8, '房地产': 0.6, '钢铁': 0.7,
            '公用事业': 0.9, '交通运输': 0.75, '电力': 0.85
        }

        # 计算因子
        df['pb_score'] = 1 - df['市净率']
        df['sector_score'] = df['行业'].map(sector_map).fillna(0.5)
        df['volume_score'] = df['成交量'].rank(pct=True)

        # 综合评分
        df['composite_score'] = (
            self.params.factor_weights.get('pb', 0.35) * df['pb_score'] +
            self.params.factor_weights.get('sector', 0.25) * df['sector_score'] +
            self.params.factor_weights.get('volume', 0.15) * df['volume_score'] +
            self.params.factor_weights.get('custom', 0.25) * df['自定义因子']
        )

        return df.sort_values('composite_score', ascending=False)

    def _execute_rebalance(self, valid_stocks):
        """执行调仓操作"""
        # 计算目标权重
        target_weights = self._calculate_position_weights(valid_stocks)

        # 执行交易
        for stock, weight in target_weights.items():
            self.order_target_percent(stock, target=weight)

    def _calculate_position_weights(self, stocks):
        """计算仓位权重"""
        weights = {}
        sector_counts = {}

        # 行业均衡分配
        for stock in stocks:
            sector = self._get_stock_sector(stock)
            sector_counts[sector] = sector_counts.get(sector, 0) + 1

        for stock in stocks:
            sector = self._get_stock_sector(stock)
            sector_weight = self.params.sector_weights.get(
                sector,
                1 / len(sector_counts)
            )

            # 动态调整
            if self.params.dynamic_weight:
                score = self._get_stock_score(stock)
                sector_weight *= score / 100

            weights[stock] = sector_weight

        return weights
