import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler

class FeatureEngineer:
    def __init__(self):
        self.scaler = MinMaxScaler()

    def load_national_team_data(self, file_path='国家队持股数据.xlsx'):
        """加载国家队持股数据"""
        sheets = ['最新公布', '持有最多', '增持最多', '持有最久']
        dfs = []

        for sheet in sheets:
            df = pd.read_excel(file_path, sheet_name=sheet)
            df['data_type'] = sheet
            dfs.append(df)

        return pd.concat(dfs, ignore_index=True)

    def load_market_data(self, days=30):
        """模拟市场行情数据（实际应从API获取）"""
        # 这里应该实现真正的市场数据获取逻辑
        # 模拟一些数据
        market_data = pd.DataFrame({
            'stock_code': ['000001', '600000', '300001', '002001'],
            'price': [10.0, 15.0, 20.0, 8.5],
            'volume': [1000000, 800000, 1200000, 900000],
            'change_rate': [1.5, -0.8, 2.3, 1.1]
        })
        return market_data

    def create_features(self, national_team_df, market_df):
        """创建特征"""
        # 合并数据
        df = pd.merge(national_team_df, market_df, on='stock_code', how='left')

        # 创建特征
        df['duration_score'] = df.groupby('stock_code')['fetch_time'].rank(method='first').astype(int)
        df['holder_count'] = df['holders_info'].str.split(',').str.len()
        df['is_new_entry'] = (df['data_type'] == '最新公布').astype(int)
        df['total_scale_rank'] = df['total_scale'].rank(ascending=False).astype(int)

        # 标准化数值特征
        numeric_cols = ['total_scale', 'holder_count', 'price', 'volume', 'change_rate']
        df[numeric_cols] = self.scaler.fit_transform(df[numeric_cols].fillna(0))

        return df

    def generate_labels(self, df, look_ahead_days=5):
        """生成标签：未来X天内的涨幅"""
        # 模拟标签生成（实际需要历史行情数据）
        np.random.seed(42)
        df['future_return'] = np.random.normal(0.02, 0.03, len(df))
        df['label'] = (df['future_return'] > 0.03).astype(int)  # 3%以上的涨幅为正样本

        return df
