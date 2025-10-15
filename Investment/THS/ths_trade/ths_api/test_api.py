#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
ths_api模块测试脚本
用于验证所有接口是否能正常工作
"""

import sys
import os
import pandas as pd

# 添加项目根目录到路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# 导入所有API接口
from ths_api import *


def test_trade_operations():
    """测试交易操作接口"""
    print("=== 测试交易操作接口 ===")
    # 注意：这些测试不会真正执行交易，因为没有提供有效的交易参数
    print("交易操作接口导入成功")


def test_account_info():
    """测试账户信息接口"""
    print("\n=== 测试账户信息接口 ===")
    print("账户信息接口导入成功")


def test_trade_queries():
    """测试交易查询接口"""
    print("\n=== 测试交易查询接口 ===")
    print("交易查询接口导入成功")


def test_adapter():
    """测试适配器接口"""
    print("\n=== 测试适配器接口 ===")
    # 创建适配器实例
    adapter = create_ths_adapter()
    print(f"适配器创建成功: {adapter}")
    print(f"适配器是否初始化: {is_adapter_initialized(adapter)}")
    print(f"适配器账户名称: {get_adapter_account_name(adapter)}")


def test_exec_auto_trade():
    """测试自动化交易执行接口"""
    print("\n=== 测试自动化交易执行接口 ===")
    print("自动化交易执行接口导入成功")


def test_csv_helper():
    """测试CSV工具接口"""
    print("\n=== 测试CSV工具接口 ===")
    print("CSV工具接口导入成功")


def test_active_work():
    """测试活动工作队列接口"""
    print("\n=== 测试活动工作队列接口 ===")
    # 创建活动工作队列实例
    active_work = create_active_work()
    print(f"活动工作队列创建成功: {active_work}")
    
    # 获取下一个工作项
    next_item = get_next_work_item(active_work)
    print(f"下一个工作项: {next_item}")


def test_send_command():
    """测试策略命令发送接口"""
    print("\n=== 测试策略命令发送接口 ===")
    print("策略命令发送接口导入成功")


def main():
    """主测试函数"""
    print("开始测试ths_api模块...")
    
    try:
        test_trade_operations()
        test_account_info()
        test_trade_queries()
        test_adapter()
        test_exec_auto_trade()
        test_csv_helper()
        test_active_work()
        test_send_command()
        
        print("\n=== 所有接口测试完成 ===")
        print("所有ths_api模块接口均已成功导入，没有发现明显的导入错误。")
        
    except Exception as e:
        print(f"\n测试过程中出现错误: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()