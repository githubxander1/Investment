#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
T0交易系统 - 主入口文件
整合了新的模块化结构，提供统一的启动入口
"""
import os
import sys
import time
import argparse
import logging
from datetime import datetime

# 添加项目根目录到路径
project_root = os.path.dirname(os.path.abspath(__file__))
if project_root not in sys.path:
    sys.path.append(project_root)

# 导入配置和核心模块
from config.settings import (
    DEFAULT_STOCK_POOL, MONITOR_INTERVAL, LOGS_DIR, 
    DEBUG_MODE, LOG_CONFIG, validate_config
)
from utils.logger import setup_logger
from core.strategy import T0Strategy
from core.trade_engine import TradeEngine

# 设置日志
logger = setup_logger(
    name='t0_main',
    log_file=os.path.join(LOGS_DIR, f't0_system_{datetime.now().strftime("%Y%m%d")}.log'),
    level=getattr(logging, LOG_CONFIG['level']),
    log_format=LOG_CONFIG['format']
)


def parse_arguments():
    """
    解析命令行参数
    
    返回:
    argparse.Namespace: 解析后的参数
    """
    parser = argparse.ArgumentParser(description='T0交易系统')
    
    # 模式选择
    parser.add_argument('--mode', type=str, default='monitor', 
                        choices=['monitor', 'backtest', 'analyze', 'single'],
                        help='运行模式: monitor(监控模式), backtest(回测模式), analyze(分析模式), single(单个股票分析)')
    
    # 股票池配置
    parser.add_argument('--stocks', type=str, nargs='+',
                        help='股票代码列表，如: 000333 600030')
    
    # 监控间隔
    parser.add_argument('--interval', type=int, 
                        help='监控间隔（秒）')
    
    # 单个股票分析
    parser.add_argument('--stock', type=str,
                        help='单个分析的股票代码')
    
    # 回测参数
    parser.add_argument('--start-date', type=str,
                        help='回测开始日期，格式: YYYY-MM-DD')
    parser.add_argument('--end-date', type=str,
                        help='回测结束日期，格式: YYYY-MM-DD')
    
    # 调试模式
    parser.add_argument('--debug', action='store_true',
                        help='启用调试模式')
    
    # 测试模式（不执行实际交易）
    parser.add_argument('--test', action='store_true',
                        help='启用测试模式（不执行实际交易）')
    
    return parser.parse_args()


def run_monitor_mode(args):
    """
    运行监控模式
    
    参数:
    args: 命令行参数
    """
    logger.info("启动T0交易系统 - 监控模式")
    
    # 获取股票池
    stock_pool = args.stocks if args.stocks else DEFAULT_STOCK_POOL
    logger.info(f"监控股票池: {stock_pool}")
    
    # 获取监控间隔
    interval = args.interval if args.interval else MONITOR_INTERVAL
    logger.info(f"监控间隔: {interval}秒")
    
    # 创建交易引擎
    trade_engine = TradeEngine(
        stock_pool=stock_pool,
        monitor_interval=interval,
        test_mode=args.test
    )
    
    try:
        # 运行监控
        trade_engine.run()
        
    except KeyboardInterrupt:
        logger.info("用户中断，停止监控")
    except Exception as e:
        logger.error(f"监控模式运行失败: {e}", exc_info=True)
    finally:
        logger.info("监控模式结束")


def run_analyze_mode(args):
    """
    运行分析模式
    
    参数:
    args: 命令行参数
    """
    logger.info("启动T0交易系统 - 分析模式")
    
    # 获取股票池
    stock_pool = args.stocks if args.stocks else DEFAULT_STOCK_POOL
    logger.info(f"分析股票池: {stock_pool}")
    
    # 创建策略实例
    strategy = T0Strategy()
    
    try:
        # 对每个股票进行分析
        for stock_code in stock_pool:
            logger.info(f"开始分析股票: {stock_code}")
            
            # 运行策略分析
            result = strategy.analyze_stock(stock_code)
            
            # 保存分析结果
            if result:
                logger.info(f"股票 {stock_code} 分析完成，信号: {result.get('signal', 'UNKNOWN')}")
                
            # 避免请求过于频繁
            time.sleep(1)
        
    except Exception as e:
        logger.error(f"分析模式运行失败: {e}", exc_info=True)
    finally:
        logger.info("分析模式结束")


def run_single_stock_analysis(args):
    """
    运行单个股票分析
    
    参数:
    args: 命令行参数
    """
    if not args.stock:
        logger.error("请指定要分析的股票代码")
        return
    
    stock_code = args.stock
    logger.info(f"启动T0交易系统 - 单个股票分析: {stock_code}")
    
    # 创建策略实例
    strategy = T0Strategy()
    
    try:
        # 运行单个股票分析
        result = strategy.analyze_stock(stock_code, show_chart=True)
        
        # 显示分析结果
        if result:
            logger.info(f"股票 {stock_code} 分析结果:")
            logger.info(f"  信号: {result.get('signal', 'UNKNOWN')}")
            logger.info(f"  信号强度: {result.get('signal_strength', 0.0)}")
            logger.info(f"  当前价格: {result.get('current_price', 0.0)}")
            logger.info(f"  支撑位: {result.get('support', 0.0)}")
            logger.info(f"  阻力位: {result.get('resistance', 0.0)}")
            
            # 保存分析图表
            chart_path = strategy.save_chart(stock_code)
            if chart_path:
                logger.info(f"分析图表已保存至: {chart_path}")
        
    except Exception as e:
        logger.error(f"单个股票分析失败: {e}", exc_info=True)
    finally:
        logger.info("单个股票分析结束")


def run_backtest_mode(args):
    """
    运行回测模式
    
    参数:
    args: 命令行参数
    """
    logger.info("启动T0交易系统 - 回测模式")
    
    # 这里可以实现回测逻辑
    logger.warning("回测模式尚未完全实现")
    
    # TODO: 实现完整的回测功能
    # - 加载历史数据
    # - 运行策略
    # - 计算收益率
    # - 生成回测报告
    
    logger.info("回测模式结束")


def main():
    """
    主函数
    """
    logger.info("T0交易系统启动")
    
    # 验证配置
    if not validate_config():
        logger.error("配置验证失败，系统启动失败")
        return 1
    
    # 解析命令行参数
    args = parse_arguments()
    
    # 设置调试模式
    global DEBUG_MODE
    if args.debug:
        DEBUG_MODE = True
        logger.setLevel(logging.DEBUG)
        logger.debug("调试模式已启用")
    
    # 根据模式运行相应功能
    try:
        if args.mode == 'monitor':
            run_monitor_mode(args)
        elif args.mode == 'analyze':
            run_analyze_mode(args)
        elif args.mode == 'single':
            run_single_stock_analysis(args)
        elif args.mode == 'backtest':
            run_backtest_mode(args)
        else:
            logger.error(f"不支持的运行模式: {args.mode}")
            return 1
        
    except Exception as e:
        logger.error(f"系统运行失败: {e}", exc_info=True)
        return 1
    finally:
        logger.info("T0交易系统关闭")
    
    return 0


if __name__ == '__main__':
    sys.exit(main())
