# -*- coding: utf-8 -*-
import logging
import sys

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', 
                    handlers=[
                        logging.FileHandler("debug.log", encoding="utf-8"),
                        logging.StreamHandler(sys.stdout)
                    ])
logger = logging.getLogger(__name__)

logger.info("开始测试...")

# 测试导入
logger.info("导入模块...")
import urllib.request
import pandas as pd
import json
import random
import time
import gzip
import io
from urllib.error import URLError, HTTPError
from datetime import datetime, timedelta

logger.info("导入完成")

# 定义模拟的获取分时数据函数
def get_fenshi_data(stock_code, date=None):
    """从缓存或生成模拟数据获取分时数据"""
    import os
    import pandas as pd
    import numpy as np
    
    if date is None:
        from datetime import datetime
        date = datetime.now().strftime('%Y%m%d')
    
    # 尝试从缓存获取数据
    project_root = os.path.dirname(os.path.abspath(__file__))
    cache_dir = os.path.join(project_root, 'cache', 'fenshi_data')
    cache_file = os.path.join(cache_dir, f'{stock_code}_{date}_fenshi.csv')
    
    if os.path.exists(cache_file):
        df = pd.read_csv(cache_file)
        logger.info(f"从缓存文件 {cache_file} 读取股票分时数据")
        return df
    
    # 生成模拟数据
    logger.info(f"未找到缓存数据，生成模拟分时数据 for {stock_code} {date}")
    
    # 创建时间序列（模拟交易日的分时数据）
    times = []
    for hour in [9, 10, 11, 13, 14]:
        start_min = 30 if hour == 9 else 0
        end_min = 31 if hour == 11 else 60
        for minute in range(start_min, end_min):
            if (hour == 11 and minute > 30) or (hour > 14):
                break
            times.append(f"{hour:02d}:{minute:02d}:00")
    
    # 生成模拟价格数据
    base_price = np.random.uniform(10, 100)
    price_changes = np.random.normal(0, 0.01, len(times))
    prices = base_price * np.exp(np.cumsum(price_changes))
    
    # 创建DataFrame
    df = pd.DataFrame({
        '时间': times,
        '开盘': prices,
        '最高': prices * (1 + np.random.uniform(0, 0.02, len(times))),
        '最低': prices * (1 - np.random.uniform(0, 0.02, len(times))),
        '收盘': prices,
        '成交量': np.random.randint(1000, 100000, len(times))
    })
    
    return df

logger.info("开始调用函数...")
df = get_fenshi_data(stock_code="600030")
logger.info(f"函数调用完成，DataFrame形状: {df.shape}")