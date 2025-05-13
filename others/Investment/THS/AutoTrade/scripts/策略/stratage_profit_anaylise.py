from pprint import pprint
import pandas as pd
import requests
from urllib.parse import quote
from others.Investment.THS.AutoTrade.config.settings import Strategy_metrics_file, Combination_headers
import os

# def strategy_analyse(trading_metrics):
# 导入配置
from others.Investment.THS.AutoTrade.config.settings import Strategy_ids, Strategy_id_to_name, DATA_DIR

def strategy_analyse(trading_metrics, strategy_id):
    # url = "https://ms.10jqka.com.cn/iwencai/iwc-web-business-center/strategy_unify/risk_analyse?strategyId=138036&period=all"
    # url = "https://ms.10jqka.com.cn/iwencai/iwc-web-business-center/strategy_unify/win_rate_analyse?strategyId=138036&period=all"
    url = f"https://ms.10jqka.com.cn/iwencai/iwc-web-business-center/strategy_unify/{trading_metrics}?strategyId=138036&period=all"
    url = f"https://ms.10jqka.com.cn/iwencai/iwc-web-business-center/strategy_unify/{trading_metrics}?strategyId={strategy_id}&period=all"
    # url = "https://ms.10jqka.com.cn/iwencai/iwc-web-business-center/strategy_unify/profit_analyse?strategyId=138036&period=all"
    # url = "https://ms.10jqka.com.cn/iwencai/iwc-web-business-center/strategy_unify/profit_analyse?strategyId=138036&period=year"
    # url = "https://ms.10jqka.com.cn/iwencai/iwc-web-business-center/strategy_unify/profit_analyse?strategyId=138036&period=month"
# @@ -31,7 +34,7 @@ def strategy_analyse(trading_metrics):
    response = requests.get(url, headers=Combination_headers)
    response.raise_for_status()  # 检查请求是否成功
    response_json = response.json()
    pprint(response_json)
    # pprint(response_json)

    # 定义字段映射
    field_mappings = {
        'win_rate_analyse': [
            {"策略胜率%": lambda x: round(x['result']['winRate'] * 100, 2)}
        ],
        'risk_analyse': [
            {"最大回撤%": lambda x: round(x['result']['benchmarkDrawDown'] * 100, 2)},
            {"策略回撤%": lambda x: round(x['result']['strategyDrawDown'] * 100, 2)},
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
        # result = []
        result = {}
        for field in field_mappings[trading_metrics]:
            for key, func in field.items():
                result.append({key: func(response_json)})
                result[key] = func(response_json)
        return result
    else:
        print(f"未找到 {trading_metrics} 的字段映射")
        # return []
        return {}
# except requests.RequestException as e:
#     print(f"请求出错: {e}")
#     # return None
#     return {}


metrics_list = ['win_rate_analyse', 'risk_analyse', 'profit_analyse', 'sharpe_analyse']

# # 使用 ExcelWriter 来管理 Excel 文件的写入操作
# with pd.ExcelWriter(Strategy_metrics_file, engine='openpyxl') as writer:
#     for trading_metrics in metrics_list:
#         result = strategy_analyse(trading_metrics)
#         if result:
#             pprint(result)
#             df = pd.DataFrame(result)
#             df.to_excel(writer, sheet_name=f'{trading_metrics}', index=False)
#         else:
#             print(f"未获取到 {trading_metrics} 数据")

# 合并所有指标为一个 DataFrame 行
def combine_strategy_data(strategy_id):
    combined_data = {"策略ID": strategy_id, "策略名称": Strategy_id_to_name.get(strategy_id, "未知策略")}
    for metric in metrics_list:
        result = strategy_analyse(metric, strategy_id)
        combined_data.update(result)
    return combined_data


# 收集所有策略数据
all_strategy_data = []
for strategy_id in Strategy_ids:
    row_data = combine_strategy_data(strategy_id)
    all_strategy_data.append(row_data)

# 创建 DataFrame
df_all = pd.DataFrame(all_strategy_data)

# 控制台打印
print(df_all.to_string(index=False))

# 保存为 CSV 文件
csv_output_path = os.path.join(DATA_DIR, "所有策略绩效汇总.csv")
df_all.to_csv(csv_output_path, index=False, encoding='utf-8-sig')
print(f"\n已保存所有策略数据至: {csv_output_path}")

# # 如果需要保存为 Excel，也可以加一句：
# excel_output_path = os.path.join(DATA_DIR, "所有策略绩效汇总.xlsx")
# df_all.to_excel(excel_output_path, index=False)
# print(f"已保存所有策略数据至: {excel_output_path}")