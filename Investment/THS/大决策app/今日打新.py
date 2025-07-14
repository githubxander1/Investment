import requests
import json


def get_today_new_stock_detail():
    """获取今日打新相关笔记详情（GET请求）"""
    # 请求URL
    url = "https://api.djc8888.com/api/v2/note/detail"

    # URL参数（包含指定noteid，对应今日打新内容）
    params = {
        "deviceToken": "f10afa3eef3c3a2d938b547f7ed0edc9",
        "noteid": "108554",  # 对应今日打新的笔记ID
        "sign": "EC8ADCDDF656669297E732B753CDDAFD",
        "timestamp": "1752411236790",
        "version": "3.7.12",
        "versionCode": "3071200",
        "deviceId": "f10afa3eef3c3a2d938b547f7ed0edc9",
        "platform": "android"
    }

    # 请求头（与原始请求保持一致）
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

    try:
        # 发送GET请求
        response = requests.get(
            url,
            params=params,
            headers=headers,
            verify=True
        )
        response.raise_for_status()  # 检查HTTP状态码
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"请求今日打新笔记详情失败: {e}")
        return None


# 测试函数
if __name__ == "__main__":
    today_new_stock_data = get_today_new_stock_detail()
    if today_new_stock_data:
        print("今日打新笔记详情:")
        print(json.dumps(today_new_stock_data, indent=2, ensure_ascii=False))  # 格式化显示中文内容