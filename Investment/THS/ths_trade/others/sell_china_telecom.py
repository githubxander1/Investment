#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
测试卖出中国电信股票的脚本
"""

import sys
import os
import logging

# 添加项目根目录到路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# 设置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('sell_china_telecom')

# 导入ths_trade适配器
try:
    from applications.adapter.ths_trade_adapter import THSTradeAdapter
    logger.info("✅ 成功导入THSTradeAdapter")
except ImportError as e:
    logger.error(f"❌ 导入THSTradeAdapter失败: {e}")
    sys.exit(1)

def main():
    """主函数"""
    logger.info("📋 开始执行卖出中国电信股票测试")
    
    # 初始化交易适配器
    try:
        adapter = THSTradeAdapter(account_name="测试账户")
        if not adapter.initialized:
            logger.error("❌ 交易客户端初始化失败，请确保同花顺交易软件已打开并登录")
            logger.info("📋 请手动打开同花顺交易软件 (xiadan.exe) 并完成登录")
            sys.exit(1)
        logger.info("✅ 交易客户端初始化成功")
        
        # 先获取持仓信息，确认是否持有中国电信
        logger.info("📊 获取当前持仓信息...")
        position = adapter.get_position()
        if position is not None:
            logger.info(f"✅ 成功获取持仓信息，共有 {len(position)} 支股票")
            # 打印持仓信息以便查看
            print("\n当前持仓:")
            print(position)
            
            # 检查是否持有中国电信
            china_telecom_holdings = position[position['证券代码'] == '601728']
            if not china_telecom_holdings.empty:
                logger.info("✅ 检测到持有中国电信股票")
                available_shares = china_telecom_holdings.iloc[0]['可用余额']
                logger.info(f"📊 中国电信可用余额: {available_shares}股")
            else:
                logger.warning("⚠️ 未检测到持有中国电信股票")
        else:
            logger.error("❌ 无法获取持仓信息")
        
        # 执行卖出操作 - 中国电信（代码：601728）卖出100股
        logger.info("📉 开始执行卖出操作: 中国电信(601728) - 100股")
        result = adapter.sell_stock(
            stock_code="601728",  # 中国电信股票代码
            stock_name="中国电信",
            amount=100,  # 卖出数量
            strategy_no="test_sell"
        )
        
        # 处理结果
        if result.get("success"):
            logger.info(f"✅ 卖出成功！合同号: {result.get('entrust_no')}")
            logger.info(f"📋 卖出结果: {result}")
        else:
            logger.error(f"❌ 卖出失败！错误信息: {result.get('msg')}")
            logger.info(f"📋 失败详情: {result}")
            
            # 根据错误信息提供解决方案
            if "股份可用数不足" in result.get('msg', ''):
                logger.info("💡 请检查持仓中中国电信的可用数量是否足够")
            elif "交易客户端未初始化成功" in result.get('msg', ''):
                logger.info("💡 请确保同花顺交易软件已打开并登录成功")
        
    except Exception as e:
        logger.error(f"❌ 执行过程中出现异常: {str(e)}", exc_info=True)
    finally:
        logger.info("📋 卖出测试执行完毕")

if __name__ == "__main__":
    main()