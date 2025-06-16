from pprint import pprint

import requests


#成长
def post_api_data(data):
    """
    发送POST请求到指定接口获取数据  低负债
    """
    url = "https://dataq.10jqka.com.cn/fetch-data-server/fetch/v1/specific_data"
    headers = {
        "Host": "dataq.10jqka.com.cn",
        "Connection": "keep-alive",
        "Content-Length": "729",
        "Accept": "application/json, text/plain, */*",
        "Platform": "mobileweb",
        "Source-id": "kamis-5914",
        "User-Agent": "Mozilla/5.0 (Linux; Android 10; Redmi Note 7 Pro Build/QKQ1.190915.002; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/87.0.4280.101 Mobile Safari/537.36 Hexin_Gphone/11.19.03 (Royal Flush) hxtheme/1 innerversion/G037.08.990.1.32 followPhoneSystemTheme/1 userid/641926488 getHXAPPAccessibilityMode/0 hxNewFont/1 isVip/0 getHXAPPFontSetting/normal getHXAPPAdaptOldSetting/0",
        "sw8": "1-Mzc4ODIzMWEtZTVhZi00ZWQyLWFiODgtOGUwOGYxYzYyMTM2-MmJiZDMzNTgtZjkzNS00ZmIwLWExYmQtMTkwNzlkZTNkNTQy-0-cG9qaW5nZ3Utb3Bwb3J0dW5pdHk8YnJvd3Nlcj4=-MzM2Xzg2MTI=-L3Jvb3Q=-ZGF0YXEuMTBqcWthLmNvbS5jbg==",
        "Content-Type": "application/json",
        "Origin": "https://eq.10jqka.com.cn",
        "X-Requested-With": "com.hexin.plat.android",
        "Sec-Fetch-Site": "same-site",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Dest": "empty",
        "Referer": "https://eq.10jqka.com.cn/webpage/kamis-renderer/index.0.3.5.html?token=K58ODYxMgB5",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7"
    }
    cookies = {
        "userid": "641926488",
        "u_name": "mo_641926488",
        "escapename": "mo_641926488",
        "user_status": "0",
        "IFUserCookieKey": '{"escapename":"mo_641926488","userid":"641926488"}',
        "user": "MDptb182NDE5MjY0ODg6Ok5vbmU6NTAwOjY1MTkyNjQ4ODo3,MTExMTExMTExMTExLDQwOzQ0LDExLDQwOzYsMS,0MDs1LDEsNDA7MSwxMDEsNDA7MiwxLDQwOzMsMSw0MDs1LDEsNDA7OCwwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMS,0MDsxMDIsMSw0MDoyNzo6OjY0MTkyNjQ4ODoxNzM2NzMyMzMwOjo6MTY1ODE0Mj34MDo2MDQ4MDA6MDoxMTcxNGNhNjA4OGM2NGZjNmY0MWVkNGQ5MmEwNTc1MzA6OjA=",
        "ticket": "1c551a19d21c9927ea95c883812c6140",
        "hxmPid": "free_ipo",
        "v": "A7N2NVxw0N5BmJwK7jKO8ohIQLzd6EeoAX6L3mVQD6EJcNym7bjX-hFMGyd2"
    }



    try:
        response = requests.post(url, json=data, headers=headers, cookies=cookies)
        response.raise_for_status()  # 若请求不成功，抛出异常
        return response.json()  # 返回解析后的JSON数据
    except requests.RequestException as e:
        print(f"请求出现错误: {e}")
        return None


def extract_result(data):
    """
    从接口返回数据中提取结果（示例，需按实际调整）
    """
    if data:
        result_list = data.get('results', [])  # 假设返回结果中有'results'字段存放关键数据
        return result_list
    return []


if __name__ == "__main__":
    """
    主函数，调用请求和提取结果函数并处理ths破净精选0113
    """
    data_selected = {  # 精选
        "code_selectors": {
            "intersection": [
                {
                    "type": "stock_code",
                    "values": ["33:002393", "17:603020", "17:600061", "33:000937", "17:601018", "17:688370",
                               "33:002344", "33:002010", "33:002545", "33:002360", "17:600120", "17:600017",
                               "33:000156", "17:603585", "17:601188", "17:600643", "17:600279", "33:002040",
                               "17:600668", "17:600063", "33:000685", "17:600023", "17:600864", "17:600637",
                               "17:600019", "17:600596", "17:600997", "33:002191", "17:600985", "17:600758",
                               "17:600827", "17:600269", "17:600969", "33:002258", "33:002144", "17:600790",
                               "33:300981", "17:600623", "33:000900", "17:600098", "17:600585", "17:601678",
                               "17:601898", "17:600801", "33:000672", "33:000789", "33:000883", "17:601880",
                               "17:600018", "17:600959"]
                }
            ]
        },
        "indexes": [
            {"index_id": "security_name"},
            {"index_id": "last_price"},
            {"index_id": "price_change_ratio_pct"},
            {"index_id": "pb_mrq"},
        ],
        "page_info": {
            "page_begin": 0,
            "page_size": 20
        },
        "sort": [
            {"idx": 3, "type": "ASC"}
        ]
    }
    data_low_liability = {  # 低负债
        "code_selectors": {
            "intersection": [
                {
                    "type": "stock_code",
                    "values": ["33:002393", "17:603020", "17:601006", "17:688057", "33:002233", "17:603980",
                               "17:600854", "17:601188", "33:300158", "33:002932", "33:002440", "17:600780",
                               "33:000910", "17:688063", "17:600637", "17:688075", "33:301290", "33:002443",
                               "33:002191", "17:600125", "33:002144", "17:601518", "33:002478", "33:001218",
                               "17:603187", "17:600585", "17:601002", "33:000923", "33:001213", "33:002538",
                               "17:600751", "17:688330", "17:600682", "17:600219", "33:000779", "33:000731",
                               "17:601677", "33:000581"]
                }
            ]
        },
        "indexes": [
            {"index_id": "security_name"},
            {"index_id": "last_price"},
            {"index_id": "price_change_ratio_pct"},
            {"index_id": "pb_mrq"}
        ],
        "page_info": {
            "page_begin": 0,
            "page_size": 20
        },
        "sort": [
            {"idx": 3, "type": "ASC"}
        ]
    }
    data_always_down = {  # 持续破精
        "code_selectors": {
            "intersection": [
                {
                    "type": "stock_code",
                    "values": ["33:000001", "33:000591", "33:000623", "33:000685", "33:000718", "33:000726",
                               "33:002091", "33:002966", "17:600015", "17:600016", "17:600019", "17:600033",
                               "17:600153", "17:600248", "17:600278", "17:600284", "17:600508", "17:600742",
                               "17:600755", "17:600820", "17:600919", "17:600926", "17:601006", "17:601009",
                               "17:601077", "17:601169", "17:601187", "17:601229", "17:601288", "17:601328",
                               "17:601398", "17:601658", "17:601665", "17:601800", "17:601818", "17:601825",
                               "17:601860", "17:601886", "17:601939", "17:601963", "17:601988", "17:601998",
                               "17:603588"]
                }
            ]
        },
        "indexes": [
            {"index_id": "security_name"},
            {"index_id": "last_price"},
            {"index_id": "price_change_ratio_pct"},
            {"index_id": "pb_mrq"}
        ],
        "page_info": {
            "page_begin": 0,
            "page_size": 20
        },
        "sort": [
            {"idx": 3, "type": "ASC"}
        ]
    }
    data_up = {  # 成长
        "code_selectors": {
            "intersection": [
                {"type": "stock_code", "values":
                    ["33:000544", "33:002966", "33:000990", "33:000797", "33:000863", "17:600811", "33:000560",
                     "17:603323", "17:600352", "33:000965", "33:300867", "33:000776", "17:601318", "17:600919",
                     "17:603980", "33:002083", "17:600739", "33:000039", "33:000563", "33:002753", "33:300158",
                     "33:002608", "33:000415", "17:600075", "33:000600", "17:600926", "17:600526", "17:601311",
                     "33:000685", "33:000850", "33:002277", "17:601838", "33:002440", "17:600023", "33:002061",
                     "17:601868", "17:600864", "17:601688", "33:002666", "33:002479", "17:600665", "17:600827",
                     "17:601101", "17:600335", "17:600969", "33:002029", "33:000728", "17:603727", "33:002454",
                     "17:605001"]
                 }

            ]},
        "indexes": [
            {"index_id": "security_name"},
            {"index_id": "last_price"},
            {"index_id": "price_change_ratio_pct"},
            {"index_id": "pb_mrq"}
        ],
        "page_info": {
            "page_begin": 0,
            "page_size": 20
        },
        "sort": [
            {"idx": 3, "type": "ASC"}
        ]
    }
    api_data = post_api_data(data_selected)
    pprint(api_data)
    extracted_result = extract_result(api_data)
    print(extracted_result)