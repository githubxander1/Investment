# utils/email_sender.py
import logging
import os
import smtplib
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from dotenv import load_dotenv

# 加载 .venv 文件
load_dotenv()

logging.basicConfig(level=logging.INFO)

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

# send_email('测试邮件', '这是一封测试邮件', '2695418206@qq.com')
