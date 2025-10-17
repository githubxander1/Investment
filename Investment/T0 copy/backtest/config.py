# T0回测系统配置文件
import os

# 项目根目录
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 回测结果保存目录
BACKTEST_DIR = os.path.join(BASE_DIR, 'backtest')
RESULTS_DIR = os.path.join(BACKTEST_DIR, 'results')
os.makedirs(RESULTS_DIR, exist_ok=True)

# 回测数据目录
BACKTEST_DATA_DIR = os.path.join(BACKTEST_DIR, 'data')
os.makedirs(BACKTEST_DATA_DIR, exist_ok=True)

# 默认回测参数
DEFAULT_INITIAL_CAPITAL = 100000  # 初始资金
DEFAULT_TRADE_AMOUNT = 100        # 每次交易数量
DEFAULT_COMMISSION_RATE = 0.0003  # 手续费率
DEFAULT_SLIPPAGE = 0.001          # 滑点

# 默认回测股票池
DEFAULT_BACKTEST_STOCKS = ['000333', '600036', '600900', '601088']

# 默认回测日期范围
DEFAULT_START_DATE = '20250901'
DEFAULT_END_DATE = '20250930'