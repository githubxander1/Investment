import os
import time

import sys
print(sys.path)
print(sys.executable)

# 获取当前文件所在目录
current_dir = os.path.dirname(os.path.abspath(__file__))
print(f'当前文件所在目录:{current_dir}')
# 获取包含 CompanyProject 的父目录
parent_dir = os.path.dirname(os.path.dirname(os.path.dirname(current_dir)))
print(f'项目目录:{parent_dir}')
# 将该目录添加到模块搜索路径中
sys.path.append(parent_dir)
project_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(current_dir))))
print(f'项目根目录:{project_dir}')
sys.path.append(project_dir)

from CompanyProject.Payok.交付.paylabs.GoogleSecure import CalGoogleCode
from CompanyProject.Payok.UI.utils.perform_slider_unlock import perform_block_slider_verification
from CompanyProject.Payok.UI.utils.sql_handler import SQLHandler

from playwright.sync_api import Playwright, sync_playwright

def payok_merchant_login(playwright: Playwright, email) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("http://payok-test.com/merchant/payok-user-login.html")
    page.get_by_role("textbox", name="Country E-mail").fill(email)
    page.get_by_role("textbox", name="Password").fill("Test001@test")
    page.wait_for_timeout(3000)

    perform_block_slider_verification(page)

    page.get_by_role("button", name="Login").click()

    # page.wait_for_timeout(3000)


    max_retries = 3  # 设置最大重试次数
    retries = 0

    while retries < max_retries:
        page.get_by_role("textbox", name="Google Verification Code").fill(generate_google_code())
        page.locator("#btnGoogleLogin").click()

        # 等待一段时间确保页面更新
        page.wait_for_timeout(1000)

        # 检查是否出现验证码错误提示
        error_locator = page.locator("text=The Google verification code is incorrect, please reenter")
        if error_locator.is_visible():
            print(f"Google Verification Code incorrect. Retrying... ({retries + 1}/{max_retries})")
            retries += 1

            page.get_by_role("textbox", name="Google Verification Code").fill(generate_google_code())
            page.locator("#btnGoogleLogin").click()
            # google_verification_code = generate_google_code()  # 重新生成验证码
        else:
            print("Google Verification Code pass")
            break

    if retries == max_retries:
        print("Max retries reached. Login failed.")
        # context.close()
        # browser.close()
        return

    page.wait_for_timeout(5000)

    # page.pause()

    # ---------------------
    context.close()
    browser.close()


def generate_google_code():
    db_handler = SQLHandler('192.168.0.227', 3306, 'WAYANGPAY', 'Z43@Mon88', 'aesygo_test')
    db_handler.connect()

    secret_key = db_handler.get_google_secret_key('merchant_operator', '92d720ee5739@drmail.in')
    if secret_key:
        print("谷歌私钥:", secret_key)
    else:
        print("未发现给定邮箱的记录")
        return None

    db_handler.disconnect()
    try:
        current_time = int(time.time()) // 30
        generated_code = CalGoogleCode.cal_google_code(secret_key, current_time)
        print(f"生成的谷歌验证码: {generated_code}")
        return generated_code
    except ValueError as e:
        print("错误:", e)
        return None


if __name__ == '__main__':
    email = '92d720ee5739@drmail.in'
    # generated_code = generate_google_code()
    with sync_playwright() as playwright:
        payok_merchant_login(playwright, email)
