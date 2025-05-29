import time

from playwright.sync_api import Playwright, sync_playwright

from CompanyProject.巴迪克.utils.generate_google_code import GoogleAuthenticator
from CompanyProject.巴迪克.utils.perform_slider_unlock import perform_block_slider_verification
from tenacity import retry, stop_after_attempt

def run(playwright: Playwright, login_email) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("http://paylabs-test.com/merchant/paylabs-user-login.html")
    page.get_by_role("textbox", name="E-mail").fill(login_email)
    page.get_by_role("textbox", name="Password").fill("Abc@123456789")
    page.locator("#mpanel2 i").click()

    perform_block_slider_verification(page)

    page.get_by_role("button", name="Login").click()

    page.wait_for_timeout(2000)
    confirm = page.get_by_role("button", name="Confirm")
    if confirm.is_visible():
        confirm.click()

    @retry(stop=stop_after_attempt(3))  # 补全stop参数
    def get_google_code():
        merchant_google_code = GoogleAuthenticator.generate(
            environment='test',
            project='paylabs',
            table='merchant_operator',
            login_name=login_email
        )
        page.get_by_role("textbox", name="Google Verification Code").fill(merchant_google_code)

        code_error_message = page.get_by_role("textbox",
                                              name="The Google verification code is incorrect, please reenter")
        page.wait_for_timeout(1000)

        # 主动抛出异常触发重试
        if code_error_message.is_visible():
            page.get_by_role("textbox", name="Google Verification Code").clear()
            raise ValueError("谷歌验证码错误")  # 添加异常抛出

        page.get_by_role("button", name="Login").click()

    get_google_code()
    page.pause()


    # ---------------------
    context.close()
    browser.close()


if __name__ == '__main__':
    login_email = "paylabs1@test.com"
    with sync_playwright() as playwright:
        run(playwright,login_email)
