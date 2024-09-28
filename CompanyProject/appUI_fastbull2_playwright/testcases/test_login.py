import pytest
from playwright.sync_api import sync_playwright

from CompanyProject.appUI_fastbull2_playwright.pages.login_pagessss import LoginPage, PhoneLoginSection, \
    EmailLoginSection


# from pages.login_pages import LoginPage, PhoneLoginSection, EmailLoginSection

@pytest.fixture(scope='module')
def setup(playwright):
    browser = playwright.chromium.launch()
    context = browser.new_context()
    page = context.new_page()
    login_page = LoginPage(page)
    yield login_page, page
    page.close()
    context.close()
    browser.close()

def test_phone_login(setup):
    login_page, page = setup
    phone_login_section = PhoneLoginSection(page)

    login_page.click_avatar()
    login_page.click_login_button()
    login_page.click_phone_login_button()

    phone_login_section.enter_phone_number('13111111111')
    phone_login_section.enter_password('a1234567')
    phone_login_section.sign_in()

    # 断言登录成功
    assert page.is_visible('android=resourceId("com.bv.fastbull:id/tv_welcome_back")')

def test_email_login(setup):
    login_page, page = setup
    email_login_section = EmailLoginSection(page)

    login_page.click_avatar()
    login_page.click_login_button()
    login_page.click_email_login_button()

    email_login_section.enter_email('7@qq.com')
    email_login_section.enter_password('a1234567')
    email_login_section.login()

    # 断言登录成功
    assert page.is_visible('android=resourceId("com.bv.fastbull:id/tv_welcome_back")')

if __name__ == '__main__':
    with sync_playwright() as playwright:
        test_phone_login(playwright)
        test_email_login(playwright)
        playwright.stop()