#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
同花顺多账户切换示例脚本
演示如何使用增强版适配器在多个账户之间切换并执行交易操作
"""

import sys
import os
import time
import logging

# 添加项目根目录到路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# 设置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('account_switch_demo')

# 导入增强版适配器
try:
    from enhanced_ths_trade_adapter import EnhancedTHSTradeAdapter
    print("✅ 成功导入增强版同花顺交易适配器")
except ImportError as e:
    logging.error(f"❌ 导入增强版适配器失败: {e}")
    sys.exit(1)


def print_separator():
    """打印分隔线"""
    print("\n" + "="*60)

def demo_account_switching():
    """
    演示多账户切换功能
    """
    print_separator()
    print("同花顺多账户切换演示")
    print_separator()
    
    # 配置多个账户
    # 注意：请根据您的实际情况修改以下配置
    accounts_config = {
        "默认账户": {"exe_path": "C:\同花顺软件\同花顺\xiadan.exe", "password": ""},
        # 取消注释并修改以下账户信息以添加更多账户
        # "长城证券": {"exe_path": "C:\同花顺软件\同花顺\xiadan.exe", "password": "您的密码"},
        # "中泰证券": {"exe_path": "C:\同花顺软件\同花顺\xiadan.exe", "password": "您的密码"},
        # "川财证券": {"exe_path": "C:\同花顺软件\同花顺\xiadan.exe", "password": "您的密码"},
        # "中山证券": {"exe_path": "C:\同花顺软件\同花顺\xiadan.exe", "password": "您的密码"},
    }
    
    # 初始化增强版适配器
    adapter = EnhancedTHSTradeAdapter(accounts_config=accounts_config)
    
    # 列出所有可用账户
    print_separator()
    print("可用账户列表:")
    accounts = adapter.list_available_accounts()
    if not accounts:
        print("❌ 没有配置可用账户")
        return
    
    for i, account in enumerate(accounts):
        print(f"{i+1}. {account}")
    
    # 演示账户切换和基本操作
    for account_name in accounts:
        print_separator()
        print(f"正在切换到账户: {account_name}")
        
        # 切换账户
        if not adapter.switch_account(account_name):
            print(f"❌ 切换到账户 {account_name} 失败，跳过该账户")
            continue
        
        print(f"✅ 成功切换到账户: {account_name}")
        
        # 演示获取账户信息
        print("\n正在获取账户信息...")
        
        # 获取持仓信息
        print("\n--- 持仓信息 ---")
        try:
            position = adapter.get_position()
            if position is not None and not position.empty:
                print(f"持仓股票数量: {len(position)}")
                print("\n持仓明细:")
                print(position[['证券代码', '证券名称', '持仓数量', '可用数量', '市价', '市值']].head())
            else:
                print("暂无持仓信息")
        except Exception as e:
            print(f"获取持仓信息时出错: {str(e)}")
        
        # 获取资金情况
        print("\n--- 资金情况 ---")
        try:
            balance = adapter.get_balance()
            if balance is not None and not balance.empty:
                print(balance)
            else:
                print("暂无资金信息")
        except Exception as e:
            print(f"获取资金信息时出错: {str(e)}")
        
        # 获取当日成交
        print("\n--- 当日成交 ---")
        try:
            trades = adapter.get_today_trades()
            if trades is not None and not trades.empty:
                print(f"当日成交笔数: {len(trades)}")
                print("\n成交明细:")
                print(trades[['证券代码', '证券名称', '买卖', '成交价格', '成交数量', '成交金额']].head())
            else:
                print("暂无当日成交记录")
        except Exception as e:
            print(f"获取当日成交时出错: {str(e)}")
        
        # 获取当日委托
        print("\n--- 当日委托 ---")
        try:
            entrusts = adapter.get_today_entrusts()
            if entrusts is not None and not entrusts.empty:
                print(f"当日委托笔数: {len(entrusts)}")
                print("\n委托明细:")
                print(entrusts[['证券代码', '证券名称', '买卖', '委托价格', '委托数量', '状态']].head())
            else:
                print("暂无当日委托记录")
        except Exception as e:
            print(f"获取当日委托时出错: {str(e)}")
        
        # 提示用户是否继续到下一个账户
        if account_name != accounts[-1]:  # 如果不是最后一个账户
            response = input("\n按Enter键继续到下一个账户，输入'q'退出: ")
            if response.lower() == 'q':
                print("用户选择退出演示")
                break
        
        # 给用户一些时间查看当前账户信息
        print("\n等待3秒后继续...")
        time.sleep(3)
    
    print_separator()
    print("演示完成")
    print_separator()

def demo_trading_with_account(account_name="默认账户"):
    """
    演示在指定账户下执行交易操作
    """
    print_separator()
    print(f"在账户 {account_name} 下执行交易操作演示")
    print_separator()
    
    # 初始化适配器
    adapter = EnhancedTHSTradeAdapter()
    
    # 切换到指定账户
    if not adapter.switch_account(account_name):
        print(f"❌ 切换到账户 {account_name} 失败，退出演示")
        return
    
    print(f"✅ 成功切换到账户: {account_name}")
    
    # 演示交易操作（这里仅作演示，实际交易前请确认）
    print("\n注意：以下交易操作仅作演示，请在实际使用时谨慎操作！")
    
    # 示例：买入操作（请修改股票代码和数量）
    stock_code = "000001"  # 平安银行
    stock_name = "平安银行"
    buy_amount = 100  # 买入1手
    
    print(f"\n示例买入操作: {stock_name}({stock_code}), 数量: {buy_amount}")
    print("提示：实际交易前请取消注释下面的代码并确认交易参数")
    
    # 取消注释下面的代码进行实际买入操作
    # buy_result = adapter.buy_stock(stock_code, stock_name, buy_amount, strategy_no="demo_strategy")
    # print(f"买入结果: {buy_result}")
    
    # 示例：卖出操作（请确保有足够的持仓）
    sell_amount = 100  # 卖出1手
    
    print(f"\n示例卖出操作: {stock_name}({stock_code}), 数量: {sell_amount}")
    print("提示：实际交易前请取消注释下面的代码并确认交易参数")
    
    # 取消注释下面的代码进行实际卖出操作
    # sell_result = adapter.sell_stock(stock_code, stock_name, sell_amount, strategy_no="demo_strategy")
    # print(f"卖出结果: {sell_result}")
    
    print_separator()
    print("交易操作演示完成")
    print_separator()


def main():
    """
    主函数，提供菜单选择
    """
    while True:
        print_separator()
        print("同花顺多账户交易系统")
        print("1. 演示多账户切换")
        print("2. 演示在指定账户下执行交易操作")
        print("3. 退出")
        print_separator()
        
        choice = input("请选择操作 (1-3): ")
        
        if choice == '1':
            demo_account_switching()
        elif choice == '2':
            account_name = input("请输入要使用的账户名称: ")
            demo_trading_with_account(account_name)
        elif choice == '3':
            print("感谢使用，再见！")
            break
        else:
            print("无效的选择，请重新输入")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n程序被用户中断")
    except Exception as e:
        print(f"程序运行出错: {str(e)}")
        import traceback
        traceback.print_exc()
    finally:
        print("程序已退出")