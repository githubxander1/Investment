import asyncio
import re

import pytesseract
from playwright.async_api import async_playwright
from playwright.sync_api import Playwright, sync_playwright, expect


async def get_email_code(username, password) -> None:
    async with async_playwright() as playwright:
        browser = await playwright.chromium.launch(headless=False)
        context = await browser.new_context()
        page = await context.new_page()
        await page.goto("http://192.168.0.228/core/auth/login/?next=/luna/")
        await page.get_by_role("textbox", name="用户名 *").fill(username)
        await page.get_by_role("textbox", name="密码").fill(password)
        await page.get_by_role("checkbox", name="天内自动登录").check()

        # 填写验证码
        # await page.get_by_role("textbox", name="Captcha *").fill("0")
        # await page.pause()

        from playwright.sync_api import sync_playwright
        # import pytesseract
        from PIL import Image
        import requests
        from io import BytesIO
        async def solve_captcha(page):
            # 定位验证码图片元素

            captcha_img = await page.locator('.captcha')
            # 获取验证码图片的src属性
            captcha_img_url = captcha_img.get_attribute('src')
            captcha_img_url = 'http://192.168.0.228'+captcha_img_url
            # 发送请求获取图片内容
            response = requests.get(captcha_img_url)
            img = Image.open(BytesIO(response.content))
            captcha_text = pytesseract.image_to_string(img).strip()
            print(captcha_text)
            # 定位隐藏输入框和验证码输入框
            captcha_0_input = await page.locator('#id_captcha_0')
            captcha_1_input = await page.locator('#id_captcha_1')
            # 获取隐藏输入框的值
            captcha_0_value = captcha_0_input.input_value()
            print(f"captcha_0_value: {captcha_0_value}")
            await page.pause()
            # 将识别的验证码填入输入框
            captcha_1_input.fill(captcha_text)

        await page.get_by_role("button", name="登录").click()
        # await page.pause()
        # await page.wait_for_timeout(1000)
        # await page.get_by_title("Default (41)").click()
        # await page.wait_for_timeout(1000)
        # await page.get_by_title("test (21)").click()
        # await page.wait_for_timeout(1000)
        # await page.get_by_title("192.168.0.224").click()
        # await page.wait_for_timeout(1000)
        # await page.pause()
        '''复制粘贴：
        cd /data/logs/tomcat/merchart
        grep \"发邮件结束 getVerificationCode 登录邮箱\" *'''
        await page.get_by_title("Default (46)").click()
        await page.wait_for_timeout(2000)
        await page.get_by_title("test (23)").click()
        await page.wait_for_timeout(2000)
        # await page.get_by_title("192.168.0.224").click()  #payok/paylabs
        await page.get_by_title("192.168.0.49").click()    #tax
        await page.wait_for_timeout(10000)
        # await page.get_by_role("textbox", name="发送文本到所有ssh终端").fill('grep "发邮件结束 getVerificationCode 登录邮箱" *') #payok的验证码
        text_box = page.get_by_role("textbox", name="发送文本到所有ssh终端")
        await text_box.fill('grep "verify code" *') #tax的验证码
        await text_box.press("Enter")
        # await page.pause()
        await page.wait_for_timeout(2000)
        await page.screenshot(path="./email_code.png")
        # ---------------------
        # context.close()
        # browser.close()

if __name__ == '__main__':
    username = 'xiaozehua'
    password = '8qudcQifW7cjydglydm{'
    asyncio.run(get_email_code(username, password))
