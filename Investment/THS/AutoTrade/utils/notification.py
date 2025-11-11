import logging
import os
import smtplib
import time
from datetime import datetime
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import requests
from dotenv import load_dotenv
from plyer import notification

from Investment.THS.AutoTrade.utils.logger import setup_logger
# from Investment.THS.AutoTrade2.utils.logger import setup_logger

# 加载 .venv 文件
load_dotenv()

# 设置日志记录
# logging.basicConfig(level=logging.INFO)
logger = setup_logger('notification.log')

def send_notification(message):
    if len(message) > 256:
        message = message[:256 - 3] + '...'
    notification.notify(
        title="trade通知",
        message=message,
        app_name="THS",
        timeout=10
    )

    # 新增钉钉通知
    send_dingtalk_notification(message)
    logger.warning(f'交易通知: {message}')
    
    # 如果通知中包含"失败"关键字，则暂停30秒
    if "失败" or '未' or '不足' in message:
        logger.info("检测到交易失败通知，暂停30秒...")
        time.sleep(30)

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
    KEYWORD =  '通知'

    data = {
        "msgtype": "markdown",
        "markdown": {
            "title": "通知",
            "text": f"{KEYWORD}：\n {message}"
            # "text": f"**{KEYWORD}**\n {message}\n 时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}"
        }
    }
    try:
        response = requests.post(DINGTALK_WEBHOOK, json=data)#,verify='D:/Xander/Pycharm_gitee/reqable-ca.crt'
        response.raise_for_status()
        # logger.info('钉钉通知发送成功')
    except Exception as e:
        logging.error(f'钉钉通知发送失败: {str(e)}')


# if __name__ == '__main__':
#     import asyncio
#
#     asyncio.run(strategy_main())