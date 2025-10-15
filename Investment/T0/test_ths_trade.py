#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
T0交易系统 - ths_trade实现测试文件

这个测试文件用于验证T0交易系统使用ths_trade实现的功能是否正常工作，
包括初始化、持仓查询、资金查询和模拟交易操作等。
"""

import sys
import os
import time
from datetime import datetime

# 添加项目根目录到路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'THS'))

from trading.ths_trade_wrapper import T0THSTradeWrapper
from monitor.trade_executor import TradeExecutor
from utils.logger import setup_logger

# 设置日志
logger = setup_logger('test_ths_trade')

def test_t0_trade_wrapper():
    """测试T0THSTradeWrapper基本功能"""
    print("=" * 60)
    print("🔍 测试T0THSTradeWrapper基本功能")
    print("=" * 60)
    
    try:
        # 创建T0THSTradeWrapper实例
        trade_wrapper = T0THSTradeWrapper()
        
        # 检查初始化状态
        if not trade_wrapper.is_initialized():
            print("❌ T0THSTradeWrapper初始化失败")
            return False
        
        print("✅ T0THSTradeWrapper初始化成功")
        
        # 测试获取账户资金
        print("\n💰 测试获取账户资金...")
        funds = trade_wrapper.get_available_funds()
        if funds:
            print(f"✅ 可用资金: {funds['可用金额']}")
            print(f"   总资产: {funds['总资产']}")
            print(f"   股票市值: {funds['股票市值']}")
        else:
            print("❌ 获取账户资金失败")
        
        # 测试获取账户持仓
        print("\n📊 测试获取账户持仓...")
        positions = trade_wrapper.get_account_position()
        if positions:
            print(f"✅ 获取到 {len(positions)} 个持仓")
            for pos in positions:
                print(f"   {pos['证券代码']} - {pos['证券名称']}: {pos['持仓数量']}股, 可用: {pos['可用数量']}股, 成本: {pos['摊薄成本价']}, 现价: {pos['最新价']}")
        else:
            print("✅ 账户暂无持仓")
        
        # 测试获取特定股票持仓
        print("\n🔍 测试获取特定股票持仓...")
        # 这里以贵州茅台为例，实际运行时可以替换为真实持有的股票代码
        stock_code = '600519'
        stock_pos = trade_wrapper.get_stock_position(stock_code)
        if stock_pos:
            print(f"✅ {stock_code}持仓信息:")
            print(f"   持仓数量: {stock_pos['持仓数量']}股")
            print(f"   可用数量: {stock_pos['可用数量']}股")
            print(f"   成本价: {stock_pos['摊薄成本价']}")
            print(f"   最新价: {stock_pos['最新价']}")
        else:
            print(f"ℹ️  未持有 {stock_code} 股票")
        
        # 测试计算T0利润（演示）
        print("\n📈 测试计算T0利润...")
        try:
            # 模拟数据
            t0_profit = trade_wrapper.calculate_t0_profit(stock_code, 100, 1800, 1820)
            print(f"✅ T0利润计算示例: 买入100股@{1800}, 卖出100股@{1820}")
            print(f"   毛利润: {t0_profit['gross_profit']:.2f}元")
            print(f"   手续费: {t0_profit['fee']:.2f}元")
            print(f"   净利润: {t0_profit['net_profit']:.2f}元")
        except Exception as e:
            print(f"❌ 计算T0利润时出错: {e}")
        
        # 清理资源
        trade_wrapper.close()
        print("\n✅ T0THSTradeWrapper测试完成并关闭资源")
        return True
        
    except Exception as e:
        print(f"❌ T0THSTradeWrapper测试失败: {e}")
        logger.error(f"T0THSTradeWrapper测试失败: {e}")
        return False

def test_trade_executor():
    """测试TradeExecutor功能"""
    print("\n" + "=" * 60)
    print("🔍 测试TradeExecutor功能")
    print("=" * 60)
    
    executor = None
    try:
        # 创建TradeExecutor实例
        executor = TradeExecutor()
        
        # 检查初始化状态
        if not executor.is_initialized():
            print("❌ TradeExecutor初始化失败")
            return False
        
        print("✅ TradeExecutor初始化成功")
        
        # 测试模拟交易 - 注意：这里使用演示模式，不会实际执行交易
        print("\n💹 测试模拟交易...")
        
        # 模拟买入
        stock_code = '600519'
        stock_name = '贵州茅台'
        indicator = 'MACD金叉'
        
        print(f"\n📥 测试模拟买入: {stock_code} - {stock_name}")
        # 设置为演示模式，不会实际下单
        executor._demo_mode = True
        
        # 执行模拟买入
        result = executor.execute_buy(stock_code, indicator, stock_name=stock_name)
        print(f"✅ 模拟买入执行结果: {result}")
        
        # 执行模拟卖出
        print(f"\n📤 测试模拟卖出: {stock_code} - {stock_name}")
        result = executor.execute_sell(stock_code, indicator, stock_name=stock_name)
        print(f"✅ 模拟卖出执行结果: {result}")
        
        # 测试统一交易接口
        print(f"\n🔄 测试统一交易接口...")
        trade_data = {
            'stock_code': stock_code,
            'stock_name': stock_name,
            'indicator_name': indicator,
            'operation': 'buy',
            'price': 1800.0
        }
        success = executor.execute_trade(trade_data)
        print(f"✅ 统一交易接口执行结果: {success}")
        
        # 清理资源
        executor.close()
        print("\n✅ TradeExecutor测试完成并关闭资源")
        return True
        
    except Exception as e:
        print(f"❌ TradeExecutor测试失败: {e}")
        logger.error(f"TradeExecutor测试失败: {e}")
        return False
    finally:
        if executor and hasattr(executor, 'close'):
            try:
                executor.close()
            except:
                pass

def main():
    """主测试函数"""
    print("""
    =================================================
                   T0交易系统 - ths_trade测试
    =================================================
    此测试将验证T0交易系统使用ths_trade实现的功能是否正常工作。
    注意：测试在演示模式下运行，不会实际执行交易。
    =================================================
    """)
    
    start_time = datetime.now()
    
    # 运行测试
    wrapper_test_result = test_t0_trade_wrapper()
    executor_test_result = test_trade_executor()
    
    # 输出测试结果摘要
    print("\n" + "=" * 60)
    print("📋 测试结果摘要")
    print("=" * 60)
    print(f"T0THSTradeWrapper测试: {'✅ 通过' if wrapper_test_result else '❌ 失败'}")
    print(f"TradeExecutor测试: {'✅ 通过' if executor_test_result else '❌ 失败'}")
    
    all_passed = wrapper_test_result and executor_test_result
    print(f"\n总体测试结果: {'✅ 全部通过' if all_passed else '❌ 部分失败'}")
    
    end_time = datetime.now()
    duration = (end_time - start_time).total_seconds()
    print(f"测试耗时: {duration:.2f} 秒")
    print("=" * 60)
    
    return 0 if all_passed else 1

if __name__ == "__main__":
    sys.exit(main())