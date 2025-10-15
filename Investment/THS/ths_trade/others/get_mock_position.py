#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
获取模拟账户持仓信息的脚本
"""

import sys
import os
import logging
import pandas as pd

# 添加项目根目录到路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# 设置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('get_mock_position')

# 导入ths_trade适配器
try:
    from applications.adapter.ths_trade_adapter import THSTradeAdapter
    logger.info("✅ 成功导入THSTradeAdapter")
except ImportError as e:
    logger.error(f"❌ 导入THSTradeAdapter失败: {e}")
    sys.exit(1)

def main():
    """主函数"""
    logger.info("📋 开始获取模拟账户持仓信息")
    
    # 初始化交易适配器
    try:
        adapter = THSTradeAdapter(account_name="模拟账户")
        if not adapter.initialized:
            logger.error("❌ 交易客户端初始化失败，请确保同花顺交易软件已打开并登录模拟账户")
            sys.exit(1)
        logger.info("✅ 交易客户端初始化成功")
        
        # 获取持仓信息
        logger.info("📊 获取当前持仓信息...")
        position = adapter.get_position()
        
        if position is not None:
            logger.info(f"✅ 成功获取持仓信息，共有 {len(position)} 支股票")
            
            # 格式化输出持仓信息
            print("\n=== 模拟账户持仓信息 ===")
            print(f"查询时间: {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')}")
            print(f"持仓股票数量: {len(position)}")
            
            # 先显示数据的列名和类型
            print("\n数据列名:")
            for col in position.columns:
                print(f"- {col}")
            
            # 显示前两行完整数据以便了解结构
            print("\n前两行数据:")
            print(position.head(2))
            
            # 显示详细持仓信息，使用安全的方式访问列
            print("\n详细持仓:")
            for _, row in position.iterrows():
                # 获取股票代码和名称（这两列根据之前的输出是存在的）
                stock_code = row.get('证券代码', 'N/A')
                stock_name = row.get('证券名称', 'N/A')
                print(f"股票代码: {stock_code}")
                print(f"股票名称: {stock_name}")
                
                # 安全地获取其他可能存在的字段
                for field in ['可用余额', '市值', '成本价', '现价', '盈亏', '盈亏比例', '持仓市值', '浮动盈亏']:
                    if field in row:
                        print(f"{field}: {row[field]}")
                
                print("-" * 50)
            
            # 保存持仓信息到文件
            output_file = f"mock_position_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}.csv"
            position.to_csv(output_file, index=False, encoding='utf-8-sig')
            logger.info(f"✅ 持仓信息已保存到: {output_file}")
            
            # 获取资金情况
            logger.info("💰 获取资金情况...")
            balance = adapter.get_balance()
            if balance is not None:
                logger.info("✅ 成功获取资金信息")
                print("\n=== 资金信息 ===")
                print(balance)
            else:
                logger.error("❌ 无法获取资金信息")
                
            # 获取当日成交
            logger.info("📋 获取当日成交...")
            trades = adapter.get_today_trades()
            if trades is not None:
                logger.info(f"✅ 成功获取当日成交，共 {len(trades)} 笔")
                print("\n=== 当日成交 ===")
                if len(trades) > 0:
                    print(trades)
                else:
                    print("当日无成交记录")
            else:
                logger.error("❌ 无法获取当日成交信息")
                
            # 获取当日委托
            logger.info("📝 获取当日委托...")
            entrusts = adapter.get_today_entrusts()
            if entrusts is not None:
                logger.info(f"✅ 成功获取当日委托，共 {len(entrusts)} 笔")
                print("\n=== 当日委托 ===")
                if len(entrusts) > 0:
                    print(entrusts)
                else:
                    print("当日无委托记录")
            else:
                logger.error("❌ 无法获取当日委托信息")
                
        else:
            logger.error("❌ 无法获取持仓信息")
            print("\n⚠️ 无法获取持仓信息，请检查同花顺交易软件连接")
            
    except Exception as e:
        logger.error(f"❌ 执行过程中出现异常: {str(e)}", exc_info=True)
        print(f"\n❌ 错误: {str(e)}")
    finally:
        logger.info("📋 持仓信息获取完成")

if __name__ == "__main__":
    main()