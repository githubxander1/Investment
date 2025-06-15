import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
import joblib
import os

class NationalTeamModel:
    def __init__(self, model_path='models/national_team_model.pkl'):
        self.model = RandomForestClassifier(n_estimators=100, random_state=42)
        self.model_path = model_path
        self.feature_columns = None

    def prepare_data(self, df):
        """准备训练数据"""
        # 确保所有特征都是数值类型
        X = df.select_dtypes(include=[np.number]).drop(['future_return', 'label'], axis=1, errors='ignore')
        y = df['label'] if 'label' in df.columns else None

        # 保存特征列名
        if self.feature_columns is None:
            self.feature_columns = X.columns.tolist()
        else:
            # 确保特征一致性
            missing_cols = set(self.feature_columns) - set(X.columns)
            for col in missing_cols:
                X[col] = 0

            X = X[self.feature_columns]

        return X, y

    def train(self, X_train, y_train):
        """训练模型"""
        self.model.fit(X_train, y_train)

        # 保存模型
        os.makedirs(os.path.dirname(self.model_path), exist_ok=True)
        joblib.dump({
            'model': self.model,
            'feature_columns': self.feature_columns
        }, self.model_path)

        print("模型训练完成并已保存")

    def evaluate(self, X_test, y_test):
        """评估模型"""
        y_pred = self.model.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)

        print(f"模型准确率: {accuracy:.2f}")
        print("\n分类报告:")
        print(classification_report(y_test, y_pred))

        return accuracy

    def predict(self, X):
        """进行预测"""
        if not self.feature_columns:
            raise ValueError("模型尚未训练，请先进行训练")

        # 确保输入数据有正确的特征
        for col in self.feature_columns:
            if col not in X.columns:
                X[col] = 0

        X = X[self.feature_columns]

        return self.model.predict_proba(X)[:, 1]
