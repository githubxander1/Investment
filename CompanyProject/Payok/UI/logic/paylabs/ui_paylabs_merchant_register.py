import re
import time

from playwright.sync_api import Playwright, sync_playwright, expect

from CompanyProject.Payok.UI.utils.GoogleSecure import CalGoogleCode
from CompanyProject.Payok.UI.utils.sql_handler import SQLHandler


def paylabs_merchant_register(playwright: Playwright, email) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("http://paylabs-test.com/merchant/paylabs-register-register.html#")
    page.locator("span").filter(has_text="id").first.click()
    page.get_by_role("link", name="EN", exact=True).click()

    page.get_by_role("textbox", name="E-mail *", exact=True).fill(email)
    page.get_by_role("textbox", name="Email Verification Code *").fill("652266")
    page.locator("#phone").fill("15318544125")
    page.locator("#phoneCode").fill("652266")
    page.get_by_role("textbox", name="Secure Email for fund account").fill(email)
    page.get_by_role("textbox", name="Please enter contact").fill(email)#PIC名字
    # page.get_by_role("textbox", name="Password *" , exact=True).fill("Abc@123456789")
    page.get_by_role("textbox", name="Password *" , exact=True).fill("A123456@test")
    page.get_by_role("textbox", name="Confirm password *", exact=True).fill("A123456@test")
    page.locator("#invitation_code").fill("123456")
    page.get_by_role("button", name="Register").click()
    page.get_by_role("button", name="I have read and agree to the").click()#同意

    #点击去登录
    # page.get_by_role("link", name="去登录").click()

    # page.get_by_role("button", name="I have read and agree to the").click()#去登录

    page.wait_for_timeout(5000)
    # has_register = page.locator("#inputEmail").text_content("The E-mail has been registered")
    # if has_register.is_exist():
    #     print("注册失败：邮箱已被注册")

    # 断言页面中某个元素的文本包含特定内容
    # element = page.query_selector('#inputEmail')
    # assert element.text_content().find('The E-mail has been registered') != -1

    # 使用expect函数断言页面中某个元素的文本包含特定内容
    # element = page.query_selector('#inputEmail')
    # expect(element).to_have_text(expect.string_contains('The E-mail has been registered'))

    if not expect(page.locator("#inputEmail")).to_contain_text("The E-mail has been registered"):
        print("注册失败：邮箱已被注册")
    else:
        print("注册成功")


    page.locator("#gologin").click()

    #绑定谷歌验证码
    # page.get_by_role("link", name="Masuk").click()
    # page.get_by_role("textbox", name="E-mail").fill(email)
    # # page.pause()
    # page.get_by_role("textbox", name="Password").fill("Abc@123456789")
    # # page.locator("#mpanel2 i").click()
    # page.get_by_role("button", name="Login").click()
    #
    # page.get_by_role("textbox", name="Google Verification Code").fill(google_verification_code)
    # page.get_by_role("button", name="Bound").click()
    #
    # # expect(page.locator("body")).to_contain_text("Google Verification Code Status")
    # if expect(page.locator("body")).to_contain_text("The Google verification code is incorrect, please reenter"):
    #     print("Google Verification Code fail")
    # else:
    #     page.get_by_role("textbox", name="The Google verification code is incorrect, please reenter").fill(google_verification_code)
    #     page.get_by_role("button", name="Bound").click()
    #     print("Google Verification Code sent again")
    #
    # # page.get_by_text("The Google verification code is incorrect, please reenter").click()
    #
    # # 登录
    # page.get_by_role("button", name="Go to login").click()
    # page.get_by_role("textbox", name="E-mail").fill(email)
    # page.get_by_role("textbox", name="Password").fill("Abc@123456789")
    # page.get_by_role("button", name="Login").click()
    #
    # page.get_by_role("textbox", name="Google Verification Code").fill(google_verification_code)
    # page.get_by_role("button", name="Login").click()
    #
    # if expect(page.locator("body")).to_contain_text("The Google verification code is incorrect, please reenter"):
    #     print("Google Verification Code fail")
    #     page.get_by_role("textbox", name="The Google verification code is incorrect, please reenter").fill(google_verification_code)
    #     page.get_by_role("button", name="Login").click()
    #     print("Google Verification Code sent again")
    # page.get_by_role("textbox", name="Google Verification Code").fill("649617")
    # page.get_by_role("button", name="Login").click()



    # ---------------------
    context.close()
    browser.close()
def generate_google_code():
    db_handler = SQLHandler('192.168.0.233', 3306, 'paylabs_payapi', 'SharkZ@DBA666', 'paylabs')
    db_handler.connect()

    # secret_key = db_handler.get_google_secret_key('2695418206@qq.com')
    secret_key = db_handler.get_google_secret_key('merchant_operator', 'paylabs2@test.com')
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
    email = "paylabs4@test.com"
    generate_google_code()

    with sync_playwright() as playwright:
        paylabs_merchant_register(playwright, email)
