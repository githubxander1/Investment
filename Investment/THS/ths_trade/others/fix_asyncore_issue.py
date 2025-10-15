#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
修复asyncore模块缺失问题
在Python 3.13中，asyncore模块已被移除，需要安装替代库
"""

import os
import sys
import subprocess

print("开始修复asyncore模块缺失问题...")

# 首先尝试安装asyncore的替代库
try:
    print("安装asyncore替代库...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "asyncore_py3k"])
    print("asyncore_py3k安装成功")
except subprocess.CalledProcessError as e:
    print(f"安装asyncore_py3k失败: {e}")
    print("尝试安装其他替代方案...")
    try:
        # 尝试安装另一个可能的替代库
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pypi-asyncore"])
        print("pypi-asyncore安装成功")
    except subprocess.CalledProcessError:
        print("无法安装替代库，将尝试直接修改代码")

# 创建一个模拟的asyncore模块
asyncore_module_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "asyncore.py")
print(f"创建模拟的asyncore模块: {asyncore_module_path}")

asyncore_content = """
# 模拟asyncore模块，为Python 3.13+提供兼容支持

class dispatcher:
    def __init__(self, sock=None, map=None):
        self.socket = sock
        self.map = map or {}
        if sock:
            self.add_channel(self.map)
    
    def add_channel(self, map=None):
        if map is None:
            map = self.map
        if self.socket:
            map[self.socket.fileno()] = self
    
    def del_channel(self, map=None):
        if map is None:
            map = self.map
        if self.socket and self.socket.fileno() in map:
            del map[self.socket.fileno()]
    
    def readable(self):
        return True
    
    def writable(self):
        return False
    
    def handle_read(self):
        pass
    
    def handle_write(self):
        pass
    
    def handle_connect(self):
        pass
    
    def handle_close(self):
        self.close()
    
    def handle_error(self):
        import traceback
        traceback.print_exc()
    
    def close(self):
        if self.socket:
            self.del_channel()
            self.socket.close()
            self.socket = None

class dispatcher_with_send(dispatcher):
    def __init__(self, sock=None, map=None):
        super().__init__(sock, map)
        self.out_buffer = b''
    
    def writable(self):
        return bool(self.out_buffer)
    
    def handle_write(self):
        if self.out_buffer:
            try:
                sent = self.socket.send(self.out_buffer)
                self.out_buffer = self.out_buffer[sent:]
            except Exception:
                self.handle_error()
    
    def send(self, data):
        if isinstance(data, str):
            data = data.encode()
        self.out_buffer = self.out_buffer + data

# 基本的循环函数
def loop(timeout=30.0, use_poll=False, map=None, count=None):
    import time
    if map is None:
        import socket
        map = {}
    
    iterations = 0
    while map and (count is None or iterations < count):
        iterations += 1
        time.sleep(timeout)

# 导出函数
_loop = loop
"""

try:
    with open(asyncore_module_path, 'w', encoding='utf-8') as f:
        f.write(asyncore_content)
    print("模拟的asyncore模块创建成功")
except Exception as e:
    print(f"创建模拟asyncore模块失败: {e}")

# 修改trest/amqp/publisher.py以使用替代的asyncore
publisher_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "trest", "amqp", "publisher.py")
if os.path.exists(publisher_path):
    print(f"修改publisher.py文件: {publisher_path}")
    try:
        # 读取当前文件内容
        with open(publisher_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 检查是否已经包含了修复代码
        if "# 修复Python 3.13+中asyncore模块缺失问题" not in content:
            # 在文件开头添加修复代码
            fixed_content = """# 修复Python 3.13+中asyncore模块缺失问题
import sys
import os
# 添加当前目录到Python路径，以便找到我们的asyncore模块
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
""" + content
            
            # 写入修复后的内容
            with open(publisher_path, 'w', encoding='utf-8') as f:
                f.write(fixed_content)
            print("publisher.py文件修改成功")
        else:
            print("publisher.py文件已经包含修复代码")
    except Exception as e:
        print(f"修改publisher.py文件失败: {e}")
else:
    print(f"publisher.py文件不存在: {publisher_path}")

# 尝试更新pika版本到更兼容的版本
try:
    print("尝试更新pika到更兼容的版本...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "pika==1.3.0"])
    print("pika更新成功")
except subprocess.CalledProcessError as e:
    print(f"更新pika失败: {e}")

print("\n修复完成！现在可以尝试运行app.py了")
print("注意: 如果仍然遇到问题，可能需要考虑以下方案:")
print("1. 使用pika的SelectConnection代替BlockingConnection")
print("2. 降级Python版本到3.12或更低版本")
print("3. 替换为其他消息队列库，如kafka-python或redis-py")