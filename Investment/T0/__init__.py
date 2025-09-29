"""T0交易策略模块包

这个包包含了T0交易策略的完整实现，包括指标计算、数据处理、可视化和工具函数等。

主要模块：
- indicators: 指标计算相关功能
- data: 数据获取和处理功能
- visualization: 数据可视化功能
- utils: 工具函数

主要入口：
- main.py: 主程序入口，整合所有功能
"""

# 版本信息
__version__ = "1.0.0"

# 导出主要类和函数，便于直接导入
from .main import T0Strategy