#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
测试T0交易包装器的模拟模式功能
"""

import sys
import os

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from Investment.T0.trading.ths_trade_wrapper import T0THSTradeWrapper

def test_mock_mode():
    """
    测试模拟模式下的T0交易包装器功能
    """
    print("=" * 50)
    print("开始测试T0交易包装器模拟模式...")
    print("=" * 50)
    
    # 使用模拟模式初始化交易包装器
    wrapper = T0THSTradeWrapper(mock_mode=True)
    
    # 测试账户资金获取
    print("\n1. 测试获取账户资金信息:")
    funds = wrapper.get_available_funds()
    print(f"   可用资金: {funds}")
    
    # 测试股票持仓获取
    print("\n2. 测试获取股票持仓信息:")
    stock_pos = wrapper.get_stock_position('000001')
    print(f"   股票持仓: {stock_pos}")
    
    # 测试账户所有持仓获取
    print("\n3. 测试获取账户所有持仓:")
    all_pos = wrapper.get_account_position()
    print(f"   账户持仓数量: {len(all_pos) if all_pos else 0}")
    if all_pos:
        for pos in all_pos[:3]:  # 只显示前3个
            print(f"   - {pos['证券代码']} {pos['证券名称']}: {pos['持仓数量']}股")
    
    # 测试买入功能
    print("\n4. 测试买入功能:")
    buy_result = wrapper.buy_stock('000001', '平安银行', 12.5, 100)
    print(f"   买入结果: {buy_result}")
    
    # 测试卖出功能
    print("\n5. 测试卖出功能:")
    sell_result = wrapper.sell_stock('000001', '平安银行', 12.6, 100)
    print(f"   卖出结果: {sell_result}")
    
    # 测试T0交易功能
    print("\n6. 测试T0交易功能:")
    t0_result = wrapper.do_t0_trade('000001', '平安银行', 12.5, 12.6, 100)
    print(f"   T0交易结果: 成功={t0_result['success']}")
    if 'profit' in t0_result:
        print(f"   利润信息: 净利润={t0_result['profit']['net_profit']:.2f}元")
    
    # 测试利润计算功能
    print("\n7. 测试利润计算功能:")
    profit = wrapper.calculate_t0_profit('000001', 100, 12.5, 12.6)
    print(f"   沪市股票利润计算:")
    print(f"   - 毛利润: {profit['gross_profit']:.2f}元")
    print(f"   - 手续费: {profit['fee']:.2f}元")
    print(f"   - 净利润: {profit['net_profit']:.2f}元")
    
    # 测试深市股票利润计算
    profit_sz = wrapper.calculate_t0_profit('000001', 100, 12.5, 12.6)
    print(f"   深市股票利润计算:")
    print(f"   - 毛利润: {profit_sz['gross_profit']:.2f}元")
    print(f"   - 手续费: {profit_sz['fee']:.2f}元")
    print(f"   - 净利润: {profit_sz['net_profit']:.2f}元")
    
    # 关闭资源
    print("\n8. 关闭资源:")
    wrapper.close()
    print("   资源已关闭")
    
    print("\n" + "=" * 50)
    print("模拟模式测试完成!")
    print("=" * 50)

if __name__ == "__main__":
    test_mock_mode()