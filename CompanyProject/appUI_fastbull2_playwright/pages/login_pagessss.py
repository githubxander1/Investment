# from base_page import BasePage
from playwright.sync_api import sync_playwright

from CompanyProject.appUI_fastbull2_playwright.pages.base_page import BasePage
class LoginPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.avatar = 'd(resourceId="com.bv.fastbull:id/iv_avatar")'
        self.login_button = 'android=resourceId("com.bv.fastbull:id/tv_mine_top_welcome")'
        self.phone_login_button = '//android.widget.RelativeLayout[@resource-id="com.bv.fastbull:id/ll_btn"]/android.widget.RelativeLayout[1]'
        self.email_login_button = 'android=resourceId("com.bv.fastbull:id/tv_email_login")'

    def click_avatar(self):
        self.click_element(self.avatar)

    def click_login_button(self):
        self.click_element(self.login_button)

    def click_phone_login_button(self):
        self.click_element(self.phone_login_button)

    def click_email_login_button(self):
        self.click_element(self.email_login_button)


class PhoneLoginSection(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.phone_input = 'android=resourceId("com.bv.fastbull:id/et_mine_edit_phone_number")'
        self.password_input = 'android=resourceId("com.bv.fastbull:id/et_password")'
        self.sign_in_button = 'android=resourceId("com.bv.fastbull:id/tv_sign")'

    def enter_phone_number(self, phone):
        self.fill_element(self.phone_input, phone)

    def enter_password(self, password):
        self.fill_element(self.password_input, password)

    def sign_in(self):
        self.click_element(self.sign_in_button)


class EmailLoginSection(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.email_input = 'android=resourceId("com.bv.fastbull:id/et_email")'
        self.password_input = 'android=resourceId("com.bv.fastbull:id/et_password")'
        self.login_button = 'android=resourceId("com.bv.fastbull:id/tv_login")'

    def enter_email(self, email):
        self.fill_element(self.email_input, email)

    def enter_password(self, password):
        self.fill_element(self.password_input, password)

    def login(self):
        self.click_element(self.login_button)

if __name__ == '__main__':
    # from playwright import sync_playwright
    playwright = sync_playwright().start()
    browser = playwright.android.launch(headless=False)
    context = browser.new_context(
        locale='zh-CN',
        geolocation={'longitude': 116.39742,
                     }
    )
    page = context.new_page()
    login_page = LoginPage(page)
    login_page.click_avatar()
    login_page.click_phone_login_button()
    phone_login_section = PhoneLoginSection(page)
    phone_login_section.enter_phone_number('')
    phone_login_section.enter_password('123456')
    phone_login_section.sign_in()
    page.wait_for_timeout(5000)
    page.screenshot(path='./screenshot.png')
