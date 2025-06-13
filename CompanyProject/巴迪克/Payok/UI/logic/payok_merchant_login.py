from playwright.sync_api import Playwright, sync_playwright

from CompanyProject.巴迪克.zothers.generate_google_code import GoogleAuthenticator
from CompanyProject.巴迪克.utils.perform_slider_unlock import perform_block_slider_verification
from tenacity import retry, stop_after_attempt

def merchant_login(playwright: Playwright, login_email,password) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("http://payok-test.com/merchant/payok-user-login.html")
    page.locator("span").filter(has_text="Indonesia").first.click()
    page.get_by_role("link", name="Indonesia").click()
    # page.get_by_role("link", name="Vietnam").click()
    page.get_by_role("textbox", name="Country E-mail").fill(login_email)
    page.get_by_role("textbox", name="Password").fill(password)
    perform_block_slider_verification(page)
    page.get_by_role("button", name="Login").click()

    @retry(stop=stop_after_attempt(3))  # 补全stop参数
    def get_google_code():
        payok_merchant_google_code = GoogleAuthenticator.generate(
        environment='test',
        project='payok',
        table='merchant_operator',
        login_name=login_email
    )
        page.get_by_role("textbox", name="Google Verification Code").fill(payok_merchant_google_code)

        code_error_message = page.get_by_role("textbox", name="The Google verification code is incorrect, please reenter")
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
    login_email= "payok@test.com"
    password= "A123456@test"
    with sync_playwright() as playwright:
        merchant_login(playwright, login_email,password)
