# Configuration settings for T0 trading system
import os
from datetime import time

# 项目根目录
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE_DIR = PROJECT_ROOT  # 兼容旧代码

# 数据目录
DATA_DIR = os.path.join(PROJECT_ROOT, 'data')
LOGS_DIR = os.path.join(PROJECT_ROOT, 'logs')
PLOTS_DIR = os.path.join(PROJECT_ROOT, 'plots')
CHARTS_DIR = os.path.join(PROJECT_ROOT, 'output', 'charts')  # 兼容旧代码
CACHE_DIR = os.path.join(PROJECT_ROOT, 'cache')

# 代理设置
PROXY_SETTINGS = {
    'enable_proxy': False,  # 是否启用代理
    'http_proxy': 'http://127.0.0.1:10809',  # HTTP代理地址
    'https_proxy': 'http://127.0.0.1:10809',  # HTTPS代理地址
}

# 确保目录存在
for dir_path in [DATA_DIR, LOGS_DIR, PLOTS_DIR, CHARTS_DIR, CACHE_DIR]:
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)


stocks = {
    '000333': '美的集团',
    '600030': '中信证券',
    '000001': '上证指数',
    '000002': '深圳成指',
    '399001': '深证成指',
    '513330': '恒生互联网ETF',
    '513050': '中概互联ETF',
}
# 默认股票池
DEFAULT_STOCK_POOL = ['510050', '510330']  
# 交易配置
TRADE_QUANTITY = 100  # 每次交易数量
MINIMUM_HOLDING = 100  # 最低持仓数量（股）
MAX_POSITION_PERCENT = 0.2  # 单个股票最大仓位比例
TOTAL_CAPITAL = 100000  # 总资金
MAX_DAILY_LOSS = 0.02  # 每日最大亏损比例
STOP_LOSS_RATIO = 0.1  # 止损比例
TAKE_PROFIT_RATIO = 0.2  # 止盈比例

# 监控配置
MONITOR_INTERVAL = 60  # 监控间隔（秒）
DATA_REFRESH_INTERVAL = 15  # 数据刷新间隔（秒）
MAX_RETRY_COUNT = 3  # 最大重试次数
RETRY_DELAY = 2  # 重试延迟（秒）

# 交易时间配置
TRADING_HOURS = {
    'morning_start': time(9, 30),
    'morning_end': time(11, 30),
    'afternoon_start': time(13, 0),
    'afternoon_end': time(15, 0)
}

# 数据配置
HISTORY_DAYS = 60  # 历史数据天数
MAX_DATA_POINTS = 1000  # 最大数据点数量

# 指标配置
INDICATOR_PARAMS = {
    'rsi_period': 14,
    'macd_fast': 12,
    'macd_slow': 26,
    'macd_signal': 9,
    'bb_period': 20,
    'bb_std_dev': 2.0,
    'ma_periods': [5, 10, 20, 60],
    'support_resistance_period': 20,
    'signal_threshold': 0.01,
    # 价格均线偏离策略参数
    'price_ma_deviation_period': 5,
    'price_ma_deviation_threshold': 0.3,
    # 波动率策略参数
    'volatility_window': 20,
    'volatility_multiplier': 2.0,
    # 动量反转策略参数
    'momentum_window': 10,
    'reversal_threshold': 0.5
}

# 日志配置
LOG_CONFIG = {
    'level': 'INFO',
    'file_max_bytes': 10485760,  # 10MB
    'backup_count': 5,
    'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
}

# 信号记录文件（兼容旧代码）
SIGNAL_RECORD_FILE = os.path.join(LOGS_DIR, 'signal_records.txt')
results = LOGS_DIR  # 兼容旧代码

# 策略配置
STRATEGY_CONFIG = {
    'signal_strength_threshold': 5.0,  # 信号强度阈值
    'min_volume_ratio': 1.5,  # 最小量比
    'max_price_change': 0.03,  # 最大价格变动比例
    'enable_tdx_indicators': True,  # 是否启用通达信指标
    'enable_technical_indicators': True,  # 是否启用技术指标
    'use_multiple_indicators': True  # 是否使用多指标综合判断
}

# 风险控制配置
RISK_CONTROL = {
    'max_positions': 10,
    'max_daily_trades': 50,
    'max_drawdown': 0.1,  # 最大回撤比例
    'enable_trailing_stop': True,
    'trailing_stop_ratio': 0.01
}

# 常量定义
TRADE_TYPES = {
    'BUY': 'BUY',
    'SELL': 'SELL'
}

SIGNAL_TYPES = {
    'BUY': 'BUY',
    'SELL': 'SELL',
    'HOLD': 'HOLD',
    'UNKNOWN': 'UNKNOWN'
}

# 错误码定义
ERROR_CODES = {
    'SUCCESS': 0,
    'DATA_FETCH_FAILED': 1001,
    'INVALID_STOCK_CODE': 1002,
    'TRADE_FAILED': 1003,
    'INSUFFICIENT_FUNDS': 1004,
    'OUTSIDE_TRADING_HOURS': 1005,
    'API_LIMIT_EXCEEDED': 1006,
    'DATA_PARSE_ERROR': 1007,
    'CONFIG_ERROR': 1008,
    'UNKNOWN_ERROR': 9999
}

# 验证配置有效性
def validate_config():
    """
    验证配置有效性
    
    返回:
    bool: 配置是否有效
    """
    try:
        # 验证交易时间配置
        if TRADING_HOURS['morning_start'] >= TRADING_HOURS['morning_end']:
            raise ValueError("上午交易时间配置错误")
        if TRADING_HOURS['afternoon_start'] >= TRADING_HOURS['afternoon_end']:
            raise ValueError("下午交易时间配置错误")
        
        # 验证比例配置
        if not (0 < MAX_POSITION_PERCENT <= 1):
            raise ValueError("单个股票最大仓位比例配置错误")
        if not (0 < MAX_DAILY_LOSS <= 1):
            raise ValueError("每日最大亏损比例配置错误")
        if not (0 < STOP_LOSS_RATIO <= 1):
            raise ValueError("止损比例配置错误")
        if not (0 < TAKE_PROFIT_RATIO <= 1):
            raise ValueError("止盈比例配置错误")
        
        # 验证监控间隔
        if MONITOR_INTERVAL <= 0:
            raise ValueError("监控间隔必须大于0")
        
        # 验证股票池
        if not DEFAULT_STOCK_POOL:
            raise ValueError("股票池不能为空")
        
        return True
        
    except Exception as e:
        print(f"配置验证失败: {e}")
        return False


# 导出配置
__all__ = [
    'PROJECT_ROOT',
    'BASE_DIR',  # 兼容旧代码
    'DATA_DIR',
    'LOGS_DIR',
    'PLOTS_DIR',
    'CHARTS_DIR',  # 兼容旧代码
    'CACHE_DIR',
    'PROXY_SETTINGS',  # 代理设置
    'DEFAULT_STOCK_POOL',
    'TRADE_QUANTITY',
    'MINIMUM_HOLDING',
    'MAX_POSITION_PERCENT',
    'TOTAL_CAPITAL',
    'MAX_DAILY_LOSS',
    'STOP_LOSS_RATIO',
    'TAKE_PROFIT_RATIO',
    'MONITOR_INTERVAL',
    'DATA_REFRESH_INTERVAL',
    'MAX_RETRY_COUNT',
    'RETRY_DELAY',
    'TRADING_HOURS',
    'HISTORY_DAYS',
    'MAX_DATA_POINTS',
    'INDICATOR_PARAMS',
    'LOG_CONFIG',
    'SIGNAL_RECORD_FILE',  # 兼容旧代码
    'results',  # 兼容旧代码
    'STRATEGY_CONFIG',
    'RISK_CONTROL',
    'TRADE_TYPES',
    'SIGNAL_TYPES',
    'ERROR_CODES',
    'validate_config'
]


# 模块初始化时验证配置
validate_config()