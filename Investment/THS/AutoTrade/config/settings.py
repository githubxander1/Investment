# config/settings.py
import os
from pprint import pprint

from fake_useragent import UserAgent

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

package_name = 'com.hexin.plat.android'
# 文件路径配置
LOGS_DIR = os.path.join(BASE_DIR, 'logs')
DATA_DIR = os.path.join(BASE_DIR, 'data')

# 日志文件路径
THS_AUTO_TRADE_LOG_FILE_PAGE = os.path.join(LOGS_DIR, 'ths_page_logic.log')
STRATEGY_TODAY_ADJUSTMENT_LOG_FILE = os.path.join(LOGS_DIR, 'strategy_portfolio_today.log')
COMBINATION_TODAY_ADJUSTMENT_LOG_FILE = os.path.join(LOGS_DIR, 'combination_portfolio_today.log')
trade_operations_log_file = os.path.join(LOGS_DIR, 'data_process.log')

# 数据文件路径
OPERATION_HISTORY_FILE = os.path.join(DATA_DIR, 'trade_operation_history.xlsx')


Strategy_portfolio_today = os.path.join(DATA_DIR, 'Strategy_portfolio_today.xlsx')
Combination_portfolio_today = os.path.join(DATA_DIR, 'Combination_portfolio_today.xlsx')

Combination_holding_file = os.path.join(DATA_DIR, 'Combination_position.xlsx')

compare_ETF_info_file = os.path.join(DATA_DIR, 'ETF组合对比.xlsx')

Strategy_info_file = os.path.join(DATA_DIR, '策略信息.csv')
Combination_list_file = os.path.join(DATA_DIR, '组合列表.xlsx')
Strategy_list_file = os.path.join(DATA_DIR, '策略列表.csv')
Strategy_metrics_file = os.path.join(DATA_DIR, '策略对比.xlsx')
#ai诊断文件
Ai_file = os.path.join(DATA_DIR, 'ai_诊股结果.csv')

Account_holding_stockes_info_file = os.path.join(DATA_DIR, 'account_info.xlsx')
account_xml_file: str = os.path.join(DATA_DIR, 'account_info_xml.xml')


fake_useragent = UserAgent()

# API配置
API_URL = "https://ms.10jqka.com.cn/iwencai/iwc-web-business-center/strategy_unify/strategy_profit"
Combination_headers = {
        # "Host": "dq.py.10jqka.com.cn",
        "Connection": "keep-alive",
        "Accept": "application/json, text/plain, */*",
        # "User-Agent": "Mozilla/5.0 (Linux; Android 10; Redmi Note 7 Pro Build/QKQ1.190915.002; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/87.0.4280.101 Mobile Safari/537.36 Hexin_Gphone/11.16.10 (Royal Flush) hxtheme/1 innerversion/G037.08.980.1.32 followPhoneSystemTheme/1 userid/641926488 getHXAPPAccessibilityMode/0 hxNewFont/1 isVip/0 getHXAPPFontSetting/normal getHXAPPAdaptOldSetting/0",
        "User-Agent": fake_useragent.random,
        "Content-Type": "application/x-www-form-urlencoded",
        "X-Requested-With": "com.hexin.plat.android",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Dest": "empty",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
        # "Referer": "https://t.10jqka.com.cn/portfolioFront/historyTransfer.html?id=14533", #可网页看
        #20250509 9:42 20250623
        "Cookie": 'user_status=0; hxmPid=adm_sjpopfuceng_441325; user=MDptb182NDE5MjY0ODg6Ok5vbmU6NTAwOjY1MTkyNjQ4ODo3LDExMTExMTExMTExLDQwOzQ0LDExLDQwOzYsMSw0MDs1LDEsNDA7MSwxMDEsNDA7MiwxLDQwOzMsMSw0MDs1LDEsNDA7OCwwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMSw0MDsxMDIsMSw0MDoyNzo6OjY0MTkyNjQ4ODoxNzUxMjQ2MTQxOjo6MTY1ODE0Mjc4MDoyNjc4NDAwOjA6MWMzNWY3ZWZlZGIyZWYwNjliOGVkZTdlODEwNzdjM2EyOjox; userid=641926488; u_name=mo_641926488; escapename=mo_641926488; ticket=b5eafad7a376b45f8bc0e43df793dfbc; IFUserCookieKey={"userid":"641926488","escapename":"mo_641926488","custid":""}; v=A_jcG90c5DqZ6Qi-GGN21lvXwK2KYVzhvsUwbzJpRDPmTZeX2nEsew7VAOaB'
        # "Cookie": 'uid=CvQTumg397R8rXMQBSppAg==; user=MDptb182NDE5MjY0ODg6Ok5vbmU6NTAwOjY1MTkyNjQ4ODo3LDExMTExMTExMTExLDQwOzQ0LDExLDQwOzYsMSw0MDs1LDEsNDA7MSwxMDEsNDA7MiwxLDQwOzMsMSw0MDs1LDEsNDA7OCwwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMSw0MDsxMDIsMSw0MDoyNzo6OjY0MTkyNjQ4ODoxNzQ5ODA1MTk1Ojo6MTY1ODE0Mjc4MDoyNjc4NDAwOjA6MWU5NThhYTRmYjRiYzZlM2RhMmI5NzU0MDI0ZGYzODU0Ojox; userid=641926488; u_name=mo_641926488; escapename=mo_641926488; ticket=d19d7223e7976c9acf0df29f2bcb2d69; user_status=0; IFUserCookieKey={"userid":"641926488","escapename":"mo_641926488","custid":""}; v=AwzMLPM8iAfDvpx7o4R4cs9M1GE-RbDvsunEs2bNGLda8aNbjlWAfwL5lEm1'
    }

Strategy_ids = ['155680', '136574', '137789']
Strategy_id_to_name = {
        '155680': 'GPT定期精选',#技术面
        '155265': '中字头资金流入战法', #资金面
        '136574': '低价小市值股战法', #技术面
        # '136509': '缩量绩优小盘股战法', #技术面

        '137789': '高现金毛利战法',#基本面
        # '155259': 'TMT资金流入战法',#资金面，停留，最新250218
        # '138006': '连续五年优质股战法',#基本面
        # '155273': '国资云概念',#消息面  两个创业板

        # '138386': '主力控盘低价股战法'# 基本面
        # '138036': '低价小盘股战法',#基本面
        # '155270': '中字头概念',# 基本面
        # '136567': '净利润同比大增低估值战法',
        # '138127': '归母净利润高战法',
        # '118188': '均线粘合平台突破'
    }


# 组合 手动创建组合ID到组合名称的映射
Combination_ids = ['11094', '7152','19347']
Combination_ids_to_name = {
    '7152': '组-中线龙头',#胜率低，收益高
    '11094': '组-低位题材埋伏',#胜率高，回撤小，收益高
    # '9564': '梦想二号',# 长期

    '19347': '超短稳定复利',# 变收费
    '13081': '好赛道出牛股',#19年，稳 7
    # '18565': '龙头一年三倍',
    '16281': '每天进步一点点', #13
    '14980': '波段突击',#胜率高 落后15

    # '18710': '用收益率征服您'
}

ETF_ids = ['29684', "29634"]
ETF_ids_to_name = {
    # '29762': '全球领先ETF',
    # '29778': '波段轮动优选ETF',#列表没了？
    '29684': 'ETF-主题成长优选',
    '29634': 'ETF-主题轮动精选',

    # '30463': '科技ETF高频',
    # '29669': '波段优选ETF',
    # '29656': '龙头驾到ETF',
    # '29617': 'ETF灵蛇智投',
    # '29734': '热点追击ETF',

    # '29678': '科技腾飞精选',
    # '27122': '热点多因子驱动',#失效
    # '29665': '轮动寻金ETF', #排名落后了
    # '29646': '热点追踪猎手'
}

zhitou_ids = ['31670','31672']
zhitou_ids_to_name = {
    '31670': '赛-情绪拐点龙头战法',

    "31672": "赛-短线趋势题材",
    "31519": "赛-KD跟踪策略",
    "31903": "太极擒龙免费组合",
    # "29774": "智投短线精选",
    "31816": "一只不休息的牛",
}

all_ids = Combination_ids + ETF_ids + zhitou_ids
# all_ids = Combination_ids + zhitou_ids
id_to_name = {**Combination_ids_to_name, **ETF_ids_to_name, **zhitou_ids_to_name}
# pprint(id_to_name)
# for id in ETF_ids:
#     print(ETF_ids_to_name.get(id,'未知'))