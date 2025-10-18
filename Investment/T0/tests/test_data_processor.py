#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
数据处理模块测试
测试数据获取和处理功能是否正确
"""
import unittest
import pandas as pd
import numpy as np
from unittest.mock import patch, MagicMock
import sys
import os

# 添加项目根目录到路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from data.data_processor import (
    validate_data,
    preprocess_data,
    get_previous_close,
    calculate_technical_indicators,
    clean_data
)
from data.data_fetcher import (
    get_stock_intraday_data,
    get_stock_daily_data,
    is_market_open
)


class TestDataProcessor(unittest.TestCase):
    """
    数据处理测试类
    """
    
    def setUp(self):
        """
        设置测试数据
        """
        # 创建测试数据
        self.valid_data = pd.DataFrame({
            'time': pd.date_range('2023-01-01 09:30:00', periods=100, freq='5min'),
            'open': np.linspace(10, 11, 100),
            'high': np.linspace(10.1, 11.1, 100),
            'low': np.linspace(9.9, 10.9, 100),
            'close': np.linspace(10, 11, 100),
            'volume': np.random.randint(1000, 10000, 100)
        })
        
        # 创建无效数据（缺少必要列）
        self.invalid_data1 = pd.DataFrame({
            'time': pd.date_range('2023-01-01 09:30:00', periods=100, freq='5min'),
            'open': np.linspace(10, 11, 100),
            # 缺少high, low, close
            'volume': np.random.randint(1000, 10000, 100)
        })
        
        # 创建无效数据（空数据）
        self.invalid_data2 = pd.DataFrame()
        
        # 创建包含NaN的数据
        self.data_with_nan = self.valid_data.copy()
        self.data_with_nan.loc[10:20, 'close'] = np.nan
    
    def test_validate_data(self):
        """
        测试数据验证功能
        """
        # 测试有效数据
        self.assertTrue(validate_data(self.valid_data))
        
        # 测试无效数据（缺少必要列）
        self.assertFalse(validate_data(self.invalid_data1))
        
        # 测试无效数据（空数据）
        self.assertFalse(validate_data(self.invalid_data2))
    
    def test_preprocess_data(self):
        """
        测试数据预处理功能
        """
        # 预处理有效数据
        result = preprocess_data(self.valid_data.copy())
        
        # 验证结果
        self.assertIsNotNone(result)
        self.assertIsInstance(result, pd.DataFrame)
        
        # 检查是否没有NaN值
        self.assertFalse(result.isnull().values.any())
        
        # 检查索引是否为时间类型
        self.assertTrue(pd.api.types.is_datetime64_any_dtype(result.index))
        
        # 预处理包含NaN的数据
        result_with_nan = preprocess_data(self.data_with_nan.copy())
        
        # 验证NaN被处理
        self.assertFalse(result_with_nan.isnull().values.any())
    
    @patch('akshare.stock_zh_a_daily')
    def test_get_previous_close(self, mock_stock_zh_a_daily):
        """
        测试获取前一日收盘价功能
        """
        # 设置模拟返回值
        mock_data = pd.DataFrame({
            'date': ['2023-01-01', '2023-01-02', '2023-01-03'],
            'close': [10.0, 10.5, 11.0]
        })
        mock_stock_zh_a_daily.return_value = mock_data
        
        # 调用函数
        prev_close = get_previous_close('000001', '2023-01-04')
        
        # 验证结果
        self.assertEqual(prev_close, 11.0)
        
        # 验证函数调用
        mock_stock_zh_a_daily.assert_called_once()
    
    def test_clean_data(self):
        """
        测试数据清理功能
        """
        # 清理包含NaN的数据
        result = clean_data(self.data_with_nan.copy())
        
        # 验证结果
        self.assertIsNotNone(result)
        self.assertIsInstance(result, pd.DataFrame)
        
        # 检查是否没有NaN值
        self.assertFalse(result.isnull().values.any())
    
    def test_calculate_technical_indicators(self):
        """
        测试技术指标计算功能
        """
        # 调用函数
        result = calculate_technical_indicators(self.valid_data.copy())
        
        # 验证结果
        self.assertIsNotNone(result)
        self.assertIsInstance(result, pd.DataFrame)
    
    @patch('data.data_fetcher.ak.stock_zh_a_minute')
    def test_get_stock_intraday_data(self, mock_stock_zh_a_minute):
        """
        测试获取股票分时数据功能
        """
        # 设置模拟返回值
        mock_data = pd.DataFrame({
            '时间': pd.date_range('2023-01-01 09:30:00', periods=100, freq='5min'),
            '开盘': np.linspace(10, 11, 100),
            '最高': np.linspace(10.1, 11.1, 100),
            '最低': np.linspace(9.9, 10.9, 100),
            '收盘': np.linspace(10, 11, 100),
            '成交量': np.random.randint(1000, 10000, 100)
        })
        mock_stock_zh_a_minute.return_value = mock_data
        
        # 调用函数
        data = get_stock_intraday_data('000001')
        
        # 验证结果
        self.assertIsNotNone(data)
        self.assertIsInstance(data, pd.DataFrame)
        
        # 验证函数调用
        mock_stock_zh_a_minute.assert_called_once()
    
    def test_is_market_open(self):
        """
        测试市场是否开盘功能
        """
        # 这里可以添加更多的测试用例，测试不同时间点
        # 由于这个函数依赖当前时间，我们可以使用patch来模拟时间
        pass


if __name__ == '__main__':
    unittest.main()