import requests
import pandas as pd
import json
from requests.exceptions import RequestException

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

# 需要查询的timeRange列表
time_ranges = ["week", "year", "all"]

# 存储所有结果的字典（key: timeRange, value: DataFrame）
results = {}

# 循环发送请求
for tr in time_ranges:
    try:
        # 复制基础请求体并修改timeRange
        payload = base_payload.copy()
        payload["timeRange"] = tr.upper()  # 接口可能需要大写（原请求是WEEK，这里统一转大写）

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
        if "result" in data and isinstance(data["result"], list):
            df = pd.DataFrame(data["result"])
            results[tr] = df
            print(f"\n===== timeRange: {tr} 数据 =====")
            print(df)  # 打印DataFrame
        else:
            print(f"\n===== timeRange: {tr} 响应格式异常 =====")
            print("响应内容:", data)

    except RequestException as e:
        print(f"\n===== timeRange: {tr} 请求失败 =====")
        print(f"错误信息: {str(e)}")
    except Exception as e:
        print(f"\n===== timeRange: {tr} 处理失败 =====")
        print(f"错误信息: {str(e)}")

# 保存到同一个Excel文件的不同工作表
if results:
    try:
        with pd.ExcelWriter("ranking_results.xlsx", engine="openpyxl") as writer:
            for tr, df in results.items():
                # 工作表名用timeRange（小写）
                df.to_excel(writer, sheet_name=tr, index=False)
        print("\n===== 数据保存成功 =====")
        print(f"文件路径: ranking_results.xlsx")
    except Exception as e:
        print(f"\n===== 数据保存失败 =====")
        print(f"错误信息: {str(e)}")
else:
    print("\n===== 无有效数据可保存 =====")