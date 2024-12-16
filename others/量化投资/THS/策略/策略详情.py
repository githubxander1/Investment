from pprint import pprint
import requests
import pandas as pd
from openpyxl import Workbook
from openpyxl.comments import Comment

# 请求的URL
url = "https://ms.10jqka.com.cn/iwencai/iwc-web-business-center/strategy_unify/detail?strategyId=155259"
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
    pprint(result)

    # 翻译字段
    translated_result = {
        "策略ID": [result["result"]["strategyId"]],
        "策略名称": [result["result"]["strategyName"]],
        "图片链接": [result["result"]["pictureUrl"]],
        "夜间图片链接": [result["result"]["nightPictureUrl"]],
        "策略类型": [result["result"]["strategyType"]],
        "子类型": [result["result"]["subType"]],
        "投资风格": [result["result"]["investStyle"]],
        "收益": [result["result"]["title"]],
        "投资理念": [result["result"]["investIdea"]],
        "投资周期": [result["result"]["investPeriod"]],
        "描述": [result["result"]["description"]],
        "查询条件": [result["result"]["query"]],
        "条件": [result["result"]["conditions"]],
        "年化收益率": [result["result"]["annualYield"]],
        "波动率": [result["result"]["rateOfVolatility"]],
        "最大回撤": [result["result"]["maxDrawDown"]],
        "总利润率": [result["result"]["totalProfitRate"]],
        "形态类型": [result["result"]["shapeType"]],
        "K线数量": [result["result"]["klineNum"]],
        "形态周期": [result["result"]["shapePeriod"]],
        "最新交易日": [result["result"]["latestTradingDay"]],
        "买入时间": [result["result"]["buyTime"]],
        "卖出时间": [result["result"]["saleTime"]],
        "交易规则": [result["result"]["tradeRule"]],
        "有效": [result["result"]["valid"]],
        "创建人姓名": [result["result"]["masterName"]],
        "创建人描述": [result["result"]["masterDesc"]],
        "创建人报价": [result["result"]["masterQuotation"]],
        "股票代码": [result["result"]["stkCodes"]],
        "股票名称": [result["result"]["stkNames"]],
        "股票信息列表": [result["result"]["stockInfoList"]],
        "涨幅": [result["result"]["rises"]],
        "代码": [result["result"]["codes"]],
        "市场代码": [result["result"]["marketCodes"]],
        "行情代码": [result["result"]["hqCodes"]],
    }

    # 处理 conditions 字段
    conditions_data = []
    for condition in result["result"]["conditions"]:
        conditions_data.append({
            "条件关键字": condition["conditionKey"],
            "条件值": condition["conditionValue"],
            "条件描述": condition["description"]
        })
    conditions_df = pd.DataFrame(conditions_data)

    # 处理 title 字段
    title_data = []
    for title in result["result"]["title"]:
        value = title['title']
        "根据key判断是否需要转化成百分比"
        if title["key"] in ["annual_yield","max_drawdown", "win_rate", "sharpe_rate", "industry_top3_rate"]:
            value = f"{value * 100:.2f}%"
        title_data.append({
            "指标关键字": title["key"],
            "指标标签": title["label"],
            "指标名称": title["name"],
            "指标值": value
        })
    title_df = pd.DataFrame(title_data)

    # 将翻译后的数据转换为DataFrame格式，方便后续保存为Excel
    main_df = pd.DataFrame(translated_result)
    print(main_df)

    # 合并所有 DataFrame
    final_df = pd.concat([main_df, conditions_df, title_df], keys=["基本信息", "条件列表", "指标标题"])

    # 保存为Excel文件，并添加中文备注
    with pd.ExcelWriter("策略详情.xlsx", engine='openpyxl') as writer:
        final_df.to_excel(writer, sheet_name="策略详情", index=False)
        workbook = writer.book
        worksheet = writer.sheets["策略详情"]

        # 添加备注到Excel文件中
        comment_text = "该表格展示了策略的各项详细信息，包括基本信息、收益风险指标、交易规则以及涉及的股票等内容，方便查看和分析策略情况。"
        comment = Comment(comment_text, "Author")
        worksheet['A1'].comment = comment
else:
    print(f"请求失败，状态码: {response.status_code}")
