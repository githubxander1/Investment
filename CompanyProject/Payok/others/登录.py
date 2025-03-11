import asyncio
from playwright.async_api import async_playwright
import pyotp
import time
from PIL import Image
import requests
from pyzbar.pyzbar import decode

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()

        # 打开登录页面并输入邮箱和密码
        await page.goto('http://bitexchange-test.com/store/bitexchange-user-login.html')

        # 输入邮箱和密码
        await page.fill('input[name="email"]', 'your_email@example.com')
        await page.fill('input[name="password"]', 'your_password')

        # 滑动滑块验证（假设有一个滑块元素）
        slider = await page.query_selector('.slider')
        if slider:
            await slider.drag_to(await page.query_selector('.slider-track'))

        # 点击登录按钮
        await page.click('button[type="submit"]')

        # 等待跳转到二维码页面
        await page.wait_for_url('http://bitexchange-test.com/qr-code-page')

        # 获取二维码内容
        qr_code_element = await page.query_selector('img[alt="QR Code"]')
        qr_code_src = await qr_code_element.get_attribute('src')

        # 从二维码中提取 secret key
        secret_key = extract_secret_from_qr(qr_code_src)

        # 创建 TOTP 对象并生成当前时间的 TOTP 验证码
        totp = pyotp.TOTP(secret_key)
        current_code = totp.now()

        # 将验证码输入到输入框并点击绑定按钮
        await page.fill('input[name="googleVerificationCode"]', current_code)
        await page.click('button[type="bind"]')

        # 关闭浏览器
        await browser.close()

def extract_secret_from_qr(qr_code_src):
    # 下载二维码图片
    response = requests.get(qr_code_src)
    image = Image.open(BytesIO(response.content))

    # 解析二维码
    decoded_objects = decode(image)
    if not decoded_objects:
        raise ValueError("No QR code found in the image")

    # 提取二维码中的数据
    data = decoded_objects[0].data.decode('utf-8')

    # 从数据中提取 secret key
    # 假设二维码数据格式为 "otpauth://totp/Example:alice@gmail.com?secret=JBSWY3DPEHPK3PXP&issuer=Example"
    if "secret=" in data:
        secret_key = data.split("secret=")[1].split("&")[0]
        return secret_key
    else:
        raise ValueError("Secret key not found in QR code data")

# 运行脚本
asyncio.run(main())
