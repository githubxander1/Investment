# notification.py
from plyer import notification

from others.量化投资.THS.自动化交易_同花顺.整合.config.settings import send_notification
from others.量化投资.THS.自动化交易_同花顺.ths_logger import setup_logger

logger = setup_logger(send_notification)
def send_notification(message):
    notification.notify(
        title="交易通知",
        message=message,
        app_name="THS 自动交易",
        timeout=10
    )
    logger.info(f'交易通知: {message}')
