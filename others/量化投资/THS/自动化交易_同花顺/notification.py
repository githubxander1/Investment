# notification.py
from plyer import notification

def send_notification(message):
    notification.notify(
        title="交易通知",
        message=message,
        app_name="THS 自动交易",
        timeout=10
    )
