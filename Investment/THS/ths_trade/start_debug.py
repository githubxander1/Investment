#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
带调试信息的应用程序启动脚本
"""

import os
import sys
import logging
import traceback

# 配置基本日志
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("debug.log"),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger('ths_trade_debug')

print("=== 开始启动同花顺交易服务 ===" )
logger.info("=== 开始启动同花顺交易服务 ===")

# 打印Python版本信息
logger.info(f"Python版本: {sys.version}")
print(f"Python版本: {sys.version}")

# 打印当前工作目录
current_dir = os.getcwd()
logger.info(f"当前工作目录: {current_dir}")
print(f"当前工作目录: {current_dir}")

# 检查Python路径
sys_path = "\n".join(sys.path)
logger.info(f"Python路径: {sys_path}")
print(f"Python路径长度: {len(sys.path)} 个路径")

# 检查关键文件是否存在
app_file = "app.py"
if os.path.exists(app_file):
    logger.info(f"找到app.py文件: {os.path.abspath(app_file)}")
    print(f"找到app.py文件: {os.path.abspath(app_file)}")
else:
    logger.error(f"未找到app.py文件: {os.path.abspath(app_file)}")
    print(f"错误: 未找到app.py文件: {os.path.abspath(app_file)}")
    sys.exit(1)

# 检查trest目录是否存在
trest_dir = "trest"
if os.path.exists(trest_dir) and os.path.isdir(trest_dir):
    logger.info(f"找到trest目录: {os.path.abspath(trest_dir)}")
    print(f"找到trest目录: {os.path.abspath(trest_dir)}")
else:
    logger.error(f"未找到trest目录: {os.path.abspath(trest_dir)}")
    print(f"错误: 未找到trest目录: {os.path.abspath(trest_dir)}")

# 检查是否存在我们创建的asyncore模块
asyncore_file = "asyncore.py"
if os.path.exists(asyncore_file):
    logger.info(f"找到模拟的asyncore模块: {os.path.abspath(asyncore_file)}")
    print(f"找到模拟的asyncore模块: {os.path.abspath(asyncore_file)}")
else:
    logger.error(f"未找到模拟的asyncore模块: {os.path.abspath(asyncore_file)}")
    print(f"错误: 未找到模拟的asyncore模块: {os.path.abspath(asyncore_file)}")

# 尝试导入一些关键模块
try:
    import pika
    logger.info(f"成功导入pika模块，版本: {pika.__version__}")
    print(f"成功导入pika模块，版本: {pika.__version__}")
except ImportError as e:
    logger.error(f"导入pika模块失败: {e}")
    print(f"错误: 导入pika模块失败: {e}")

try:
    import asyncore
    logger.info("成功导入asyncore模块")
    print("成功导入asyncore模块")
except ImportError as e:
    logger.error(f"导入asyncore模块失败: {e}")
    print(f"错误: 导入asyncore模块失败: {e}")

try:
    import raven
    logger.info("成功导入raven模块")
    print("成功导入raven模块")
except ImportError as e:
    logger.error(f"导入raven模块失败: {e}")
    print(f"错误: 导入raven模块失败: {e}")

# 尝试启动应用程序
print("\n=== 开始执行app.py ===")
logger.info("=== 开始执行app.py ===")

# 创建一个修改后的app.py代码，添加更多调试信息
with open(app_file, 'r', encoding='utf-8') as f:
    original_app_code = f.read()

# 在app.py代码的开头添加调试信息
modified_app_code = """
import sys
import os
print(f"[APP.PY] Python版本: {sys.version}")
print(f"[APP.PY] Python路径: {sys.path}")

# 在导入redis之前先打印路径
print("[APP.PY] 尝试导入redis模块...")
try:
    import redis
    print(f"[APP.PY] 成功导入redis模块，路径: {redis.__file__}")
except ImportError as e:
    print(f"[APP.PY] 导入redis模块失败: {e}")
    print("[APP.PY] 检查Python路径中的site-packages:")
    for path in sys.path:
        if 'site-packages' in path and os.path.exists(path):
            redis_path = os.path.join(path, 'redis')
            redis_init = os.path.join(path, 'redis.py')
            if os.path.exists(redis_path) or os.path.exists(redis_init):
                print(f"[APP.PY] 在 {path} 中找到redis模块")
            else:
                print(f"[APP.PY] 在 {path} 中未找到redis模块")
""" + original_app_code

try:
    # 在执行前设置环境变量，以便更好地调试
    os.environ['PYTHONUNBUFFERED'] = '1'
    os.environ['PYTHONIOENCODING'] = 'utf-8'
    
    # 执行修改后的app.py代码
    print("执行修改后的app.py代码...")
    exec(modified_app_code, globals())
    
except Exception as e:
    logger.error(f"执行app.py时出错: {str(e)}")
    logger.error(f"异常详情: {traceback.format_exc()}")
    print(f"错误: 执行app.py时出错: {str(e)}")
    print(f"异常详情:")
    print(traceback.format_exc())
    sys.exit(1)