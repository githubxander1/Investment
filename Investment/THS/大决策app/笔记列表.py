import requests
import json


def get_dk_note_list():
    """获取笔记列表数据（POST请求）"""
    # 请求URL
    url = "https://api.djc8888.com/api/v2/note/dkNoteList"

    # URL参数（拼接在URL后）
    params = {
        "deviceToken": "f10afa3eef3c3a2d938b547f7ed0edc9",
        "sign": "7AEDEA4301F744578BC7670E1435A340",
        "timestamp": "1752409144225",
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
        "Cookie": '$Version="1"; acw_tc="0aef815717524091047248391e00660ff0d8b48847fdc9e4cc5af9c93fc559";$Path="/";$Domain="api.djc8888.com"'
    }

    # 请求体（JSON数据）
    payload = {
        "list_type": "4",
        "pageNo": "1",
        "sign": "教学",
        "pageSize": "20",
        "noteAuthorid": "22",
        "note_type": "1,3,5,6"
    }

    try:
        # 发送POST请求，JSON参数通过json参数传递（自动处理Content-Type）
        response = requests.post(
            url,
            params=params,
            headers=headers,
            json=payload,  # 自动序列化并设置Content-Type为application/json
            verify=True
        )
        response.raise_for_status()  # 检查HTTP状态码
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"请求笔记列表失败: {e}")
        return None


# 测试函数
if __name__ == "__main__":
    note_data = get_dk_note_list()
    if note_data:
        print("笔记列表数据:")
        print(json.dumps(note_data, indent=2, ensure_ascii=False))  # 格式化打印JSON