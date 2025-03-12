# notification.py
import logging
import os
import smtplib
from datetime import datetime
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import requests
from dotenv import load_dotenv
from plyer import notification

from others.Investment.THS.AutoTrade.utils import logger

# 加载 .venv 文件
load_dotenv()

# 设置日志记录
logging.basicConfig(level=logging.INFO)

def send_notification(message):
    notification.notify(
        title="交易通知",
        message=message,
        app_name="THS 自动交易",
        timeout=10
    )

    # 新增钉钉通知
    send_dingtalk_notification(message)
    logging.info(f'交易通知: {message}')

def send_http_request(url, data):
    response = requests.post(url, json=data)
    if response.status_code != 200:
        raise Exception(f"HTTP请求发送失败，状态码: {response.status_code}")

# def send_wechat_notification(message):
#     data = {
#         "msgtype": "text",
#         "text": {
#             "content": message
#         }
#     }
#     send_http_request(WECHAT_WEBHOOK_URL, data)

def get_smtp_connection():
    smtp_server = os.getenv('SMTP_SERVER')
    smtp_port = int(os.getenv('SMTP_PORT'))
    from_email = os.getenv('EMAIL_FROM')
    password = os.getenv('EMAIL_PASSWORD')

    try:
        server = smtplib.SMTP_SSL(smtp_server, smtp_port)
        server.login(from_email, password)
        return server
    except Exception as e:
        logging.error(f"Failed to connect to SMTP server: {e}")
        raise

def send_email(subject, body, to_email, attachment_path=None):
    from_email = os.getenv('EMAIL_FROM')

    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))

    if attachment_path and os.path.exists(attachment_path):
        with open(attachment_path, "rb") as attachment:
            part = MIMEApplication(attachment.read(), Name=os.path.basename(attachment_path))
            part['Content-Disposition'] = f'attachment; filename="{os.path.basename(attachment_path)}"'
            msg.attach(part)
    elif attachment_path:
        logging.warning(f"Attachment path {attachment_path} does not exist, skipping attachment.")

    try:
        server = get_smtp_connection()
        text = msg.as_string()
        server.sendmail(from_email, to_email, text)
        server.quit()
        logging.info("Email sent successfully.")
    except Exception as e:
        logging.error(f"Failed to send email: {e}")

# 发送钉钉通知
def send_dingtalk_notification(message):
    # DINGTALK_WEBHOOK = os.getenv('DINGTALK_WEBHOOK')
    # KEYWORD = os.getenv('DINGTALK_KEYWORD', '交易通知')
    DINGTALK_WEBHOOK = 'https://oapi.dingtalk.com/robot/send?access_token=ad751f38f241c5088b291765818cfe294c2887198b93655e0e20b1605a8cd6a2'
    KEYWORD =  '交易通知'

    data = {
        "msgtype": "markdown",
        "markdown": {
            "title": "调仓通知",
            "text": f"**{KEYWORD}**\n {message}\n"
            # "text": f"**{KEYWORD}**\n {message}\n 时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}"
        }
    }
    try:
        response = requests.post(DINGTALK_WEBHOOK, json=data)
        response.raise_for_status()
        # logger.info('钉钉通知发送成功')
    except Exception as e:
        logging.error(f'钉钉通知发送失败: {str(e)}')


# def send_dingtalk_notification():
#     # project_name = test_script.split('.')[0]
#     project_name = '交易通知'
#     dingtalk_webhook = 'https://oapi.dingtalk.com/robot/send?access_token=ad751f38f241c5088b291765818cfe294c2887198b93655e0e20b1605a8cd6a2'
#     keyword = 'fastbull'
#     message = {
#         "msgtype": "text",
#         "text": {
#             "content": f"'{project_name}'调仓通知\n"
#                        f"时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
#                        f"执行人：我是你华哥\n"
#                        # f"{keyword}接口报告链接: {report_url}"
#         }
#     }
#     response = requests.post(dingtalk_webhook, json=message)
#     if response.status_code == 200:
#         print("钉钉消息发送成功")
#     else:
#         print(f"钉钉消息发送失败：{response.text}")
# if __name__ == '__main__':
#     import asyncio
#
#     asyncio.run(strategy_main())
