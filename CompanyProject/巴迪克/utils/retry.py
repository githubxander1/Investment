from tenacity import retry, stop_after_attempt, wait_exponential, before_sleep_log
import logging

# 设置日志以便输出重试信息
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 自定义回调函数显示中文提示
def log_retry(retry_state):
    logger.info("重试中，请稍候...")

# 使用 before_sleep 参数替代 text 提示
default_retry = retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=5),
    before_sleep=log_retry
)
