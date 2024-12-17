import requests

# 请求的URL
url = "https://dataq.10jqka.com.cn/fetch-data-server/fetch/v1/specific_data"

# 请求头，直接复制原请求中的请求头信息
headers = {
    "Host": "dataq.10jqka.com.cn",
    "Connection": "keep-alive",
    "Content-Length": "923",
    "Accept": "application/json, text/plain, */*",
    "Origin": "https://eq.10jqka.com.cn",
    "Platform": "mobileweb",
    "Source-id": "hsgt-project",
    "User-Agent": "Mozilla/5.0 (Linux; Android 9; ASUS_I003DD Build/PI; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/68.0.3440.70 Mobile Safari/537.36 Hexin_Gphone/11.17.03 (Royal Flush) hxtheme/0 innerversion/G037.08.983.1.32 followPhoneSystemTheme/0 userid/641926488 getHXAPPAccessibilityMode/0 hxNewFont/1 isVip/0 getHXAPPFontSetting/normal getHXAPPAdaptOldSetting/0",
    "Content-Type": "application/json",
    "Referer": "https://eq.10jqka.com.cn/webpage/hsgt-project/index.html",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "zh-CN,en-US;q=0.9",
    "Cookie": "user_status=0; user=MDptb182NDE5MjY0ODg6Ok5vbmU6NTAwOjY1MTkyNjQ4ODo3,ExMTExMTExMTExLDQwOzQ0LDExLDQwOzYsMSw0MDs1LDEsNDA7MSwxMDEsNDA7MiwxLDQwOzMsMSw0MDs1LDEsNDA7OCwwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMSw0MDsxMDIsMSw0MDoyNzo6OjY0MTkyNjQ4ODoxNzMzMTQxMTExOjo6MTY1ODE0Mjc4MDoyNjc4NDAwOjA6MWEwZGI0MTE4MTk4NThiZDE2MDFjMDVmNDQ4N2M4ZjcxOjox; userid=641926488; u_name=mo_641926488; escapename=mo_641926488; ticket=c9840d8b7eefc37ee4c5aa8dd6b90656; IFUserCookieKey={\"escapename\":\"mo_641926488\",\"userid\":\"641926488\"}; hxmPid=juece_new; v=A5uNwnmxeEOXqoS3aOMdO8VtI_QFcK9-qYdzJo3Yd5WxwrTuFUA_wrlUA2ae",
    "X-Requested-With": "com.hexin.plat.android"
}

# 请求体数据，直接复制原请求中的请求体信息
payload = {
    "code_selectors": {
        "include": [
            {
                "type": "tag",
                "values": ["lgt_top_deal_list"],
                "start": 1734278400,
                "end": 1734278400
            }
        ]
    },
    "indexes": [
        {"index_id": "security_name"},
        {"index_id": "inr-price_change_ratio_pct-sum", "time_type": "DAY_1", "timestamp": 1734278400, "attribute": {"win_size": "1"}},
        {"index_id": "lgt_stock_industry_name"},
        {"index_id": "lgt_stock_turnover", "attribute": {"start": 1734278400, "end": 1734278400}},
        {"index_id": "lgt_stock_market_turnover", "attribute": {"start": 1734278400, "end": 1734278400}},
        {"index_id": "lgt_stock_turnover_per", "attribute": {"start": 1734278400, "end": 1734278400}},
        {"index_id": "lgt_stock_hold_num", "attribute": {"start": 1734278400, "end": 1734278400}},
        {"index_id": "lgt_stock_hold_tradeable_per", "attribute": {"start": 1734278400, "end": 1734278400}},
        {"index_id": "lgt_stock_list_top_deal_tag", "attribute": {"start": 1734278400, "end": 1734278400}}
    ],
    "page_info": {"page_begin": 0, "page_size": 20},
    "sort": [{"idx": 3, "type": "desc"}]
}

# 发送POST请求
response = requests.post(url, json=payload, headers=headers)
# 确保请求成功，状态码为200
if response.status_code == 200:
    data = response.json()
    try:
        # 尝试提取data下的data信息
        result_data = data.get('data', {}).get('data', [])
        for item in result_data:
            print(item)
    except KeyError:
        print("返回数据格式不符合预期，找不到对应的'data'下的'data'字段。")
else:
    print(f"请求失败，状态码: {response.status_code}")