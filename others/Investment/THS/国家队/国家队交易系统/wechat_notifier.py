import requests
import json

# 替换为您的企业微信机器人Webhook地址
WEBHOOK_URL = "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=30130d8c-0973-4aaf-9888-b0e23b7f63ac"

def send_wechat_message(candidates):
    """使用企业微信机器人发送消息"""
    try:
        # 格式化消息内容
        message = "今日精选股池:\n\n" + candidates.to_string(index=False)

        # 构建请求数据
        payload = {
            "msgtype": "text",
            "text": {
                "content": message
            }
        }

        # 发送请求
        headers = {'Content-Type': 'application/json'}
        response = requests.post(
            WEBHOOK_URL,
            data=json.dumps(payload),
            headers=headers
        )

        # 检查响应
        if response.status_code == 200 and response.json().get('errcode') == 0:
            print("企业微信消息发送成功")
        else:
            print(f"发送失败: {response.text}")
    except Exception as e:
        print(f"企业微信消息发送异常: {e}")
