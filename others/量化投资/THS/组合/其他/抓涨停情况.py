import requests
import pandas as pd
from pprint import pprint

# def get_package_feature_info(product_id):
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

def get_package_feature_info(product_id):
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

def process_product_ids(product_ids):
    all_data = []
    for product_id in product_ids:
        result = get_package_feature_info(product_id)
        if result and result['status_code'] == 0:
            pprint(result)
            data = result['testdata']
            data['product_id'] = product_id

            all_data.append(data)
        else:
            print(f"Failed to retrieve testdata for product_id: {product_id}")

    df = pd.DataFrame(all_data)
    df.to_excel(r'D:\1document\1test\PycharmProject_gitee\others\量化投资\THS\组合\保存的数据\抓涨停情况.xlsx', index=False)

product_ids = [
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

process_product_ids(product_ids)
