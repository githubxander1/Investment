import requests
from pprint import pprint

def fetch_portfolio_ids():
    url = "https://t.10jqka.com.cn/portfoliolist/tgserv/v1/operate_recommend"
    headers = {
        "Host": "t.10jqka.com.cn",
        "Connection": "keep-alive",
        "Accept": "application/json, text/plain, */*",
        "User-Agent": "Mozilla/5.0 (Linux; Android 9; ASUS_I005DA Build/PI; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/68.0.3440.70 Mobile Safari/537.36 Hexin_Gphone/11.29.03 (Royal Flush) hxtheme/0 innerversion/G037.09.031.1.32 followPhoneSystemTheme/0 userid/641926488 getHXAPPAccessibilityMode/0 hxNewFont/1 isVip/0 getHXAPPFontSetting/normal getHXAPPAdaptOldSetting/0",
        "Content-Type": "application/x-www-form-urlencoded",
        "Referer": "https://t.10jqka.com.cn/rankfront/rankHomepage/index.html?listType=3&where=shouye3",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,en-US;q=0.9",
        "Cookie": "user_status=0; hxmPid=thsstore_search.result.show; user=MDptb182NDE5MjY0ODg6Ok5vbmU6NTAwOjY1MTkyNjQ4ODo3LDExMTExMTExMTExLDQwOzQ0LDExLDQwOzYsMSw0MDs1LDEsNDA7MSwxMDEsNDA7MiwxLDQwOzMsMSw0MDs1LDEsNDA7OCwwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMSw0MDsxMDIsMSw0MDoyNzo6OjY0MTkyNjQ4ODoxNzQ5ODY5NjQ0Ojo6MTY1ODE0Mjc4MDoyNjc4NDAwOjA6MWRkY2E1ZjdlMTQ2ZmRiNjFlYjIyZmJmZjZmMWFkZjI4Ojox; userid=641926488; u_name=mo_641926488; escapename=mo_641926488; ticket=b5af882e5c3acd46c7f94fd3f6aa8d41; IFUserCookieKey={\"userid\":\"641926488\",\"escapename\":\"mo_641926488\",\"custid\":\"\"}; v=A3rwL_TzxpvCT0r30wCcduVpwqucK_4XcK5yqYRzJ7vYMxURbLtOFUA_wrdX",
        "X-Requested-With": "com.hexin.plat.android"
    }
    params = {
        "type": "4"
    }

    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        json_data = response.json()
        pprint(json_data)

        # 提取portfolio_id
        portfolio_infos = []

        if "data" in json_data and isinstance(json_data["data"], list):
            for item in json_data["data"]:  # 遍历数据列表中的每个组合对象
                if "portfolio_id" in item:  # 确保包含portfolio_id字段
                    labels = []
                    if "portfolio_labels" in item and isinstance(item["portfolio_labels"], list):
                        labels = [label.get("label") for label in item["portfolio_labels"] if "label" in label]

                    # 获取最新收益日期和数值
                    latest_income_date = None
                    latest_income_rate = None

                    if "income_echarts" in item and isinstance(item["income_echarts"], list):
                        if len(item["income_echarts"]) > 0:
                            last_income = item["income_echarts"][-1]
                            latest_income_date = last_income.get("date")
                            latest_income_rate = round(last_income.get("income_rate"),2)

                    portfolio_info = {
                        '组合id': item.get("portfolio_id"),
                        '名称': item.get("portfolio_name"),
                        '收益率': round(item.get("income_rate", 0) * 100, 2),
                        '标签': labels,
                        '最新收益日期': latest_income_date,
                        '最新收益值': latest_income_rate
                    }

                    portfolio_infos.append(portfolio_info)

        return portfolio_infos

    except requests.RequestException as e:
        print(f"请求失败: {e}")
        return []

if __name__ == '__main__':
    portfolio_ids = fetch_portfolio_ids()
    print("获取到的portfolio信息列表:")
    for pid in portfolio_ids:
        print(pid)
