#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
股票分时数据提供类
专门用于获取和处理股票分时数据
"""

import pandas as pd
import akshare as ak
from datetime import datetime
import os
import sys
from typing import Optional

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

try:
    from Investment.T0.utils.logger import setup_logger
except ImportError:
    # 如果无法导入自定义logger，则使用标准logging
    import logging
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    setup_logger = lambda name: logging.getLogger(name)

logger = setup_logger('intraday_data_provider')


class IntradayDataProvider:
    """
    股票分时数据提供类
    专门用于获取和处理股票分时数据
    """

    def __init__(self):
        """初始化数据提供类"""
        pass

    def get_hist_min_em_data(self, stock_code: str, trade_date: str) -> Optional[pd.DataFrame]:
        """
        使用 stock_zh_a_hist_min_em 接口获取分时数据
        
        Args:
            stock_code: 股票代码
            trade_date: 交易日期
            
        Returns:
            分时数据DataFrame，包含以下列：
            - 时间: datetime格式的时间
            - 开盘: 开盘价
            - 收盘: 收盘价
            - 最高: 最高价
            - 最低: 最低价
            - 成交量: 成交量
            - 成交额: 成交额
            - 均价: 均价
        """
        try:
            logger.info(f"使用 stock_zh_a_hist_min_em 接口获取 {stock_code} 在 {trade_date} 的分时数据")
            
            # 构造时间范围
            start_time = f'{trade_date} 09:30:00'
            end_time = f'{trade_date} 15:00:00'
            
            # 获取数据
            df = ak.stock_zh_a_hist_min_em(
                symbol=stock_code,
                period="1",
                start_date=start_time,
                end_date=end_time,
                adjust=""
            )
            
            if df is not None and not df.empty:
                logger.info(f"✅ stock_zh_a_hist_min_em 成功获取数据，数据行数: {len(df)}")
                logger.debug(f"原始数据列名: {df.columns.tolist()}")
                
                # 重命名列以匹配统一格式
                df = df.rename(columns={
                    '时间': '时间',
                    '开盘': '开盘',
                    '收盘': '收盘',
                    '最高': '最高',
                    '最低': '最低',
                    '成交量': '成交量',
                    '成交额': '成交额',
                    '均价': '均价'
                })
                
                # 确保时间列是datetime格式
                df['时间'] = pd.to_datetime(df['时间'])
                
                # 数据清洗：处理NaN值
                numeric_columns = ['开盘', '收盘', '最高', '最低', '均价']
                for col in numeric_columns:
                    if col in df.columns:
                        df[col] = pd.to_numeric(df[col], errors='coerce')
                
                # 如果开盘价等数据为空，尝试用收盘价填充
                if '收盘' in df.columns:
                    df['开盘'] = df['开盘'].fillna(df['收盘'])
                    df['最高'] = df['最高'].fillna(df['收盘'])
                    df['最低'] = df['最低'].fillna(df['收盘'])
                    df['均价'] = df['均价'].fillna(df['收盘'])
                
                logger.debug(f"处理后数据列名: {df.columns.tolist()}")
                return df
            else:
                logger.warning(f"stock_zh_a_hist_min_em 接口未返回 {stock_code} 在 {trade_date} 的数据")
                return None
                
        except Exception as e:
            logger.error(f"使用 stock_zh_a_hist_min_em 接口获取数据失败: {e}")
            return None

    def get_a_minute_data(self, stock_code: str) -> Optional[pd.DataFrame]:
        """
        使用 stock_zh_a_minute 接口获取分时数据
        
        Args:
            stock_code: 股票代码
            
        Returns:
            分时数据DataFrame，包含以下列：
            - 时间: datetime格式的时间 (对应原始的 'day')
            - 开盘: 开盘价 (对应原始的 'open')
            - 收盘: 收盘价 (对应原始的 'close')
            - 最高: 最高价 (对应原始的 'high')
            - 最低: 最低价 (对应原始的 'low')
            - 成交量: 成交量 (对应原始的 'volume')
            注意：此接口不提供成交额和均价
        """
        try:
            logger.info(f"使用 stock_zh_a_minute 接口获取 {stock_code} 的分时数据")
            
            # 根据股票代码前缀判断市场
            if stock_code.startswith('6'):
                market_stock_code = f'sh{stock_code}'
            else:
                market_stock_code = f'sz{stock_code}'
            
            # 获取数据
            df = ak.stock_zh_a_minute(symbol=market_stock_code, period="1", adjust="qfq")
            
            if df is not None and not df.empty:
                logger.info(f"✅ stock_zh_a_minute 成功获取数据，数据行数: {len(df)}")
                logger.debug(f"原始数据列名: {df.columns.tolist()}")
                
                # 重命名列以匹配统一格式
                df = df.rename(columns={
                    'day': '时间',
                    'open': '开盘',
                    'high': '最高',
                    'low': '最低',
                    'close': '收盘',
                    'volume': '成交量'
                })
                
                # 确保时间列是datetime格式
                df['时间'] = pd.to_datetime(df['时间'])
                
                # 数据清洗：确保数值列是数值类型
                numeric_columns = ['开盘', '最高', '最低', '收盘']
                for col in numeric_columns:
                    if col in df.columns:
                        df[col] = pd.to_numeric(df[col], errors='coerce')
                
                # 添加缺失的列（成交额和均价）
                df['成交额'] = 0.0
                df['均价'] = df['收盘']  # 使用收盘价作为均价的近似值
                
                # 如果开盘价等数据为空，尝试用收盘价填充
                if '收盘' in df.columns:
                    df['开盘'] = df['开盘'].fillna(df['收盘'])
                    df['最高'] = df['最高'].fillna(df['收盘'])
                    df['最低'] = df['最低'].fillna(df['收盘'])
                
                logger.debug(f"处理后数据列名: {df.columns.tolist()}")
                return df
            else:
                logger.warning(f"stock_zh_a_minute 接口未返回 {stock_code} 的数据")
                return None
                
        except Exception as e:
            logger.error(f"使用 stock_zh_a_minute 接口获取数据失败: {e}")
            return None

    def get_eastmoney_data(self, stock_code: str) -> Optional[pd.DataFrame]:
        """
        使用东方财富接口获取分时数据
        
        Args:
            stock_code: 股票代码
            
        Returns:
            分时数据DataFrame，包含以下列：
            - 时间: datetime格式的时间
            - 开盘: 开盘价
            - 收盘: 收盘价
            - 最高: 最高价
            - 最低: 最低价
            - 成交量: 成交量
            - 成交额: 成交额
            - 均价: 均价
        """
        try:
            logger.info(f"使用东方财富接口获取 {stock_code} 的分时数据")
            
            # 导入东方财富数据获取函数
            sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
            from data_source.data2dfcf import get_eastmoney_fenshi_with_pandas
            
            # 根据股票代码前缀判断市场
            if stock_code.startswith('6'):
                secid = f"1.{stock_code}"  # 沪市
            else:
                secid = f"0.{stock_code}"  # 深市
            
            # 获取数据
            df = get_eastmoney_fenshi_with_pandas(secid=secid)
            
            if df is not None and not df.empty:
                logger.info(f"✅ 东方财富接口成功获取数据，数据行数: {len(df)}")
                logger.debug(f"数据列名: {df.columns.tolist()}")
                return df
            else:
                logger.warning(f"东方财富接口未返回 {stock_code} 的数据")
                return None
                
        except Exception as e:
            logger.error(f"使用东方财富接口获取数据失败: {e}")
            import traceback
            logger.error(f"详细错误信息: {traceback.format_exc()}")
            return None

    def get_intraday_data(self, stock_code: str, trade_date: str) -> Optional[pd.DataFrame]:
        """
        获取分时数据的统一接口
        
        Args:
            stock_code: 股票代码
            trade_date: 交易日期
            
        Returns:
            分时数据DataFrame，包含统一格式的列：
            - 时间: datetime格式的时间
            - 开盘: 开盘价
            - 收盘: 收盘价
            - 最高: 最高价
            - 最低: 最低价
            - 成交量: 成交量
            - 成交额: 成交额
            - 均价: 均价
        """
        logger.info("=" * 60)
        logger.info("开始加载分时数据")
        logger.info(f"股票代码: {stock_code}")
        logger.info(f"交易日期: {trade_date}")
        
        # 首先尝试使用 stock_zh_a_hist_min_em 接口
        df = self.get_hist_min_em_data(stock_code, trade_date)
        if df is not None and not df.empty:
            logger.info("使用 stock_zh_a_hist_min_em 接口获取数据成功")
            logger.info(f"数据列: {', '.join(df.columns.tolist())}")
            logger.info(f"数据行数: {len(df)}")
            # 检查是否有有效数据
            if not df[['开盘', '收盘', '最高', '最低']].isnull().all().all():
                logger.info("=" * 60)
                return df
        
        # 如果失败，尝试使用 stock_zh_a_minute 接口
        df = self.get_a_minute_data(stock_code)
        if df is not None and not df.empty:
            logger.info("使用 stock_zh_a_minute 接口获取数据成功")
            logger.info(f"数据列: {', '.join(df.columns.tolist())}")
            logger.info(f"数据行数: {len(df)}")
            # 检查是否有有效数据
            if not df[['开盘', '收盘', '最高', '最低']].isnull().all().all():
                logger.info("=" * 60)
                return df
        
        # 如果还失败，尝试使用东方财富接口
        df = self.get_eastmoney_data(stock_code)
        if df is not None and not df.empty:
            logger.info("使用东方财富接口获取数据成功")
            logger.info(f"数据列: {', '.join(df.columns.tolist())}")
            logger.info(f"数据行数: {len(df)}")
            logger.info("=" * 60)
            return df
        
        # 如果都失败了
        logger.error("❌ 无法获取分时数据")
        logger.info("=" * 60)
        return None


# 保持原有的函数接口以确保向后兼容
def fetch_intraday_data(stock_code: str, trade_date: str) -> Optional[pd.DataFrame]:
    """
    向后兼容的函数接口
    
    Args:
        stock_code: 股票代码
        trade_date: 交易日期
        
    Returns:
        分时数据DataFrame
    """
    provider = IntradayDataProvider()
    return provider.get_intraday_data(stock_code, trade_date)