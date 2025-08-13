import logging.handlers  # 引入 RotatingFileHandler 支持
import inspect
import os
import logging
import colorlog
from Investment.THS.AutoTrade.config.settings import LOGS_DIR


def ensure_log_dir():
    """确保日志目录存在"""
    if not os.path.exists(LOGS_DIR):
        os.makedirs(LOGS_DIR)


def setup_logger(log_file: str = "app.log", logger_name: str = None,
                level: int = logging.DEBUG) -> logging.Logger:
    """
    创建或返回已有的 logger
    :param log_file: 日志文件名
    :param logger_name: logger 名称，默认为调用模块名
    :param level: 默认日志级别
    :return: logging.Logger
    """
    # 如果 logger_name 未指定，则使用调用模块的名称
    if logger_name is None:
        logger_name = inspect.currentframe().f_back.f_globals['__name__']
        logger_name = logger_name.split('.')[-1]
        # print(logger_name)

    # 如果 logger 已存在，直接返回
    if logger_name in logging.Logger.manager.loggerDict:
        return logging.getLogger(logger_name)

    # 确保日志目录存在
    ensure_log_dir()

    # 构建完整日志路径
    log_path = os.path.join(LOGS_DIR, log_file)

    # 定义颜色格式
    log_colors = {
        'DEBUG': 'cyan',
        'INFO': 'green',
        'WARNING': 'yellow',
        'ERROR': 'red',
        'CRITICAL': 'bold_red',
    }

    formatter = colorlog.ColoredFormatter(
        "%(log_color)s%(asctime)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        log_colors=log_colors
    )

    # 文件 handler（限制单个日志文件大小为10MB，最多保留5个备份）
    file_handler = logging.handlers.RotatingFileHandler(
        log_path, maxBytes=10 * 1024 * 1024, backupCount=5, encoding='utf-8'
    )
    file_handler.setFormatter(formatter)

    # 控制台 handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    # 初始化 logger
    logger = logging.getLogger(logger_name)
    logger.setLevel(level)

    # 设置propagate为False，避免日志传递到root logger
    logger.propagate = False

    # 清除旧的 handlers
    if logger.hasHandlers():
        logger.handlers.clear()

    # 添加新 handlers
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger