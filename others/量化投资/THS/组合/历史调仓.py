import requests
import pandas as pd
from pprint import pprint
import datetime

# 接口的URL


# 请求头
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

def get_product_info(product_id):
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
    params = {
        "product_id": product_id,
        "product_type": "portfolio"
    }
    try:
        response = requests.get(url, params=params, headers=headers)
        response.raise_for_status()
        result = response.json()
        if result['status_code'] == 0:
            product_name = result['data']['baseInfo']['productName']
            product_desc = result['data']['baseInfo']['productDesc']
            return {
                "策略id": product_id,
                "策略名称": product_name,
                "策略描述": product_desc
            }
        else:
            print(f"Failed to retrieve data for product_id: {product_id}")
            return None
    except requests.RequestException as e:
        print(f"请求出现错误: {e}")
        return None
# pprint(get_product_info(19483))
def get_history_data(portfolioId):
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
    params = {
        "id": portfolioId,
        "dynamic_id": 0
    }
    try:
        response = requests.get(url, params=params, headers=headers)
        response.raise_for_status()
        # pprint(response.json())
        return response.json()
    except requests.RequestException as e:
        print(f"请求出现错误: {e}")
        return None

def process_ids(ids):
    all_data = []
    for portfolio_id in ids:
        result = get_history_data(portfolio_id)
        if result and result['status_code'] == 0:
            for entry in result['data']:
                entry['portfolioId'] = portfolio_id
                relocate_list = entry.pop('relocateList')
                for relocate in relocate_list:
                    relocate.update(entry)
                    all_data.append(relocate)
        else:
            print(f"Failed to retrieve data for portfolioId: {portfolio_id}")

    df = pd.DataFrame(all_data)
    df.to_excel('全部历史调仓信息.xlsx', index_label=False)
    # df = df[['code', 'currentRatio', 'finalPrice', 'name', 'newRatio', 'createAt', 'portfolioId']]
    # df.sort_values(by='createAt', ascending=False, inplace=True)
    # df.drop_duplicates(subset=['portfolioId'], keep='first', inplace=True)
    print('历史调仓：')
    # pprint(df)
    df.to_excel('历史调仓.xlsx', index=False)

def process_ids_for_new_df(ids):
    all_data = []
    current_date = datetime.datetime.now().date()  # 获取当前日期
    # 将 createAt 列转换为 datetime 类型，并格式化为年月日时分秒

    for portfolio_id in ids:
        product_info = get_product_info(portfolio_id)
        if not product_info:
            print(f"Failed to retrieve product info for portfolioId: {portfolio_id}")
            continue

        result = get_history_data(portfolio_id)
        if result and result['status_code'] == 0:
            for entry in result['data']:
                entry['portfolioId'] = portfolio_id
                relocate_list = entry.pop('relocateList')
                for relocate in relocate_list:
                    relocate.update(entry)
                    relocate.update(product_info)  # 合并产品信息
                    relocate['市场'] = determine_market(relocate['code'])  # 添加市场列
                    relocate['操作'] = '卖出' if relocate['newRatio'] < relocate['currentRatio'] else '买入'  # 添加操作列

                    # 提取 createAt 字段中的年月日部分
                    create_at_date = pd.to_datetime(relocate['createAt']).date()

                    # 对比年月日是否为当天
                    if create_at_date == current_date:
                        all_data.append(relocate)
        else:
            print(f"Failed to retrieve data for portfolioId: {portfolio_id}")
    pprint(all_data)

    # 创建 DataFrame 并翻译列名
    df = pd.DataFrame(all_data)
    column_mapping = {
        '策略名称': '策略名称',
        '策略描述': '策略描述',
        'portfolioId': '策略ID',
        'name': '股票名称',
        'code': '股票代码',
        'content': '内容',
        'createAt': '创建时间',
        'finalPrice': '参考成交价',
        'currentRatio': '当前比例',
        'newRatio': '新比例',
        '市场': '市场',
        '操作': '操作'
    }
    df.rename(columns=column_mapping, inplace=True)

    # 将 createAt 列转换为 datetime 类型
    # df['创建时间'] = pd.to_datetime(df['创建时间']).dt.date
    # 将 createAt 列转换为 datetime 类型，并格式化为年月日时分秒
    df['创建时间'] = pd.to_datetime(df['创建时间']).dt.strftime('%Y-%m-%d %H:%M:%S')

    # 过滤出当天的操作记录
    # df = df[df['创建时间'] == current_date]

    # 将比例转换为百分比
    df['当前比例'] = df['当前比例'].apply(lambda x: f"{x * 100:.2f}%")
    df['新比例'] = df['新比例'].apply(lambda x: f"{x * 100:.2f}%")

    # 选择需要的列
    df = df[['策略ID', '策略名称', '策略描述', '股票代码', '股票名称', '市场', '内容', '创建时间', '参考成交价', '操作', '当前比例', '新比例',  ]]

    # 按策略ID和创建时间排序
    df.sort_values(by=['策略ID', '创建时间'], ascending=[True, False], inplace=True)

    # 去重，保留每个策略最新的记录
    df.drop_duplicates(subset=['策略ID'], keep='first', inplace=True)

    print('新历史调仓（当天）：')
    pprint(df)
    df.to_excel(r'D:\1document\1test\PycharmProject_gitee\others\量化投资\THS\组合\保存的数据\新历史调仓.xlsx', index=False)






ids = [
    19483,
    14533,
    16281,
    23768,
    8426,
    9564,
    6994,
    7152,
    20335,
    21302,
    19347,
    8187,
    18565,
    14980,
    16428
]

process_ids(ids)
process_ids_for_new_df(ids)
