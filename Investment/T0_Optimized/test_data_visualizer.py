#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
T0数据可视化工具测试脚本
验证数据库读取功能
"""

import sys
import os
from pathlib import Path

# 添加项目根目录到路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from core.data_manager import DataManager
from core.db_manager import DBManager
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def test_data_access():
    """测试数据访问"""
    
    # 测试配置
    test_stocks = ['600030', '000333', '002415']
    test_date = '2025-10-24'
    
    logger.info("="*60)
    logger.info("开始测试数据访问")
    logger.info("="*60)
    
    for stock_code in test_stocks:
        logger.info(f"\n测试股票: {stock_code}")
        
        # 测试DBManager
        try:
            logger.info("  → 尝试使用DBManager...")
            db_mgr = DBManager()
            df = db_mgr.get_minute_data(stock_code, test_date)
            db_mgr.close_all()
            
            if df is not None and not df.empty:
                logger.info(f"  ✅ DBManager成功: {len(df)} 条数据")
                logger.info(f"     数据列: {', '.join(df.columns.tolist())}")
                logger.info(f"     时间范围: {df['时间'].min()} ~ {df['时间'].max()}")
            else:
                logger.warning("  ⚠️ DBManager返回空数据")
        except Exception as e:
            logger.error(f"  ❌ DBManager失败: {e}")
        
        # 测试DataManager
        try:
            logger.info("  → 尝试使用DataManager...")
            dm = DataManager()
            df = dm.get_minute_data(stock_code, test_date)
            dm.close()
            
            if df is not None and not df.empty:
                logger.info(f"  ✅ DataManager成功: {len(df)} 条数据")
                logger.info(f"     数据列: {', '.join(df.columns.tolist())}")
                logger.info(f"     时间范围: {df['时间'].min()} ~ {df['时间'].max()}")
            else:
                logger.warning("  ⚠️ DataManager返回空数据")
        except Exception as e:
            logger.error(f"  ❌ DataManager失败: {e}")
    
    logger.info("\n" + "="*60)
    logger.info("测试完成")
    logger.info("="*60)

def test_cache_access():
    """测试缓存文件访问"""
    
    cache_dir = project_root / 'cache' / 'fenshi_data'
    logger.info(f"\n缓存目录: {cache_dir}")
    logger.info(f"缓存目录存在: {cache_dir.exists()}")
    
    if cache_dir.exists():
        csv_files = list(cache_dir.glob('*.csv'))
        logger.info(f"缓存文件数量: {len(csv_files)}")
        
        for csv_file in csv_files:
            logger.info(f"  - {csv_file.name} ({csv_file.stat().st_size / 1024:.2f} KB)")
    else:
        logger.warning("缓存目录不存在")

if __name__ == "__main__":
    logger.info("T0数据可视化工具 - 数据访问测试")
    logger.info("")
    
    # 测试缓存访问
    test_cache_access()
    
    # 测试数据库访问
    test_data_access()
    
    logger.info("\n测试完成！您现在可以运行 t0_data_visualizer.py 启动主程序")
