from pprint import pprint

import pandas as pd
import requests

from urllib.parse import quote
from Investment.THS.AutoTrade.config.settings import Strategy_list_file


def get_strategy_list(type):

    # 使用 quote 方法对中文部分进行编码
    subType = quote(f"{type}")  # 将 "技术面" 转换为 URL 编码 基本面，技术面，资金面，消息面
    url = f"https://ms.10jqka.com.cn/iwencai/iwc-web-business-center/strategy_unify/strategies_page?type=classic&subType={subType}&page=0&pageSize=10&annualYieldOrder=desc"

    # print(url)
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
        "Referer": "https://bowerbird.10jqka.com.cn/thslc/editor/view/f2184305Bf",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7"
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # 检查请求是否成功
        response = response.json()
        pprint(response)

        # 提取需要的数据
        technical_result = response['result']['datas']
        technical_list= []
        for technical_result in technical_result:
            technical_list.append({
                "策略名称": technical_result['strategyName'],
                "策略ID": technical_result['strategyId'],
                "年化%": round(technical_result['annualYield'] * 100, 2),
                "最大回撤%": round(technical_result['maxDrawDown'] * 100,2),
                "波动率%": round(technical_result['rateOfVolatility'] * 100,2),
                "描述": technical_result['description'],
                "投资理念": technical_result['investIdea'],
                "投资周期": technical_result['investPeriod'],
                # "投资方式": technical_result['investStyle'],
                "选股规则": technical_result['query'],
                # "交易规则": (technical_result['buyTime'],technical_result['saleTime']),
            })
            # pprint(response)  # 打印响应内容
        return technical_list
    except requests.RequestException as e:
        print(f"请求发生错误: {e}")

type_list = ['基本面','技术面', '资金面', '消息面']

# 使用 ExcelWriter 来管理 Excel 文件的写入操作
with pd.ExcelWriter(Strategy_list_file, engine='openpyxl') as writer:
    for type in type_list:
        strategy_list_datas = get_strategy_list(type)
        pprint(f'{type}策略列表')
        if strategy_list_datas:
            df = pd.DataFrame(strategy_list_datas)
            df.to_excel(writer, sheet_name=f'{type}', index=False)
            pprint(df)
        else:
            print(f"未获取到 {type} 策略数据")
