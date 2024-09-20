from playwright.sync_api import Page

class BasePage:
    def __init__(self, page: Page):
        self.page = page

    def wait_for_element(self, selector, timeout=5000):
        """等待元素出现"""
        self.page.wait_for_selector(selector, timeout=timeout)

    def click_element(self, selector):
        """点击元素"""
        self.page.locator(selector).click()

    def fill_element(self, selector, value):
        """填充元素内容"""
        self.page.locator(selector).fill(value)

    def is_element_visible(self, selector):
        """检查元素是否可见"""
        return self.page.is_visible(selector)
