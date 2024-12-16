import requests
import pandas as pd

# 请求的URL
url = "https://ms.10jqka.com.cn/iwencai/iwc-web-business-center/strategy_unify/relate_recommend?strategyId=155259&type=classic"
# 请求头，直接复制提供内容
headers = {
    "Host": "ms.10jqka.com.cn",
    "Connection": "keep-alive",
    "Origin": "https://bowerbird.10jqka.com.cn",
    "User-Agent": "Mozilla/5.0 (Linux; Android 9; ASUS_I003DD Build/PI; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/68.0.3440.70 Mobile Safari/537.36 Hexin_Gphone/11.17.03 (Royal Flush) hxtheme/0 innerversion/G037.08.983.1.32 followPhoneSystemTheme/0 userid/641926488 getHXAPPAccessibilityMode/0 hxNewFont/1 isVip/0 getHXAPPFontSetting/normal getHXAPPAdaptOldSetting/0",
    "Accept": "*/*",
    "Referer": "https://bowerbird.10jqka.com.cn/thslc/editor/view/15f2E0a579?strategyId=155259",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "zh-CN,en-US;q=0.9",
    "X-Requested-With": "com.hexin.plat.android"
}

# 发送GET请求
response = requests.get(url, headers=headers)

# 判断请求是否成功（状态码为200表示成功）
if response.status_code == 200:
    result = response.json()
    # 提取重要信息并翻译字段
    extracted_data = []
    columns = [col["index_name"] for col in result["columns"]]
    for data in result["datas"]:
        extracted_data.append({
            "策略名称": data["strategyName"],
            "投资理念": data["investIdea"],
            "波动率": data["rateOfVolatility"],
            "查询条件": data["query"],
            "年化收益率": data["annualYield"],
            "描述": data["description"],
            "总利润率": data["totalProfitRate"],
            "买入时间": data["buyTime"],
            "投资周期": data["investPeriod"],
            "策略类型": data["strategyType"],
            "是否有效": data["valid"],
            "卖出时间": data["saleTime"],
            "投资风格": data["investStyle"],
            "策略ID": data["strategyId"],
            "子类型": data["subType"],
            "最大回撤": data["maxDrawDown"],
            "交易规则": data["tradeRule"],
            "股票代码1": data.get("stkCodes1", ""),
            "股票代码2": data.get("stkCodes2", ""),
            "股票名称1": data.get("stkNames1", ""),
            "股票名称2": data.get("stkNames2", ""),
            "涨幅1": data.get("rises1", ""),
            "涨幅2": data.get("rises2", ""),
            "代码1": data.get("codes1", ""),
            "代码2": data.get("codes2", ""),
            "市场代码1": data.get("marketCodes1", ""),
            "市场代码2": data.get("marketCodes2", "")
        })

    # 将提取的数据转换为DataFrame格式
    df = pd.DataFrame(extracted_data)
    # 在控制台显示数据
    print(df)
    # 保存为Excel文件
    df.to_excel("策略推荐信息.xlsx", index=False)
else:
    print(f"请求失败，状态码: {response.status_code}")