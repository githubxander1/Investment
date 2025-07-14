import requests
import json


def get_note_detail():
    """获取笔记详情数据（GET请求）"""
    # 请求URL
    url = "https://api.djc8888.com/api/v2/note/detail"

    # URL参数
    params = {
        "deviceToken": "f10afa3eef3c3a2d938b547f7ed0edc9",
        "noteid": "108713",  # 笔记ID，对应详情查询
        "sign": "C979223C1941D4AB72714600A2043F67",
        "timestamp": "1752411016601",
        "version": "3.7.12",
        "versionCode": "3071200",
        "deviceId": "f10afa3eef3c3a2d938b547f7ed0edc9",
        "platform": "android"
    }

    # 请求头
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
        response.raise_for_status()  # 检查响应状态码
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"请求笔记详情失败: {e}")
        return None


# 测试函数
if __name__ == "__main__":
    note_detail = get_note_detail()
    if note_detail:
        print("笔记详情数据:")
        print(json.dumps(note_detail, indent=2, ensure_ascii=False))  # 格式化显示详情内容