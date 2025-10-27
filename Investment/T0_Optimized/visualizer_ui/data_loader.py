#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
数据加载模块 - 负责从数据库和缓存加载数据
"""

import os
import sys
import pandas as pd
import numpy as np
import logging
from pathlib import Path
from datetime import datetime, timedelta

# 添加项目根目录到路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

logger = logging.getLogger(__name__)

# 导入数据库管理器
try:
    from core.data_manager import DataManager
    from core.db_manager import DBManager
    USE_DATABASE = True
    logger.info("✅ 成功导入数据库管理器")
except ImportError as e:
    logger.warning(f"⚠️ 无法导入数据库管理器: {e}")
    USE_DATABASE = False

from .config import STOCKS, CACHE_DIR


class DataLoader:
    """数据加载器"""
    
    def __init__(self):
        self.data_cache = {}
    
    def load_from_cache(self, stock_code, date):
        """从缓存加载数据"""
        try:
            cache_file = os.path.join(CACHE_DIR, f"{stock_code}_{date.replace('-', '')}_fenshi.csv")
            logger.info(f"尝试从缓存加载：{cache_file}")

            if os.path.exists(cache_file):
                df = pd.read_csv(cache_file)
                if '时间' in df.columns:
                    df['时间'] = pd.to_datetime(df['时间'])
                logger.info(f"成功从缓存加载 {len(df)} 条数据")
                return df

            logger.info(f"缓存文件不存在：{cache_file}")
            return None

        except Exception as e:
            logger.error(f"从缓存加载数据失败: {e}")
            return None

    def save_to_cache(self, stock_code, date, df):
        """保存数据到缓存"""
        try:
            cache_file = os.path.join(CACHE_DIR, f"{stock_code}_{date.replace('-', '')}_fenshi.csv")
            df.to_csv(cache_file, index=False, encoding='utf-8-sig')
            logger.info(f"数据已保存到缓存：{cache_file}")

        except Exception as e:
            logger.error(f"保存数据到缓存失败: {e}")

    def load_stock_data(self, stock_code, date):
        """加载指定股票的数据 - 优先数据库，缺失则从接口获取"""
        try:
            logger.info(f"正在加载股票 {STOCKS[stock_code]} 的分时数据，日期：{date}")

            df = None
            
            # 第一步：尝试从数据库获取数据
            if USE_DATABASE:
                try:
                    # 优先使用DBManager（分层数据库）
                    try:
                        db_mgr = DBManager()
                        df = db_mgr.get_minute_data(stock_code, date)
                        db_mgr.close_all()
                        
                        if df is not None and not df.empty:
                            logger.info(f"✅ 使用DBManager成功读取 {len(df)} 条数据")
                    except Exception as e:
                        logger.warning(f"⚠️ DBManager读取失败: {e}，尝试DataManager")
                        
                        # 回退到DataManager
                        dm = DataManager()
                        df = dm.get_minute_data(stock_code, date)
                        dm.close()
                        
                        if df is not None and not df.empty:
                            logger.info(f"✅ 使用DataManager成功读取 {len(df)} 条数据")
                    
                    # 验证数据类型
                    if df is not None and not isinstance(df, pd.DataFrame):
                        logger.error(f"数据库返回的数据类型错误: {type(df).__name__}")
                        df = None
                    
                    if df is not None and not df.empty:
                        logger.info(f"成功从数据库获取到数据，形状：{df.shape}")
                        logger.info(f"数据列：{df.columns.tolist()}")
                    
                except Exception as e:
                    logger.error(f"从数据库获取数据失败: {e}")
                    df = None
            
            # 第二步：如果数据库没有数据，从接口获取
            if df is None or df.empty:
                logger.info(f"数据库中没有{date}的数据，尝试从接口获取...")
                df = self._fetch_from_api_and_save(stock_code, date)

            # 数据预处理
            df = self.preprocess_data(df, stock_code, date)
            
            # 保存到缓存
            self.save_to_cache(stock_code, date, df)
            
            # 更新缓存
            self.data_cache[stock_code] = df

            logger.info(f"成功加载股票 {STOCKS[stock_code]} 的分时数据，共 {len(df)} 条记录")
            
            return df

        except Exception as e:
            logger.error(f"加载股票 {STOCKS[stock_code]} 数据失败: {e}")
            raise
    
    def _fetch_from_api_and_save(self, stock_code, date):
        """从接口获取数据并保存到数据库"""
        try:
            logger.info(f"开始从接口获取 {stock_code} {date} 的分时数据...")
            
            # 尝试导入数据获取模块
            try:
                sys.path.insert(0, str(Path(__file__).parent.parent.parent / 'T0'))
                from data2dfcf import get_eastmoney_fenshi_by_date
                
                # 获取数据 - 使用现有的get_eastmoney_fenshi_by_date函数
                df = get_eastmoney_fenshi_by_date(stock_code, date)
                
                if df is None or df.empty:
                    raise ValueError(f"接口返回空数据")
                
                logger.info(f"✅ 成功从接口获取 {len(df)} 条数据")
                
                # 保存到数据库
                if USE_DATABASE:
                    try:
                        db_mgr = DBManager()
                        db_mgr.save_minute_data(stock_code, date, df)
                        db_mgr.close_all()
                        logger.info(f"✅ 数据已保存到数据库")
                    except Exception as e:
                        logger.warning(f"⚠️ 保存到数据库失败: {e}")
                
                return df
                
            except ImportError as e:
                logger.error(f"无法导入data2dfcf模块: {e}")
                raise ValueError("接口模块不可用，请检查data2dfcf.py文件是否存在且包含get_eastmoney_fenshi_by_date函数")
                
        except Exception as e:
            logger.error(f"从接口获取数据失败: {e}")
            # 不再使用模拟数据，而是抛出异常
            raise ValueError(f"无法获取真实数据: {str(e)}")
            # 移除模拟数据生成逻辑，确保只使用真实数据

    def preprocess_data(self, df, stock_code, date):
        """数据预处理"""
        # 确保有时间列
        if '时间' not in df.columns:
            logger.warning("数据中缺少'时间'列，创建模拟时间")
            base_time = datetime.strptime(f"{date} 09:30:00", "%Y-%m-%d %H:%M:%S")
            times = [base_time + timedelta(minutes=i) for i in range(len(df))]
            df['时间'] = times
        else:
            # 确保时间列是datetime类型
            if not pd.api.types.is_datetime64_any_dtype(df['时间']):
                df['时间'] = pd.to_datetime(df['时间'])

        # 确保数据按时间排序
        df = df.sort_values('时间')
        
        # 过滤掉11:30-13:00之间的时间段数据
        if '时间' in df.columns:
            def is_trading_hour(timestamp):
                hour = timestamp.hour
                minute = timestamp.minute
                morning_trading = (hour == 9 and minute >= 30) or (hour == 10) or (hour == 11 and minute <= 30)
                afternoon_trading = (hour == 13) or (hour == 14) or (hour == 15 and minute == 0)
                return morning_trading or afternoon_trading
            
            df = df[df['时间'].apply(is_trading_hour)]
            logger.info(f"过滤后数据行数: {len(df)}")

        # 确保有价格相关列
        if '收盘' not in df.columns and '开盘' in df.columns:
            df['收盘'] = df['开盘']

        # 计算涨跌幅
        if '收盘' in df.columns and '开盘' in df.columns:
            open_price = df['开盘'].iloc[0]
            df['涨跌幅'] = (df['收盘'] / open_price - 1) * 100
        
        return df

    # 移除generate_mock_data方法，不再使用模拟数据
