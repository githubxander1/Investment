import requests
import json

def get_strategy_detail():
    # 请求URL
    url = "https://emapp.emoney.cn/SmartInvestment/Strategy/Detail"
    
    # 请求头信息
    headers = {
        "X-Protocol-Id": "SmartInvestment%2FStrategy%2FDetail",
        "X-Request-Id": "null",
        "EM-Sign": "23082404151001:a0443b49b1c0c9a5d3182cd67b074ae5:bwqKUviNHF:1754225006705",
        "Authorization": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCIsImN0eSI6IkpXVCJ9.eyJ1dWQiOjEwMTUwNDYxMDEsInVpZCI6MjkwMTg0NjIsImRpZCI6IjExY2ZlMmQzZmZlOTkzMDMzMTY2NmNiZmIwZWNkMmJjIiwidHlwIjo0LCJhY2MiOiIxMWNmZTJkM2ZmZTk5MzAzMzE2NjZjYmZiMGVjZDJiYyIsInN3dCI6MSwibGd0IjoxNzU0MjIyMjg1MjEyLCJuYmYiOjE3NTQyMjIyODUsImV4cCI6MTc1NTk1MDI4NSwiaWF0IjoxNzU0MjIyMjg1fQ.91dKxwW5Z9rh9PjHHUhfnOFnnCHzoU_ToZGq6HuTdhg",
        "X-Android-Agent": "EMAPP/5.12.0(Android;29)",
        "Emapp-ViewMode": "1",
        "Content-Type": "application/json",
        "Host": "emapp.emoney.cn",
        "Connection": "Keep-Alive",
        "Accept-Encoding": "gzip",
        "User-Agent": "okhttp/3.12.13"
    }
    
    # 请求体数据
    data = {
        "stockPoolSize": -1,
        "id": 70009
    }
    
    try:
        # 发送POST请求
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()  # 检查请求是否成功
        
        # 解析响应为JSON
        result = response.json()
        
        # 修改返回结果中的auth字段为true（若存在）
        if "auth" in result:
            result["auth"] = True
        else:
            # 若原结果中无auth字段，主动添加
            result["auth"] = True
        
        # 打印处理后的结果（可根据需求改为返回结果）
        print("处理后的详情结果：")
        print(json.dumps(result, ensure_ascii=False, indent=2))
        
        return result
        
    except requests.exceptions.RequestException as e:
        print(f"请求失败：{e}")
    except json.JSONDecodeError:
        print("响应内容不是有效的JSON格式")
    return None

if __name__ == "__main__":
    # 执行函数获取详情
    get_strategy_detail()
    https://appstatic.emoney.cn/ymstock/compare/?goodsAid=600017&goodsBid=1000528&goodsCid=1002001&emoneyScaleType=0&emoneyLandMode=0&token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCIsImN0eSI6IkpXVCJ9.eyJ1dWQiOjEwMTUwNDYxMDEsInVpZCI6MjkwMTg0NjIsImRpZCI6IjExY2ZlMmQzZmZlOTkzMDMzMTY2NmNiZmIwZWNkMmJjIiwidHlwIjo0LCJhY2MiOiIxMWNmZTJkM2ZmZTk5MzAzMzE2NjZjYmZiMGVjZDJiYyIsInN3dCI6MSwibGd0IjoxNzU0MjIyMjg1MjEyLCJuYmYiOjE3NTQyMjIyODUsImV4cCI6MTc1NTk1MDI4NSwiaWF0IjoxNzU0MjIyMjg1fQ.91dKxwW5Z9rh9PjHHUhfnOFnnCHzoU_ToZGq6HuTdhg