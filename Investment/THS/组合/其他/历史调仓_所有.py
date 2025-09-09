import requests
import pandas as pd
from pprint import pprint
import datetime

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
            product_name = result['testdata']['baseInfo']['productName']
            product_desc = result['testdata']['baseInfo']['productDesc']
            return {
                "策略id": product_id,
                "策略名称": product_name,
                "策略描述": product_desc
            }
        else:
            print(f"Failed to retrieve testdata for product_id: {product_id}")
            return None
    except requests.RequestException as e:
        print(f"请求出现错误: {e}")
        return None
# pprint(get_product_info(19483))
def get_history_post_data(portfolioId):
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
        relocate_post = get_history_post_data(portfolio_id)['testdata']
        pprint(relocate_post)

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
        all_data.extend(extract_info)
    df = pd.DataFrame(all_data)
    return df

def save_to_excel(data, file_path):
    with pd.ExcelWriter(file_path) as writer:
        for portfolio_id, extract_info in data:
            sheetName = get_product_info(portfolio_id)
            if sheetName is not None:
                sheet_name = sheetName['策略名称'].replace('/', '_').replace('\\', '_')[:31]  # 处理特殊字符和长度限制
                df = pd.DataFrame(extract_info)
                df.to_excel(writer, sheet_name=sheet_name, index=False)
            else:
                print(f"无法获取策略名称，ID: {portfolio_id}")

ids = [
    19483, 14533, 16281, 23768, 8426, 9564, 6994, 7152,
    20335, 21302, 19347, 8187, 18565, 14980, 16428
]

data = process_ids(ids)
save_to_excel(data, r"/zothers/Investment/THS/组合/保存的数据/历史调仓_所有.xlsx")
print("已成功保存到 '历史调仓_所有.xlsx' 文件中。")
