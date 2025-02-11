import re

from playwright.sync_api import Page


class MedicinePage:
    def __init__(self, page: Page):
        self.page = page
        self.medicine_link = page.get_by_role("link", name=" 药品")
        self.add_medicine_button = page.get_by_role("button", name="+ 添加药品")
        self.medicine_name_input = page.locator("div").filter(has_text=re.compile(r"^药品名称$")).get_by_role("textbox")
        self.medicine_id_input = page.locator("div").filter(has_text=re.compile(r"^编号$")).get_by_role("textbox")
        self.description_input = page.locator("textarea")
        self.create_button = page.get_by_role("button", name="创建")

    def navigate(self):
        self.medicine_link.click()

    def add_medicine(self, name, medicine_id, description):
        self.add_medicine_button.click()
        self.medicine_name_input.fill(name)
        self.medicine_id_input.fill(medicine_id)
        self.description_input.fill(description)
        self.create_button.click()
