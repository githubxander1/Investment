import requests
import pandas as pd
from pprint import pprint

# 接口URL
url = "https://dq.10jqka.com.cn/fuyao/tg_package/package/v1/get_package_portfolio_infos"

# 请求头
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

def get_package_portfolio_infos(product_id):
    params = {
        "product_id": product_id,
        "product_type": "portfolio"
    }
    try:
        response = requests.get(url, params=params, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"请求出现错误: {e}")
        return None
# pprint(get_package_portfolio_infos(14533))
def process_product_ids(product_ids):
    all_data = []
    for product_id in product_ids:
        result = get_package_portfolio_infos(product_id)
        pprint(result)
        if result and result['status_code'] == 0:
            pprint(result)
            data = result['data']
            data['product_id'] = product_id
            all_data.append(data)
        else:
            print(f"Failed to retrieve data for product_id: {product_id}")

    df = pd.DataFrame(all_data)
    pprint(df)
    df.to_excel(r'D:\1document\1test\PycharmProject_gitee\others\量化投资\THS\组合\保存的数据\组合信息.xlsx', index=False)

product_ids = [
    14533
    # 16281,
    # 23768,
    # 8426,
    # 9564,
    # 6994,
    # 7152,
    # 20335,
    # 21302,
    # 19347,
    # 8187,
    # 18565,
    # 14980,
    # 16428
]

process_product_ids(product_ids)
