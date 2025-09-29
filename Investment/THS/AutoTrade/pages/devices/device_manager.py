import uiautomator2 as u2
from utils.logger import setup_logger

logger = setup_logger(__name__)

class DeviceManager:
    """设备管理类，负责设备连接和应用启动等操作"""
    
    def __init__(self):
        self.device = None

    def connect_to_device(self):
        """
        连接设备
        
        Returns:
            uiautomator2.Device: 设备连接对象，失败时返回None
        """
        try:
            self.device = u2.connect()
            logger.info(f"连接设备: {self.device.serial}")
            return self.device
        except Exception as e:
            logger.error(f"连接设备失败: {e}", exc_info=True)
            return None

    def start_app(self, device, package_name="com.hexin.plat.android"):
        """
        启动同花顺App
        
        Args:
            device: 设备连接对象
            package_name: 应用包名
            
        Returns:
            bool: 启动是否成功
        """
        try:
            device.app_start(package_name, wait=True)
            logger.info(f"启动App成功: {package_name}")
            return True
        except Exception as e:
            logger.error(f"启动app失败 {package_name}: {e}", exc_info=True)
            return False

    def initialize_device(self):
        """
        初始化设备
        
        Returns:
            uiautomator2.Device: 设备连接对象，失败时返回None
        """
        self.device = self.connect_to_device()
        if not self.device:
            logger.error("设备连接失败")
            return None

        if not self.start_app(self.device):
            logger.error("App启动失败")
            return None

        return self.device

    def is_device_connected(self, device):
        """
        检查设备是否还在线
        
        Args:
            device: 设备连接对象
            
        Returns:
            bool: 设备是否在线
        """
        try:
            return device.info['screenOn']
        except:
            return False
            
    def restart_device(self, device):
        """
        重启设备连接
        
        Args:
            device: 设备连接对象
        """
        if not self.is_device_connected(device):
            logger.info("设备已断开连接，正在重新连接...")
            self.device = self.initialize_device()
            if not self.device:
                logger.error("设备重连失败")
                return
            logger.info("设备已重新连接")
            if not self.start_app(self.device):
                logger.error("App启动失败")
                return
            logger.info("App已启动")