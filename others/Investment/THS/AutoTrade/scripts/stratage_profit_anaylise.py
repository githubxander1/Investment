from pprint import pprint

import requests


def strategy_profit_analyse():
    # url = "https://ms.10jqka.com.cn/iwencai/iwc-web-business-center/strategy_unify/risk_analyse?strategyId=138036&period=all"
    # url = "https://ms.10jqka.com.cn/iwencai/iwc-web-business-center/strategy_unify/win_rate_analyse?strategyId=138036&period=all"
    url = "https://ms.10jqka.com.cn/iwencai/iwc-web-business-center/strategy_unify/sharpe_analyse?strategyId=138036&period=all"
    # url = "https://ms.10jqka.com.cn/iwencai/iwc-web-business-center/strategy_unify/profit_analyse?strategyId=138036&period=all"
    # url = "https://ms.10jqka.com.cn/iwencai/iwc-web-business-center/strategy_unify/profit_analyse?strategyId=138036&period=year"
    # url = "https://ms.10jqka.com.cn/iwencai/iwc-web-business-center/strategy_unify/profit_analyse?strategyId=138036&period=month"
    # url = "https://ms.10jqka.com.cn/iwencai/iwc-web-business-center/strategy_unify/profit_analyse?strategyId=138036&period=week"
    headers = {
        "Host": "ms.10jqka.com.cn",
        "Connection": "keep-alive",
        "User-Agent": "Mozilla/5.0 (Linux; Android 10; Redmi Note 7 Pro Build/QKQ1.190915.002; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/87.0.4280.101 Mobile Safari/537.36 Hexin_Gphone/11.24.02 (Royal Flush) hxtheme/1 innerversion/G037.09.011.1.32 followPhoneSystemTheme/1 userid/641926488 getHXAPPAccessibilityMode/0 hxNewFont/1 isVip/0 getHXAPPFontSetting/normal getHXAPPAdaptOldSetting/0",
        "Accept": "*/*",
        "Origin": "https://bowerbird.10jqka.com.cn",
        "X-Requested-With": "com.hexin.plat.android",
        "Sec-Fetch-Site": "same-site",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Dest": "empty",
        "Referer": "https://bowerbird.10jqka.com.cn/thslc/editor/view/15f2E0a579?strategyId=138036",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7"
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # 检查请求是否成功

        response = response.json()
        pprint(response)
        # profit_result = []
        # profit_result.append({
        #     "策略%" : round(response['result']['strategyYield'] * 100, 2),
        #     "基准%(沪深300)" : round(response['result']['benchmarkYield'] * 100, 2),
        #     "年化%" : round(response['result']['annualYield'] * 100, 2),
        #     "超额%" : round(response['result']['excessYield'] * 100, 2),
        # })

        # risk_result = []
        # risk_result.append({
        #     "最大回撤%" : round(response['result']['benchmarkDrawDown'] * 100, 2),
        #     "策略回测%" : round(response['result']['strategyDrawDown'] * 100, 2),
        #     "沪深300回撤%" : round(response['result']['benchmarkDrawDown'] * 100, 2),
        #     "策略最长回撤天数" : round(response['result']['strategyMaxDrawDownDays'], 2),
        # })

        # win_rate_result = []
        # win_rate_result.append({
        #     "策略胜率%" : round(response['result']['winRate'] * 100, 2),
        # })

        sharpe_result = []
        sharpe_result.append({
            "策略夏普比率" : round(response['result']['sharpeRate'], 2),
        })

        # return risk_result
        # return win_rate_result
        return sharpe_result
    except requests.RequestException as e:
        print(f"请求出错: {e}")
        return None

result = strategy_profit_analyse()
if result:
    pprint(result)