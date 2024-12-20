import uiautomator2 as u2
import logging

# 设置日志记录
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

try:
    # 连接到设备
    d = u2.connect()
    logging.info(f"Connected to device: {d.serial}")
    
    # 打印设备信息
    device_info = d.info
    logging.info(f"Device info: {device_info}")

except Exception as e:
    logging.error(f"Failed to connect to the device: {e}")
