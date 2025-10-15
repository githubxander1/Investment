#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
通用工具模块
提供各种辅助函数
"""

import os
import re
import time
import pandas as pd
from typing import Optional, List, Dict, Any, Tuple
import datetime
from Investment.THS.ths_trade.utils.logger import setup_logger

logger = setup_logger('utils.log')


def ensure_directory(directory: str) -> None:
    """
    确保目录存在，如果不存在则创建
    
    Args:
        directory: 目录路径
    """
    if not os.path.exists(directory):
        os.makedirs(directory)
        logger.info(f"创建目录: {directory}")


def is_trading_time() -> bool:
    """
    判断当前是否为交易时间
    
    Returns:
        bool: 是否为交易时间
    """
    now = datetime.datetime.now()
    
    # 检查是否为周末
    if now.weekday() >= 5:
        return False
    
    # 检查是否为交易时段
    morning_start = now.replace(hour=9, minute=30, second=0, microsecond=0)
    morning_end = now.replace(hour=11, minute=30, second=0, microsecond=0)
    afternoon_start = now.replace(hour=13, minute=0, second=0, microsecond=0)
    afternoon_end = now.replace(hour=15, minute=0, second=0, microsecond=0)
    
    return (morning_start <= now <= morning_end) or (afternoon_start <= now <= afternoon_end)


def format_stock_code(stock_code: str) -> str:
    """
    格式化股票代码，去除前缀和后缀
    
    Args:
        stock_code: 股票代码
        
    Returns:
        str: 格式化后的股票代码
    """
    # 移除非数字字符，只保留数字
    cleaned_code = re.sub(r'[^0-9]', '', stock_code)
    
    # 确保代码长度为6位
    if len(cleaned_code) != 6:
        logger.warning(f"股票代码格式不正确: {stock_code}")
    
    return cleaned_code


def get_stock_market(stock_code: str) -> str:
    """
    根据股票代码判断市场类型
    
    Args:
        stock_code: 股票代码
        
    Returns:
        str: 市场类型 ('sh' 或 'sz')
    """
    stock_code = format_stock_code(stock_code)
    
    # 上证股票: 60开头
    if stock_code.startswith('6'):
        return 'sh'
    # 深证股票: 00, 30开头
    elif stock_code.startswith('0') or stock_code.startswith('3'):
        return 'sz'
    else:
        logger.warning(f"无法判断股票市场: {stock_code}")
        return 'sh'  # 默认返回上证


def get_full_stock_code(stock_code: str) -> str:
    """
    获取带市场前缀的完整股票代码
    
    Args:
        stock_code: 股票代码
        
    Returns:
        str: 完整股票代码，如 'sh600000'
    """
    stock_code = format_stock_code(stock_code)
    market = get_stock_market(stock_code)
    return f"{market}{stock_code}"


def calculate_trade_amount(price: float, volume: int, fee_rate: float = 0.0003) -> Dict[str, float]:
    """
    计算交易金额和手续费
    
    Args:
        price: 价格
        volume: 数量
        fee_rate: 手续费率
        
    Returns:
        Dict: 包含总金额、手续费等信息的字典
    """
    total_amount = price * volume
    commission = max(total_amount * fee_rate, 5.0)  # 最低5元
    
    return {
        'total_amount': total_amount,
        'commission': commission,
        'actual_amount': total_amount + commission
    }


def load_stock_name_map(file_path: str = 'data/all_stocks.xlsx') -> Dict[str, str]:
    """
    加载股票代码和名称的映射
    
    Args:
        file_path: Excel文件路径
        
    Returns:
        Dict: 股票代码到名称的映射
    """
    stock_map = {}
    
    try:
        if os.path.exists(file_path):
            df = pd.read_excel(file_path)
            if '代码' in df.columns and '名称' in df.columns:
                stock_map = dict(zip(df['代码'].astype(str), df['名称']))
                logger.info(f"成功加载股票映射，共 {len(stock_map)} 条记录")
            else:
                logger.error(f"Excel文件缺少必要列: {file_path}")
        else:
            logger.warning(f"股票映射文件不存在: {file_path}")
    except Exception as e:
        logger.error(f"加载股票映射失败: {e}")
    
    return stock_map


def retry(func, max_retries: int = 3, delay: float = 1.0, *args, **kwargs):
    """
    重试装饰器
    
    Args:
        func: 要重试的函数
        max_retries: 最大重试次数
        delay: 重试间隔（秒）
        *args: 函数参数
        **kwargs: 函数关键字参数
        
    Returns:
        函数返回值
    """
    def wrapper(*args, **kwargs):
        last_exception = None
        
        for attempt in range(max_retries):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                last_exception = e
                logger.warning(f"尝试 {attempt + 1}/{max_retries} 失败: {e}")
                if attempt < max_retries - 1:
                    time.sleep(delay)
        
        logger.error(f"达到最大重试次数，执行失败")
        raise last_exception
    
    return wrapper