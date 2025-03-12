import requests

url = "https://api.siliconflow.cn/v1/video/submit"

payload = {
    "model": "Lightricks/LTX-Video",
    "prompt": "生成一个戴着可爱帽子的小狗在逗猫棒的挑逗下玩耍的视频",
    "image": "<string>",
    "seed": 123
}
headers = {
    "Authorization": "Bearer sk-eixzutqzkikrbdsnlbxzukadwtgtxtburewlkttafvxzytev",
    "Content-Type": "application/json"
}

response = requests.request("POST", url, json=payload, headers=headers)

print(response.text)