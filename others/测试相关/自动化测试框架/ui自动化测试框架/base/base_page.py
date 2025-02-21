import logging

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

logger = logging.getLogger(__name__)

class BasePage:
    def __init__(self, driver):
        self.driver = driver

    def find_element(self, by=By.ID, value=None, timeout=10):
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located((by, value))
            )
            return element
        except Exception as e:
            logger.error(f"Element not found: {e}")
            raise

    def click(self, by=By.ID, value=None, timeout=10):
        element = self.find_element(by, value, timeout)
        element.click()

    def send_keys(self, by=By.ID, value=None, text=None, timeout=10):
        element = self.find_element(by, value, timeout)
        element.send_keys(text)