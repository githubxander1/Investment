#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
简单测试脚本，验证ths_trade_wrapper.py是否能正常导入和初始化
"""
import logging
import sys
import os

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('test_wrapper')

def main():
    try:
        logger.info("开始测试ths_trade_wrapper模块导入...")
        
        # 导入ths_trade_wrapper模块
        from Investment.T0.trading.ths_trade_wrapper import T0THSTradeWrapper
        logger.info("✅ 成功导入T0THSTradeWrapper类")
        
        # 检查类的基本信息
        logger.info(f"类名: {T0THSTradeWrapper.__name__}")
        logger.info(f"类文档: {T0THSTradeWrapper.__doc__}")
        
        # 打印类的方法列表
        methods = [method for method in dir(T0THSTradeWrapper) if not method.startswith('__')]
        logger.info(f"类方法列表: {methods}")
        
        # 尝试创建实例（可能会失败，因为需要THS交易环境）
        try:
            logger.info("尝试创建T0THSTradeWrapper实例...")
            wrapper = T0THSTradeWrapper(account_name="测试账户")
            logger.info(f"✅ 成功创建实例，初始化状态: {wrapper.is_initialized()}")
        except Exception as e:
            logger.warning(f"⚠️ 创建实例时出现异常（可能是因为缺少THS交易环境）: {e}")
        
        logger.info("测试完成!")
        return 0
        
    except ImportError as e:
        logger.error(f"❌ 导入模块失败: {e}")
        return 1
    except Exception as e:
        logger.error(f"❌ 测试过程中发生异常: {e}")
        import traceback
        logger.error(traceback.format_exc())
        return 1

if __name__ == "__main__":
    sys.exit(main())