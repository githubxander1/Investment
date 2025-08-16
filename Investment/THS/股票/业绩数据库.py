from pprint import pprint

import pandas as pd
import requests


def post_api_data():
    url = "https://data.10jqka.com.cn/dataapi/performance_forecast/v2/notice_query"
    headers = {
        "Connection": "keep-alive",
        "Content-Length": "199",
        "Accept": "application/json, text/plain, */*",
        "User-Agent": "Mozilla/5.0 (Linux; Android 10; Redmi Note 7 Pro Build/QKQ1.190915.002; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/87.0.4280.101 Mobile Safari/537.36 Hexin_Gphone/11.19.03 (Royal Flush) hxtheme/1 innerversion/G037.08.990.1.32 followPhoneSystemTheme/1 userid/641926488 getHXAPPAccessibilityMode/0 hxNewFont/1 isVip/0 getHXAPPFontSetting/normal getHXAPPAdaptOldSetting/0",
        "Content-Type": "application/json;charset=UTF-8",
        "Origin": "https://eq.10jqka.com.cn",
        "X-Requested-With": "com.hexin.plat.android",
        "Sec-Fetch-Site": "same-site",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Dest": "empty",
        "Referer": "https://eq.10jqka.com.cn/webpage/kamis-renderer/index.0.3.5.html?token=KEENjkwNwB5&source=juhelist&performance_type=%E6%89%AD%E4%BA%8F%E4%B8%BA%E7%9B%88&report=2024-4",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7"
    }
    data = {
        "pom": 1,
        "size": 50,
        "filters": [
            {"field": "report", "args": ["2024-4"], "exp": "equals"},
            {"field": "performance_type", "args": ["盈利大增"], "exp": "equals"},
            {"field": "listing_block_id", "args": ["216001"], "exp": "in"},#沪深A股
            # {"field": "forecast_type", "args": ["notice"], "exp": "equals"}#业绩快报express 业绩预告preview
            # {"field": "parent_holder_net_profit_yoy", "args": [0, 50], "exp": "between",
            #  "or_filter":
            #      {"field": "parent_holder_net_profit_yoy", "args": [0], "exp": "less_than"}}#between

        ],#2023-4  所有报告，业绩公告，业绩快报，业绩预报  所有业绩 盈利大增，盈利略增 扭亏为盈 盈利大减 盈利略减 连续亏损 其他
        "sort_field": "declare_date",
        "sort_type": "desc"
    }
    try:
        response = requests.post(url, json=data, headers=headers)
        response.raise_for_status()  # 若请求不成功，抛出异常
        return response.json()  # 返回解析后的 JSON stock_data
    except requests.RequestException as e:
        print(f"请求出现错误: {e}")
        return None

def extract_result(data):
    if data and data['status_code'] == 0:
        result_list = data.get("testdata", {}).get("testdata", [])
        extracted_data = []
        for item in result_list:
            extracted_data.append({
                '股票代码': item.get('stock_code'),
                '股票名称': item.get('stock_name'),
                '预测净利润': item.get('parent_holder_net_profit'),
                '预测净利润同比增长率': item.get('parent_holder_net_profit_yoy'),
                '预测营业收入': item.get('operating_income'),
                '预测营业收入同比增长率': item.get('operating_income_yoy'),
                # '业绩描述': item.get('performance_describe').strip()
            })
        return extracted_data
    return []

if __name__ == "__main__":
    api_data = post_api_data()
    pprint(api_data)
    extracted_result = extract_result(api_data)
    if extracted_result:
        df = pd.DataFrame(extracted_result)
        print(df)
        df.to_excel('业绩数据.xlsx', index=False)
    else:
        print("未提取到有效数据")