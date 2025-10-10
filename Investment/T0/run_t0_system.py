#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
T0交易系统实际运行脚本

这个脚本将启动T0交易系统的实时监控模式，
在交易时间内持续监控股票并生成交易信号。
"""

import sys
import os
from datetime import datetime

# 添加项目根目录到路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.settings import DEFAULT_STOCK_POOL
from monitor.T0_main import T0Monitor
from utils.logger import setup_logger

# 设置日志
logger = setup_logger('run_t0_system')

def main():
    """主函数"""
    print("=" * 50)
    print("T0交易系统 - 实际运行模式")
    print("=" * 50)
    print(f"启动时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # 获取股票池
    stock_pool = sys.argv[1:] if len(sys.argv) > 1 else None
    if not stock_pool:
        stock_pool = DEFAULT_STOCK_POOL
        print(f"使用默认股票池: {stock_pool}")
    else:
        print(f"使用指定股票池: {stock_pool}")
    
    logger.info("启动T0交易系统实际运行模式")
    logger.info(f"股票池: {stock_pool}")
    
    try:
        # 创建并运行监控器
        monitor = T0Monitor(stock_pool)
        
        print("\n正在启动监控系统...")
        print("系统将在交易时间内自动运行")
        print("交易时间: 09:30-11:30, 13:00-15:00")
        print("按 Ctrl+C 可以停止系统运行\n")
        
        # 运行监控系统
        monitor.run()
        
    except KeyboardInterrupt:
        print("\n\n系统被用户中断")
        logger.info("系统被用户中断")
    except Exception as e:
        print(f"\n系统运行出错: {e}")
        logger.error(f"系统运行出错: {e}")
    finally:
        print("\nT0交易系统已停止运行")
        logger.info("T0交易系统已停止运行")

if __name__ == "__main__":
    main()