#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
配置管理模块 - 统一管理系统配置

功能：
1. 加载和保存配置文件
2. 提供配置访问接口
3. 支持运行时配置更新
4. 配置验证
"""

import json
import yaml
from pathlib import Path
from typing import Any, Dict, Optional
import logging

logger = logging.getLogger(__name__)


# 默认配置
DEFAULT_CONFIG = {
    # 股票配置
    'stocks': {
        '000333': '美的集团',
        '600030': '中信证券',
        '002415': '海康威视'
    },
    
    # 交易时段
    'trading_hours': {
        'morning': {'start': '09:30', 'end': '11:30'},
        'afternoon': {'start': '13:00', 'end': '15:00'}
    },
    
    # 数据源配置
    'data_source': {
        'primary': 'akshare',
        'fallback': 'dfcf',
        'cache_enabled': True,
        'cache_format': 'sqlite',  # sqlite/csv
        'cache_db': 'db/t0_trading.db',
        'cache_csv_dir': 'cache/fenshi_data'
    },
    
    # 指标配置
    'indicators': {
        'comprehensive_t0_strategy': {
            'enabled': True,
            'display_name': '综合T0策略',
            'color': '#1f77b4',  # blue
            'line_width': 1.5
        },
        'price_ma_deviation': {
            'enabled': True,
            'display_name': '价格偏离(基础)',
            'color': '#9467bd',  # purple
            'line_width': 1.5
        },
        'price_ma_deviation_optimized': {
            'enabled': True,
            'display_name': '价格偏离(优化)',
            'color': '#ff7f0e',  # orange
            'line_width': 1.5
        }
    },
    
    # UI配置
    'ui': {
        'theme': 'light',  # light/dark
        'window_size': {'width': 1400, 'height': 900},
        'chart_height_ratio': [3, 1, 1, 1],  # 主图:子图比例
        'font': {
            'family': 'Microsoft YaHei',
            'size': {
                'title': 14,
                'label': 11,
                'tick': 9
            }
        },
        'colors': {
            'up': '#FF3B30',      # 红色（涨）
            'down': '#34C759',    # 绿色（跌）
            'neutral': '#8E8E93', # 灰色
            'background': '#FFFFFF',
            'grid': '#E5E5EA'
        },
        'line_styles': {
            'price': {'color': 'black', 'width': 1.5},
            'avg_price': {'color': '#1f77b4', 'width': 1.2},
            'signal_line': {'color': 'purple', 'width': 1.0, 'style': '--'}
        }
    },
    
    # 实时监控配置
    'monitor': {
        'enabled': False,
        'interval': 60,  # 秒
        'notification': {
            'enabled': True,
            'sound': False,
            'desktop': True
        },
        'auto_start': False
    },
    
    # 播放控制配置
    'playback': {
        'default_speed': 1.0,
        'speed_range': [0.1, 5.0],
        'step_size': 5,  # 分钟
        'loop': False
    },
    
    # 日志配置
    'logging': {
        'level': 'INFO',
        'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        'file': 'logs/t0_trading.log',
        'max_bytes': 10 * 1024 * 1024,  # 10MB
        'backup_count': 5
    }
}


class ConfigManager:
    """配置管理器"""
    
    def __init__(self, config_file: str = None):
        """
        初始化配置管理器
        
        Args:
            config_file: 配置文件路径，默认为config/settings.yaml
        """
        if config_file is None:
            project_root = Path(__file__).parent.parent
            config_dir = project_root / 'config'
            config_dir.mkdir(exist_ok=True)
            config_file = str(config_dir / 'settings.yaml')
        
        self.config_file = Path(config_file)
        self.config: Dict = {}
        
        # 加载配置
        self._load_config()
        
        logger.info(f"配置管理器初始化完成，配置文件: {self.config_file}")
    
    def _load_config(self):
        """加载配置文件"""
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    if self.config_file.suffix == '.json':
                        self.config = json.load(f)
                    elif self.config_file.suffix in ['.yaml', '.yml']:
                        self.config = yaml.safe_load(f)
                    else:
                        logger.error(f"不支持的配置文件格式: {self.config_file.suffix}")
                        self.config = DEFAULT_CONFIG.copy()
                
                logger.info(f"成功加载配置文件: {self.config_file}")
                
                # 合并默认配置（填补缺失的配置项）
                self.config = self._merge_config(DEFAULT_CONFIG, self.config)
                
            except Exception as e:
                logger.error(f"加载配置文件失败: {e}，使用默认配置")
                self.config = DEFAULT_CONFIG.copy()
        else:
            logger.info("配置文件不存在，使用默认配置")
            self.config = DEFAULT_CONFIG.copy()
            # 保存默认配置到文件
            self.save_config()
    
    def _merge_config(self, default: Dict, custom: Dict) -> Dict:
        """
        递归合并配置字典
        
        Args:
            default: 默认配置
            custom: 自定义配置
            
        Returns:
            合并后的配置
        """
        result = default.copy()
        
        for key, value in custom.items():
            if key in result and isinstance(result[key], dict) and isinstance(value, dict):
                result[key] = self._merge_config(result[key], value)
            else:
                result[key] = value
        
        return result
    
    def save_config(self):
        """保存配置到文件"""
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                if self.config_file.suffix == '.json':
                    json.dump(self.config, f, indent=2, ensure_ascii=False)
                elif self.config_file.suffix in ['.yaml', '.yml']:
                    yaml.safe_dump(self.config, f, allow_unicode=True, default_flow_style=False)
            
            logger.info(f"配置已保存到: {self.config_file}")
        except Exception as e:
            logger.error(f"保存配置文件失败: {e}")
    
    def get(self, key: str, default: Any = None) -> Any:
        """
        获取配置项（支持点号分隔的嵌套键）
        
        Args:
            key: 配置键，如 'ui.theme' 或 'stocks'
            default: 默认值
            
        Returns:
            配置值
        """
        keys = key.split('.')
        value = self.config
        
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default
        
        return value
    
    def set(self, key: str, value: Any):
        """
        设置配置项（支持点号分隔的嵌套键）
        
        Args:
            key: 配置键
            value: 配置值
        """
        keys = key.split('.')
        config = self.config
        
        # 导航到倒数第二层
        for k in keys[:-1]:
            if k not in config:
                config[k] = {}
            config = config[k]
        
        # 设置最后一层的值
        config[keys[-1]] = value
        logger.debug(f"设置配置: {key} = {value}")
    
    def get_stocks(self) -> Dict[str, str]:
        """获取股票配置"""
        return self.get('stocks', {})
    
    def get_trading_hours(self) -> Dict:
        """获取交易时段"""
        return self.get('trading_hours', {})
    
    def get_indicators_config(self) -> Dict:
        """获取指标配置"""
        return self.get('indicators', {})
    
    def get_ui_config(self) -> Dict:
        """获取UI配置"""
        return self.get('ui', {})
    
    def is_monitor_enabled(self) -> bool:
        """是否启用实时监控"""
        return self.get('monitor.enabled', False)
    
    def get_monitor_interval(self) -> int:
        """获取监控间隔（秒）"""
        return self.get('monitor.interval', 60)
    
    def reload(self):
        """重新加载配置文件"""
        self._load_config()
        logger.info("配置已重新加载")


# ==================== 使用示例 ====================

if __name__ == '__main__':
    import logging
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    
    # 创建配置管理器
    config = ConfigManager()
    
    # 读取配置
    print("\n=== 股票配置 ===")
    print(config.get_stocks())
    
    print("\n=== 交易时段 ===")
    print(config.get_trading_hours())
    
    print("\n=== 指标配置 ===")
    indicators = config.get_indicators_config()
    for name, info in indicators.items():
        print(f"- {name}: {info.get('display_name')}, 启用: {info.get('enabled')}")
    
    print("\n=== UI配置 ===")
    ui = config.get_ui_config()
    print(f"主题: {ui.get('theme')}")
    print(f"窗口大小: {ui.get('window_size')}")
    
    # 修改配置
    config.set('ui.theme', 'dark')
    print(f"\n修改后的主题: {config.get('ui.theme')}")
    
    # 保存配置
    config.save_config()
    print(f"\n配置已保存到: {config.config_file}")
