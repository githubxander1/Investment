import time
import uiautomator2 as u2

from others.量化投资.THS.自动化交易_同花顺.ths_logger import logger
from others.量化投资.THS.自动化交易_同花顺.ths_page import THSPage

def connect_to_device():
    try:
        d = u2.connect()
        logger.info(f"连接设备: {d.serial}")
        return d
    except Exception as e:
        logger.error(f"连接设备失败: {e}", exc_info=True)
        return None

def start_app(d, package_name):
    try:
        d.app_start(package_name)
        logger.info(f"启动app: {package_name}")
    except Exception as e:
        logger.error(f"启动app失败 {package_name}: {e}", exc_info=True)

def main():
    d = connect_to_device()
    if d is None:
        return

    start_app(d, 'com.hexin.plat.android')
    time.sleep(4)

    ths_page = THSPage(d)
    buy_stock_name = '中国电信'
    ths_page.buy_stock(buy_stock_name, 200)
    logger.info(f'买入{buy_stock_name}流程结束',exc_info=True)

    sale_stock_name = '中国联通'
    ths_page.sell_stock(sale_stock_name, '200')
    logger.info(f'卖出{sale_stock_name}流程结束',exc_info=True)

    # 打印设备信息
    device_info = d.info
    logger.info(f"设备信息: {device_info}", exc_info=True)

if __name__ == "__main__":
    main()
