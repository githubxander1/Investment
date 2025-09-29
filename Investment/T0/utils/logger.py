# T0交易系统日志模块
import logging
import os
from datetime import datetime

# 确保日志目录存在
log_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'logs')
os.makedirs(log_dir, exist_ok=True)

def setup_logger(name, log_file=None, level=logging.INFO):
    """设置日志记录器"""
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    # 避免重复添加处理器
    if logger.handlers:
        logger.handlers.clear()
    
    # 文件处理器
    if log_file is None:
        log_file = os.path.join(log_dir, f'{name}.log')
    
    file_handler = logging.FileHandler(log_file, encoding='utf-8')
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    
    # 控制台处理器
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    return logger

def log_signal(stock_code, indicator_name, signal_type, details=""):
    """记录信号日志"""
    log_file = os.path.join(log_dir, 'signal_records.txt')
    with open(log_file, 'a', encoding='utf-8') as f:
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        f.write(f"[{timestamp}] {stock_code} - {indicator_name} - {signal_type} - {details}\n")