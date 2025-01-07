import requests

# 请求的URL
url = "https://dataq.10jqka.com.cn/fetch-data-server/fetch/v1/specific_data"

# 请求头
headers = {
    "Host": "dataq.10jqka.com.cn",
    "Connection": "keep-alive",
    "Content-Length": "651",
    "Accept": "application/json, text/plain, */*",
    "Origin": "https://eq.10jqka.com.cn",
    "Platform": "mobileweb",
    "Source-id": "HSGT-project",
    "User-Agent": "Mozilla/5.0 (Linux; Android 9; ASUS_I003DD Build/PI; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/68.0.3440.70 Mobile Safari/537.36 Hexin_Gphone/11.17.03 (Royal Flush) hxtheme/0 innerversion/G037.08.983.1.32 followPhoneSystemTheme/0 userid/641926488 getHXAPPAccessibilityMode/0 hxNewFont/1 isVip/0 getHXAPPFontSetting/normal getHXAPPAdaptOldSetting/0",
    "Content-Type": "application/json",
    "Referer": "https://eq.10jqka.com.cn/webpage/hsgt-project/index.html",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "zh-CN,en-US;q=0.9",
    "Cookie": "user_status=0; user=MDptb182NDE5MjY0ODg6Ok5vbmU6NTAwOjY1MTkyNjQ4ODo3,ExMTExMTExMTExLDQwOzQ0LDExLDQwOzYsMSw0MDs1LDEsNDA7MSwxMDEsNDA7MiwxLDQwOzMsMSw0MDs1LDEsNDA7OCwwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMSw0MDsxMDIsMSw0MDoyNzo6OjY0MTkyNjQ4ODoxNzMzMTQxMTExOjo6MTY1ODE0Mjc4MDoyNjc4NDAwOjA6MWEwZGI0MTE4MTk4NThiZDE2MDFjMDVmNDQ4N2M4ZjcxOjox; userid=641926488; u_name=mo_641926488; escapename=mo_641926488; ticket=c9840d8b7eefc37ee4c5aa8dd6b90656; IFUserCookieKey={\"escapename\":\"mo_641926488\",\"userid\":\"641926488\"}; hxmPid=juece_new; v=Ax8JThWlhLdzFoCrtonRD2GBp3iphHMyjd13GrFsul4UbDBiuVQDdp2oB3fC",
    "X-Requested-With": "com.hexin.plat.android"
}

# 请求体
payload = {
    "code_selectors": {
        "include": [
            {
                "type": "tag",
                "values": ["lgt_stock_holding_list"],
                "start": 1727625600,
                "end": 1727625600
            }
        ]
    },
    "indexes": [
        {"index_id": "security_name"},
        {"index_id": "lgt_stock_hold_market_value", "time_type": "SNAPSHOT"},
        {"index_id": "lgt_stock_hold_tradeable_per", "time_type": "SNAPSHOT"},
        {"index_id": "inr-price_change_ratio_pct-sum", "time_type": "DAY_1", "timestamp": 1734416148, "attribute": {"win_size": "1"}},
        {"index_id": "lgt_stock_add_hold_per", "time_type": "SNAPSHOT"},
        {"index_id": "lgt_stock_hold_total_per", "time_type": "SNAPSHOT"},
        {"index_id": "lgt_stock_industry_name"}
    ],
    "page_info": {"page_begin": 0, "page_size": 20},
    "sort": [{"idx": 1, "type": "desc"}]
}

# 发送POST请求
response = requests.post(url, json=payload, headers=headers)
# 检查请求是否成功（状态码为200）
if response.status_code == 200:
    try:
        data = response.json()
        # 尝试提取data下的data信息
        result_data = data.get('data', {}).get('data', [])

        # 解析数据
        parsed_data = []
        for item in result_data:
            parsed_item = {}
            for value in item['values']:
                parsed_item[value['idx']] = value['value']
            parsed_data.append(parsed_item)

        # 转换为DataFrame
        df = pd.DataFrame(parsed_data)
        df.to_csv('data.csv', index=False)
        print(df)
    except (ValueError) as e:
        print(f"解析 JSON 失败: {e}")
    except KeyError as e:
        print(f"键不存在: {e}")
else:
    print(f"请求失败，状态码: {response.status_code}")