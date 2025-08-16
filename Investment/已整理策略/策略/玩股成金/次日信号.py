
import requests
import json
from pprint import pprint

def nextday_single(robot_id="9a09cbd9-be78-469c-b3d2-b2d07ad50862"):
    url = "http://ai.api.traderwin.com/api/ai/robot/tip.json"

    headers = {
        "Content-Type": "application/json",
        "from": "Android",
        "token": "27129c04fb43a33723a9f7720f280ff9",
        "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 10; Redmi Note 7 Pro MIUI/V12.5.4.0.QFHCNXM)",
        "Accept-Encoding": "gzip",
        "Connection": "Keep-Alive"
    }

    payload = {
        "cmd": "9017",
        "robotId": robot_id
    }

    try:
        response = requests.post(url, headers=headers, data=json.dumps(payload))
        response.raise_for_status()
        response_data = response.json()
        pprint(response_data)
        return response_data
    except requests.exceptions.RequestException as e:
        print(f"请求失败: {e}")
        return None


# 请求次日信号数据
result = nextday_single()

if result and result.get("message", {}).get("state") == 0:
    data_list = result.get("data", [])

    signal_records = []

    for signal in data_list:
        signal_info = {
            "股票ID": signal.get("stockId"),
            "股票代码": signal.get("symbol"),
            "股票名称": signal.get("symbolName"),
            "信号类型": "买入" if signal.get("buy") == 1 else "卖出" if signal.get("buy") == 0 else "未知",
            "信号时间": convert_timestamp(signal.get("created")),
            "有效期": signal.get("validDate"),
            "备注": signal.get("remark")
        }
        signal_records.append(signal_info)

    # 转换为 DataFrame
    df_signals = pd.DataFrame(signal_records)

    # 保存到 Excel 文件
    output_path = r"D:\1document\Investment\Investment\THS\大决策app\玩股成金\次日信号数据.xlsx"
    df_signals.to_excel(output_path, sheet_name='次日信号', index=False)

    print(f"✅ 数据已成功保存到：{output_path}")

else:
    print("未收到有效响应或状态码错误")