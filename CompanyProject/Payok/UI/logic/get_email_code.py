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

    from playwright.sync_api import sync_playwright
    # import pytesseract
    from PIL import Image
    import requests
    from io import BytesIO
    def solve_captcha(page):
        # 定位验证码图片元素

        captcha_img = page.locator('.captcha')
        # 获取验证码图片的src属性
        captcha_img_url = captcha_img.get_attribute('src')
        captcha_img_url = 'http://192.168.0.228'+captcha_img_url
        # 发送请求获取图片内容
        response = requests.get(captcha_img_url)
        img = Image.open(BytesIO(response.content))
        captcha_text = pytesseract.image_to_string(img).strip()
        print(captcha_text)
        # 定位隐藏输入框和验证码输入框
        captcha_0_input = page.locator('#id_captcha_0')
        captcha_1_input = page.locator('#id_captcha_1')
        # 获取隐藏输入框的值
        captcha_0_value = captcha_0_input.input_value()
        print(f"captcha_0_value: {captcha_0_value}")
        page.pause()
        # 将识别的验证码填入输入框
        captcha_1_input.fill(captcha_text)

    page.get_by_role("button", name="登录").click()
    page.pause()
    page.get_by_title("Default (46)").click()
    page.wait_for_timeout(1000)
    page.get_by_title("test (23)").click()
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


with sync_playwright() as playwright:
    '''复制粘贴：
            cd /data/logs/tomcat/merchart
            grep "发邮件结束 getVerificationCode 登录邮箱" *
            '''
    get_email_code(playwright, 'xiaozehua', '8qudcQifW7cjydglydm{')
