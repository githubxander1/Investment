# error_handler.py
import logging

def setup_logger(log_file):
    """设置日志记录器"""
    logging.basicConfig(
        filename=log_file,
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    return logging.getLogger()

def handle_request_error(e, portfolio_id):
    """处理请求错误"""
    logger = logging.getLogger()
    logger.error(f"请求出错 (ID: {portfolio_id}): {str(e)}")
    print(f"请求出错 (ID: {portfolio_id}): {e}")
    return []

def save_empty_indicator(file_path):
    """创建空数据指示文件"""
    with open(file_path, 'w') as f:
        f.write('')
