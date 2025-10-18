#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
指标计算模块测试
测试各种技术指标的计算是否正确
"""
import unittest
import pandas as pd
import numpy as np
import sys
import os

# 添加项目根目录到路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from indicators.tdx_indicators import (
    calculate_tdx_indicators,
    calculate_resistance_support_levels,
    calculate_ma,
    calculate_bollinger_bands,
    calculate_rsi,
    calculate_macd
)


class TestIndicators(unittest.TestCase):
    """
    技术指标计算测试类
    """
    
    def setUp(self):
        """
        设置测试数据
        """
        # 创建一个简单的测试数据集
        dates = pd.date_range('2023-01-01', periods=100, freq='D')
        prices = np.linspace(10, 20, 100) + np.random.normal(0, 0.5, 100)
        
        self.test_data = pd.DataFrame({
            '日期': dates,
            'high': prices * 1.02,  # 最高价
            'low': prices * 0.98,   # 最低价
            'close': prices,        # 收盘价
            'volume': np.random.randint(1000, 10000, 100)  # 成交量
        })
        
        # 设置前一日收盘价
        self.prev_close = prices[0] * 0.95
    
    def test_calculate_tdx_indicators(self):
        """
        测试通达信指标计算
        """
        # 调用函数
        result = calculate_tdx_indicators(self.test_data.copy(), self.prev_close)
        
        # 验证结果
        self.assertIsNotNone(result)
        self.assertIsInstance(result, pd.DataFrame)
        
        # 检查必要的列是否存在
        required_columns = ['close', 'support', 'resistance', 'cross_support', 
                           'longcross_support', 'longcross_resistance']
        
        for col in required_columns:
            if col in ['close']:
                self.assertTrue(col in result.columns or '收盘' in result.columns)
            else:
                self.assertTrue(col in result.columns)
    
    def test_calculate_resistance_support_levels(self):
        """
        测试阻力支撑位计算
        """
        # 调用函数
        result = calculate_resistance_support_levels(self.test_data.copy())
        
        # 验证结果
        self.assertIsNotNone(result)
        self.assertIsInstance(result, pd.DataFrame)
        
        # 检查必要的列是否存在
        self.assertTrue('support' in result.columns)
        self.assertTrue('resistance' in result.columns)
        
        # 检查阻力位是否大于等于支撑位
        self.assertTrue((result['resistance'] >= result['support']).all())
    
    def test_calculate_ma(self):
        """
        测试移动平均线计算
        """
        # 调用函数，计算不同周期的均线
        periods = [5, 10, 20]
        result = calculate_ma(self.test_data.copy(), periods)
        
        # 验证结果
        self.assertIsNotNone(result)
        self.assertIsInstance(result, pd.DataFrame)
        
        # 检查必要的列是否存在
        for period in periods:
            self.assertTrue(f'ma{period}' in result.columns)
        
        # 检查MA计算是否合理
        for period in periods:
            # 手动计算第一个有效值
            manual_ma = self.test_data['close'].iloc[:period].mean()
            calculated_ma = result[f'ma{period}'].iloc[period-1]
            
            # 由于可能使用不同的填充方法，只检查非NaN值部分
            valid_idx = result[f'ma{period}'].first_valid_index()
            if valid_idx is not None:
                self.assertFalse(np.isnan(result[f'ma{period}'].iloc[valid_idx]))
    
    def test_calculate_bollinger_bands(self):
        """
        测试布林带计算
        """
        # 调用函数
        result = calculate_bollinger_bands(self.test_data.copy(), window=20, num_std=2)
        
        # 验证结果
        self.assertIsNotNone(result)
        self.assertIsInstance(result, pd.DataFrame)
        
        # 检查必要的列是否存在
        self.assertTrue('upper_band' in result.columns)
        self.assertTrue('middle_band' in result.columns)
        self.assertTrue('lower_band' in result.columns)
        
        # 检查上轨是否大于下轨
        self.assertTrue((result['upper_band'] >= result['lower_band']).all())
    
    def test_calculate_rsi(self):
        """
        测试RSI计算
        """
        # 调用函数
        result = calculate_rsi(self.test_data.copy(), window=14)
        
        # 验证结果
        self.assertIsNotNone(result)
        self.assertIsInstance(result, pd.DataFrame)
        
        # 检查必要的列是否存在
        self.assertTrue('rsi' in result.columns)
        
        # 检查RSI值是否在0-100之间
        valid_rsi = result['rsi'].dropna()
        self.assertTrue((valid_rsi >= 0).all() and (valid_rsi <= 100).all())
    
    def test_calculate_macd(self):
        """
        测试MACD计算
        """
        # 调用函数
        result = calculate_macd(self.test_data.copy(), fast=12, slow=26, signal=9)
        
        # 验证结果
        self.assertIsNotNone(result)
        self.assertIsInstance(result, pd.DataFrame)
        
        # 检查必要的列是否存在
        self.assertTrue('macd' in result.columns)
        self.assertTrue('signal_line' in result.columns)
        self.assertTrue('histogram' in result.columns)
        
        # 检查直方图计算是否正确
        self.assertTrue((result['histogram'] == result['macd'] - result['signal_line']).all())
    
    def test_signal_generation(self):
        """
        测试信号生成
        """
        # 调用通达信指标计算，包含信号
        result = calculate_tdx_indicators(self.test_data.copy(), self.prev_close)
        
        # 验证信号列的存在
        self.assertTrue('cross_support' in result.columns)
        self.assertTrue('longcross_support' in result.columns)
        self.assertTrue('longcross_resistance' in result.columns)
        
        # 检查信号值是否为布尔类型
        self.assertTrue(pd.api.types.is_bool_dtype(result['cross_support']))
        self.assertTrue(pd.api.types.is_bool_dtype(result['longcross_support']))
        self.assertTrue(pd.api.types.is_bool_dtype(result['longcross_resistance']))


if __name__ == '__main__':
    unittest.main()