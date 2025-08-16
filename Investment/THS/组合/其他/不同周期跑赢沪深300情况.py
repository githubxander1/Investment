from pprint import pprint

import pandas as pd
import requests


def get_portfolio_profitability_period_win_hs300(id):
    # 请求的URL
    url = "https://t.10jqka.com.cn/portfolioedge/calculate/v1/get_portfolio_profitability"
    # 请求头，直接复制你提供的内容
    headers = {
        "Host": "估值.py.10jqka.com.cn",
        "Connection": "keep-alive",
        "Accept": "application/json, text/plain, */*",
        "User-Agent": "Mozilla/5.0 (Linux; Android 9; ASUS_I003DD Build/PI; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/68.0.3440.70 Mobile Safari/537.36 Hexin_Gphone/11.17.03 (Royal Flush) hxtheme/0 innerversion/G037.08.983.1.32 followPhoneSystemTheme/0 userid/641926488 getHXAPPAccessibilityMode/0 hxNewFont/1 isVip/0 getHXAPPFontSetting/normal getHXAPPAdaptOldSetting/0",
        "Content-Type": "application/x-www-form-urlencoded",
        "Referer": "https://t.10jqka.com.cn/pkgfront/tgService.html?type=portfolio&id=14533",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,en-US;q=0.9",
        "X-Requested-With": "com.hexin.plat.android"
    }

    params = {
        "id": id
    }

    # 发送GET请求
    response = requests.get(url, headers=headers, params=params)

    # 判断请求是否成功（状态码为200表示成功）
    if response.status_code == 200:
        result = response.json()
        pprint(result)
        # 翻译字段
        translated_result = {
            "stock_data": {
                "盈利水平": result["testdata"]["profitabilityLevel"],
                "时间跨度": result["testdata"]["timeSpan"],
                "盈利数据列表": [
                    {
                        "时间跨度": item["timeSpan"],
                        "组合收益": item["portfolioIncome"],
                        "沪深300收益": item["hs300Income"]
                    }
                    for item in result["testdata"]["profitabilityDataList"]
                ]
            }
        }
        pprint(translated_result)

        # 将翻译后的数据转换为DataFrame格式，方便后续保存为Excel
        df = pd.DataFrame(translated_result["stock_data"]["盈利数据列表"])
        df["组合收益"] = df["组合收益"].apply(lambda x: f"{x:.2%}")
        df["沪深300收益"] = df["沪深300收益"].apply(lambda x: f"{x:.2%}")

        # 合并组合收益和沪深300收益为一行
        df['收益对比'] = df.apply(lambda row: f"组合收益: {row['组合收益']}, 沪深300收益: {row['沪深300收益']}", axis=1)

        # 选择需要的列
        df_final = df[['时间跨度', '收益对比']]


        print(df_final)

    else:
        print(f"请求失败，状态码: {response.status_code}")
        return None

# 示例调用
result = get_portfolio_profitability_period_win_hs300(14533)
if result is not None:
    print(result)


