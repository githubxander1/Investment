import requests
import json

# 设置基础 URL
base_url = "http://127.0.0.1:5000"

# 测试 POST 请求
def test_create_schedule():
    url = f"{base_url}/api/schedules"
    print('访问地址：',url)
    data = {
        "title": "测试 标题Schedule",
        "description": "日程内容"
    }
    response = requests.post(url, json=data)
    print('返回结果：',response.json())
    assert response.status_code == 201
    print(f"POST request to {url}: {response.status_code} - {json.loads(response.text)}")

# 测试 GET 请求
def test_get_schedules():
    url = f"{base_url}/api/schedules"
    print('访问地址：',url)
    response = requests.get(url)
    print('返回结果：',response.json())
    assert response.status_code == 200
    print(f"GET request to {url}: {response.status_code} - {json.loads(response.text)}")

# 测试 DELETE 请求
def test_delete_schedule():
    url = f"{base_url}/api/schedules/0"
    print('访问地址：', url)
    response = requests.delete(url)
    print('返回结果：',response.json())
    assert response.status_code == 204
    print(f"DELETE request to {url}: {response.status_code}")

# 主函数
if __name__ == "__main__":
    test_create_schedule()
    test_get_schedules()
    test_delete_schedule()
