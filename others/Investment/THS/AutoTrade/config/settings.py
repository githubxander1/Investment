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
ETF_ADJUSTMENT_LOG_FILE = os.path.join(LOGS_DIR, 'ETF今天调仓.log')

SCHEDULER_LOG_FILE = os.path.join(LOGS_DIR, '自动化交易定时任务.log')
send_notification = os.path.join(LOGS_DIR, '发送通知.log')
file_monitor_file = os.path.join(LOGS_DIR, '文件监控.log')
trade_operations_log_file = os.path.join(LOGS_DIR, '自动化交易操作记录.log')

# 数据文件路径
OPERATION_HISTORY_FILE = os.path.join(DATA_DIR, '交易操作历史.csv')
SUCCESSFUL_OPERATIONS_FILE = os.path.join(DATA_DIR, '自动化交易操作历史_成功.csv')

STRATEGY_TODAY_ADJUSTMENT_FILE = os.path.join(DATA_DIR, '策略今天调仓.csv')
ETF_Combination_TODAY_ADJUSTMENT_FILE = os.path.join(DATA_DIR, 'Etf_stock_portfolio_today.csv')
# COMBINATION_TODAY_ADJUSTMENT_FILE = os.path.join(DATA_DIR, '组合今天调仓.csv')

ETF_NEWEST_ADJUSTMENT_FILE = os.path.join(DATA_DIR, 'ETF最新调仓_所有.csv')
ETF_adjustment_holding_file = os.path.join(DATA_DIR, 'etf_stock_position.xlsx')
Combination_info_file = os.path.join(DATA_DIR, '股票组合持仓_历史调仓_今天调仓.csv')

compare_ETF_info_file = os.path.join(DATA_DIR, 'ETF组合对比.xlsx')
# compare_Strategy_info_file = os.path.join(DATA_DIR, '策略信息.csv')
compare_Combination_info_file = os.path.join(DATA_DIR, '股票组合对比.csv')

Strategy_info_file = os.path.join(DATA_DIR, '策略信息.csv')
Combination_list_file = os.path.join(DATA_DIR, '组合列表.xlsx')
Strategy_list_file = os.path.join(DATA_DIR, '策略列表.csv')
Strategy_metrics_file = os.path.join(DATA_DIR, '策略对比.csv')
#ai诊断文件
Ai_file = os.path.join(DATA_DIR, 'ai_诊股结果.csv')

Holding_Stockes_info_file = os.path.join(DATA_DIR, '账户持仓信息.csv')

TEMP_ADJUSTMENT_FILE = os.path.join(DATA_DIR, '调仓操作记录.csv')

CLEAR_FLAG_FILE = os.path.join(DATA_DIR, '清仓昨天操作记录.flag')

OPRATION_RECORD_DONE_FILE = os.path.join(DATA_DIR, '调仓操作记录完成.flag')

# 监控文件夹
WATCHED_FOLDER = os.path.join(DATA_DIR)

# API配置
API_URL = "https://ms.10jqka.com.cn/iwencai/iwc-web-business-center/strategy_unify/strategy_profit"
Combination_headers = {
        "Host": "t.10jqka.com.cn",
        "Connection": "keep-alive",
        "Accept": "application/json, text/plain, */*",
        "User-Agent": "Mozilla/5.0 (Linux; Android 10; Redmi Note 7 Pro Build/QKQ1.190915.002; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/87.0.4280.101 Mobile Safari/537.36 Hexin_Gphone/11.16.10 (Royal Flush) hxtheme/1 innerversion/G037.08.980.1.32 followPhoneSystemTheme/1 userid/641926488 getHXAPPAccessibilityMode/0 hxNewFont/1 isVip/0 getHXAPPFontSetting/normal getHXAPPAdaptOldSetting/0",
        "Content-Type": "application/x-www-form-urlencoded",
        "X-Requested-With": "com.hexin.plat.android",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Dest": "empty",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
        #20250509 9:42
        "Cookie": 'userid=641926488; u_name=mo_641926488; escapename=mo_641926488; user_status=0; IFUserCookieKey={"escapename":"mo_641926488","userid":"641926488","custid":"100113495581"}; _clck=l14ts7%7C2%7Cfv9%7C0%7C0; _clck=l14ts7%7C2%7Cfv9%7C0%7C0; _clsk=1mnl85m%7C1745213579117%7C1%7C1%7C; user=MDptb182NDE5MjY0ODg6Ok5vbmU6NTAwOjY1MTkyNjQ4ODo3LDExMTExMTExMTExLDQwOzQ0LDExLDQwOzYsMSw0MDs1LDEsNDA7MSwxMDEsNDA7MiwxLDQwOzMsMSw0MDs1LDEsNDA7OCwwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMSw0MDsxMDIsMSw0MDoyNzo6OjY0MTkyNjQ4ODoxNzQ2OTYxMzcxOjo6MTY1ODE0Mjc4MDoyNjc4NDAwOjA6MWE0ZGNmZTg2NmFkYmE4ZWI2Y2I0OTdkZDBkNDUzM2VhOjox; userid=641926488; u_name=mo_641926488; escapename=mo_641926488; ticket=9f3bd3da8c83f79c4fc92386aec0b43f; user_status=0; user=MDptb182NDE5MjY0ODg6Ok5vbmU6NTAwOjY1MTkyNjQ4ODo3LDExMTExMTExMTExLDQwOzQ0LDExLDQwOzYsMSw0MDs1LDEsNDA7MSwxMDEsNDA7MiwxLDQwOzMsMSw0MDs1LDEsNDA7OCwwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMSw0MDsxMDIsMSw0MDoyNzo6OjY0MTkyNjQ4ODoxNzQ2OTYxMzcxOjo6MTY1ODE0Mjc4MDoyNjc4NDAwOjA6MWE0ZGNmZTg2NmFkYmE4ZWI2Y2I0OTdkZDBkNDUzM2VhOjox; ticket=9f3bd3da8c83f79c4fc92386aec0b43f; hxmPid=ths_mob_hotmap; v=AyvurZQYx1IF7RsGIlCo_CkQuEQVQD_DuVUDdp2oB7nBt0Q-JRDPEskkk8yu; hxmPid=hqMarketPkgVersionControl; v=A2uubdTYh5OladtHnVRovGnQ-IRVgH8C-ZRDtt3oR6oBfIR-ZVAPUglk0wfu'
    }

Strategy_ids = ['155680', '137789', '138006', '155273']
Strategy_id_to_name = {
        '155680': 'GPT定期精选',#技术面
        '137789': '高现金毛利战法',#基本面
        '138006': '连续五年优质股战法',#基本面
        '155273': '国资云概念'#消息面  两个创业板

        # '138036': '低价小盘股战法',
        # '155270': '中字头概念',
        # '136567': '净利润同比大增低估值战法',
        # '138127': '归母净利润高战法',
        # '118188': '均线粘合平台突破'
    }


# 组合 手动创建组合ID到组合名称的映射
Combination_ids = ['19347', '9564', '11094', '7152']
# Combination_ids = [ 16281, 19347, 6994]
Combination_ids_to_name = {
    '19347': '超短稳定复利',
    '11094': '低位题材埋伏',#胜率高，回撤小，收益高
    '7152': '中线龙头',#胜率低，收益高
    '9564': '梦想二号',# 长期

    '13081': '好赛道出牛股',#19年，稳 7
    # '18565': '龙头一年三倍',
    '16281': '每天进步一点点', #13
    '14980': '波段突击',#胜率高 落后15

    # '18710': '用收益率征服您'
}

# ETF_ids = [ '29617', '29669', '29678', '29734', '29656']
ETF_ids = [ '29762', '30463', '29684', '29778']
ETF_ids_to_name = {
    '29762': '全球领先ETF',
    '30463': '科技ETF高频',
    '29684': '主题成长优选',
    '29778': '波段轮动优选',


    '29617': 'ETF灵蛇智投',
    '29669': '波段优选ETF',
    # '29734': '热点追击ETF',
    '29656': '龙头驾到ETF',

    "31672": "短线趋势题材",
    "29774": "智投短线精选",
    "31816": "一只不休息的牛",
    # '29678': '科技腾飞精选',
    # '27122': '热点多因子驱动',#失效
    # '29665': '轮动寻金ETF', #排名落后了
    # '29646': '热点追踪猎手'
}

zhitou_ids = [ '31672', '29774', '31816']
zhitou_ids_to_name = {
    "31672": "短线趋势题材",
    "29774": "智投短线精选",
    "31816": "一只不休息的牛",
}

all_ids = Combination_ids + ETF_ids + zhitou_ids
id_to_name = {**Combination_ids_to_name, **ETF_ids_to_name, **zhitou_ids_to_name}
# for id in ETF_ids:
#     print(ETF_ids_to_name.get(id,'未知'))