import re
import time

from playwright.sync_api import Playwright, sync_playwright, expect

from CompanyProject.Payok.UI.utils.GoogleSecure import CalGoogleCode
from CompanyProject.Payok.UI.utils.perform_slider_unlock import perform_slider_verification
from CompanyProject.Payok.UI.utils.sql_handler import SQLHandler


def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("http://paylabs-test.com/merchant/paylabs-user-login.html")
    page.get_by_role("textbox", name="E-mail").fill("paylabs1@test.com")
    page.get_by_role("textbox", name="Password").fill("Abc@123456789")
    page.locator("#mpanel2 i").click()

    perform_slider_verification(page)

    page.get_by_role("button", name="Login").click()

    page.wait_for_timeout(2000)
    confirm = page.get_by_role("button", name="Confirm")
    if confirm.is_visible():
        confirm.click()

    max_retries = 3  # 设置最大重试次数
    retries = 0

    while retries < max_retries:
        page.get_by_role("textbox", name="Google Verification Code").fill(generate_google_code())
        page.locator("#btnGoogleLogin").click()

        # 等待一段时间确保页面更新
        time.sleep(2)

        # 检查是否出现验证码错误提示
        error_locator = page.locator("text=The Google verification code is incorrect, please reenter")
        if error_locator.is_visible():
            print(f"谷歌验证码错误，正在重试... ({retries + 1}/{max_retries})")
            retries += 1
        else:
            print("谷歌验证码正确")
            break

    if retries == max_retries:
        print("已达最大尝试次数，登录失败")
        context.close()
        browser.close()
        return

    # page.get_by_role("textbox", name="Google Verification Code").fill(google_verifivation_code)
    # page.get_by_role("button", name="Login").click()
    # page.get_by_role("link", name="Payin Summary").click()
    # page.get_by_role("link", name="ﰲ Transaction Details ").click()
    # page.get_by_role("link", name="Payin List").click()
    # page.locator("div").filter(has_text=re.compile(r"^Fees Type AllBENOURAll$")).locator("b").click()
    # page.get_by_role("treeitem", name="BEN").click()
    # page.get_by_role("combobox", name="All").locator("span").nth(1).click()
    # page.get_by_role("treeitem", name="Processing").click()
    # page.locator("#txtTransType").select_option("0")
    # page.locator("#sourceFrom").select_option("h5")
    # page.locator("#txtSettleType").select_option("0")
    # page.locator("#txtSettleStatus").select_option("1")
    # page.get_by_role("button", name=" Search").click()
    # page.get_by_role("link", name="﮹ Accounts ").click()

    # ---------------------
    context.close()
    browser.close()

def generate_google_code():
    db_handler = SQLHandler('192.168.0.233', 3306, 'paylabs_payapi', 'SharkZ@DBA666', 'paylabs')
    db_handler.connect()

    # secret_key = db_handler.get_google_secret_key('operator', email)
    secret_key = db_handler.get_google_secret_key('merchant_operator', 'paylabs1@test.com')
    if secret_key:
        print("Google Secret Key:", secret_key)

    db_handler.disconnect()
    try:
        current_time = int(time.time()) // 30
        generated_code = CalGoogleCode.cal_google_code(secret_key, current_time)
        # print(f"Generated Code: {generated_code}")
        # print(CalGoogleCode.cal_google_code(secret_key))  # 并未实例化CalGoogleCode，也可以调用它的方法
        return generated_code
    except ValueError as e:
        print("错误:", e)

if __name__ == '__main__':
    email = "paylabs1@test.com"
    with sync_playwright() as playwright:
        run(playwright)
