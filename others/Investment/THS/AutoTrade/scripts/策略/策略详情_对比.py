import logging

import pandas as pd
import requests
from openpyxl import Workbook
from openpyxl.utils.dataframe import dataframe_to_rows

from others.Investment.THS.AutoTrade.config.settings import Strategy_ids, Strategy_metrics_file

logging.basicConfig(level=logging.INFO, format="%(asctime)s-%(levername)s-%(message)s")

def strategy_detail(strategy_id):
    url = "https://ms.10jqka.com.cn/iwencai/iwc-web-business-center/strategy_unify/detail"
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
    params = {
        "strategyId": strategy_id,
        # "_": "155259"
    }

    # 发送GET请求
    response = requests.get(url, headers=headers, params=params)

    # 判断请求是否成功（状态码为200表示成功）
    if response.status_code != 200:
        logging.warning(f"Failed to fetch testdata for strategy ID {strategy_id}. Status code: {response.status_code}")
        return []

    try:
        extract_data = []
        result = response.json()['result']
        # pprint(result)
        if not result:
            return []
        else:
            annualYield = result["annualYield"]
            strategyName = result["strategyName"]
            strategyType = result["strategyType"]
            description = result["description"]
            hqCodes = result["hqCodes"]
            rises = result["rises"]
            subType = result["subType"]
            investIdea = result["investIdea"]
            investPeriod = result["investPeriod"]
            investStyle = result["investStyle"]
            klineNum = result["klineNum"]
            latestTradingDay = result["latestTradingDay"]
            marketCodes = result["marketCodes"]
            maxDrawDown = result["maxDrawDown"]
            query = result["query"]
            rateOfVolatility = result["rateOfVolatility"]
            saleTime = result["saleTime"]
            buyTime = result["buyTime"]
            stkCodes = result["stkCodes"]
            stkNames = result["stkNames"]
            totalProfitRate = result["totalProfitRate"]
            tradeRule = result["tradeRule"]

            stockInfoList = result["stockInfoList"]
            for stockInfo in stockInfoList:
                code = stockInfo["code"]
                hqCode = stockInfo["hqCode"]
                marketCode = stockInfo["marketCode"]
                rise = stockInfo["rise"]
                stkCode = stockInfo["stkCode"]
                stkName = stockInfo["stkName"]

            conditions = result["conditions"]
            for condition in conditions:
                conditionKey = condition["conditionKey"]
                conditionValue = condition["conditionValue"]
                description = condition["description"]

            anylysis = result["title"]
            win_rate_value = None
            sharpe_rate_value = None
            industry_top3_rate_value = None
            for anylysi in anylysis:
                if anylysi["key"] == "win_rate":
                    win_rate_value = anylysi['value']
                elif anylysi["key"] == "sharpe_rate":
                    sharpe_rate_value = anylysi["value"]
                elif anylysi["key"] == "industry_top3_rate":
                    industry_top3_rate_value = anylysi["value"]
                # label = anylysi["label"]
                # name = anylysi["name"]
                # value = anylysi["value"]

            # 提取 stkName 和 rise 字段
            extracted_info = [{"stkName": stock["stkName"], "rise": stock["rise"]} for stock in stockInfoList]

            extract_data.append({
                "策略ID": strategy_id,
                "策略名称": strategyName,
                "描述": description,
                "说明": investIdea,
                "周期": investPeriod,
                "风格": investStyle,
                "子风格": subType,
                "选股": query,
                "规则": tradeRule,

                "总利润率": f"{totalProfitRate * 100:.2f}%",
                # "总利润率": totalProfitRate * 100:.2f,
                "年化收益": f'{annualYield * 100:.2f}%',
                "最大回撤-20%": f"{maxDrawDown * 100:.2f}%",
                "波动率": f"{rateOfVolatility * 100:.2f}%",
                "胜率": f"{win_rate_value * 100:.2f}%",
                "夏普比率-超额收益": sharpe_rate_value,
                "持仓所属行业集中度": f"{industry_top3_rate_value * 100:.2f}%",

                "选股结果": extracted_info,
            })

        return extract_data
    except Exception as e:
        logging.error(f"Error processing testdata for strategy ID {strategy_id}: {str(e)}")
        return []
def save_to_excel(df, filename):
    wb = Workbook()
    ws = wb.active

    # 将 DataFrame 写入工作表
    for r in dataframe_to_rows(df, index=False, header=True):
        ws.append(r)

    # 自动调整列宽
    for column_cells in ws.columns:
        length = max(len(str(cell.value)) for cell in column_cells)
        column = column_cells[0].column_letter
        ws.column_dimensions[column].width = length + 2  # 加2作为缓冲

    wb.save(filename)


def main():
    # 要查询的id列表
    strategy_ids = Strategy_ids
    all_results = []

    # 遍历每个id
    for strategy_id in strategy_ids:
        result = strategy_detail(strategy_id)
        # pprint(result)
        if result:
            all_results.extend(result)
        # print(all_results)
        else:
            logging.info("没有成功获取任何数据")

    # 打印到控制台
    if all_results:
        df_all = pd.DataFrame(all_results)
        df_all.to_excel(Strategy_metrics_file, index=False)
        print('保存成功')
    else:
        logging.info("No successful testdata retrieved for any strategies.")

if __name__ == "__main__":
    main()











    # 翻译字段
    # translated_result = {
    #     "策略ID": [result["result"]["strategyId"]],
    #     "策略名称": [result["result"]["strategyName"]],
    #     "图片链接": [result["result"]["pictureUrl"]],
    #     "夜间图片链接": [result["result"]["nightPictureUrl"]],
    #     "策略类型": [result["result"]["strategyType"]],
    #     "子类型": [result["result"]["subType"]],
    #     "投资风格": [result["result"]["investStyle"]],
    #     "收益": [result["result"]["title"]],
    #     "投资理念": [result["result"]["investIdea"]],
    #     "投资周期": [result["result"]["investPeriod"]],
    #     "描述": [result["result"]["description"]],
    #     "查询条件": [result["result"]["query"]],
    #     "条件": [result["result"]["conditions"]],
    #     "年化收益率": [result["result"]["annualYield"]],
    #     "波动率": [result["result"]["rateOfVolatility"]],
    #     "最大回撤": [result["result"]["maxDrawDown"]],
    #     "总利润率": [result["result"]["totalProfitRate"]],
    #     "形态类型": [result["result"]["shapeType"]],
    #     "K线数量": [result["result"]["klineNum"]],
    #     "形态周期": [result["result"]["shapePeriod"]],
    #     "最新交易日": [result["result"]["latestTradingDay"]],
    #     "买入时间": [result["result"]["buyTime"]],
    #     "卖出时间": [result["result"]["saleTime"]],
    #     "交易规则": [result["result"]["tradeRule"]],
    #     "有效": [result["result"]["valid"]],
    #     "创建人姓名": [result["result"]["masterName"]],
    #     "创建人描述": [result["result"]["masterDesc"]],
    #     "创建人报价": [result["result"]["masterQuotation"]],
    #     "股票代码": [result["result"]["stkCodes"]],
    #     "股票名称": [result["result"]["stkNames"]],
    #     "股票信息列表": [result["result"]["stockInfoList"]],
    #     "涨幅": [result["result"]["rises"]],
    #     "代码": [result["result"]["codes"]],
    #     "市场代码": [result["result"]["marketCodes"]],
    #     "行情代码": [result["result"]["hqCodes"]],
    # }

    # 处理 conditions 字段
#     conditions_data = []
#     for condition in result["result"]["conditions"]:
#         conditions_data.append({
#             "条件关键字": condition["conditionKey"],
#             "条件值": condition["conditionValue"],
#             "条件描述": condition["description"]
#         })
#     conditions_df = pd.DataFrame(conditions_data)
#
#     # 处理 title 字段
#     title_data = []
#     for title in result["result"]["title"]:
#         value = title['title']
#         "根据key判断是否需要转化成百分比"
#         if title["key"] in ["annual_yield","max_drawdown", "win_rate", "sharpe_rate", "industry_top3_rate"]:
#             value = f"{value * 100:.2f}%"
#         title_data.append({
#             "指标关键字": title["key"],
#             "指标标签": title["label"],
#             "指标名称": title["name"],
#             "指标值": value
#         })
#     title_df = pd.DataFrame(title_data)
#
#     # 将翻译后的数据转换为DataFrame格式，方便后续保存为Excel
#     main_df = pd.DataFrame(translated_result)
#     print(main_df)
#
#     # 合并所有 DataFrame
#     final_df = pd.concat([main_df, conditions_df, title_df], keys=["基本信息", "条件列表", "指标标题"])
#
#     # 保存为Excel文件，并添加中文备注
#     with pd.ExcelWriter("策略详情.xlsx", engine='openpyxl') as writer:
#         final_df.to_excel(writer, sheet_name="策略详情", index=False)
#         workbook = writer.book
#         worksheet = writer.sheets["策略详情"]
#
#         # 添加备注到Excel文件中
#         comment_text = "该表格展示了策略的各项详细信息，包括基本信息、收益风险指标、交易规则以及涉及的股票等内容，方便查看和分析策略情况。"
#         comment = Comment(comment_text, "Author")
#         worksheet['A1'].comment = comment
# else:
#     print(f"请求失败，状态码: {response.status_code}")
