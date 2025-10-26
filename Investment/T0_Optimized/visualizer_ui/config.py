#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
配置模块 - 存储全局配置和常量
"""

import os
import matplotlib.pyplot as plt

# 股票配置
STOCKS = {
    '600030': '中信证券',
    '000333': '美的集团',
    '002415': '海康威视'
}

# 缓存目录
CACHE_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'cache', 'fenshi_data')

# 创建缓存目录
os.makedirs(CACHE_DIR, exist_ok=True)

# 配置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei', 'Arial Unicode MS', 'Microsoft YaHei']
plt.rcParams['axes.unicode_minus'] = False

# 窗口配置
WINDOW_TITLE = "T0交易系统 - 分时数据可视化"
WINDOW_GEOMETRY = "1200x800"
WINDOW_MIN_SIZE = (1000, 600)

# 图表配置
MAIN_CHART_SIZE = (12, 4)  # 主分时图尺寸
INDICATOR_CHART_SIZE = (8, 5)  # 指标图尺寸（缩小）
DPI = 100

# 播放配置
DEFAULT_PLAY_SPEED = 1.0
MIN_PLAY_SPEED = 0.1
MAX_PLAY_SPEED = 3.0
