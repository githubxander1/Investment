import datetime
from pprint import pprint
import requests
import pandas as pd
import logging

# 设置日志记录
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

#1获取数据部分

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
            product_name = result['data']['baseInfo']['productName']
            product_desc = result['data']['baseInfo']['productDesc']
            return {"策略id": product_id, "策略名称": product_name, "策略描述": product_desc}
        else:
            logging.error(f"Failed to retrieve data for product_id: {product_id}")
            return None
    except requests.RequestException as e:
        logging.error(f"请求出现错误: {e}")
        return None

# 获取当前持仓信息
def get_current_positions(portfolio_id):
    headers = {
        "Host": "t.10jqka.com.cn",
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
        # pprint(data)
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

# 获取历史数据
def get_historical_data(portfolio_id):
    url = "https://t.10jqka.com.cn/portfolio/post/v2/get_relocate_post_list"
    headers = {
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

# 获取历史调仓数据
def get_historical_posts(portfolio_id):
    return get_historical_data(portfolio_id)

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


# 2处理数据部分

# 提取并过滤今天的调仓数
def get_all_today_trades(ids):
    all_records = []
    today = datetime.date.today().strftime('%Y-%m-%d')

    for portfolio_id in ids:
        data = get_historical_data(portfolio_id)
        if data:
            for item in data['data']:
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

    today_trade_df = pd.DataFrame(all_records)
    today_trade_df.sort_values(by='时间', ascending=False, inplace=True)
    return today_trade_df


# 提取并过滤持仓数据，汇总
def fetch_and_process_positions(ids):
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

# 提取和过滤历史调仓数据
def process_historical_posts(ids):
    all_data = []
    for portfolio_id in ids:
        relocate_post = get_historical_posts(portfolio_id)['data']
        extract_info = []
        for record in relocate_post:
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
    return all_data

# 3保存数据
def save_to_excel(summary_df, today_trade_df, stats_df, post_df, ids, custom_sheet_names=None):
    file_path = r"D:\1document\1test\PycharmProject_gitee\others\量化投资\THS\组合\保存的数据\组合_持仓_今天调仓_历史调仓.xlsx"
    if custom_sheet_names is None:
        custom_sheet_names = {}
    with pd.ExcelWriter(file_path) as writer:
        sheet_name_summary = custom_sheet_names.get('summary_df', "汇总表")
        summary_df.to_excel(writer, sheet_name=sheet_name_summary, index=False)
        if not today_trade_df.empty:
            sheet_name_today_trade = custom_sheet_names.get('today_trade_df', "今天调仓")
            today_trade_df.to_excel(writer, sheet_name=sheet_name_today_trade, index=False)
        sheet_name_stats = custom_sheet_names.get('stats_df', "策略收益统计")
        stats_df.to_excel(writer, sheet_name=sheet_name_stats, index=False)
        for portfolio_id, extract_info in post_df:
            sheet_name = custom_sheet_names.get(portfolio_id, get_strategy_details(portfolio_id).get('策略名称', f"策略_{portfolio_id}"))
            sheet_name = sheet_name.replace('/', '_').replace('\\', '_')[:31]
            if sheet_name is not None:
                post_df = pd.DataFrame(extract_info)
                post_df.to_excel(writer, sheet_name=sheet_name, index=False)
            else:
                logging.error(f"无法获取策略名称，ID: {portfolio_id}")
        if 'Sheet1' in writer.book.sheetnames:
            del writer.book['Sheet1']
    logging.info("已成功保存到 '组合_持仓_今天调仓_历史调仓.xlsx' 文件中。")


# 主程序入口
def main():
    ids = [
        6994, 18565, 14980, 16281, 7152, 13081, 11094
    ]
    summary_df, stats_df = fetch_and_process_positions(ids)
    today_trade_df = get_all_today_trades(ids)
    # logging.info(today_trade_df)
    post_df = process_historical_posts(ids)
    custom_sheet_names = {
        'summary_df': '持仓汇总表',
        'today_trade_df': '今天调仓',
        'stats_df': '策略收益统计'
    }
    save_to_excel(summary_df, today_trade_df, stats_df, post_df, ids, custom_sheet_names)

if __name__ == "__main__":
    main()
