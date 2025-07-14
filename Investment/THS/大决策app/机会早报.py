import requests
import json


def get_opportunity_morning_report():
    """获取机会x早报列表数据（POST请求）"""
    # 请求URL
    url = "https://api.djc8888.com/api/v2/note/dkNoteList"

    # URL参数（拼接在请求地址后）
    params = {
        "deviceToken": "f10afa3eef3c3a2d938b547f7ed0edc9",
        "sign": "EDB14AAA130207BC67AA9E9089A38865",
        "timestamp": "1752410791327",
        "version": "3.7.12",
        "versionCode": "3071200",
        "deviceId": "f10afa3eef3c3a2d938b547f7ed0edc9",
        "platform": "android"
    }

    # 请求头信息
    headers = {
        "mobileInfo": "Android 29 xiaomi Redmi Note 7 Pro",
        "vendingPackageName": "com.mi.djc",
        "Accept": "application/json; charset=UTF-8",
        "Connection": "Keep-Alive",
        "User-Agent": "android/10 com.djc.qcyzt/3.7.12",
        "Charset": "UTF-8",
        "Accept-Encoding": "gzip",
        "packageName": "com.djc.qcyzt",
        "deviceId": "f10afa3eef3c3a2d938b547f7ed0edc9",
        "version": "3.7.12",
        "versionCode": "3071200",
        "Content-Type": "application/json; charset=utf-8",
        "Host": "api.djc8888.com",
        "Cookie": '$Version="1"; acw_tc="0aef815717524097434225549e0085bc86f9531ed08212d4f017f16a875237";$Path="/";$Domain="api.djc8888.com"'
    }

    # 请求体JSON数据
    payload = {
        "list_type": "4",
        "pageNo": "1",
        "pageSize": "20",
        "noteAuthorid": "29093",
        "note_type": "1,3,5,6"
    }

    try:
        # 发送POST请求
        response = requests.post(
            url,
            params=params,
            headers=headers,
            json=payload,  # 自动处理JSON序列化及Content-Type
            verify=True
        )
        response.raise_for_status()  # 检查HTTP响应状态码
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"请求机会x早报失败: {e}")
        return None


# 测试函数
if __name__ == "__main__":
    morning_report_data = get_opportunity_morning_report()
    if morning_report_data:
        print("机会x早报数据:")
        print(json.dumps(morning_report_data, indent=2, ensure_ascii=False))  # 格式化显示中文