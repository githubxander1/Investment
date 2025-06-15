import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
import akshare as ak

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
        # 使用真实行情数据
        stock_zh_a_spot_df = ak.stock_zh_a_spot()
        return stock_zh_a_spot_df[['code', 'price', 'volume', 'changepercent']].rename(
            columns={
                'code': 'stock_code',
                'price': 'price',
                'volume': 'volume',
                'changepercent': 'change_rate'
            })

    def create_features(self, national_team_df, market_df):
        """创建特征"""
        # 合并数据
        df = pd.merge(national_team_df, market_df, on='stock_code', how='left')

        # 使用数值字段计算股东数量
        df['holder_count'] = df[['social_security', 'pension', 'central_bank', 'huijin']].apply(
            lambda x: (x > 0).sum(), axis=1)

        df['is_new_entry'] = (df['data_type'] == '最新公布').astype(int)
        df['total_scale_rank'] = df['total_scale'].rank(ascending=False).astype(int)

        # 标准化数值特征
        numeric_cols = ['total_scale', 'holder_count', 'price', 'volume', 'change_rate']
        df[numeric_cols] = self.scaler.fit_transform(df[numeric_cols].fillna(0))

        return df
