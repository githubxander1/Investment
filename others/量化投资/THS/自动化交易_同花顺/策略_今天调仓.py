import os
from pprint import pprint
import requests
from fake_useragent import UserAgent
import pandas as pd
from datetime import datetime
from plyer import notification

# 手动创建策略ID到策略名称的映射
strategy_id_to_name = {
    '155259': 'TMT资金流入战法',
    '155680': 'GPT定期精选',
    '138036': '低价小盘股战法',
    '155270': '中字头概念',
    '137789': '高现金毛利战法',
    '138006': '连续五年优质股战法',
    '136567': '净利润同比大增低估值战法',
    '138127': '归母净利润高战法',
    '118188': '均线粘合平台突破'
}

ua = UserAgent()
def get_latest_position_and_trade(strategy_id):
    url = "https://ms.10jqka.com.cn/iwencai/iwc-web-business-center/strategy_unify/strategy_profit"
    params = {"strategyId": strategy_id}

    headers = {
        "User-Agent": ua.random,
        "Accept": "*/*",
        "Origin": "https://bowerbird.10jqka.com.cn",
        "X-Requested-With": "com.hexin.plat.android",
        "Sec-Fetch-Site": "same-site",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Dest": "empty",
        "Referer": f"https://bowerbird.10jqka.com.cn/thsic/editor/view/15f2E0a579?strategyId={{strategy_id}}",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7"
    }
    response = requests.get(url, params=params, headers=headers)

    if response.status_code == 200:
        data = response.json()
        # pprint(data)
        # 提取 latestTrade 信息
        latest_trade = data.get('result', {}).get('latestTrade', {})
        trade_date = latest_trade.get('tradeDate', 'N/A')
        trade_stocks = latest_trade.get('tradeStocks', [])

        # 提取latestTrade所需字段
        latest_trade_info = []
        today_trades_info = []
        for trade_info in trade_stocks:
            name = trade_info.get('stkName', 'N/A')
            code = trade_info.get('stkCode', 'N/A').split('.')[0]  # 提取股票代码
            market = determine_market(code)  # 判断市场
            operation = trade_info.get('operationType', 'N/A')
            time_str = trade_date  # 使用 latestTrade 的 tradeDate
            price = trade_info.get('tradePrice', 'N/A')
            quantity = trade_info.get('tradeAmount', 'N/A')

            latest_trade_info.append({
                '策略名称': strategy_id_to_name.get(strategy_id, '未知策略'),
                '时间': time_str,
                '操作': operation,
                '股票名称': name,
                '市场': market,
                '参考价': price,
                '数量': quantity,
            })

        # 当前日期
        current_date = datetime.now().date().strftime('%Y%m%d')
        # 提取当天的交易信息
        today_trades = [trade for trade in latest_trade_info if trade['时间'] == current_date]
        today_trades_info.append(today_trades)

        # 过滤掉创业板股票的交易信息
        all_latest_trade_info = [trade for trade in latest_trade_info if not trade['市场'] == '创业板']
        today_trades_info = [trade for trade in latest_trade_info if not trade['市场'] == '创业板']

        return trade_date, latest_trade_info,  today_trades_info
    else:
        print(f"请求失败，状态码: {response.status_code}，策略ID: {strategy_id}")
        return [], 'N/A'

def determine_market(stock_code):
    # 根据股票代码判断市场
    if stock_code.startswith(('60', '00')):
        return '沪深A股'
    elif stock_code.startswith('688'):
        return '科创板'
    elif stock_code.startswith('300'):
        return '创业板'
    elif stock_code.startswith(('4', '8')):
        return '北交所'
    else:
        return '其他'

def save_to_excel(df, filename, sheet_name, index=False):
    # 保存DataFrame到Excel文件
    with pd.ExcelWriter(filename, engine='openpyxl') as writer:
        df.to_excel(writer, sheet_name=sheet_name, index=index)

def main():
    # 要查询的策略ID列表
    strategy_ids = ['155259', '155270', '137789',
                    '155680', '138006', '118188']

    # 存储所有策略的交易信息
    for strategy_id in strategy_ids:
        all_latest_trade_info = get_latest_position_and_trade(strategy_id)
        print(all_latest_trade_info)
        all_today_trades_info = []

    # 创建DataFrame
    last_trades_df = pd.DataFrame(all_latest_trade_info)
    today_trades_without_cyb_df = pd.DataFrame(all_today_trades_info)

    # 检查是否有数据并保存
    if not today_trades_without_cyb_df.empty:
        today_trades_file_path = r'D:\1document\1test\PycharmProject_gitee\others\量化投资\THS\自动化交易_同花顺\保存的数据\策略今天调仓.xlsx'
        # today_trades_file_path = r'/others/量化投资/THS/自动化交易_同花顺/保存的数据\策略今天调仓.xlsx'
        save_to_excel(last_trades_df, today_trades_file_path, '策略今天调仓')
    else:
        print("No today's trade data to save.")

    # 打印当天交易信息到控制台
    print("\n当天交易信息:")
    if not today_trades_without_cyb_df.empty:
        print(today_trades_without_cyb_df)
        # 发送系统通知
        notification.notify(
            title="今日调仓提醒",
            message="发现今日有新的调仓操作！策略",
            app_name="量化投资监控",
            timeout=10
        )
    else:
        print("No today's trade data available.")

if __name__ == '__main__':
    main()
