import json

import requests


def send_dingtalk_notification(report_url):
    webhook = "YOUR_DINGTALK_WEBHOOK_URL"
    headers = {
        "Content-Type": "application/json"
    }
    data = {
        "msgtype": "text",
        "text": {
            "content": f"UI 自动化测试报告已生成，请查看：{report_url}"
        }
    }
    response = requests.post(webhook, headers=headers, data=json.dumps(data))
    if response.status_code != 200:
        print(f"DingTalk notification failed: {response.text}")