#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
ths_api模块导入测试脚本
用于验证所有接口是否能正常导入
"""

import sys
import os

# 添加项目根目录到路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def test_imports():
    """测试所有模块是否能正常导入"""
    modules_to_test = [
        'ths_api',
        'ths_api.trade_operations',
        'ths_api.account_info',
        'ths_api.trade_queries',
        'ths_api.adapter',
        'ths_api.exec_auto_trade',
        'ths_api.ths_trade_adapter',
        'ths_api.csv_helper',
        'ths_api.active_work',
        'ths_api.send_command',
        'ths_api.error_codes'
    ]
    
    failed_imports = []
    
    for module in modules_to_test:
        try:
            __import__(module)
            print(f"✓ {module} 导入成功")
        except Exception as e:
            print(f"✗ {module} 导入失败: {e}")
            failed_imports.append((module, str(e)))
    
    if failed_imports:
        print("\n以下模块导入失败:")
        for module, error in failed_imports:
            print(f"  - {module}: {error}")
        return False
    else:
        print("\n所有模块导入成功!")
        return True


def main():
    """主测试函数"""
    print("开始测试ths_api模块导入...")
    
    import_success = test_imports()
    
    if import_success:
        print("\n=== 所有导入测试通过 ===")
        print("ths_api模块已正确创建，所有接口文件均可正常导入。")
    else:
        print("\n=== 导入测试失败 ===")
        print("部分模块无法导入，请检查代码。")


if __name__ == "__main__":
    main()