#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
查看模拟账户持仓信息的简化脚本
"""

import sys
import os
import logging

# 添加项目根目录到路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# 设置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('view_mock_holdings')

# 导入ths_trade适配器
try:
    from applications.adapter.ths_trade_adapter import THSTradeAdapter
    logger.info("成功导入THSTradeAdapter")
except ImportError as e:
    logger.error(f"导入THSTradeAdapter失败: {e}")
    sys.exit(1)

def main():
    """主函数"""
    logger.info("开始获取模拟账户持仓信息")
    
    try:
        # 初始化交易适配器
        adapter = THSTradeAdapter(account_name="模拟账户")
        if not adapter.initialized:
            logger.error("交易客户端初始化失败")
            sys.exit(1)
        
        # 只获取持仓信息
        print("\n===== 模拟账户持仓信息 =====")
        position = adapter.get_position()
        
        if position is not None and not position.empty:
            print(f"\n当前持有 {len(position)} 支股票:")
            print("-" * 60)
            print("证券代码    证券名称    持仓数量    可用余额    当日买入    当日卖出")
            print("-" * 60)
            
            # 只显示关键信息
            for _, row in position.iterrows():
                # 安全地获取数据
                code = row.get('证券代码', 'N/A')
                name = row.get('证券名称', 'N/A')
                balance = row.get('股票余额', 0)
                available = row.get('可用余额', 0)
                buy_today = row.get('当日买入', 0)
                sell_today = row.get('当日卖出', 0)
                
                # 格式化输出
                print(f"{code:<8} {name:<8} {balance:<8} {available:<8} {buy_today:<8} {sell_today:<8}")
            
            print("-" * 60)
            
            # 筛选出实际持有股票（股票余额 > 0）
            actual_holdings = position[position.get('股票余额', 0) > 0]
            if not actual_holdings.empty:
                print("\n实际持有股票:")
                print("-" * 60)
                for _, row in actual_holdings.iterrows():
                    print(f"{row.get('证券代码')} {row.get('证券名称')}: {row.get('股票余额')}股")
            else:
                print("\n当前无实际持有股票")
                
        else:
            print("未获取到持仓信息")
            
    except Exception as e:
        logger.error(f"执行错误: {str(e)}")
        print(f"\n错误: {str(e)}")
    finally:
        logger.info("持仓信息获取完成")

if __name__ == "__main__":
    main()