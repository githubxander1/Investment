# utils/logger.py
import logging
import os
from ..config.settings import Config

os.makedirs(os.path.dirname(Config.LOG_PATH), exist_ok=True)

def setup_logger():
    logger = logging.getLogger("PerformanceTest")
    logger.setLevel(logging.INFO)

    file_handler = logging.FileHandler(Config.LOG_PATH, encoding='utf-8')
    stream_handler = logging.StreamHandler()

    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    stream_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)
    return logger

logger = setup_logger()
