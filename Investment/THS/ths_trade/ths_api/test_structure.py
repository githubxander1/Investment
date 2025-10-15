#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
ths_api模块结构测试脚本
用于验证所有接口文件是否存在且结构正确
"""

import os
import sys

# 添加项目根目录到路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def test_file_existence():
    """测试所有接口文件是否存在"""
    api_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)))
    expected_files = [
        '__init__.py',
        'trade_operations.py',
        'account_info.py',
        'trade_queries.py',
        'adapter.py',
        'exec_auto_trade.py',
        'ths_trade_adapter.py',
        'csv_helper.py',
        'active_work.py',
        'send_command.py',
        'error_codes.py'
    ]
    
    missing_files = []
    for file in expected_files:
        file_path = os.path.join(api_dir, file)
        if os.path.exists(file_path):
            print(f"✓ {file} 存在")
        else:
            print(f"✗ {file} 不存在")
            missing_files.append(file)
    
    if missing_files:
        print(f"\n缺失文件: {missing_files}")
        return False
    else:
        print("\n所有文件都存在!")
        return True


def test_init_file():
    """测试__init__.py文件内容"""
    init_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '__init__.py')
    
    try:
        with open(init_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 检查是否包含所有模块的导入语句
        expected_imports = [
            'trade_operations',
            'account_info', 
            'trade_queries',
            'adapter',
            'exec_auto_trade',
            'ths_trade_adapter',
            'csv_helper',
            'active_work',
            'send_command',
            'error_codes'
        ]
        
        missing_imports = []
        for imp in expected_imports:
            if imp in content:
                print(f"✓ 包含 {imp} 的导入")
            else:
                print(f"✗ 缺少 {imp} 的导入")
                missing_imports.append(imp)
        
        # 检查是否包含__all__列表
        if '__all__' in content:
            print("✓ 包含 __all__ 列表")
        else:
            print("✗ 缺少 __all__ 列表")
            missing_imports.append('__all__')
        
        return len(missing_imports) == 0
    except Exception as e:
        print(f"读取__init__.py文件时出错: {e}")
        return False


def main():
    """主测试函数"""
    print("开始测试ths_api模块结构...")
    
    print("\n=== 测试文件存在性 ===")
    files_ok = test_file_existence()
    
    print("\n=== 测试__init__.py内容 ===")
    init_ok = test_init_file()
    
    if files_ok and init_ok:
        print("\n=== 所有结构测试通过 ===")
        print("ths_api模块已正确创建，文件结构完整。")
    else:
        print("\n=== 结构测试失败 ===")
        print("模块结构存在问题，请检查文件和内容。")


if __name__ == "__main__":
    main()