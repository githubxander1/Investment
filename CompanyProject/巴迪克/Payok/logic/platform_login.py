from playwright.sync_api import Playwright, sync_playwright, expect
from tenacity import stop_after_attempt, retry

from CompanyProject.巴迪克.utils.GoogleSecure import GoogleAuth
# from CompanyProject.巴迪克.Paylabs.UI.paylabs_merchant_register import generate_google_code
from CompanyProject.巴迪克.utils.perform_slider_unlock import perform_block_slider_verification


def platform_login(playwright: Playwright ,operator_login_name, operator_password):
    # 平台登录
    page = playwright.chromium.launch(headless=False).new_page()

    page.goto("http://payok-test.com/platform/payok-user-login.html")
    page.get_by_text("Bahasa").click()
    page.get_by_role("link", name="中文").click()

    page.get_by_role("textbox", name="邮箱").fill(operator_login_name)
    page.get_by_placeholder("请输入密码").fill(operator_password)
    perform_block_slider_verification(page)

    page.get_by_role("button", name=" 登录").click()
    # google_code = generate_google_code('192.168.0.227', 3306, 'WAYANGPAY', 'Z43@Mon88', 'aesygo_test', 'operator',
    #                                    operator_login_name)
    @retry(stop=stop_after_attempt(3))
    def get_google_code(page):
        # if env == 'sitch':
        #     google_code = GoogleAuth._calculate("4cavnkhcy3x46g46jwhe45ajulmsouwe")
        # else:
        google_code = GoogleAuth.generate(
            environment='test',
            project='payok',
            table='platform_operator',
            login_name=operator_login_name
        )
        page.locator("#googleCode").fill(google_code)
        page.get_by_role("button", name="Login").click()

        if page.locator(".googleCodeError").is_visible():
            page.get_by_role("textbox", name="Google Verification Code").clear()
            print("谷歌验证码错误")
            raise ValueError("谷歌验证码错误")

    get_google_code(page)
    # page.get_by_role("textbox", name="谷歌验证码").fill(google_code)
    page.get_by_role("button", name="确认").click()
    url ='http://payok-test.com/platform/payok-trans-trans.html'
    #断言是否进入这个url，如果不是这个url，就报错
    try:
        expect(page).to_have_url(url)
        print("平台端登录成功")
    except:
        print("平台端登录失败")
        page.pause()


if __name__ == '__main__':
    login_email= "3@qq.com"
    operator_password= "A123456@test"
    with sync_playwright() as playwright:
        platform_login(playwright, login_email,operator_password)
