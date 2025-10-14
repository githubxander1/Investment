import uiautomator2
from Investment.THS.AutoTrade.utils.logger import setup_logger

logger = setup_logger("page_base.log")

class BasePage:
    """
    页面基础类，提供通用的页面操作方法
    """
    
    def __init__(self, d=None):
        """
        初始化基础页面类
        
        Args:
            d: uiautomator2设备连接对象
        """
        self.d = d or uiautomator2.connect()
        self._current_page = None
        
    def click_element(self, element, timeout=10):
        """
        安全点击元素
        
        Args:
            element: 要点击的元素
            timeout: 等待超时时间
            
        Returns:
            bool: 点击是否成功
        """
        try:
            if element.wait(timeout=timeout):
                element.click()
                return True
            else:
                logger.warning("点击失败：元素不存在")
                return False
        except Exception as e:
            logger.error(f"点击元素时发生异常: {e}")
            return False
            
    def get_element_text(self, element, default=""):
        """
        安全获取元素文本
        
        Args:
            element: 元素对象
            default: 默认返回值
            
        Returns:
            str: 元素文本或默认值
        """
        try:
            if element.exists:
                return element.get_text()
            return default
        except Exception as e:
            logger.error(f"获取元素文本时发生异常: {e}")
            return default
            
    def input_text(self, element, text):
        """
        在元素中输入文本
        
        Args:
            element: 输入框元素
            text: 要输入的文本
            
        Returns:
            bool: 输入是否成功
        """
        try:
            element.set_text(text)
            return True
        except Exception as e:
            logger.error(f"输入文本时发生异常: {e}")
            return False
            
    def swipe(self, fx, fy, tx, ty, duration=0.5):
        """
        屏幕滑动
        
        Args:
            fx: 起始点x坐标(比例)
            fy: 起始点y坐标(比例)
            tx: 终点x坐标(比例)
            ty: 终点y坐标(比例)
            duration: 滑动持续时间
        """
        try:
            self.d.swipe(fx, fy, tx, ty, duration=duration)
            return True
        except Exception as e:
            logger.error(f"滑动时发生异常: {e}")
            return False