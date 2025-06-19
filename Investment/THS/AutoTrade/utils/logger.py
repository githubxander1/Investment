# utils/logger.py

import os
import logging
import colorlog
from Investment.THS.AutoTrade.config.settings import LOGS_DIR


def ensure_log_dir():
    """确保日志目录存在"""
    if not os.path.exists(LOGS_DIR):
        os.makedirs(LOGS_DIR)


def setup_logger(log_file: str = "app.log", logger_name: str = "THSLogger",
                level: int = logging.DEBUG) -> logging.Logger:
    """
    创建或返回已有的 logger
    :param log_file: 日志文件名
    :param logger_name: logger 名称
    :param level: 默认日志级别
    :return: logging.Logger
    """
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

    # 文件 handler
    file_handler = logging.FileHandler(log_path, encoding='utf-8')
    file_handler.setFormatter(formatter)

    # 控制台 handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    # 初始化 logger
    logger = logging.getLogger(logger_name)
    logger.setLevel(level)

    # 清除旧的 handlers
    if logger.hasHandlers():
        logger.handlers.clear()

    # 添加新 handlers
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger
