from pprint import pprint

import requests
import pandas as pd

from pprint import pprint

import requests
import pandas as pd

def get_portfolio_profitability_period_win_hs300(id):
    # 请求的URL
    url = "https://t.10jqka.com.cn/portfolioedge/calculate/v1/get_portfolio_profitability"
    # 请求头，直接复制你提供的内容
    headers = {
        "Host": "t.10jqka.com.cn",
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

    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()  # 如果响应状态码不是200，会抛出异常
        data = response.json()
        # pprint(data)

        if 'data' in data and 'profitabilityDataList' in data['data']:
            profitabilityDataList = data["data"]["profitabilityDataList"]

            # 初始化结果字典
            result = {}

            for item in profitabilityDataList:
                time_span = item["timeSpan"]
                portfolio_income = f'{item["portfolioIncome"] * 100:.2f}%'
                hs300_income = f'{item["hs300Income"] * 100:.2f}%'

                # 将时间跨度作为列标题
                # result[f'时间跨度_{time_span}'] = time_span
                result[f'收益对比_{time_span}'] = {
                    '组合收益': portfolio_income,
                    '沪深300收益': hs300_income
                }

            return result
        else:
            print(f"API 响应格式不正确 (id={id}): {data}")
            return None
    except requests.RequestException as e:
        print(f"请求出现错误 (id={id}): {e}")
        return None
    except Exception as e:
        print(f"处理响应时出现错误 (id={id}): {e}")
        return None


# 示例调用
ids = [14533]  # 替换为实际的ID列表
profitability_info = get_portfolio_profitability_period_win_hs300(ids)
pprint(profitability_info)

