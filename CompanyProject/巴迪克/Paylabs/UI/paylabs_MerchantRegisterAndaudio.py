from tenacity import retry, stop_after_attempt
import os
from playwright.sync_api import expect, Playwright, sync_playwright
from CompanyProject.巴迪克.utils.GoogleSecure import GoogleAuth
from CompanyProject.巴迪克.utils.perform_slider_unlock import perform_block_slider_verification







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
    def get_google_code():
        google_code = GoogleAuth._calculate("bodioyzf2ojyh7qawk7ip2k5pnw7dzdn") #sitch-sales,找开发要sitch环境的key
        # google_code = GoogleAuth._calculate("urq7ocrpbxptnmr5zsw2upxxu76qbil6")
        # print("google_code:", google_code)
        # google_code = GoogleAuth.generate(
        #     environment='test',
        #     project='paylabs',
        #     table='operator',
        #     login_name=paylabs_operator_login_name
        # )
        # page.pause()
        page.locator("#googleCode").fill(google_code)

        if page.query_selector(".error-message:visible"):
            page.get_by_role("textbox", name="Google Verification Code").clear()
            raise ValueError("谷歌验证码错误")

    get_google_code()
    # paylabs_platform_google_code = generate_google_code('192.168.0.233', 3306, 'paylabs_payapi', 'SharkZ@DBA666', 'logic', 'operator', paylabs_operator_login_name)
    # page.pause()
    # page.get_by_role("textbox", name="Google Verification Code").fill(paylabs_platform_google_code)

    # error_code = page.get_by_role("textbox", name="The Google verification code is incorrect, please reenter")
    # if error_code.is_visible():
    #     page.get_by_role("textbox", name="Google Verification Code").fill(paylabs_platform_google_code)
    page.wait_for_timeout(1000)
    page.get_by_role("button", name="Submit").click()
    # page.wait_for_timeout(2000)
    # assert page.url.to_have_url("https://sitch-admin.paylabs.co.id/paylabs-trans-trans.html")
    expect(page).to_have_url("https://sitch-admin.paylabs.co.id/paylabs-trans-trans.html", timeout=5000)
    # assert page.url.startswith("https://sitch-admin.paylabs.co.id/paylabs-merchant-list.html")
    print("平台端登录成功")









def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()

    #商户注册
    # register_email = "paylabsmerchant@sitch.com"
    # paylabs_merchant_register(playwright, "test", register_email)
    #
    #
    # # sales端提交资料
#     sales_login_name = '15318544153'
# #     # merchant_id = "010327"
#     page = context.new_page()
#     sales_login(page, 'sitch',sales_login_name)
#     # # #
#     # # 获取第一条商户id
#     page.get_by_role("link", name="ﱖ Merchant ").click()
#     page.get_by_role("link", name="Merchant", exact=True).click()
#     # # 通过xpath获取元素的text值  //*[@id="merchant-datatable"]/tbody/tr[1]/td[1]
#     merchant_id = page.locator('//*[@id="merchant-datatable"]/tbody/tr[1]/td[1]').text_content()
#     print(merchant_id)
#     # #
#     # sales_setting_sales(page,merchant_id) #设置销售人员
#     sales_submit_info(page,register_email,merchant_id) #提交销售资料
#     # #
#     # # 平台审核
#     # paylabs_operator_login_name = 'test001@qq.com'
#     paylabs_operator_login_name = 'Xander1@sitch.paylabs.co.id'
#     page2 = context.new_page()
#     platform_login(page2, paylabs_operator_login_name)#登录平台
#
#     platform_risk_control_audit(page2,merchant_id)# 风控审核
#     # page2.wait_for_timeout(3000)
#     # platform_legal_risk_audit(page2,merchant_id)#法律审核
#     # platform_request_activation(page2,merchant_id)# 激活请求审核
#     # platform_activation_audit(page2,merchant_id)# 激活审核
#
#
#     context.close()
#     browser.close()

if __name__ == '__main__':
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    DATA_DIR = os.path.join(BASE_DIR, '../../common', 'data')
    # print(os.path.abspath('../../common'))
    pdf_file_path = os.path.join(DATA_DIR, "合同.pdf")
    #判断文件是否存在
    if not os.path.exists(pdf_file_path):
        print('文件不存在')

    with sync_playwright() as playwright:
        run(playwright)
