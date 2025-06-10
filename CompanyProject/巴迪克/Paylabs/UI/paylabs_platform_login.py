
from playwright.sync_api import Playwright, sync_playwright, expect

from CompanyProject.巴迪克.utils.GoogleSecure import GoogleAuth
from CompanyProject.巴迪克.utils.generate_google_code import GoogleAuthenticator
from CompanyProject.巴迪克.utils.perform_slider_unlock import perform_block_slider_verification
from tenacity import retry, stop_after_attempt

def platform_login(page,env:str,paylabs_operator_login_name):
    # 平台登录
    url = 'http://test.paylabs.id/platform/paylabs-user-login.html' if env == 'test' else 'https://sitch-admin.paylabs.co.id/paylabs-user-login.html'
    page.goto(url)
    page.locator("span").filter(has_text="Bahasa").first.click()
    page.get_by_role("link", name="English").click()

    # 登录
    page.get_by_role("textbox", name="E-mail").fill(paylabs_operator_login_name)
    page.get_by_role("textbox", name="Password Verification Code").fill("A123456@test")

    perform_block_slider_verification(page)
    page.get_by_role("button", name=" Login").click()
    page.wait_for_timeout(2000)
    # 如果有弹窗，点确定
    has_login = page.get_by_role("heading", name="This user has logged in on")
    if has_login.is_visible():
        page.get_by_role("button", name="Confirm").click()

    @retry(stop=stop_after_attempt(3))
    def get_google_code(env):
        if env == 'sitch':
            google_code = GoogleAuth._calculate("bodioyzf2ojyh7qawk7ip2k5pnw7dzdn") #sitch-sales,找开发要sitch环境的key
            # google_code = GoogleAuth._calculate("urq7ocrpbxptnmr5zsw2upxxu76qbil6")
            print("google_code:", google_code)
        else:
            google_code = GoogleAuth.generate(
                environment='test',
                project='paylabs',
                table='platform_operator',
                login_name=paylabs_operator_login_name
            )
        # page.pause()
        page.locator("#googleCode").fill(google_code)

        if page.query_selector(".error-message:visible"):
            page.get_by_role("textbox", name="Google Verification Code").clear()
            raise ValueError("谷歌验证码错误")

    get_google_code('test')
    page.get_by_role("button", name="Submit").click()
    page.wait_for_timeout(1000)
    assert_url = "https://sitch-admin.paylabs.co.id/paylabs-trans-trans.html" if env == 'sitch' else "http://test.paylabs.id/platform/paylabs-trans-trans.html"
    print("平台端登录成功") if page.url.startswith(assert_url) else print("平台端登录失败")


if __name__ == '__main__':
    login_email = "xzh@test.com"

    with sync_playwright() as playwright:
        platform_login(playwright, 'test',login_email)
