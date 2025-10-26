"""  
T0交易系统核心模块

包含：
- data_manager: 数据管理（SQLite操作）
- indicator_loader: 指标动态加载器
- config_manager: 配置管理
"""

# 延迟导入以避免循环依赖
__all__ = ['DataManager', 'IndicatorLoader', 'ConfigManager']

def __getattr__(name):
    if name == 'DataManager':
        from .data_manager import DataManager
        return DataManager
    elif name == 'IndicatorLoader':
        from .indicator_loader import IndicatorLoader
        return IndicatorLoader
    elif name == 'ConfigManager':
        from .config_manager import ConfigManager
        return ConfigManager
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
