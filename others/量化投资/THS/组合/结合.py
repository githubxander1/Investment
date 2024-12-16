import requests
import pandas as pd
from pprint import pprint

# 定义要请求的id列表
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

# 定义英文列名到中文列名的映射
column_mapping = {
    "策略id": "策略id",
    "策略名称": "策略名称",
    "策略描述": "策略描述",
    "createAt": "创建时间",
    "dailyIncomeRate": "日收益率",
    "maxDrawdownRate": "最大回撤率",
    "totalIncomeRate": "总收益率",
    "product_name": "产品名称",
    "product_desc": "产品描述"
}

# 存储所有结果的列表
all_results = []

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

def get_position_income_info(id):
    url = "https://t.10jqka.com.cn/portfolio/v2/position/get_position_income_info"
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
        "Referer": "https://t.10jqka.com.cn/pkgfront/tgService.html?type=portfolio&id=19483",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
        "Cookie": "IFUserCookieKey={}; user=MDptb182NDE5MjY0ODg6Ok5vbmU6NTAwOjY1MTkyNjQ4ODo3,ExMTExMTExMTExLDQwOzQ0LDExLDQwOzYsMSw0MDs1LDEsNDA7MSwxMDEsNDA7MiwxLDQwOzMsMSw0MDs1LDEsNDA7OCwwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMSw0MDsxMDIsMSw0MDoyNzo6OjY0MTkyNjQ4ODoxNzM0MDUzNTg5Ojo6MTY1ODE0Mjc4MDoyNjc4NDAwOjA6MTE3MTRjYTYwODhjNjRmYzZmNDFlZDRkOTJhMDU3NTMwOjox; userid=641926488; u_name=mo_641926488; escapename=mo_641926488; ticket=58d0f4bf66d65411bb8d8aa431e00721; user_status=0; hxmPid=sns_my_pay_new; v=Ax_acQjchI2vDoCRe4xZjXburHiphHMmjdh3GrFsu04VQDBiuVQDdp2oB2PC"
    }
    try:
        params = {"id": id}
        response = requests.get(url, params=params, headers=headers)
        response.raise_for_status()
        data = response.json()
        if data['status_code'] == 0:
            result = data['data']
            result['策略ID'] = id
            createAt = result['createAt']
            dailyIncomeRate = result['dailyIncomeRate'] = f"{result['dailyIncomeRate'] * 100:.2f}%"
            maxDrawdownRate = result['maxDrawdownRate'] = f"{result['maxDrawdownRate'] * 100:.2f}%"
            totalIncomeRate = result['totalIncomeRate'] = f"{result['totalIncomeRate'] * 100:.2f}%"
            return {
                "创建时间": createAt,
                "日收益率": dailyIncomeRate,
                "最大回撤率": maxDrawdownRate,
                "总收益率": totalIncomeRate
            }
        else:
            print(f"请求错误 (id={id}): {data['status_msg']}")
            return None
    except requests.RequestException as e:
        print(f"请求出现错误 (id={id}): {e}")
        return None

def get_package_feature_info(product_id):
    url = "https://dq.10jqka.com.cn/fuyao/tg_package/package/v1/get_package_feature_info"
    headers = {
        "Host": "dq.10jqka.com.cn",
        "Connection": "keep-alive",
        "Accept": "application/json, text/plain, */*",
        "Origin": "https://t.10jqka.com.cn",
        "User-Agent": "Mozilla/5.0 (Linux; Android 9; ASUS_I003DD Build/PI; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/68.0.3440.70 Mobile Safari/537.36 Hexin_Gphone/11.17.03 (Royal Flush) hxtheme/0 innerversion/G037.08.983.1.32 followPhoneSystemTheme/0 userid/641926488 getHXAPPAccessibilityMode/0 hxNewFont/1 isVip/0 getHXAPPFontSetting/normal getHXAPPAdaptOldSetting/0",
        "Content-Type": "application/x-www-form-urlencoded",
        "Referer": "https://t.10jqka.com.cn/pkgfront/tgService.html?type=portfolio&id=14533",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,en-US;q=0.9",
        "X-Requested-With": "com.hexin.plat.android"
    }
    params = {
        "product_id": product_id,
        "product_type": "portfolio"
    }
    try:
        response = requests.get(url, params=params, headers=headers)
        response.raise_for_status()
        response = response.json()

        data = response['data']
        slogan = data['slogan']
        labels = data['labels']

        return {
            '涨停次数': slogan,
            '标签': labels
        }
        # return response.json()
    except requests.RequestException as e:
        print(f"请求出现错误: {e}")
        return None


# 循环请求每个id
for id in ids:
    product_info = get_product_info(id)
    position_income_info = get_position_income_info(id)
    package_feature_info = get_package_feature_info(id)
    if product_info and position_income_info:
        combined_info = {**product_info, **position_income_info, **package_feature_info}
        all_results.append(combined_info)
# print(all_results)

# 将所有结果转换为DataFrame
if all_results:
    df = pd.DataFrame(all_results)
#     # 重命名列
#     # df.rename(columns=column_mapping, inplace=True)
    # 打印到终端
    pprint(df)
    # 保存到Excel文件
    df.to_excel('结合.xlsx', index=False)
    print("数据已成功保存到 '结合.xlsx'")
else:
    print("没有获取到任何数据")
