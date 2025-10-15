#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
组合持仓策略示例
演示如何使用CombinationHoldingProcessor进行组合调仓
"""

import logging
from datetime import datetime

# 设置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# 导入组合持仓处理器
from ths_trade.strategies import CombinationHoldingProcessor

def run_combination_strategy():
    """
    运行组合持仓策略示例
    """
    try:
        # 记录开始时间
        start_time = datetime.now()
        logger.info("=== 开始执行组合持仓策略 ===")
        
        # 创建组合持仓处理器实例
        # 可以根据实际情况修改策略名称和账户名称
        processor = CombinationHoldingProcessor(
            strategy_name="my_portfolio_strategy",  # 替换为实际的策略名称
            account_name="main_account"             # 替换为实际的账户名称
        )
        
        # 执行策略调仓
        logger.info("开始执行策略调仓操作...")
        success = processor.operate_strategy_with_account()
        
        # 记录结束时间
        end_time = datetime.now()
        duration = end_time - start_time
        
        if success:
            logger.info(f"✅ 组合策略调仓任务成功完成，耗时: {duration}")
        else:
            logger.error(f"❌ 组合策略调仓任务失败，耗时: {duration}")
            
        logger.info("=== 组合持仓策略执行结束 ===")
        
    except Exception as e:
        logger.error(f"执行组合持仓策略时发生异常: {e}")
        import traceback
        logger.error(traceback.format_exc())

def run_strategy_with_custom_data():
    """
    使用自定义数据运行策略的示例
    在实际应用中，可以从自定义数据源获取策略持仓数据
    """
    try:
        logger.info("=== 开始执行带自定义数据的组合持仓策略 ===")
        
        # 创建处理器实例
        processor = CombinationHoldingProcessor(
            strategy_name="custom_data_strategy",
            account_name="test_account"
        )
        
        # 这里可以添加自定义的数据处理逻辑
        # 例如，从CSV文件、数据库或API获取策略持仓数据
        # 然后可以修改processor._update_strategy_holdings方法的实现
        # 或者直接设置processor的相关属性
        
        logger.info("自定义数据处理完成，准备执行调仓")
        
        # 执行调仓
        processor.operate_strategy_with_account()
        
        logger.info("=== 带自定义数据的组合持仓策略执行结束 ===")
        
    except Exception as e:
        logger.error(f"执行带自定义数据的策略时发生异常: {e}")

if __name__ == "__main__":
    # 运行基本示例
    run_combination_strategy()
    
    # 运行自定义数据示例（可选）
    # run_strategy_with_custom_data()