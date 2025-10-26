#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
指标加载器 - 动态加载和管理交易指标

功能：
1. 自动发现indicators目录下的指标模块
2. 动态加载指标
3. 验证指标接口
4. 提供指标元数据
"""

import importlib
import inspect
from pathlib import Path
from typing import Dict, List, Callable, Optional
import logging

logger = logging.getLogger(__name__)


class IndicatorLoader:
    """指标加载器 - 插件化指标管理"""
    
    def __init__(self, indicators_dir: str = None):
        """
        初始化指标加载器
        
        Args:
            indicators_dir: 指标模块目录，默认为项目根目录下的indicators
        """
        if indicators_dir is None:
            project_root = Path(__file__).parent.parent
            indicators_dir = str(project_root / 'indicators')
        
        self.indicators_dir = Path(indicators_dir)
        self.indicators: Dict[str, Dict] = {}
        
        # 加载所有指标
        self._load_all_indicators()
        
        logger.info(f"指标加载器初始化完成，加载了 {len(self.indicators)} 个指标")
    
    def _load_all_indicators(self):
        """自动加载所有指标模块"""
        if not self.indicators_dir.exists():
            logger.error(f"指标目录不存在: {self.indicators_dir}")
            return
        
        # 遍历indicators目录下的所有.py文件
        for py_file in self.indicators_dir.glob('*.py'):
            # 跳过__init__.py和私有文件
            if py_file.name.startswith('_') or py_file.name.startswith('test'):
                continue
            
            module_name = py_file.stem
            
            try:
                self._load_indicator(module_name)
            except Exception as e:
                logger.error(f"加载指标模块失败: {module_name}, 错误: {e}")
    
    def _load_indicator(self, module_name: str):
        """
        加载单个指标模块
        
        Args:
            module_name: 模块名称（不含.py后缀）
        """
        try:
            # 动态导入模块
            module_path = f"indicators.{module_name}"
            module = importlib.import_module(module_path)
            
            # 查找analyze函数（指标的标准接口）
            analyze_func = None
            func_name = None
            
            # 优先查找特定名称的analyze函数
            for name in [f'analyze_{module_name}', 'analyze', 'calculate']:
                if hasattr(module, name) and callable(getattr(module, name)):
                    analyze_func = getattr(module, name)
                    func_name = name
                    break
            
            # 如果还没找到，查找所有以analyze开头的函数
            if not analyze_func:
                for name, obj in inspect.getmembers(module, inspect.isfunction):
                    if name.startswith('analyze_'):
                        analyze_func = obj
                        func_name = name
                        break
            
            if not analyze_func:
                logger.warning(f"指标模块 {module_name} 没有找到analyze函数，跳过")
                return
            
            # 验证函数签名
            sig = inspect.signature(analyze_func)
            params = list(sig.parameters.keys())
            
            # 至少需要一个DataFrame参数
            if not params:
                logger.warning(f"指标函数 {func_name} 没有参数，跳过")
                return
            
            # 提取元数据
            doc = inspect.getdoc(analyze_func) or ""
            
            # 尝试从模块获取显示名称和描述
            display_name = getattr(module, 'INDICATOR_NAME', module_name)
            description = getattr(module, 'INDICATOR_DESC', doc.split('\n')[0] if doc else "")
            
            # 注册指标
            self.indicators[module_name] = {
                'module': module,
                'function': analyze_func,
                'function_name': func_name,
                'display_name': display_name,
                'description': description,
                'parameters': params,
                'doc': doc
            }
            
            logger.info(f"成功加载指标: {module_name} ({display_name})")
            
        except ImportError as e:
            logger.error(f"导入指标模块失败: {module_name}, 错误: {e}")
        except Exception as e:
            logger.error(f"加载指标模块时发生错误: {module_name}, 错误: {e}")
    
    def get_indicator(self, indicator_name: str) -> Optional[Dict]:
        """
        获取指标信息
        
        Args:
            indicator_name: 指标名称
            
        Returns:
            指标信息字典，如果不存在则返回None
        """
        return self.indicators.get(indicator_name)
    
    def get_all_indicators(self) -> Dict[str, Dict]:
        """获取所有已加载的指标"""
        return self.indicators.copy()
    
    def list_indicator_names(self) -> List[str]:
        """获取所有指标名称列表"""
        return list(self.indicators.keys())
    
    def execute_indicator(self, indicator_name: str, *args, **kwargs):
        """
        执行指标分析函数
        
        Args:
            indicator_name: 指标名称
            *args: 位置参数
            **kwargs: 关键字参数
            
        Returns:
            指标分析结果
        """
        indicator = self.get_indicator(indicator_name)
        if not indicator:
            raise ValueError(f"指标不存在: {indicator_name}")
        
        analyze_func = indicator['function']
        
        try:
            result = analyze_func(*args, **kwargs)
            logger.debug(f"成功执行指标: {indicator_name}")
            return result
        except Exception as e:
            logger.error(f"执行指标失败: {indicator_name}, 错误: {e}")
            raise
    
    def reload_indicator(self, indicator_name: str):
        """
        重新加载指标（用于开发时热更新）
        
        Args:
            indicator_name: 指标名称
        """
        if indicator_name in self.indicators:
            old_module = self.indicators[indicator_name]['module']
            importlib.reload(old_module)
            self._load_indicator(indicator_name)
            logger.info(f"重新加载指标: {indicator_name}")
        else:
            logger.warning(f"指标不存在，无法重新加载: {indicator_name}")
    
    def get_indicator_metadata(self) -> List[Dict]:
        """
        获取所有指标的元数据（用于UI显示）
        
        Returns:
            指标元数据列表
        """
        metadata = []
        for name, info in self.indicators.items():
            metadata.append({
                'name': name,
                'display_name': info['display_name'],
                'description': info['description'],
                'function_name': info['function_name']
            })
        return metadata


# ==================== 使用示例 ====================

if __name__ == '__main__':
    import logging
    import pandas as pd
    
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    
    # 创建指标加载器
    loader = IndicatorLoader()
    
    # 列出所有指标
    print("\n=== 已加载的指标 ===")
    for name in loader.list_indicator_names():
        info = loader.get_indicator(name)
        print(f"- {name}: {info['display_name']}")
        print(f"  函数: {info['function_name']}")
        print(f"  参数: {info['parameters']}")
        print(f"  描述: {info['description'][:100]}...")
        print()
    
    # 获取元数据
    print("\n=== 指标元数据 ===")
    metadata = loader.get_indicator_metadata()
    for meta in metadata:
        print(f"- {meta['display_name']}: {meta['description'][:50]}...")
