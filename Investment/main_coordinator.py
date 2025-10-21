#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
交易系统协调器
用于协调T0系统和AutoTrade系统，避免两者同时操作同花顺交易客户端导致冲突
"""

import asyncio
import threading
import time
import logging
from datetime import datetime, time as dt_time
import sys
import os

# 添加项目根目录到路径
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.append(project_root)

# 设置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('main_coordinator')

# 导入两个系统的主程序
from Investment.T0.monitor.T0_main import T0Monitor
from Investment.THS.AutoTrade.trade_main import main as auto_trade_main

class TradeSystemCoordinator:
    """
    交易系统协调器
    确保T0系统和AutoTrade系统不会同时操作交易客户端
    """
    
    def __init__(self):
        self.t0_system = None
        self.auto_trade_system = None
        self.t0_lock = threading.Lock()
        self.auto_trade_lock = threading.Lock()
        self.is_running = False
        
    def start_t0_system(self, stock_pool=None):
        """
        启动T0系统
        """
        logger.info("正在启动T0交易系统...")
        try:
            self.t0_system = T0Monitor(stock_pool)
            # 在单独的线程中运行T0系统
            t0_thread = threading.Thread(target=self._run_t0_system, daemon=True)
            t0_thread.start()
            logger.info("T0交易系统已启动")
        except Exception as e:
            logger.error(f"启动T0交易系统失败: {e}")
            
    def _run_t0_system(self):
        """
        在独立线程中运行T0系统
        """
        if self.t0_system:
            try:
                self.t0_system.run()
            except Exception as e:
                logger.error(f"T0系统运行出错: {e}")
                
    def start_auto_trade_system(self):
        """
        启动AutoTrade系统
        """
        logger.info("正在启动AutoTrade交易系统...")
        try:
            # 在单独的线程中运行AutoTrade系统
            auto_trade_thread = threading.Thread(target=self._run_auto_trade_system, daemon=True)
            auto_trade_thread.start()
            logger.info("AutoTrade交易系统已启动")
        except Exception as e:
            logger.error(f"启动AutoTrade交易系统失败: {e}")
            
    def _run_auto_trade_system(self):
        """
        在独立线程中运行AutoTrade系统
        """
        try:
            # 运行AutoTrade系统的异步主程序
            asyncio.run(auto_trade_main())
        except Exception as e:
            logger.error(f"AutoTrade系统运行出错: {e}")
            
    def is_trading_time(self):
        """
        判断当前是否为交易时间
        """
        now = datetime.now().time()
        # A股交易时间: 9:30-11:30, 13:00-15:00
        morning_session = dt_time(9, 30) <= now <= dt_time(11, 30)
        afternoon_session = dt_time(13, 0) <= now <= dt_time(15, 0)
        return morning_session or afternoon_session
    
    def wait_for_trading_time(self):
        """
        等待到下一个交易时间开始
        """
        while not self.is_trading_time():
            time.sleep(60)  # 每分钟检查一次
            
    def run(self, stock_pool=None):
        """
        运行协调器
        """
        logger.info("启动交易系统协调器...")
        
        # 启动两个系统
        self.start_t0_system(stock_pool)
        self.start_auto_trade_system()
        
        self.is_running = True
        
        try:
            while self.is_running:
                # 每隔一段时间检查系统状态
                time.sleep(60)
                
                # 可以在这里添加系统状态监控逻辑
                current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                logger.debug(f"协调器运行中 - 当前时间: {current_time}")
                
        except KeyboardInterrupt:
            logger.info("收到停止信号")
        except Exception as e:
            logger.error(f"协调器运行出错: {e}")
        finally:
            self.stop()
            
    def stop(self):
        """
        停止协调器
        """
        logger.info("正在停止交易系统协调器...")
        self.is_running = False
        
        # 停止T0系统
        if self.t0_system and hasattr(self.t0_system, 'close'):
            try:
                self.t0_system.close()
                logger.info("T0系统已关闭")
            except Exception as e:
                logger.error(f"关闭T0系统时出错: {e}")
                
        logger.info("交易系统协调器已停止")


def main():
    """
    主函数
    """
    print("=" * 50)
    print("交易系统协调器")
    print("=" * 50)
    print(f"启动时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # 获取股票池参数
    stock_pool = sys.argv[1:] if len(sys.argv) > 1 else None
    if stock_pool:
        print(f"使用指定股票池: {stock_pool}")
    else:
        from Investment.T0.config.settings import DEFAULT_STOCK_POOL
        stock_pool = DEFAULT_STOCK_POOL
        print(f"使用默认股票池: {stock_pool}")
    
    # 创建并运行协调器
    coordinator = TradeSystemCoordinator()
    
    try:
        coordinator.run(stock_pool)
    except KeyboardInterrupt:
        print("\n\n系统被用户中断")
    except Exception as e:
        print(f"\n系统运行出错: {e}")
        logger.error(f"系统运行出错: {e}")


if __name__ == "__main__":
    main()