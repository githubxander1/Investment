#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试redis模块导入
"""

import sys
print(f"Python版本: {sys.version}")
print(f"Python路径: {sys.path}")

try:
    import redis
    print("成功导入redis模块")
    print(f"redis模块路径: {redis.__file__}")
    
    # 尝试创建一个简单的redis连接对象（不实际连接）
    try:
        r = redis.Redis(host='localhost', port=6379, db=0)
        print("成功创建redis连接对象")
    except Exception as e:
        print(f"创建redis连接对象时出错（这是预期的，因为可能没有运行redis服务器）: {e}")
        print("但redis模块本身已成功导入")
        
except ImportError as e:
    print(f"导入redis模块失败: {e}")
    
    # 尝试找出问题所在
    print("\n尝试找出问题所在...")
    
    # 检查redis是否在site-packages中
    import os
    for path in sys.path:
        if 'site-packages' in path and os.path.exists(path):
            redis_path = os.path.join(path, 'redis')
            redis_init = os.path.join(path, 'redis.py')
            
            if os.path.exists(redis_path) or os.path.exists(redis_init):
                print(f"在 {path} 中找到redis模块")
            else:
                print(f"在 {path} 中未找到redis模块")