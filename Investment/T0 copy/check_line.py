#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
简单脚本，精确打印文件的第20-30行
"""
import os

# 文件路径
file_path = os.path.join(os.path.dirname(__file__), 'trading', 'ths_trade_wrapper.py')

try:
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    print(f"文件: {file_path}")
    print(f"显示第20到30行:")
    
    # 只打印第20-30行
    for i in range(19, 30):  # 0-based index
        if i < len(lines):
            print(f"第{i+1}行: {repr(lines[i])}")
        else:
            print(f"第{i+1}行: (超出文件范围)")
            
except Exception as e:
    print(f"错误: {e}")