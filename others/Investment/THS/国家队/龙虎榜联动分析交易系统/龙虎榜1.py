from pprint import pprint
import requests
import json
import pandas as pd


def get_stock_transaction_data(
    date="2025-06-13",
    page=1,
    size=10,
    order_field="hot_rank",
    order_type="asc"
):
    """
    获取股票交易数据列表
    :param date: 日期，格式YYYY-MM-DD，默认2025-06-13
    :param page: 页码，默认1
    :param size: 每页数据量，默认50
    :param order_field: 排序字段，默认hot_rank
    :param order_type: 排序方式(asc/desc)，默认asc
    :return: 响应数据字典，失败返回None
    """
    url = "https://data.10jqka.com.cn/dataapi/transaction/stock/v1/list"
    params = {
        "order_field": order_field,
        "order_type": order_type,
        "date": date,
        "filter": "",
        "page": page,
        "size": size,
        "module": "all",
        "order_null_greater": 1# 机构：order_field=org_net_value, module=org,order_type=desc,order_null_greater=0为机构净买入倒序,
    } #游资：field=hot_money_net_value,module=hot_money,order_type=desc,order_null_greater=0为游资净买入倒序,
    #游资+机构：field=change,module=org_hot_money,order_null_greater=0为机构净卖出倒序,
    #市场高度：field=high_days_value，module=market_height,order_null_greater=0为市场高度
    #首榜：field=limit_order_amount,module=first_limit,order_null_greater=0为首榜倒序,
    headers = {
        "Host": "data.10jqka.com.cn",
        "Connection": "keep-alive",
        "sec-ch-ua": "\"Chromium\";v=\"116\", \"Not)A;Brand\";v=\"24\", \"Android WebView\";v=\"116\"",
        "Accept": "application/json, text/plain, */*",
        "hexin-v": "A6YVsMol8nyCUqbYsCUo_ed-9Rcoh-pBvMsepZBPkkmkE0mN-Bc6UYxbbr1j",
        "sec-ch-ua-mobile": "?1",
        "User-Agent": "Mozilla/5.0 (Linux; Android 14; V2353A Build/UP1A.231005.007; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/116.0.0.0 Mobile Safari/537.36 Hexin_Gphone/11.30.02 (Royal Flush) hxtheme/1 innerversion/G037.09.033.1.32 followPhoneSystemTheme/1 userid/641926488 getHXAPPAccessibilityMode/0 hxNewFont/1 isVip/0 getHXAPPFontSetting/normal getHXAPPAdaptOldSetting/0",
        "sec-ch-ua-platform": "\"Android\"",
        "X-Requested-With": "com.hexin.plat.android",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Dest": "empty",
        "Referer": "https://data.10jqka.com.cn/mobile/transaction/index.html?up=new",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
        "Cookie": "user_status=0; user=MDptb182NDE5MjY0ODg6Ok5vbmU6NTAwOjY1MTkyNjQ4ODo3LDExMTExMTExMTExLDQwOzQ0LDExLDQwOzYsMSw0MDs1LDEsNDA7MSwxMDEsNDA7MiwxLDQwOzMsMSw0MDs1LDEsNDA7OCwwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMSw0MDsxMDIsMSw0MDoyNzo6OjY0MTkyNjQ4ODoxNzQ5NjkzMjg5Ojo6MTY1ODE0Mjc4MDoyNjc4NDAwOjA6MTVjNGY3MWViY2M0YmQwNDBkNGU1MDEzYzdmM2Q0NWRmOjox; userid=641926488; u_name=mo_641926488; escapename=mo_641926488; ticket=536749b3c84105bd1c392b267cb5d589; IFUserCookieKey={\"userid\":\"641926488\",\"escapename\":\"mo_641926488\",\"custid\":\"\"}; _clck=a5x9j2%7C2%7Cfwp%7C0%7C0; hxmPid=free_lhbnew.shouye; v=A6YVsMol8nyCUqbYsCUo_ed-9Rcoh-pBvMsepZBPkkmkE0mN-Bc6UYxbbr1j"
    }

    try:
        response = requests.get(url, params=params, headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"请求失败，状态码：{response.status_code}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"请求异常：{e}")
        return None


def extract_lhb_data(json_data):
    """
    提取龙虎榜中的关键信息
    """
    items = json_data.get('data', {}).get('items', [])
    extracted_data = []

    for item in items:
        # 合并概念名称
        concept_names = ' + '.join([concept['name'] for concept in item.get('concept_list', [])])

        # 合并标签名称
        tag_names = ' + '.join([tag['name'] for tag in item.get('tags', [])])

        extracted_data.append({
            '股票代码': item['stock_code'],
            '股票名称': item['stock_name'],
            '涨跌幅(%)': round(item['change'] * 100, 2),
            '买卖净额': round(item['net_value'], 2),
            '买入金额': round(item['buy_value'], 2),
            '卖出金额': round(item['sell_value'], 2),
            '上榜原因': item.get('limit_reason', ''),
            '所属概念': concept_names,
            '热点标签': tag_names,
            '热度排名': item['hot_rank']
        })

    return extracted_data


start_date = "2024-06-13"
if __name__ == "__main__":

    # 定义要请求的模块及对应的参数
    modules = {
        "hot_rank":
            {"module": "all",
             "order_null_greater": 1,
             "desc": False,
             "title": "市场热度"},
        "org_net_value":
            {"module": "org",
             "order_null_greater": 0,
             "desc": True,
             "title": "机构净买入"},
        "hot_money_net_value":
            {"module": "hot_money",
             "order_null_greater": 0,
             "desc": True,
             "title": "游资净买入"},
        "change":
            {"module": "org_hot_money",
             "order_null_greater": 0,
             "desc": True,
             "title": "游资+机构净卖出"},
        "high_days_value":
            {"module": "market_height",
             "order_null_greater": 0,
             "desc": True,
             "title": "市场高度"},
        "limit_order_amount":
            {"module": "first_limit",
             "order_null_greater": 0,
             "desc": False,
             "title": "首榜倒序"}
    }

    all_dfs = {}  # 存储所有 DataFrame，用于写入多个sheet
    selected_stocks = {}

    for order_field, config in modules.items():
        print(f"正在获取【{config['title']}】数据...")
        data = get_stock_transaction_data(
            date=start_date,
            page=1,
            size=10,
            order_field=order_field,
            order_type="desc" if config["desc"] else "asc"
        )

        if data:
            df = pd.DataFrame(extract_lhb_data(data))
            #买卖金额排序，买入最多的排前面
            df = df.sort_values(by='买卖净额', ascending=False)

            # 取前两支股票
            top_two_stocks = df.head(2)
            selected_stocks[config['title']] = top_two_stocks[['股票代码', '股票名称']].values.tolist()

            print(f"\n📊 {config['title']} 数据表：")
            print(df)

            # 存入字典，后续写入Excel
            all_dfs[config['title']] = df
        else:
            print(f"获取【{config['title']}】数据失败")

    # 写入 Excel
    output_file = '龙虎榜综合数据.xlsx'
    with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
        for sheet_name, df in all_dfs.items():
            df.to_excel(writer, sheet_name=sheet_name, index=False)

    print(f"\n✅ 所有数据已保存至 {output_file}")

# # 龙虎榜1.py (部分修改)
# if __name__ == "__main__":
#     selected_stocks = {}
#     for order_field, config in modules.items():
#         data = get_stock_transaction_data(
#             date="2024-06-13",
#             page=1,
#             size=10,
#             order_field=order_field,
#             order_type="desc" if config["desc"] else "asc"
#         )
#
#         if data:
#             df = pd.DataFrame(extract_lhb_data(data))
#             top_two_stocks = df.head(2)
#             selected_stocks[config['title']] = top_two_stocks[['股票代码', '股票名称']].values.tolist()
#
#     all_stock_codes = [code for sublist in selected_stocks.values() for code, name in sublist]
#     unique_stock_codes = list(set(all_stock_codes))  # 去重
#
#     print("Selected Stocks:", selected_stocks)
#     print("Unique Stock Codes:", unique_stock_codes)
#
#     # 下载 K 线数据
#     from download_stock_data import download_stock_data
#     download_stock_data(unique_stock_codes, start_date="2024-06-14", end_date="2023-10-01")
#
#     # 进行回测
#     import backtrader as bt
#     from HoldingPeriodStrategy import HoldingPeriodStrategy
#
#     cerebro = bt.Cerebro()
#
#     # 添加数据 feed
#     for code in unique_stock_codes:
#         data = bt.feeds.YahooFinanceData(dataname=f"{code}.csv")
#         cerebro.adddata(data)
#
#     # 添加策略
#     cerebro.addstrategy(HoldingPeriodStrategy)
#
#     # 运行回测
#     cerebro.run()
#
#     # 打印分析结果
#     print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())
#
#
