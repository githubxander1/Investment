# get_email_code.py
import re
import requests
from io import BytesIO
from PIL import Image
import pytesseract
from playwright.sync_api import Playwright, sync_playwright, expect


def get_email_code(username, password) -> None:
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()

        page.goto("http://192.168.0.228/core/auth/login/?next=/luna/")
        page.get_by_role("textbox", name="用户名 *").fill(username)
        page.get_by_role("textbox", name="密码").fill(password)
        page.get_by_role("checkbox", name="天内自动登录").check()

        def solve_captcha():
            captcha_img = page.locator('.captcha')
            captcha_img_url = captcha_img.get_attribute('src')
            captcha_img_url = 'http://192.168.0.228' + captcha_img_url
            response = requests.get(captcha_img_url)
            img = Image.open(BytesIO(response.content))
            captcha_text = pytesseract.image_to_string(img).strip()
            print(f"识别的验证码: {captcha_text}")
            captcha_1_input = page.locator('#id_captcha_1')
            captcha_1_input.fill(captcha_text)

        page.get_by_role("button", name="登录").click()

        try:
            page.wait_for_selector('#id_captcha_1', timeout=3000)
            solve_captcha()
            page.get_by_role("button", name="登录").click()
        except:
            pass

        page.get_by_title("Default (46)").click()
        page.wait_for_timeout(2000)
        page.get_by_title("test (23)").click()
        page.wait_for_timeout(2000)
        page.get_by_title("192.168.0.49").click()
        page.pause()

        text_box = page.get_by_role("textbox", name="发送文本到所有ssh终端")
        text_box.fill('cd /data/logs/tomcat/merchart')
        text_box.press("Enter")
        text_box.fill('grep "verify code" *')
        text_box.press("Enter")
        page.pause()

        context.close()
        browser.close()


if __name__ == '__main__':
    get_email_code('xiaozehua', '8qudcQifW7cjydglydm{')
