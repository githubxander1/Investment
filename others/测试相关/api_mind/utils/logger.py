# utils/logger.py
import logging
import os

def setup_logger():
    log_dir = "reports"
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    log_file = os.path.join(log_dir, "test.log")
    logger = logging.getLogger("api_test")
    logger.setLevel(logging.DEBUG)
    handler = logging.FileHandler(log_file)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger

logger = setup_logger()
