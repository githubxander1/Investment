import re

from playwright.sync_api import Page


class OrderPage:
    def __init__(self, page: Page):
        self.page = page
        self.order_link = page.get_by_role("link", name=" 订单")
        self.add_order_button = page.get_by_role("button", name="+ 添加订单")
        self.order_name_input = page.locator("div").filter(has_text=re.compile(r"^订单名称$")).get_by_role("textbox")
        self.customer_select = page.get_by_role("listbox").first
        self.keyword_input = page.get_by_placeholder("请输入关键字查找").nth(1)
        self.create_button = page.get_by_role("button", name="创建")

    def navigate(self):
        self.order_link.click()

    def add_order(self, name, customer_id, keyword):
        self.add_order_button.click()
        self.order_name_input.fill(name)
        self.customer_select.select_option(customer_id)
        self.keyword_input.fill(keyword)
        self.create_button.click()
