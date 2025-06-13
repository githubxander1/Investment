# import requests
#
# url = "https://linshiyou.com/mail.php?unseen=1"
#
# headers = {
#     "accept": "*/*",
#     "accept-language": "zh-CN,zh;q=0.9",
#     "sec-ch-ua": "\"Chromium\";v=\"121\", \"Not A(Brand\";v=\"99\"",
#     "sec-ch-ua-mobile": "?0",
#     "sec-ch-ua-platform": "\"Windows\"",
#     "sec-fetch-dest": "empty",
#     "sec-fetch-mode": "cors",
#     "sec-fetch-site": "same-origin",
#     "x-requested-with": "XMLHttpRequest",
#     "referer": "https://linshiyou.com/"
# }
#
# cookies = {
#     "session_id": "your_session_id",  # 替换为实际的 session_id
#     "other_cookie": "value"           # 其他需要携带的 cookie
# }
#
# response = requests.get(url, headers=headers, cookies=cookies)
#
# if response.status_code == 200:
#     print("请求成功")
#     print(response.text)
# else:
#     print(f"请求失败，状态码: {response.status_code}")
#     print(response.text)
