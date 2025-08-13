from pprint import pprint
import requests
import pandas as pd
import json
from requests.exceptions import RequestException

def get_data():
    # 基础配置
    url = "https://prod-lianghuawang-api.yd.com.cn/rankingEntrance/list"
    headers = {
        "accept": "application/json",
        "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1aWQiOiIwIiwidiI6MSwiY2xhaW1zIjp7ImNhdGlkIjowLCJzeXNyb2xlIjoidXNlciIsInBpZCI6MCwidmlzaXRvciI6MSwidXNlcmlkIjowfSwiYWRtaW4iOmZhbHNlLCJleHAiOjE3NTY4MjE1OTcsImlhdCI6MTc1NDE0MzE5N30.aiSRRVBnz02QXx28Z1CAFOKsOaySsyo_G9JxFb1UomU",
        "Content-Type": "application/json",
        "Host": "prod-lianghuawang-api.yd.com.cn",
        "Connection": "Keep-Alive",
        "Accept-Encoding": "gzip",
        "User-Agent": "okhttp/4.12.0"
    }

    # 基础请求体（仅timeRange会动态修改）
    base_payload = {
        "timeRange": "",  # 此处会替换为week/year/all
        "policyType": 0,
        "pageNo": 1,
        "pageSize": 20,
        "order": "desc",
        "winYear": ["", ""],
        "backtestingIncome": ["", ""],
        "maxIncome": ["", ""],
        "winRate": ["", ""],
        "xpbl": ["", ""],
        "winLoseRatio": ["", ""],
        "style": None,
        "riskPreference": None,
        "fundingVolume": None
    }

    # 复制基础请求体并修改timeRange
    payload = base_payload.copy()
    # payload["timeRange"] = tr.upper()  # 接口可能需要大写（原请求是WEEK，这里统一转大写）

    # 发送POST请求
    response = requests.post(
        url,
        headers=headers,
        data=json.dumps(payload),  # 手动序列化JSON（确保格式正确）
        timeout=10
    )
    response.raise_for_status()  # 状态码非200时抛出异常

    # 解析响应（假设数据在'result'字段中，根据实际响应调整）
    data = response.json()
    # print(f"\n===== timeRange: {tr} 原始响应 =====")
    return data



def extract_important_data(raw_data):
    """
    提取重要数据字段
    """

    # if "data" in raw_data and isinstance(raw_data["data"], dict) and "results" in raw_data["data"]:
    raw_results = raw_data["data"]["results"]
    print(f"原始数据条数: {len(raw_results) if raw_results else 0}")

    if not raw_results or not isinstance(raw_results, list):
        return pd.DataFrame()

    important_fields = []
    for item in raw_results:
        if not isinstance(item, dict):
            continue

        extracted = {
            '策略ID': item.get('lhid', ''),
            '策略名称': item.get('name', ''),
            '年化收益': item.get('winYear', 0),
            '回测收益': item.get('backtestingIncome', 0),
            '最大收益': item.get('maxIncome', 0),
            '胜率': item.get('winRate', 0),
            '盈亏比': item.get('winLoseRatio', 0),
            '夏普比率': item.get('xpbl', 0),
            '总收益': item.get('cesy', 0),
            '近1月收益': item.get('ysy', 0),
            '近3月收益': item.get('zsy', 0),
            '近6月收益': item.get('hnsy', 0),
            '风格': item.get('style', ''),
            '风险偏好': item.get('riskPreference', ''),
            '资金规模': item.get('fundingVolume', ''),
            '简介': item.get('introduction', '')
        }
        important_fields.append(extracted)

    return pd.DataFrame(important_fields)

def main():
    # 需要查询的timeRange列表
    time_ranges = ["week", "year", "all"]

    # 存储所有结果的字典（key: timeRange, value: DataFrame）
    results = {}
    # 循环发送请求
    for tr in time_ranges:
        try:
            raw_results = get_data()
            # 提取重要数据
            df = extract_important_data(raw_results)

            if not df.empty:
                results[tr] = df
                print(f"\n===== timeRange: {tr} 提取后数据 =====")
                print(f"提取后数据条数: {len(df)}")
                print(df.head())  # 打印前几行
            else:
                print(f"\n===== timeRange: {tr} 无有效数据 =====")
                print("原因: 数据提取后为空")

        except RequestException as e:
            print(f"\n===== timeRange: {tr} 请求失败 =====")
            print(f"错误信息: {str(e)}")
        except Exception as e:
            print(f"\n===== timeRange: {tr} 处理失败 =====")
            print(f"错误信息: {str(e)}")
            import traceback
            traceback.print_exc()

    # 保存到同一个Excel文件的不同工作表
    print(f"\n===== 保存数据 =====")
    print(f"有数据的timeRange数量: {len(results)}")

    if results:
        try:
            with pd.ExcelWriter("Strategy_ranking_results.xlsx", engine="openpyxl") as writer:
                for tr, df in results.items():
                    # 工作表名用timeRange（小写）
                    df.to_excel(writer, sheet_name=tr, index=False)
                    print(f"已保存 {tr} 数据，共 {len(df)} 条记录")
            print("\n===== 数据保存成功 =====")
            print(f"文件路径: Strategy_ranking_results.xlsx")
        except Exception as e:
            print(f"\n===== 数据保存失败 =====")
            print(f"错误信息: {str(e)}")
            import traceback
            traceback.print_exc()
    else:
        print("\n===== 无有效数据可保存 =====")
        print("可能原因:")
        print("1. 所有请求都失败了")
        print("2. 请求成功但返回的数据为空")
        print("3. 数据提取过程出现问题")
        print("4. 数据过滤后为空")

if __name__ == '__main__':
    main()