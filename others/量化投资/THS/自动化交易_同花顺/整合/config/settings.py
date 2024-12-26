# config/settings.py
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 文件路径配置
LOGS_DIR = os.path.join(BASE_DIR, 'logs')
DATA_DIR = os.path.join(BASE_DIR, 'data')

# 日志文件路径
THS_AUTO_TRADE_LOG_FILE = os.path.join(LOGS_DIR, '自动化交易日志.log')
THS_AUTO_TRADE_LOG_FILE_PAGE = os.path.join(LOGS_DIR, '自动化交易日志_page.log')
STRATEGY_TODAY_ADJUSTMENT_LOG_FILE = os.path.join(LOGS_DIR, '策略_今天调仓.log')
COMBINATION_TODAY_ADJUSTMENT_LOG_FILE = os.path.join(LOGS_DIR, '组合_今天调仓.log')
SCHEDULER_LOG_FILE = os.path.join(LOGS_DIR, '自动化交易定时任务.log')

file_monitor_file = os.path.join(LOGS_DIR, '文件监控.log')
trade_operations_log_file = os.path.join(LOGS_DIR, '自动化交易操作记录.log')

# 数据文件路径
OPERATION_HISTORY_FILE = os.path.join(DATA_DIR, '交易操作历史.xlsx')
SUCCESSFUL_OPERATIONS_FILE = os.path.join(DATA_DIR, '自动化交易操作历史_成功.xlsx')
STRATEGY_TODAY_ADJUSTMENT_FILE = os.path.join(DATA_DIR, '策略今天调仓.xlsx')
COMBINATION_TODAY_ADJUSTMENT_FILE = os.path.join(DATA_DIR, '组合今天调仓.xlsx')

OPRATION_RECORD_DONE_FILE = os.path.join(DATA_DIR, '调仓操作记录完成.flag')

# 监控文件夹
WATCHED_FOLDER = os.path.join(DATA_DIR)

# API配置
API_URL = "https://ms.10jqka.com.cn/iwencai/iwc-web-business-center/strategy_unify/strategy_profit"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Linux; Android 10; Redmi Note 7 Pro Build/QKQ1.190915.002; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/87.0.4280.101 Mobile Safari/537.36 Hexin_Gphone/11.16.10 (Royal Flush) hxtheme/1 innerversion/G037.08.980.1.32 followPhoneSystemTheme/1 userid/641926488 getHXAPPAccessibilityMode/0 hxNewFont/1 isVip/0 getHXAPPFontSetting/normal getHXAPPAdaptOldSetting/0",
    "Accept": "*/*",
    "Origin": "https://bowerbird.10jqka.com.cn",
    "X-Requested-With": "com.hexin.plat.android",
    "Sec-Fetch-Site": "same-site",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Dest": "empty",
    "Referer": "https://bowerbird.10jqka.com.cn/thsic/editor/view/15f2E0a579?strategyId={strategy_id}",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7"
}

# 组合 手动创建组合ID到组合名称的映射
COMBINATION_ID_TO_NAME = {
    '13081': '好赛道出牛股',
    '16281': '每天进步一点点',
    '18565': '龙头一年三倍',

    '7152': '中线龙头',
    '6994': '梦想一号',
    '11094': '低位题材',
    '14980': '波段突击'
}

STRATEGY_ID_TO_NAME = {
    '137789': '高现金高毛利战法',
    '138006': '连续五年优质股战法',
    '155259': 'TMT资金流入战法',
    '155270': '中字头概念',
    '118188': '均线粘合平台突破',
    '138036': '低价小盘股战法',
    # '136567': '净利润同比大增低估值战法',
    # '138220': '高roic低市盈率战法'
}