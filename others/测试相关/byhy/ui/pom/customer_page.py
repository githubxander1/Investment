import re

from playwright.sync_api import Page


class CustomerPage:
    def __init__(self, page: Page):
        self.page = page
        self.add_customer_button = page.get_by_role("button", name="+ 添加客户")
        self.customer_name_input = page.locator("div").filter(has_text=re.compile(r"^客户名$")).get_by_role("textbox")
        self.phone_input = page.locator("div").filter(has_text=re.compile(r"^联系电话$")).get_by_role("textbox")
        self.address_input = page.locator("textarea")
        self.create_button = page.get_by_role("button", name="创建")
        self.delete_button = page.get_by_text("删除").nth(1)

    def add_customer(self, name, phone, address):
        self.add_customer_button.click()
        self.customer_name_input.fill(name)
        self.phone_input.fill(phone)
        self.address_input.fill(address)
        self.create_button.click()
        self.page.once("dialog", lambda dialog: dialog.dismiss())

    def delete_customer(self):
        self.delete_button.click()
