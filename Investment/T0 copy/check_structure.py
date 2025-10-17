#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
检查目录结构和Python路径
"""
import os
import sys

# 打印当前工作目录
print(f"当前工作目录: {os.getcwd()}")

# 打印Python路径
print("\nPython路径:")
for path in sys.path:
    print(f"  {path}")

# 检查当前目录结构
print("\n当前目录结构:")
def print_directory_structure(path, level=0):
    if level > 3:  # 限制深度
        return
    try:
        items = os.listdir(path)
        for item in items:
            item_path = os.path.join(path, item)
            prefix = '  ' * level
            if os.path.isdir(item_path):
                print(f"{prefix}📁 {item}/")
                print_directory_structure(item_path, level + 1)
            elif item.endswith('.py'):
                print(f"{prefix}📄 {item}")
    except Exception as e:
        print(f"{prefix}❌ 无法访问 {path}: {e}")

# 从当前目录开始print_directory_structure('.')

# 检查Investment目录是否存在于正确位置
print("\n检查Investment目录:")
for i in range(5):
    check_path = os.path.join(*(['..'] * i), 'Investment')
    check_path_abs = os.path.abspath(check_path)
    if os.path.isdir(check_path_abs):
        print(f"✅ 在 {check_path_abs} 找到Investment目录")
        # 检查里面的内容
        print(f"  内容: {os.listdir(check_path_abs)}")