import requests
import json

# 设置基础 URL
base_url = "http://127.0.0.1:5000"


# 测试 POST 请求
def test_create_schedule():
    url = f"{base_url}/api/schedules"
    data = {
        "title": "Test Schedule",
        "description": "This is a test schedule."
    }
    response = requests.post(url, json=data)
    assert response.status_code == 201
    print(f"POST request to {url}: {response.status_code} - {response.json()}")

    # 返回创建的日程 ID 用于后续测试
    return response.json()['id']


# 测试 GET 请求
def test_get_schedules():
    url = f"{base_url}/api/schedules"
    response = requests.get(url)
    assert response.status_code == 200
    print(f"GET request to {url}: {response.status_code} - {response.json()}")


# 测试 DELETE 请求
def test_delete_schedule(schedule_id):
    url = f"{base_url}/api/schedules/{schedule_id}"
    response = requests.delete(url)
    assert response.status_code == 204
    print(f"DELETE request to {url}: {response.status_code}")


# 主函数
if __name__ == "__main__":
    # 测试创建日程
    schedule_id = test_create_schedule()

    # 测试查询所有日程
    test_get_schedules()

    # 测试删除日程
    test_delete_schedule(schedule_id)