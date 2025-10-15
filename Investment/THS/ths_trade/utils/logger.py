#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
日志设置模块
提供统一的日志记录功能
"""

import logging
import os
from datetime import datetime
import sys


def setup_logger(log_name='app.log', level=logging.INFO):
    """
    设置日志记录器
    
    Args:
        log_name: 日志文件名
        level: 日志级别
        
    Returns:
        logger: 配置好的日志记录器实例
    """
    # 创建logs目录（如果不存在）
    log_dir = 'logs'
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    
    # 创建日志记录器
    logger = logging.getLogger(log_name)
    logger.setLevel(level)
    
    # 避免重复添加处理器
    if not logger.handlers:
        # 创建控制台处理器
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(level)
        
        # 创建文件处理器
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        log_filename = f"{log_dir}/{log_name.split('.')[0]}_{timestamp}.log"
        file_handler = logging.FileHandler(log_filename, encoding='utf-8')
        file_handler.setLevel(level)
        
        # 设置日志格式
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        console_handler.setFormatter(formatter)
        file_handler.setFormatter(formatter)
        
        # 添加处理器到记录器
        logger.addHandler(console_handler)
        logger.addHandler(file_handler)
    
    return logger


# 默认日志记录器
default_logger = setup_logger()