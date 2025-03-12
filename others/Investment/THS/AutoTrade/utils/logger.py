# utils/logger.py
import logging
import os

import colorlog

# from config.settings import LOGS_DIR
from others.Investment.THS.AutoTrade.config.settings import LOGS_DIR


def setup_logger(log_file, logger_name='THSLogger'):
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

    file_handler = logging.FileHandler(
        str(os.path.join(LOGS_DIR, log_file)),  # 添加str()显式类型转换
        encoding='utf-8')
    file_handler.setFormatter(formatter)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    logger = logging.getLogger(logger_name)
    if not logger.hasHandlers():
        logger.setLevel(logging.DEBUG)
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

    return logger
