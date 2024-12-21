from plyer import notification

def send_notification(title, message):
    notification.notify(
        title=title,
        message=message,
        app_name="量化投资监控",
        timeout=10
    )
