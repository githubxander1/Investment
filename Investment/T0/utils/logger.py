import logging
import os
from datetime import datetime

# 确保日志目录存在
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOGS_DIR = os.path.join(BASE_DIR, 'logs')
os.makedirs(LOGS_DIR, exist_ok=True)

def setup_logger(name, log_file=None, level=logging.INFO):
    """设置日志记录器"""
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    
    # 创建日志记录器
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    # 避免重复添加处理器
    if not logger.handlers:
        # 文件处理器
        if log_file is None:
            log_file = f'{name}.log'
        file_handler = logging.FileHandler(os.path.join(LOGS_DIR, log_file), encoding='utf-8')
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
        
        # 控制台处理器
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)
    
    return logger

def log_signal(stock_code, indicator, signal_type, details):
    """记录交易信号到文件"""
    try:
        signal_record_file = os.path.join(BASE_DIR, 'logs', 'signal_records.txt')
        with open(signal_record_file, 'a', encoding='utf-8') as f:
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            f.write(f"[{timestamp}] {stock_code} - {indicator} - {signal_type} - {details}\n")
    except Exception as e:
        print(f"记录信号失败: {e}")