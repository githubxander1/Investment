import re
import time

from playwright.sync_api import Playwright, sync_playwright, expect

from CompanyProject.Payok.utils.GoogleSecure import CalGoogleCode
from CompanyProject.Payok.utils.sql_handler import SQLHandler


def run(playwright: Playwright, email, google_verification_code) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("http://paylabs-test.com/platform/paylabs-user-login.html")
    page.locator("span").filter(has_text="Bahasa").first.click()
    page.get_by_role("link", name="English").click()
    page.get_by_role("textbox", name="E-mail").fill(email)
    page.get_by_role("textbox", name="Password Verification Code").fill("Asd123456789.")
    page.get_by_role("button", name=" Login").click()
    page.get_by_role("textbox", name="Google Verification Code").fill(google_verification_code)

    if expect(page.locator("body")).to_contain_text("The Google verification code is incorrect, please reenter"):
        page.get_by_role("textbox", name="The Google verification code is incorrect, please reenter").fill(google_verification_code)
        page.get_by_role("button", name="Submit").click()
        print("Google Verification Code fail")
    else:
        print("Google Verification Code sent again")

    page.get_by_role("button", name="Submit").click()


    page.locator(".select2-selection__arrow").first.click()
    page.get_by_role("treeitem", name="BEN").click()
    page.locator("div:nth-child(8) > span > .selection > .select2-selection > .select2-selection__arrow").click()
    page.get_by_role("treeitem", name="All").click()
    page.get_by_role("combobox", name="Please select merchant first").locator("span").nth(1).click()
    page.get_by_role("combobox", name="Please select merchant first").locator("b").click()
    page.get_by_role("combobox", name="Please select merchant first").locator("span").nth(1).click()
    page.locator("div:nth-child(12) > span > .selection > .select2-selection > .select2-selection__arrow").click()
    page.get_by_role("treeitem", name="Success").click()
    page.locator("div:nth-child(13) > span > .selection > .select2-selection > .select2-selection__arrow").click()
    page.get_by_role("treeitem", name="Payin").click()
    page.locator("div:nth-child(14) > span > .selection > .select2-selection > .select2-selection__arrow").click()
    page.get_by_role("treeitem", name="All").click()
    page.locator("div:nth-child(19) > span > .selection > .select2-selection > .select2-selection__arrow").click()
    page.get_by_role("treeitem", name="Paylabs Settlement").click()
    page.locator("div:nth-child(20) > span > .selection > .select2-selection > .select2-selection__arrow").click()
    page.get_by_role("treeitem", name="Settled", exact=True).click()
    page.locator("div:nth-child(22) > span > .selection > .select2-selection > .select2-selection__arrow").click()
    page.get_by_role("treeitem", name="Advertising").click()
    page.get_by_role("button", name=" Search").click()
    page.get_by_role("link", name="Static VA Number").click()
    page.get_by_role("combobox", name="All").locator("span").nth(1).click()
    page.get_by_role("treeitem", name="010390-[]").click()
    page.locator("#useStatus").select_option("1")
    page.get_by_role("button", name=" Search").click()
    page.get_by_role("link", name="ﰴ Payout ").click()
    page.get_by_role("link", name="Payout List").click()

    # ---------------------
    context.close()
    browser.close()

def generate_google_code(email):
    db_handler = SQLHandler('192.168.0.233', 3306, 'paylabs_payapi', 'SharkZ@DBA666', 'paylabs')
    db_handler.connect()

    # secret_key = db_handler.get_google_secret_key('2695418206@qq.com')
    secret_key = db_handler.get_google_secret_key('merchant_operator', email)
    if secret_key:
        print("Google Secret Key:", secret_key)

    db_handler.disconnect()
    try:
        current_time = int(time.time()) // 30
        print(f"Current Time: {current_time}")
        generated_code = CalGoogleCode.cal_google_code(secret_key, current_time)
        print(f"Generated Code: {generated_code}")
        print(CalGoogleCode.cal_google_code(secret_key))  # 并未实例化CalGoogleCode，也可以调用它的方法
        return generated_code
    except ValueError as e:
        print("错误:", e)

if __name__ == '__main__':
    email = "xzh@test.com"
    generate_google_code(email)
    print("Google Code:", generate_google_code(email))
    with sync_playwright() as playwright:
        run(playwright, email ,generate_google_code(email))
