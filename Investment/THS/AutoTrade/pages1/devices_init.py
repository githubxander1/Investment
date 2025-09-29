import uiautomator2 as u2
from utils.logger import setup_logger

logger = setup_logger(__name__)

async def connect_to_device():
    """连接设备"""
    try:
        d = u2.connect()
        logger.info(f"连接设备: {d.serial}")
        return d
    except Exception as e:
        logger.error(f"连接设备失败: {e}", exc_info=True)
        return None

async def start_app(d, package_name="com.hexin.plat.android"):
    """启动同花顺App"""
    try:
        d.app_start(package_name, wait=True)
        logger.info(f"启动App成功: {package_name}")
        return True
    except Exception as e:
        logger.error(f"启动app失败 {package_name}: {e}", exc_info=True)
        return False

async def initialize_device():
    """初始化设备"""
    d = await connect_to_device()
    if not d:
        logger.error("设备连接失败")
        return None

    if not await start_app(d):
        logger.error("App启动失败")
        return None

    return d

def is_device_connected(d):
    """简单心跳检测设备是否还在线"""
    try:
        return d.info['screenOn']
    except:
        return False
# 重启
async def restart_device(d):
    """重启设备"""
    if not is_device_connected(d):
        logger.info("设备已断开连接，正在重新连接...")
        d = await initialize_device()
        if not d:
            logger.error("设备重连失败")
            return
        logger.info("设备已重新连接")
        if not await start_app(d):
            logger.error("App启动失败")
            return
        logger.info("App已启动")
