import re

import pytesseract
from playwright.sync_api import Playwright, sync_playwright, expect


def get_email_code(playwright: Playwright, username, password) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("http://192.168.0.228/core/auth/login/?next=/luna/")
    page.get_by_role("textbox", name="用户名 *").fill(username)
    page.get_by_role("textbox", name="密码").fill(password)
    page.get_by_role("checkbox", name="天内自动登录").check()

    # 填写验证码
    # page.get_by_role("textbox", name="Captcha *").fill("0")
    # page.pause()


    page.get_by_role("button", name="登录").click()
    page.pause()
    page.get_by_title("Default (43)").click()
    page.wait_for_timeout(1000)
    page.get_by_title("test (21)").click()
    page.wait_for_timeout(1000)
    page.get_by_title("192.168.0.224").click()
    page.wait_for_timeout(1000)
    page.pause()
    '''复制粘贴：
    cd /data/logs/tomcat/merchart
    grep \"发邮件结束 getVerificationCode 登录邮箱\" *'''
    # page.screenshot(path="./email_code.png")
    # ---------------------
    # context.close()
    # browser.close()


# with sync_playwright() as playwright:
#     get_email_code(playwright)
