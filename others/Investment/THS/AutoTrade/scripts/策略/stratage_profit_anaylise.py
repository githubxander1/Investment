from pprint import pprint
import pandas as pd
import requests
from urllib.parse import quote
from others.Investment.THS.AutoTrade.config.settings import Strategy_metrics_file

def strategy_analyse(trading_metrics):
    # url = "https://ms.10jqka.com.cn/iwencai/iwc-web-business-center/strategy_unify/risk_analyse?strategyId=138036&period=all"
    # url = "https://ms.10jqka.com.cn/iwencai/iwc-web-business-center/strategy_unify/win_rate_analyse?strategyId=138036&period=all"
    url = f"https://ms.10jqka.com.cn/iwencai/iwc-web-business-center/strategy_unify/{trading_metrics}?strategyId=138036&period=all"
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
        response_json = response.json()
        pprint(response_json)

        # 定义字段映射
        field_mappings = {
            'win_rate_analyse': [
                {"策略胜率%": lambda x: round(x['result']['winRate'] * 100, 2)}
            ],
            'risk_analyse': [
                {"最大回撤%": lambda x: round(x['result']['benchmarkDrawDown'] * 100, 2)},
                {"策略回测%": lambda x: round(x['result']['strategyDrawDown'] * 100, 2)},
                {"沪深300回撤%": lambda x: round(x['result']['benchmarkDrawDown'] * 100, 2)},
                {"策略最长回撤天数": lambda x: round(x['result']['strategyMaxDrawDownDays'], 2)}
            ],
            'profit_analyse': [
                {"策略%": lambda x: round(x['result']['strategyYield'] * 100, 2)},
                {"基准%(沪深300)": lambda x: round(x['result']['benchmarkYield'] * 100, 2)},
                {"年化%": lambda x: round(x['result']['annualYield'] * 100, 2)},
                {"超额%": lambda x: round(x['result']['excessYield'] * 100, 2)}
            ],
            'sharpe_analyse': [
                {"策略夏普比率": lambda x: round(x['result']['sharpeRate'], 2)}
            ]
        }

        # 提取数据
        if trading_metrics in field_mappings:
            result = []
            for field in field_mappings[trading_metrics]:
                for key, func in field.items():
                    result.append({key: func(response_json)})
            return result
        else:
            print(f"未找到 {trading_metrics} 的字段映射")
            return []
    except requests.RequestException as e:
        print(f"请求出错: {e}")
        return None

metrics_list = ['win_rate_analyse', 'risk_analyse', 'profit_analyse', 'sharpe_analyse']

# 使用 ExcelWriter 来管理 Excel 文件的写入操作
with pd.ExcelWriter(Strategy_metrics_file, engine='openpyxl') as writer:
    for trading_metrics in metrics_list:
        result = strategy_analyse(trading_metrics)
        if result:
            pprint(result)
            df = pd.DataFrame(result)
            df.to_excel(writer, sheet_name=f'{trading_metrics}', index=False)
        else:
            print(f"未获取到 {trading_metrics} 数据")
