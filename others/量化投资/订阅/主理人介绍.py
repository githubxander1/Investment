import requests
import pandas as pd
from pprint import pprint

def get_owner_principal_info(product_id):
    """
    发送GET请求获取所有者主体信息的函数
    """
    url = "https://dq.10jqka.com.cn/fuyao/tg_package/package/v1/get_owner_principal_info"
    params = {
        "product_id": product_id,
        "product_type": "portfolio",
        "userid": 324869371
    }
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

    try:
        response = requests.get(url, params=params, headers=headers)
        response.raise_for_status()
        return response.json()  # 假设返回的数据是JSON格式，返回解析后的内容
    except requests.RequestException as e:
        print(f"请求出现错误 (product_id={product_id}): {e}")
        return None

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

# 存储所有结果的列表
all_results = []

# 循环请求每个id
for product_id in ids:
    data = get_owner_principal_info(product_id)
    if data and data['status_code'] == 0:
        result = data['data']
        result['product_id'] = product_id
        all_results.append(result)
    else:
        print(f"没有获取到有效数据 (product_id={product_id})")

# 将所有结果转换为DataFrame
if all_results:
    df = pd.DataFrame(all_results)
    # 打印到终端
    pprint(df)
    # 保存到Excel文件
    df.to_excel('主理人介绍.xlsx', index=False)
    print("数据已成功保存到 '主理人介绍.xlsx'")
else:
    print("没有获取到任何数据")
