# get_email_code.py
import asyncio
import re
import requests
from io import BytesIO
from PIL import Image
import pytesseract
from playwright.async_api import async_playwright, Page, BrowserContext


async def get_email_code(username, password) -> None:
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context()
        page = await context.new_page()

        await page.goto("http://192.168.0.228/core/auth/login/?next=/luna/")
        await page.get_by_role("textbox", name="用户名 *").fill(username)
        await page.get_by_role("textbox", name="密码").fill(password)
        await page.get_by_role("checkbox", name="天内自动登录").check()

        async def solve_captcha():
            captcha_img = await page.locator('.captcha').element_handle()
            captcha_img_url = await captcha_img.get_attribute('src')
            captcha_img_url = 'http://192.168.0.228' + captcha_img_url
            response = requests.get(captcha_img_url)
            img = Image.open(BytesIO(response.content))
            captcha_text = pytesseract.image_to_string(img).strip()
            print(f"识别的验证码: {captcha_text}")
            await page.locator('#id_captcha_1').fill(captcha_text)

        await page.get_by_role("button", name="登录").click()

        try:
            await page.wait_for_selector('#id_captcha_1', timeout=3000)
            await solve_captcha()
            await page.get_by_role("button", name="登录").click()
        except:
            pass

        await page.get_by_title("Default (46)").click()
        await page.wait_for_timeout(2000)
        await page.get_by_title("test (23)").click()
        await page.wait_for_timeout(2000)
        await page.get_by_title("192.168.0.49").click()
        await page.pause()

        text_box = await page.get_by_role("textbox", name="发送文本到所有ssh终端").element_handle()
        await text_box.fill('cd /data/logs/tomcat/merchart')
        await text_box.press("Enter")
        await text_box.fill('grep "verify code" *')
        await text_box.press("Enter")
        await page.pause()

        await context.close()
        await browser.close()


if __name__ == '__main__':
    asyncio.run(get_email_code('xiaozehua', '8qudcQifW7cjydglydm{'))
