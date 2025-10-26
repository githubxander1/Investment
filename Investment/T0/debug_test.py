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

# 测试函数调用
from data2dfcf import get_eastmoney_fenshi_by_date

logger.info("开始调用函数...")
df = get_eastmoney_fenshi_by_date(stock_code="600030")
logger.info(f"函数调用完成，DataFrame形状: {df.shape}")