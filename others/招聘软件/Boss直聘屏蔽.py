import os
from pprint import pprint

import pandas as pd
import requests

# 使用环境变量或配置文件来管理URL、Headers、Cookie和Token
BASE_URL_SUGGEST = os.getenv("BASE_URL_SUGGEST", "https://www.zhipin.com/wapi/zpgeek/maskcompany/suggest.json")
BASE_URL_ADD = os.getenv("BASE_URL_ADD", "https://www.zhipin.com/wapi/zpgeek/maskcompany/add.json")
BASE_URL_GROUP_QUERY = os.getenv("BASE_URL_GROUP_QUERY", "https://www.zhipin.com/wapi/zpgeek/maskcompany/group/query.json")

HEADERS = {
    "accept": "application/json, text/plain, */*",
    "accept-encoding": "gzip, deflate, br, zstd",
    "accept-language": "zh-CN,zh;q=0.9",
    "dnt": "1",
    "referer": "https://www.zhipin.com/web/geek/privacy-set?type=privacySet&from=1&ka=privacy_set",
    "sec-ch-ua": "\"Chromium\";v=\"121\", \"Not A(Brand\";v=\"99\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"Windows\"",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "token": os.getenv("TOKEN", "3PsdwzbvzhsH31rR"),
    "traceid": os.getenv("TRACEID", "F-66b228maWy4FOmzo"),
    "x-requested-with": "XMLHttpRequest",
    "zp_token": os.getenv("ZP_TOKEN", "V2QNglEuX12l9vVtRuzBoaKy247DrQwik~|QNglEuX12l9vVtRuzBoaKy247DrSxCg~")
}

COOKIES = {
    "lastCity": "101280600",
    "__g": "-",
    "Hm_lvt_194df3105ad7148dcf2b98a91b5e727a": "1736337961",
    "HMACCOUNT": "8A738BBDBACE51F5",
    "__zp_seo_uuid__": "f4942b45-0d39-4935-b9e3-67d201793c50",
    "__l": "r=https%3A%2F%2Fwww.baidu.com%2Flink%3Furl%3DusOkdWbqcXRCLA1AC0OYuc8bWCAbeoaWLUVxvjnWMUyY7VmsW4jvar9b2ELegeJw%26wd%3D%26eqid%3D828ca59a000aabcd00000006677f9563&l=%2F&s=1",
    "wt2": "DXejSOGWqWtK9FLIVgT9ThsQowzuDq7mYW85nNPIAf4RPziiTwL1HzTobGJ6JuPGinoCiW6XEIxYTON1o92oOEg~~",
    "wbg": "0",
    "zp_at": "p5d7IkjPBbX7lxIoOgXkIBqJzJA6v1qD8SF6kKWxjWo~",
    "ab_guid": "f14964c1-21a7-47e5-bc0f-f0a6cecd8bec",
    "gdxidpyhxdE": "0hQite0zUjeO2gPIY%5Cz1vL%2BY%2FEKh%5CaD3oM7Mn5cwmdAcVhodBQHWPcfh9%2Bj46qE5PgeK48A4sGV%5CmQLw3SyEbpHPnXl8%2FLztHyvRsW6MejOYuzMcoKCVgGzJcuTz1kI4EMz3o%2BANmzDT4VQQsCi1WbkPPwPRgoehNSV%2F329w%5CYZeVwdS%3A1736415513152",
    "__zp_stoken__": "d0e7fw4VLc18zVQZfCFVrwoJycFZUZsK8dMK9SsKzfVRSwr3CtsKdwrVUwrLClcKow4Fiwo1gwqlMwqtTwoRxwr3CqMO2wrXCn2TCmcOAwqjCq8Kowq3Cj8Kswo1Zw6zCqcKPw4HCmEjClsKjw5PCmMOewqrDpsKQw6jCrcS0wpzEgsK4xLnCpcSowr7Dr8K%2Bw5%2FDtsS%2FwqDDmsOtw4zCisOaw6jEnsKtw4vFrcSiw5zFsMO8w7LCt8KUNTERBREGCgsHCwgEBBALCAQSBhIFCQsHCwgEQCvDu8OaxIBCNTY4JkRQRApSU15LXUYNVExJND8OXwhaPzE7ODQ7wrTDm8K2R8OAw5fDgUPCt8ObwrXCpjg8OzfDgVsnLMK2CQTCucSAKMOCxLkQw4I2D8K4wokPw4dUwrfCrlPCtMOvKzpBwrfEvEE5HUFCNTtCNjM1OS02P8OIW8K8wrFaGyk7Fjo1OTk0QjU5NzY0KTkzPSw1NCtCDwMKEAUxQsK4UsK3w5U1OQ%3D%3D",
    "Hm_lpvt_194df3105ad7148dcf2b98a91b5e727a": "1736414825",
    "bst": "V2QNglEuX12l9vVtRuzBoaKy247DrQwik~|QNglEuX12l9vVtRuzBoaKy247DrSxCg~",
    "__c": "1736337961",
    "__a": "13889061.1736337961..1736337961.9.1.9.9"
}

# 创建一个全局会话对象
session = requests.Session()
session.headers.update(HEADERS)
session.cookies.update(COOKIES)

def query_companyIds(query):
    params = {
        "query": query
    }
    response = session.get(BASE_URL_SUGGEST, params=params)
    response.raise_for_status()  # 检查请求是否成功
    data = response.json()
    if data["code"] != 0:
        print(f"Error: {data['message']}")
        return [], 0

    total_count = data["zpData"]["totalCount"]
    print(f'总数: {total_count}')
    suggestList = data["zpData"]["suggestList"]
    company_infos = []
    for item in suggestList:
        item_info = {
            "名字": item['company']["name"],
            "id": item["comId"],
            "encryptComId": item["encryptComId"],
        }
        company_infos.append(item_info)

    df = pd.DataFrame(company_infos)
    print(df)
    encryptComIds = [item["encryptComId"] for item in company_infos]
    return encryptComIds, total_count

def add_company(query):
    encryptComIds, total_count = query_companyIds(query)
    if not encryptComIds:
        print("没有找到公司信息，跳过添加操作")
        return

    for encryptComId in encryptComIds:
        params = {
            "comIds": encryptComId,
            "checkall": "1",
            "totalCount": total_count,
            "name": query
        }
        try:
            response = session.get(BASE_URL_ADD, params=params)
            response.raise_for_status()  # 检查请求是否成功
            data = response.json()
            if data["message"] == "Success":
                pass
                # print("添加成功")
            else:
                print("添加失败")
        except requests.exceptions.RequestException as e:
            print(f"请求失败: {e}")
            print("添加失败")

def get_company_info():
    try:
        response = session.get(BASE_URL_GROUP_QUERY)
        response.raise_for_status()  # 检查请求是否成功
        data = response.json()
        if data["code"] != 0:
            print(f"Error: {data['message']}")
            return

        groupList = data["zpData"]["groupList"]
        # pprint(groupList)
        all_mast_infos = []

        for group in groupList:
            groupName = group["groupName"]
            print(f"Group Name: {groupName}")
            maskResult = group["maskResult"]
            dataList = maskResult["dataList"]

            for item in dataList:
                mask_info = {
                    "comName": item["comName"],
                }
                all_mast_infos.append(mask_info)
                pprint(mask_info.get("comName", ""))
            print('\n')

        # df = pd.DataFrame(all_mast_infos)
        # print(df)
    except requests.exceptions.RequestException as e:
        print(f"请求失败: {e}")

if __name__ == '__main__':
    query = '菲客网络'
    # query_companyIds(query)
    add_company(query)
    get_company_info()
    # 如果get_company_info成功，再执行其他操作
    # if session.cookies.get("zp_at"):
