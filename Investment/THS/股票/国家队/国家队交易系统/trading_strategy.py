import backtrader as bt
import pandas as pd
import numpy as np
import os
import joblib

class NationalTeamStrategy(bt.Strategy):
    params = (
        ('print_log', True),
        ('risk_ratio', 0.05),  # 风险比例
        ('stop_loss', 0.03),   # 止损比例
        ('take_profit', 0.05) # 止盈比例
    )

    def log(self, txt, dt=None):
        if self.params.print_log:
            dt = dt or self.datas[0].datetime.date(0)
            print(f'{dt.isoformat()} {txt}')

    def __init__(self):
        self.data_close = self.datas[0].close
        self.order = None
        self.buy_price = None
        self.position_size = None

        # 加载机器学习模型
        model_path = 'models/national_team_model.pkl'
        if os.path.exists(model_path):
            self.ml_model = joblib.load(model_path)
            self.feature_columns = self.ml_model['feature_columns']
            self.model = self.ml_model['model']
        else:
            self.ml_model = None
            self.model = None
            self.feature_columns = None

    def next(self):
        if self.order:
            return

        # 计算当前特征
        features = self._extract_current_features()

        if self.feature_columns and self.model:
            # 使用机器学习模型预测
            prediction = self.model.predict_proba(features)[0][1]

            # 如果预测上涨且未持仓
            if prediction > 0.7 and not self.position:
                size = self.broker.getcash() * self.p.risk_ratio // self.data_close[0]
                if size > 0:
                    self.log(f'买入信号 - 概率: {prediction:.2f}, 数量: {size}')
                    self.order = self.buy(size=size)
                    self.buy_price = self.data_close[0]
                    self.position_size = size

        # 止损或止盈
        elif self.position:
            returns = (self.data_close[0] - self.buy_price) / self.buy_price

            # 止损
            if returns <= -self.p.stop_loss:
                self.log(f'止损卖出! 收益率: {returns:.2%}')
                self.order = self.sell(size=self.position_size)

            # 止盈
            elif returns >= self.p.take_profit:
                self.log(f'止盈卖出! 收益率: {returns:.2%}')
                self.order = self.sell(size=self.position_size)

            # 到达最大持仓时间
            elif len(self) >= 5:  # 最大持仓5天
                self.log(f'持仓到期卖出! 收益率: {returns:.2%}')
                self.order = self.sell(size=self.position_size)

    def _extract_current_features(self):
        """提取当前特征"""
        # 实际应用中这里应该根据真实数据构建特征
        features = pd.DataFrame([{
            'total_scale': 0.05,
            'holder_count': 3,
            'price': self.data_close[0],
            'volume': 1000000,
            'change_rate': 1.5,
            'is_new_entry': 1,
            'total_scale_rank': 10
        }])

        # 补全缺失特征
        if self.feature_columns:
            for col in self.feature_columns:
                if col not in features.columns:
                    features[col] = 0

        return features[self.feature_columns]
