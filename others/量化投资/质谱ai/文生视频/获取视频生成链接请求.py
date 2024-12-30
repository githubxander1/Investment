import requests

url = "https://api.siliconflow.cn/v1/video/status"

# payload = {"requestId": "03bf14c1-cf7f-4029-8e46-c0fe615d427e"}
payload = {"requestId": "b951456b-49ae-47f0-bc2e-87f72041f842"}
headers = {
    "Authorization": "Bearer sk-eixzutqzkikrbdsnlbxzukadwtgtxtburewlkttafvxzytev",
    "Content-Type": "application/json"
}

response = requests.request("POST", url, json=payload, headers=headers)

print(response.json())