import time

from playwright.sync_api import Playwright, sync_playwright

from CompanyProject.Payok.交付.paylabs.GoogleSecure import CalGoogleCode
from CompanyProject.Payok.UI.utils.perform_slider_unlock import perform_slider_verification
from CompanyProject.Payok.UI.utils.sql_handler import SQLHandler


def run(playwright: Playwright, email, google_verification_code) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("http://paylabs-test.com/platform/paylabs-user-login.html")
    # page.goto("http://paylabs-test.com/merchant/paylabs-user-login.html")
    page.locator("span").filter(has_text="Bahasa").first.click()
    page.get_by_role("link", name="English").click()
    page.get_by_role("textbox", name="E-mail").fill(email)
    page.get_by_role("textbox", name="Password Verification Code").fill("Asd123456789.")

    # 滑块验证
    perform_slider_verification(page)

    page.get_by_role("button", name=" Login").click()

    # if expect(page.locator("h5")).to_contain_text("This user has logged in on another device, is it force to log in?"):
    # if expect(page.get_by_role("heading", name="This user has logged in on")).to_be_visible():
    # if expect(page.get_by_role("heading", name="This user has logged in on another device, is it force to log in?")).to_be_visible():
    error_locator = page.locator("text=This user has logged in on another device, is it force to log in?")
    if error_locator.is_visible():
        page.get_by_role("button", name="Confirm").click()

    max_retries = 3  # 设置最大重试次数
    retries = 0

    while retries < max_retries:
        page.get_by_role("textbox", name="Google Verification Code").fill(google_verification_code)
        page.locator("#btnGoogleLogin").click()

        # 等待一段时间确保页面更新
        time.sleep(2)

        # 检查是否出现验证码错误提示
        error_locator = page.locator("text=The Google verification code is incorrect, please reenter")
        if error_locator.is_visible():
            print(f"Google Verification Code incorrect. Retrying... ({retries + 1}/{max_retries})")
            retries += 1
            google_verification_code = generate_google_code(email)  # 重新生成验证码
        else:
            print("Google Verification Code pass")
            break

    if retries == max_retries:
        print("Max retries reached. Login failed.")
        context.close()
        browser.close()
        return

    # page.locator(".select2-selection__arrow").first.click()
    # page.get_by_role("treeitem", name="BEN").click()
    # page.locator("div:nth-child(8) > span > .selection > .select2-selection > .select2-selection__arrow").click()
    # page.get_by_role("treeitem", name="All").click()
    # page.get_by_role("combobox", name="Please select merchant first").locator("span").nth(1).click()
    # page.get_by_role("combobox", name="Please select merchant first").locator("b").click()
    # page.get_by_role("combobox", name="Please select merchant first").locator("span").nth(1).click()
    # page.locator("div:nth-child(12) > span > .selection > .select2-selection > .select2-selection__arrow").click()
    # page.get_by_role("treeitem", name="Success").click()
    # page.locator("div:nth-child(13) > span > .selection > .select2-selection > .select2-selection__arrow").click()
    # page.get_by_role("treeitem", name="Payin").click()
    # page.locator("div:nth-child(14) > span > .selection > .select2-selection > .select2-selection__arrow").click()
    # page.get_by_role("treeitem", name="All").click()
    # page.locator("div:nth-child(19) > span > .selection > .select2-selection > .select2-selection__arrow").click()
    # page.get_by_role("treeitem", name="Paylabs Settlement").click()
    # page.locator("div:nth-child(20) > span > .selection > .select2-selection > .select2-selection__arrow").click()
    # page.get_by_role("treeitem", name="Settled", exact=True).click()
    # page.locator("div:nth-child(22) > span > .selection > .select2-selection > .select2-selection__arrow").click()
    # page.get_by_role("treeitem", name="Advertising").click()
    # page.get_by_role("button", name=" Search").click()
    # page.get_by_role("link", name="Static VA Number").click()
    # page.get_by_role("combobox", name="All").locator("span").nth(1).click()
    # page.get_by_role("treeitem", name="010390-[]").click()
    # page.locator("#useStatus").select_option("1")
    # page.get_by_role("button", name=" Search").click()
    # page.get_by_role("link", name="ﰴ Payout ").click()
    # page.get_by_role("link", name="Payout List").click()

    # ---------------------
    context.close()
    browser.close()

def generate_google_code(email):
    db_handler = SQLHandler('192.168.0.233', 3306, 'paylabs_payapi', 'SharkZ@DBA666', 'paylabs')
    db_handler.connect()

    secret_key = db_handler.get_google_secret_key('operator', email)
    # secret_key = db_handler.get_google_secret_key('merchant_operator', email)
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
    email = "xzh@test.com"

    with sync_playwright() as playwright:
        run(playwright, email ,generate_google_code(email))
