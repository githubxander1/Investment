# T0交易系统配置文件
import os

# 项目根目录
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 股票池配置 - 使用美的集团和中信证券进行测试
DEFAULT_STOCK_POOL = ['000333', '600030']  # 000333美的集团，600030中信证券

# 监控间隔（秒）
MONITOR_INTERVAL = 60

# 交易数量
TRADE_QUANTITY = 100

# 最低持仓数量（股）
MINIMUM_HOLDING = 100

# 信号记录文件
SIGNAL_RECORD_FILE = os.path.join(BASE_DIR, 'logs', 'signal_records.txt')
results = os.path.join(BASE_DIR, 'logs')

# 图表保存目录
CHARTS_DIR = os.path.join(BASE_DIR, 'output', 'charts')
os.makedirs(CHARTS_DIR, exist_ok=True)

# 缓存目录
CACHE_DIR = os.path.join(BASE_DIR, 'cache')
os.makedirs(CACHE_DIR, exist_ok=True)

# 确保日志目录存在
os.makedirs(os.path.join(BASE_DIR, 'logs'), exist_ok=True)