from pprint import pprint
import requests
import pandas as pd

from Investment.THS.AutoTrade.config.settings import Combination_headers

def strategy_list(sub_type):
    # 请求URL和参数
    url = "https://ms.10jqka.com.cn/iwencai/iwc-web-business-center/strategy_unify/strategies_page"
    params = {
        "type": "classic",
        "subType": sub_type,  # 解码后的中文：基本面
        "page": 0,
        "pageSize": 10,
        "annualYieldOrder": ""
    }
    headers = Combination_headers

    try:
        # 发送请求
        response = requests.get(url, params=params, headers=headers)

        # 检查响应状态
        if response.status_code == 200:
            return response.json()  # 假设返回JSON数据
        else:
            print(f"请求失败，状态码: {response.status_code}")
            return None
    except Exception as e:
        print(f"请求发生错误: {e}")
        return None

# 定义 sub_types
sub_types = ["基本面", "技术面", "资金面", "消息面"]

# 创建一个字典来存储每个 sub_type 的数据
data_dict = {}

for sub_type in sub_types:
    result = strategy_list(sub_type)
    if result and 'result' in result:
        data_dict[sub_type] = result['result']['datas']
    else:
        data_dict[sub_type] = []

# 提取重要数据
def extract_important_data(datas):
    important_data = []
    seen_strategy_ids = set()  # 用于存储已见过的 strategyId

    for data in datas:
        strategy_id = data.get('strategyId', '')
        if strategy_id in seen_strategy_ids:
            continue  # 跳过已见过的 strategyId

        seen_strategy_ids.add(strategy_id)

        stock_info_list = data.get('stockInfoList', [])
        if not isinstance(stock_info_list, list):
            stock_info_list = []
        else:
            stock_info_list = [info for info in stock_info_list if isinstance(info, dict)]

        item = {
            'subType': data.get('subType', ''),
            'strategyType': data.get('strategyType', ''),
            'strategyId': strategy_id,
            'strategyName': data.get('strategyName', ''),
            'annualYield': data.get('annualYield', ''),
            'investStyle': data.get('investStyle', ''),
            'investIdea': data.get('investIdea', ''),
            'investPeriod': data.get('investPeriod', ''),
            'description': data.get('description', ''),
            'totalProfitRate': data.get('totalProfitRate', ''),
            'maxDrawDown': data.get('maxDrawDown', ''),
            'rateOfVolatility': round(data.get('rateOfVolatility', 0), 2),
            'tradeRule': data.get('tradeRule', ''),
            'query': data.get('query', ''),
            'buyTime': data.get('buyTime', ''),
            'saleTime': data.get('saleTime', ''),
            'stockInfoList': stock_info_list
        }
        important_data.append(item)

    return important_data


important_data_dict = {sub_type: extract_important_data(data) for sub_type, data in data_dict.items()}

# 保存到 Excel 文件
with pd.ExcelWriter('strategy_data.xlsx') as writer:
    for sub_type, data in important_data_dict.items():
        df = pd.DataFrame(data)
        # print(df)

        if 'stockInfoList' in df.columns and not df['stockInfoList'].empty:
            df['stockInfoList'] = df['stockInfoList'].apply(lambda x: x if isinstance(x, list) else [])
            df_expanded = df.explode('stockInfoList').reset_index(drop=True)
            df_expanded['stockInfoList'] = df_expanded['stockInfoList'].apply(lambda x:
                {'stkName': x.get('stkName', ''), 'stkCode': x.get('stkCode', '')} if isinstance(x, dict) else
                {'stkName': '', 'stkCode': ''}
            )
            df_expanded[['stkName', 'stkCode']] = pd.DataFrame(df_expanded['stockInfoList'].tolist(), index=df_expanded.index)
            df_expanded.drop(columns=['stockInfoList'], inplace=True)
            df_expanded.to_excel(writer, sheet_name=sub_type, index=False)
        else:
            df.to_excel(writer, sheet_name=sub_type, index=False)

print("数据已成功保存到 strategy_data.xlsx")
