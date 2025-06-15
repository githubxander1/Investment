import datetime
from pprint import pprint
import requests
import pandas as pd
import logging

# 设置日志记录
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# 获取策略名称和描述
def get_strategy_details(product_id):
    url = "https://dq.10jqka.com.cn/fuyao/tg_package/package/v1/get_package_portfolio_infos"
    headers = {
        "Host": "dq.10jqka.com.cn",
        "Connection": "keep-alive",
        "Accept": "application/json, text/plain, */*",
        "User-Agent": "Mozilla/5.0 (Linux; Android 10; Redmi Note 7 Pro Build/QKQ1.190915.002; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/87.0.4280.101 Mobile Safari/537.36 Hexin_Gphone/11.16.10 (Royal Flush) hxtheme/1 innerversion/G037.08.980.1.32 followPhoneSystemTheme/1 userid/641926488 getHXAPPAccessibilityMode/0 hxNewFont/1 isVip/0 getHXAPPFontSetting/normal getHXAPPAdaptOldSetting/0",
        "Content-Type": "application/x-www-form-urlencoded",
        "Origin": "https://t.10jqka.com.cn",
        "X-Requested-With": "com.hexin.plat.android",
        "Sec-Fetch-Site": "same-site",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Dest": "empty",
        "Referer": "https://t.10jqka.com.cn/pkgfront/tgService.html?type=portfolio&id=19483",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
        "Cookie": "IFUserCookieKey={}; user=MDptb182NDE5MjY0ODg6Ok5vbmU6NTAwOjY1MTkyNjQ4ODo3,ExMTExMTExMTExLDQwOzQ0LDExLDQwOzYsMSw0MDs1LDEsNDA7MSwxMDEsNDA7MiwxLDQwOzMsMSw0MDs1LDEsNDA7OCwwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMSw0MDsxMDIsMSw0MDoyNzo6OjY0MTkyNjQ4ODoxNzM0MDUzNTg5Ojo6MTY1ODE0Mjc4MDoyNjc4NDAwOjA6MTE3MTRjYTYwODhjNjRmYzZmNDFlZDRkOTJhMDU3NTMwOjox; userid=641926488; u_name=mo_641926488; escapename=mo_641926488; ticket=58d0f4bf66d65411bb8d8aa431e00721; user_status=0; hxmPid=sns_my_pay_new; v=AxLXmrX7ofaqkd2K73acRpPBYdP0Ixa9SCcK4dxrPkWw771JxLNmzRi3WvOv"
    }
    params = {"product_id": product_id, "product_type": "portfolio"}
    try:
        response = requests.get(url, params=params, headers=headers)
        response.raise_for_status()
        result = response.json()
        if result['status_code'] == 0:
            product_name = result['testdata']['baseInfo']['productName']
            product_desc = result['testdata']['baseInfo']['productDesc']
            return {"策略id": product_id, "策略名称": product_name, "策略描述": product_desc}
        else:
            logging.error(f"Failed to retrieve testdata for product_id: {product_id}")
            return None
    except requests.RequestException as e:
        logging.error(f"请求出现错误: {e}")
        return None

# 获取当前持仓信息
def get_current_positions(portfolio_id):
    headers = {
        "Host": "估值.py.10jqka.com.cn",
        "Connection": "keep-alive",
        "Accept": "application/json, text/plain, */*",
        "User-Agent": "Mozilla/5.0 (Linux; Android 9; ASUS_I003DD Build/PI; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/68.0.3440.70 Mobile Safari/537.36 Hexin_Gphone/11.17.03 (Royal Flush) hxtheme/0 innerversion/G037.08.983.1.32 followPhoneSystemTheme=0 userid=641926488 getHXAPPAccessibilityMode=0 hxNewFont=1 isVip=0 getHXAPPFontSetting=normal getHXAPPAdaptOldSetting=0",
        "Content-Type": "application/x-www-form-urlencoded",
        "Referer": "https://t.10jqka.com.cn/pkgfront/tgService.html?type=portfolio&id=14533",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,en-US;q=0.9",
        "Cookie": "user_status=0; user=MDptb182NDE5MjY0ODg6Ok5vbmU6NTAwOjY1MTkyNjQ4ODo3,ExMTExMTExMTExLDQwOzQ0LDExLDQwOzYsMSw0MDs1LDEsNDA7MSwxMDEsNDA7MiwxLDQwOzMsMSw0MDs1LDEsNDA7OCwwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMSw0MDsxMDIsMSw0MDoyNzo6OjY0MTkyNjQ4ODoxNzMzMTQxMTExOjo6MTY1ODE0834NDAwOjA6MWEwZGI0MTE4MTk4NThiZDE2MDFjMDVmNDQ4N2M4ZjcxOjox; userid=641926488; u_name=mo_641926488; escapename=mo_641926488; ticket=c9840d8b7eefc37ee4c5aa8dd6b90656; IFUserCookieKey={\"escapename\":\"mo_488\",\"userid\":\"641926488\"}; hxmPid=hqMarketPkgVersionControl; v=A-74WWxOBbvQTHHfb2LwELiaNk-w77LBxLJmzRi3Wxqu5oH1gH8C-ZRDtsvr",
        "X-Requested-With": "com.hexin.plat.android"
    }
    url = f"https://t.10jqka.com.cn/portfolio/relocate/user/getPortfolioHoldingData?id={portfolio_id}"

    params = {
        "id": portfolio_id
    }
    response = requests.get(url, headers=headers, params=params)

    # 判断请求是否成功（状态码为200）
    if response.status_code == 200:
        data = response.json()
        # pprint(testdata)
        positions = data["result"]["positions"]
        for item in positions:
            # profitLossRate = item["profitLossRate"]
            item["incomeRate"] = f'{item["incomeRate"] * 100:.2f}%'
            item["positionRealRatio"] = f'{item["positionRealRatio"] * 100:.2f}%'
            item["positionRelocatedRatio"] = f'{item["positionRelocatedRatio"] * 100:.2f}%'
            item["profitLossRate"] = f'{item["profitLossRate"] * 100:.2f}%'
            # item["profitLossRate"] = item["profitLossRate"]   # 修改这里

        return positions
    else:
        logging.error(f"请求失败，ID: {portfolio_id}")
        return None

# 获取历史调仓数据
def get_historical_data(portfolio_id):
    url = "https://t.10jqka.com.cn/portfolio/post/v2/get_relocate_post_list"
    headers = {
        "Host": "估值.py.10jqka.com.cn",
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
        "Cookie": "IFUserCookieKey={}; user=MDptb182NDE5MjY0ODg6Ok5vbmU6NTAwOjY1MTkyNjQ4ODo3LDExMTExMTExMTExLDQwOzQ0LDExLDQwOzYsMSw0MDs1LDEsNDA7MSwxMDEsNDA7MiwxLDQwOzMsMSw0MDs1LDEsNDA7OCwwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMSw0MDsxMDIsMSw0MDoyNzo6OjY0MTkyNjQ4ODoxNzM0MDUzNTg5Ojo6MTY1ODE0Mjc4MDoyNjc4NDAwOjA6MTE3MTRjYTYwODhjNjRmYzZmNDFlZDRkOTJhMDU3NTMwOjox; userid=641926488; u_name=mo_641926488; escapename=mo_641926488; ticket=58d0f4bf66d65411bb8d8aa431e00721; user_status=0; hxmPid=sns_my_pay_new; v=A-gtFDtpG9AGTjdUiWYWoHVzu936EUwbLnUgn6IZNGNW_YfHSiEcq36F8Czx"
    }
    params = {"id": portfolio_id, "dynamic_id": 0}
    try:
        response = requests.get(url, params=params, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        logging.error(f"请求出现错误: {e}")
        return None

# 根据股票代码判断市场
def determine_market(stock_code):
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

# 处理汇总数据
def process_summary_data(ids):
    summary_df = pd.DataFrame(columns=[
        '策略名称', 'code', 'costPrice', 'freezeRatio', 'incomeRate', 'marketCode',
        'name', 'positionRealRatio', 'positionRelocatedRatio', 'price'
    ])
    positions_list = []
    strategy_stats = {}

    for portfolio_id in ids:
        positions = get_current_positions(portfolio_id)
        if positions:
            positions_list.extend([(portfolio_id, pos) for pos in positions])
            strategy_stats[portfolio_id] = {'total_profit_loss': 0, 'positive_count': 0, 'negative_count': 0}

    for portfolio_id, position in positions_list:
        position['策略名称'] = get_strategy_details(portfolio_id).get('策略名称')
        profit_loss_rate = float(position['profitLossRate'].rstrip('%'))
        strategy_stats[portfolio_id]['total_profit_loss'] += profit_loss_rate
        if profit_loss_rate > 0:
            strategy_stats[portfolio_id]['positive_count'] += 1
        elif profit_loss_rate < 0:
            strategy_stats[portfolio_id]['negative_count'] += 1
            #有报错
        summary_df = pd.concat([summary_df, pd.DataFrame([position])], ignore_index=True)

    summary_df.fillna('', inplace=True)

    stats_df = pd.DataFrame(strategy_stats.items(), columns=['策略id', '统计数据'])
    stats_df[['total_profit_loss', 'positive_count', 'negative_count']] = stats_df['统计数据'].apply(pd.Series)
    stats_df.drop(columns=['统计数据'], inplace=True)
    stats_df['策略名称'] = stats_df['策略id'].apply(lambda x: get_strategy_details(x).get('策略名称'))

    total_positive_count = sum(stats_df['positive_count'])
    total_negative_count = sum(stats_df['negative_count'])

    stats_df.loc[len(stats_df)] = [None, '总计', total_positive_count, total_negative_count, None]

    return summary_df, stats_df

# 处理今天调仓数据
def process_today_trades(ids):
    all_records = []
    today = datetime.date.today().strftime('%Y-%m-%d')

    for portfolio_id in ids:
        data = get_historical_data(portfolio_id)
        # print('testdata')
        # pprint(testdata)
        if data:
            for item in data['testdata']:
                create_at = item['createAt']
                date_part = create_at.split()[0]
                if date_part == today:
                    content = item['content']
                    need_relocate_reason = item['needRelocateReason']
                    for stock in item['relocateList']:
                        code = stock['code']
                        current_ratio = stock['currentRatio']
                        final_price = stock['finalPrice']
                        name = stock['name']

                        # 检查股票名称是否为“匿名”
                        if '***' in name:
                            logging.warning(f"未订阅或股票名称显示异常 - 股票代码: {code}, 时间: {create_at}")
                            continue

                        new_ratio = stock['newRatio']
                        market = determine_market(code)
                        operation = '卖出' if new_ratio < current_ratio else '买入'

                        all_records.append({
                            '策略id': portfolio_id,
                            '策略名称': get_strategy_details(portfolio_id).get("策略名称"),
                            '描述': get_strategy_details(portfolio_id).get("策略描述"),
                            '说明': content,
                            '时间': create_at,
                            '股票名称': name,
                            '所属市场': market,
                            '参考价': final_price,
                            '操作': operation,
                            '当前比例': f"{current_ratio * 100:.2f}%",
                            '新比例': f"{new_ratio * 100:.2f}%"
                        })

    if not all_records:
        logging.info("所选组合今天无调仓")
        return None

    today_trade_df = pd.DataFrame(all_records)
    # today_trade_df.sort_values(by='时间', ascending=False, inplace=True)
    # pprint(all_records)

    return today_trade_df

# 处理历史调仓数据
def process_historical_posts(ids):
    all_data = []

    for portfolio_id in ids:
        relocate_post = get_historical_data(portfolio_id)
        if relocate_post and 'testdata' in relocate_post:
            extract_info = []

            for record in relocate_post['testdata']:
                createAt = record['createAt']

                for item in record['relocateList']:
                    code = item['code']
                    currentRatio = item['currentRatio']
                    finalPrice = item['finalPrice']
                    name = item['name']
                    newRatio = item['newRatio']
                    operation = '卖出' if newRatio < currentRatio else '买入'

                    extract_info.append({
                        "调仓时间": createAt,
                        "股票代码": code,
                        "股票名称": name,
                        "股票市场": determine_market(code),
                        "参考价": finalPrice,
                        "当前比例": currentRatio,
                        "调仓后比例": newRatio,
                        "操作类型": operation
                    })

            all_data.append((portfolio_id, extract_info))

        # pprint('alldata')
        # pprint(all_data)

    return all_data

# 保存数据到Excel
def save_to_excel(data_dict, file_path, custom_sheet_names=None):
    """
    将多个DataFrame保存到一个Excel文件的不同工作表中。

    参数:
    - data_dict: dict, 键为数据框名称（字符串），值为对应的数据框（pd.DataFrame）。
    - file_path: str, Excel文件路径。
    - custom_sheet_names: dict, 可选参数，键为数据框名称，值为自定义的工作表名称。
    """
    if custom_sheet_names is None:
        custom_sheet_names = {}

    with pd.ExcelWriter(file_path) as writer:
        for df_name, df in data_dict.items():
            if isinstance(df, list):  # 如果df是列表，则表示这是历史调仓数据
                for portfolio_id, extract_info in df:
                    sheet_name = custom_sheet_names.get(portfolio_id, get_strategy_details(portfolio_id).get('策略名称',
                                                                                                             f"策略_{portfolio_id}"))
                    sheet_name = sheet_name.replace('/', '_').replace('\\', '_')[:31]
                    if sheet_name is not None:
                        post_df = pd.DataFrame(extract_info)
                        post_df.to_excel(writer, sheet_name=sheet_name, index=False)
                    else:
                        logging.error(f"无法获取策略名称，ID: {portfolio_id}")
            else:
                sheet_name = custom_sheet_names.get(df_name, df_name)
                sheet_name = sheet_name.replace('/', '_').replace('\\', '_')[:31]
                df.to_excel(writer, sheet_name=sheet_name, index=False)

        if 'Sheet1' in writer.book.sheetnames:
            del writer.book['Sheet1']

    logging.info(f"已成功保存到 '{file_path}' 文件中。")

# 示例用法
def main():
    # ids = [
    #     6994, 18565, 16281, 7152, 13081
    # ]
    ids = [6994, 18710,16281,19347,13081]

    summary_df, stats_df = process_summary_data(ids)

    today_trade_df = process_today_trades(ids)
    if today_trade_df is not None:
        today_trade_df_print = today_trade_df.drop(columns=['策略id', '描述', '说明'])
        pprint(today_trade_df_print)
    else:
        logging.info("没有今天的调仓数据可供打印")

    post_df = process_historical_posts(ids)

    data_dict = {
        'summary_df': summary_df,
        'stats_df': stats_df,
        # 'today_trade_df': today_trade_df
    }

    if today_trade_df is not None:
        data_dict['today_trade_df'] = today_trade_df

    for i, (portfolio_id, extract_info) in enumerate(post_df):
        if extract_info:  # 检查 extract_info 是否为空
            data_dict[f'post_df_{portfolio_id}'] = pd.DataFrame(extract_info)

    file_path = r"D:\1document\1test\PycharmProject_gitee\others\量化投资\THS\组合\保存的数据\组合_持仓_今天调仓_历史调仓.xlsx"
    custom_sheet_names = {
        'summary_df': '持仓汇总表',
        'today_trade_df': '今天调仓',
        'stats_df': '策略收益统计'
    }

    save_to_excel(data_dict, file_path, custom_sheet_names)

if __name__ == "__main__":
    main()

# 第二个文件
import os
from pprint import pprint
import requests
from fake_useragent import UserAgent
import pandas as pd
from datetime import datetime

# 手动创建策略ID到策略名称的映射
strategy_id_to_name = {
    '155259': 'TMT资金流入战法',
    '155680': 'GPT定期精选',
    '138036': '低价小盘股战法',
    # '138386': '主力控盘低价股战法',
    '155270': '中字头概念',
    '137789': '高现金毛利战法',
    '138006': '连续五年优质股战法',
    '136567': '净利润同比大增低估值战法',
    '138127': '归母净利润高战法',
    '118188': '均线粘合平台突破'
    # '155182': '国资云强势股'
    # 添加更多策略ID和名称
}

def fetch_strategy_profit(strategy_id):
    ua = UserAgent()
    url = "https://ms.10jqka.com.cn/iwencai/iwc-web-business-center/strategy_unify/strategy_profit"
    params = {
        "strategyId": strategy_id
    }
    headers = {
        "User-Agent": ua.random
    }

    response = requests.get(url, params=params, headers=headers)

    if response.status_code == 200:
        data = response.json()

        # 提取 latestTrade 信息
        latest_trade = data.get('result', {}).get('latestTrade', {})
        trade_date = latest_trade.get('tradeDate', 'N/A')
        trade_stocks = latest_trade.get('tradeStocks', [])

        # 提取latestTrade所需字段
        latestTrade_info = []
        for trade in trade_stocks:
            name = trade.get('stkName', 'N/A')
            code = trade.get('stkCode', 'N/A').split('.')[0]  # 提取股票代码
            market = determine_market(code)  # 判断市场
            operation = trade.get('operationType', 'N/A')
            time_str = trade_date  # 使用 latestTrade 的 tradeDate
            price = trade.get('tradePrice', 'N/A')
            quantity = trade.get('tradeAmount', 'N/A')

            latestTrade_info.append({
                '策略名称': strategy_id_to_name.get(strategy_id, '未知策略'),
                '操作': operation,
                '股票名称': name,
                # '股票代码': code,
                '市场': market,
                '价格': price,
                '数量': quantity,
                '时间': time_str,
            })

        # 提取 positionStocks 信息
        position_stocks = data.get('result', {}).get('positionStocks', [])
        # 提取positionStocks所需字段
        positions_info = []
        for position in position_stocks:
            name = position.get('stkName', 'N/A')
            code = position.get('stkCode', 'N/A').split('.')[0]  # 提取股票代码
            market = determine_market(code)  # 判断市场
            industry = position.get('industry', 'N/A')
            price = position.get('price', 'N/A')
            position_date_ms = position.get('positionDate', 'N/A')
            position_ratio = position.get('positionRatio', 'N/A')
            profit_and_loss_ratio = position.get('profitAndLossRatio', 'N/A')

            # 将 positionDate 从毫秒时间戳转换为可读的日期时间格式
            if isinstance(position_date_ms, int):
                position_date_s = position_date_ms / 1000
                position_date = datetime.fromtimestamp(position_date_s)
                position_date_str = position_date.strftime('%Y-%m-%d %H:%M:%S')
            elif isinstance(position_date_ms, str):
                position_date_str = position_date_ms
            else:
                position_date_str = 'N/A'

            # 将 positionRatio 和 profitAndLossRatio 转换为百分比形式
            if isinstance(position_ratio, (int, float)):
                position_ratio = f"{position_ratio * 100:.2f}%"
            if isinstance(profit_and_loss_ratio, (int, float)):
                profit_and_loss_ratio = f"{profit_and_loss_ratio * 100:.2f}%"

            positions_info.append({
                '策略名称': strategy_id_to_name.get(strategy_id, '未知策略'),
                '股票名称': name,
                '股票代码': code,
                '市场': market,
                '行业': industry,
                '价格': price,
                '持仓比例': position_ratio,
                '盈亏比例': profit_and_loss_ratio,
                '持仓日期': position_date_str,
            })

        return latestTrade_info, positions_info, trade_date
    else:
        print(f"请求失败，状态码: {response.status_code}，策略ID: {strategy_id}")
        return [], [], 'N/A'

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
    #待卖出国光股份，新华文轩，燕京啤酒后去掉118188

    # 存储所有策略的交易信息和持仓信息
    all_latestTrade_info = []
    all_positions_info = []
    all_today_trades_info = []

    # 当前日期
    current_date = datetime.now().date().strftime('%Y%m%d')

    # 遍历每个策略ID，获取其交易信息和持仓信息
    for strategy_id in strategy_ids:
        latestTrade_info, positions_info, trade_date = fetch_strategy_profit(strategy_id)
        all_latestTrade_info.extend(latestTrade_info)
        all_positions_info.extend(positions_info)

        # 提取当天的交易信息
        today_trades = [trade for trade in latestTrade_info if trade['时间'] == current_date]
        all_today_trades_info.extend(today_trades)

    # 创建DataFrame
    last_trades_df = pd.DataFrame(all_latestTrade_info)
    last_positions_df = pd.DataFrame(all_positions_info)
    today_trades_df = pd.DataFrame(all_today_trades_info)

    # 检查是否有数据并保存
    if not last_positions_df.empty:
        positions_file_path = r'D:\1document\1test\PycharmProject_gitee\others\量化投资\THS\策略\策略保存的数据\策略最新持仓_所有.xlsx'
        save_to_excel(last_positions_df, positions_file_path, '策略最新持仓')
    else:
        print("No position testdata to save.")

    if not last_trades_df.empty:
        trades_file_path = r'D:\1document\1test\PycharmProject_gitee\others\量化投资\THS\策略\策略保存的数据\策略最新调仓_所有.xlsx'
        save_to_excel(last_trades_df, trades_file_path, '策略最新调仓')
    else:
        print("No trade testdata to save.")

    if not today_trades_df.empty:
        today_trades_file_path = r'D:\1document\1test\PycharmProject_gitee\others\量化投资\THS\策略\策略保存的数据\策略今天调仓_所有.xlsx'
        save_to_excel(today_trades_df, today_trades_file_path, '策略今天调仓')
    else:
        print("No today's trade testdata to save.")

    # 打印当天交易信息到控制台
    print("\n当天交易信息:")
    if not today_trades_df.empty:
        print(today_trades_df)
    else:
        print("No today's trade testdata available.")


if __name__ == '__main__':
    main()
