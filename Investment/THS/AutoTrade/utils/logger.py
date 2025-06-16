# logger.py
import logging
import os

import colorlog

from Investment.THS.AutoTrade.config.settings import LOGS_DIR


def setup_logger(log_file, logger_name='THSLogger'):
    log_colors = {
        'DEBUG': 'cyan',
        'INFO': 'green',
        'WARNING': 'yellow',
        'ERROR': 'red',
        'CRITICAL': 'bold_red',
    }

    # 如果 logger 已经存在，直接返回现有的 logger
    if logger_name in logging.Logger.manager.loggerDict:
        return logging.getLogger(logger_name)

    formatter = colorlog.ColoredFormatter(
        "%(log_color)s%(asctime)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        log_colors=log_colors
    )

    file_handler = logging.FileHandler(
        str(os.path.join(LOGS_DIR, log_file)),  # 添加str()显式类型转换
        encoding='utf-8')
    file_handler.setFormatter(formatter)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    logger = logging.getLogger(logger_name)

    # 清除可能存在的重复 handler
    if logger.hasHandlers():
        logger.handlers.clear()

    logger.setLevel(logging.DEBUG)
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger
