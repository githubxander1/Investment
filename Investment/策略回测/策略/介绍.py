import requests
import json
from requests.exceptions import RequestException

# 接口配置
url = "https://prod-lianghuawang-api.yd.com.cn/liangHuaEntrance/l/getLiangHuaCeLue"
headers = {
    "accept": "application/json",
    "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1aWQiOiIwIiwidiI6MSwiY2xhaW1zIjp7ImNhdGlkIjowLCJzeXNyb2xlIjoidXNlciIsInBpZCI6MCwidmlzaXRvciI6MSwidXNlcmlkIjowfSwiYWRtaW4iOmZhbHNlLCJleHAiOjE3NTY4MjQ2MDEsImlhdCI6MTc1NDE0NjIwMX0.TbqTdscc1UyS6E3XYJgu9zGEbIgDBb8X4B_HR0Jwte0",
    "Content-Type": "application/json",
    "Host": "prod-lianghuawang-api.yd.com.cn",
    "Connection": "Keep-Alive",
    "Accept-Encoding": "gzip",
    "User-Agent": "okhttp/4.12.0"
}

# 请求体（查询id为8007的策略介绍）
payload = {"id": "8007"}

try:
    # 发送POST请求
    response = requests.post(
        url,
        headers=headers,
        json=payload,  # 自动处理JSON序列化
        timeout=10
    )
    response.raise_for_status()  # 状态码非200时抛出异常

    # 解析响应数据（假设为策略介绍信息）
    strategy_info = response.json()
    print("===== 策略介绍响应原始数据 =====")
    print(json.dumps(strategy_info, ensure_ascii=False, indent=2))  # 格式化打印，方便查看结构

    # 提取介绍相关关键字段（根据实际响应结构调整字段名，以下为常见假设）
    intro_fields = {
        "策略ID": strategy_info.get("id", "未知"),
        "策略名称": strategy_info.get("name", "未知"),
        "策略简介": strategy_info.get("intro", "无简介信息"),
        "策略详情": strategy_info.get("detail", "无详情信息"),
        "策略特点": strategy_info.get("features", "无特点描述"),
        "创建时间": strategy_info.get("createTime", "未知")
    }

    # 打印提取的介绍信息
    print("\n===== 策略核心介绍 =====")
    for key, value in intro_fields.items():
        print(f"{key}: {value}")

    # 保存介绍信息到文本文件
    with open("strategy_8007_intro.txt", "w", encoding="utf-8") as f:
        f.write("策略介绍信息:\n")
        for key, value in intro_fields.items():
            f.write(f"{key}: {value}\n")
    print("\n===== 介绍信息已保存 =====")
    print(f"文件路径: strategy_8007_intro.txt")

except RequestException as e:
    print(f"\n===== 请求失败 =====")
    print(f"错误信息: {str(e)}")
except Exception as e:
    print(f"\n===== 数据处理失败 =====")
    print(f"错误信息: {str(e)}")