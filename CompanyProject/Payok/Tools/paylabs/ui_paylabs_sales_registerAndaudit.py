#paylabs商户注册和审核全流程
import os
from playwright.sync_api import Playwright, sync_playwright
from CompanyProject.Payok.Tools.paylabs.ui_paylabs_merchant_register import paylabs_merchant_register
from CompanyProject.Payok.Tools.paylabs.GoogleSecure import CalGoogleCode
from CompanyProject.Payok.Tools.paylabs.perform_slider_unlock import perform_block_slider_verification

def sales_login(page , sales_login_name):
    # page.goto("http://paylabs-test.com/sales/paylabs-user-login.html")
    page.goto("https://sitch-sales.paylabs.co.id/paylabs-user-login.html") #sith环境
    # 切换语言
    page.locator("span").filter(has_text="Bahasa").first.click()
    page.get_by_role("link", name="English").click()

    # sales 端登录
    page.get_by_role("textbox", name="Phone Number").fill(sales_login_name)
    page.get_by_role("textbox", name="Password").fill("A123456@test")
    perform_block_slider_verification(page)
    page.get_by_role("button", name="Login").click()
    calculategooglecode = CalGoogleCode()
    paylabs_merchant_google_code = calculategooglecode.generate_google_code('192.168.0.233', 3306, 'paylabs_payapi', 'SharkZ@DBA666',
                                                        'paylabs', 'sales_operator', sales_login_name)
    page.wait_for_timeout(1000)
    try:
        # page.get_by_role("textbox", name="Google Verification Code").fill(paylabs_merchant_google_code)
        page.pause()
        error_code = page.get_by_role("textbox", name="The Google verification code is incorrect, please reenter")
        if error_code.is_visible(timeout=3000):
            page.get_by_role("textbox", name="Google Verification Code").fill(paylabs_merchant_google_code)
        page.get_by_role("button", name="Login").click()
    except Exception as e:
        print(f'输入谷歌验证码失败：{e}')
    print("sales端登录成功")

def sales_setting_sales(page, merchant_id):
    page.get_by_role("link", name="ﱖ Merchant ").click()
    page.locator("#left-bar-menu").get_by_role("link", name="Merchant", exact=True).click()
    scroll_div = page.wait_for_selector('#scrollDiv')
    scroll_div_table = page.query_selector('#scrollDivTable')
    scroll_width = scroll_div_table.evaluate('(element) => element.offsetWidth')
    scroll_div.evaluate(f'(element) => element.scrollLeft = {scroll_width}')
    row = page.locator(f"tbody tr").filter(has_text=merchant_id)
    setting_sales_button = row.locator("#btnSetSales").first
    page.evaluate('(button) => button.click()', setting_sales_button.element_handle())
    page.locator('#select2-newSalesManModal-container').click()
    page.pause()
    # page.get_by_role("treeitem", name="test").click()
    page.get_by_role("textbox", name="Remarks").fill("1设置sales")
    page.locator("#btnSureSaleModal").click()
    print("销售设置成功")
def sales_submit_info(page,email, merchant_id):
    # 开始提交资料
    page.get_by_role("link", name="ﱖ Merchant ").click()
    page.locator("#left-bar-menu").get_by_role("link", name="Merchant", exact=True).click()

    page.wait_for_timeout(1000)
    with page.expect_popup() as page1_info:
        scroll_div = page.wait_for_selector('#scrollDiv')
        scroll_div_table = page.query_selector('#scrollDivTable')
        scroll_width = scroll_div_table.evaluate('(element) => element.offsetWidth')
        scroll_div.evaluate(f'(element) => element.scrollLeft = {scroll_width}')
        row = page.locator(f"tbody tr").filter(has_text=merchant_id)
        submit_button = row.locator("#btnSubmitInfo").first
        page.evaluate('(button) => button.click()', submit_button.element_handle())

    page = page1_info.value
    page.wait_for_timeout(3000)
    page.get_by_role("textbox", name="Company Name *").fill("test")
    # page.get_by_role("textbox", name="Company Name *").fill(email)
    page.get_by_role("textbox", name="Company Brand Name").fill(email)
    page.get_by_role("textbox", name="Company Abbreviation").fill("公司缩写")
    page.get_by_label("Types of Companies *").select_option("100")
    page.get_by_role("textbox", name="Official Website *").click()
    page.get_by_label("Types of Companies *").select_option("105")
    # page1.get_by_label("Types of Companies *").select_option("100")
    page.get_by_role("textbox", name="Official Website *").fill("http://paylabs-test.com/sales/paylabs-merchant-info.html?k=1bdd7098b1cebd36e3d4be0028b9a7c3")
    page.get_by_role("textbox", name="Company Address *").fill("广东省深圳市南山区桃源街道中广时代广场001")
    page.get_by_role("textbox", name="PIC Name *").fill("PIC名称")
    page.get_by_role("textbox", name="PIC Contact Number *").fill("123456789")
    page.get_by_role("textbox", name="PIC Email *").fill("1@qq.com")
    page.get_by_role("textbox", name="PIC Address").fill("广东省深圳市南山区桃源街道中广时代广场001")
    page.locator("#select2-merchantType-container").click()
    page.get_by_role("treeitem", name="Advertising").click()
    page.get_by_role("textbox", name="Default Amount Range (Upper").fill("100")
    page.get_by_role("textbox", name="Default Amount Range", exact=True).fill("1000")
    page.get_by_role("textbox", name="Default Transaction Range (").fill("2147")
    page.get_by_role("textbox", name="Default Transaction Range", exact=True).fill("3000")
    page.get_by_role("textbox", name="Default Income Range (Upper").fill("100")
    page.get_by_role("textbox", name="Default Income Range", exact=True).fill("1000")
    page.get_by_role("textbox", name="##.###.###.#-###.###").fill("00.000.000.0-000.000")
    page.locator("#checkNPWP").click()
    page.get_by_role("textbox", name="LawanTransaksiID").fill("13546512456")
    page.get_by_role("textbox", name="NIK").fill("124")
    page.locator("#checkNIK").click()
    page.get_by_role("textbox", name="Account Number *").fill("15354879")
    page.get_by_role("textbox", name="Account Name *").fill("账户名称")
    page.get_by_role("textbox", name="Bank Name *").fill("中国人民银行")
    page.get_by_role("textbox", name="SWIFT Code *").fill("1236547")
    page.get_by_role("textbox", name="Business Contact *").fill("商务联系人")
    page.get_by_role("textbox", name="Technical Contact *").fill("技术联系人")
    page.get_by_role("textbox", name="Technical Contact Number *").fill("15318544154")
    page.get_by_role("textbox", name="Technical Contact Email *").fill("1@qq.com")
    page.get_by_role("textbox", name="Finance Contact *").fill("财务联系人")
    page.get_by_role("textbox", name="Finance Contact Number *").fill("15318544154")
    page.get_by_role("textbox", name="Business Contact Number *").fill("15318544154")
    page.get_by_role("textbox", name="Business Contact Email *").fill("1@qq.com")
    page.get_by_role("textbox", name="Finance Contact Email *").fill("1@qq.com")
    page.get_by_role("textbox", name="CS Contact", exact=True).fill("CS联系人")
    page.get_by_role("textbox", name="CS Contact Number").fill("15318544154")
    page.get_by_role("textbox", name="CS Contact Email").fill("1@qq.com")
    
    def upload_file(file_path, form_id):
        if not os.path.exists(file_path):
            return print(f"文件不存在: {file_path}")
        page.on('filechooser', lambda file_chooser: file_chooser.set_files(file_path))
        page.locator(f"#btnUpload{form_id}").click()

    upload_file(pdf_file_path, "11")
    upload_file(pdf_file_path, "12")
    upload_file(pdf_file_path, "13")
    upload_file(pdf_file_path, "14")
    upload_file(pdf_file_path, "15")
    upload_file(pdf_file_path, "16")
    upload_file(pdf_file_path, "17")
    upload_file(pdf_file_path, "18")
    upload_file(pdf_file_path, "24")

    page.pause()
    # page.get_by_role("heading", name="").locator("i").click()
    # page.locator("#select2-selTempsModal-container").click()
    select_bank_account = page.get_by_role("treeitem", name="Copy of Bank Account Book")
    # if select_bank_account.is_disabled():
    #     page.get_by_role("button", name="Cancel").click()#取消
    # else:
    # select_bank_account.click()
    # page.locator("#merFormModal i").click()

    # page.on('filechooser', lambda file_chooser: file_chooser.set_files(pdf_file_path))
    # page.locator("#temps-modal").click()
    # page.wait_for_timeout(1000)
    # page.locator("#btnSureTempModal").click()
    
    page.get_by_text("I declare that the application information submitted by the merchant for").click()
    page.get_by_text("I declare that the above").click()
    page.get_by_role("button", name="Save").click()
    page.locator("#btnSubmit").click()
    # page.get_by_role("link", name="I got it").click()
    print("客户端资料提交成功")

def platform_login(page ,paylabs_operator_login_name):
    # 平台登录
    # page.goto("http://paylabs-test.com/platform/paylabs-user-login.html")
    page.goto("https://sitch-admin.paylabs.co.id/paylabs-user-login.html")
    page.locator("span").filter(has_text="Bahasa").first.click()
    page.get_by_role("link", name="English").click()

    page.get_by_role("textbox", name="E-mail").fill(paylabs_operator_login_name)
    # page.get_by_role("textbox", name="Password Verification Code").fill("Abc@123456789")
    page.get_by_role("textbox", name="Password Verification Code").fill("A123456@test")
    perform_block_slider_verification(page)
    page.get_by_role("button", name=" Login").click()
    page.wait_for_timeout(1000)
    # 如果有弹窗，点确定
    has_login = page.get_by_role("heading", name="This user has logged in on")
    if has_login.is_visible():
        page.get_by_role("button", name="Confirm").click()
    calculategooglecode = CalGoogleCode()
    paylabs_platform_google_code = calculategooglecode.generate_google_code('192.168.0.233', 3306, 'paylabs_payapi', 'SharkZ@DBA666', 'paylabs', 'operator', paylabs_operator_login_name)
    page.pause()
    # page.get_by_role("textbox", name="Google Verification Code").fill(paylabs_platform_google_code)
    try:
        error_code = page.get_by_role("textbox", name="The Google verification code is incorrect, please reenter")
        if error_code.is_visible():
            page.get_by_role("textbox", name="Google Verification Code").fill(paylabs_platform_google_code)
    except Exception as e:
        print(f"获取验证码失败：{e}")

    page.get_by_role("button", name="Submit").click()
    page.wait_for_timeout(2000)
    print("平台端登录成功")

def platform_risk_control_audit(page, merchant_id):
    # 开始风险审核
    page.get_by_role("link", name=" Risk Control ").click()
    page.get_by_role("link", name="Risk Control", exact=True).click()

    scroll_div = page.wait_for_selector('#scrollDiv')
    scroll_div_table = page.query_selector('#scrollDivTable')
    scroll_width = scroll_div_table.evaluate('(element) => element.offsetWidth')
    scroll_div.evaluate(f'(element) => element.scrollLeft = {scroll_width}')
    row = page.locator(f"tbody tr").filter(has_text=merchant_id)
    risk_control_audit_button = row.get_by_role("button", name="Risk Control Audit")
    page.evaluate('(button) => button.click()', risk_control_audit_button.element_handle())
    page.get_by_role("textbox", name="Max 200 characters can be").fill("评论：风险控制审计通过")
    page.locator("#toRiskAudit").click()
    page.get_by_role("link", name="None").click()
    page.on('filechooser', lambda file_chooser: file_chooser.set_files(pdf_file_path))
    page.locator("#reportForm1").click()
    page.get_by_role("textbox", name="Max 200 characters can be").fill("评论：风控报告上传成功，风险控制审计通过2")
    page.get_by_role("button", name="Approve").click()
    page.locator("#btnSubmitSure").click()
    print("风险审核通过")

def platform_legal_risk_audit(page, merchant_id):
    # 法律风控
    page.get_by_role("link", name="ﶇ Merchant ").click()
    page.get_by_role("link", name="Merchant List").click()
    scroll_div = page.wait_for_selector('#scrollDiv')  # 等待目标 div 加载
    scroll_div_table = page.query_selector('#scrollDivTable')  # 获取 scrollDivTable 的宽度
    scroll_width = scroll_div_table.evaluate('(element) => element.offsetWidth')
    scroll_div.evaluate(f'(element) => element.scrollLeft = {scroll_width}')  # 滚动到最右侧
    row = page.locator(f"tbody tr").filter(has_text=merchant_id)
    legal_audit_button = row.get_by_role("button", name="Legal Audit")
    page.evaluate('(button) => button.click()', legal_audit_button.element_handle())
    page.on('filechooser', lambda file_chooser: file_chooser.set_files(pdf_file_path))
    page.locator("#reportForm2").click()
    page.on('filechooser', lambda file_chooser: file_chooser.set_files(pdf_file_path))
    page.locator("#reportForm3").click()
    page.get_by_role("button", name="Approve").click()
    page.wait_for_timeout(2000)
    page.pause()
    page.locator("#btnSurePass").click()
    print("法律风控审核通过")

def platform_request_activation(page,merchant_id):
    # 激活请求
    page.get_by_role("link", name="ﶇ Merchant ").click()
    page.get_by_role("link", name="Merchant List").click()
    page.wait_for_timeout(1000)
    scroll_div = page.wait_for_selector('#scrollDiv')
    scroll_div_table = page.query_selector('#scrollDivTable')
    scroll_width = scroll_div_table.evaluate('(element) => element.offsetWidth')
    scroll_div.evaluate(f'(element) => element.scrollLeft = {scroll_width}')
    row = page.locator(f"tbody tr").filter(has_text=merchant_id)
    request_activate_button = row.get_by_role('button', name="Request Activation ")
    page.evaluate('(button) => button.click()', request_activate_button.element_handle())
    page.locator("#nav_1 div").filter(has_text="DanamonVA Settlement Type").get_by_role("button").click()
    page.get_by_role("listitem").filter(has_text="Danamon Paylabs").locator("label").first.click()
    page.locator("#rate232").fill("99")
    page.locator("#fee232").fill('10000')
    page.locator("#transSharingRate232").fill("0")
    page.locator("#transSharingFee232").fill("10")
    # page.pause()
    # page.get_by_role("listitem").filter(has_text="Danamon Paylabs").locator("select[name=\"selMerVat\"]").select_option(
    #     "0.11")
    page.get_by_role("cell", name="Non-active").locator("label").click()
    page.get_by_role("cell", name="Active").get_by_role("list").click()
    page.get_by_role("button", name="Select all").click()
    page.get_by_role("cell", name="Merchant Cost ").click()
    page.get_by_role("cell", name="*Merchant Fee % Sample:0.7000").get_by_role("textbox").first.fill("7")
    page.get_by_role("textbox", name="1000").fill("7000")
    # page.get_by_role("cell", name="*Merchant Fee 4 % Sample:0.").get_by_role("combobox").select_option("0.11")
    page.get_by_role("textbox", name="Merchant RSA Public Key").fill("123456789")
    page.get_by_role("button", name="Submit Request").click()
    print("激活请求提交成功")

def platform_activation_audit(page,merchant_id):
    # 激活审核
    page.get_by_role("link", name="ﶇ Merchant ").click()
    page.get_by_role("link", name="Merchant List").click()
    scroll_div = page.wait_for_selector('#scrollDiv')  # 等待目标 div 加载
    scroll_div_table = page.query_selector('#scrollDivTable')  # 获取 scrollDivTable 的宽度
    scroll_width = scroll_div_table.evaluate('(element) => element.offsetWidth')
    scroll_div.evaluate(f'(element) => element.scrollLeft = {scroll_width}')  # 滚动到最右侧
    row = page.locator(f"tbody tr").filter(has_text=merchant_id)
    activate_audit_button = row.get_by_role('button', name="Activation Audit")
    page.evaluate('(button) => button.click()', activate_audit_button.element_handle())
    page.get_by_role("textbox", name="Max 200 characters can be").fill("评论：激活审核通过")
    page.get_by_role("button", name="Passed").click()
    print("商户入驻成功！")


    # 退出登录
    page.locator("#txtOperatorName").click()
    page.locator("a").filter(has_text="Log Out").click()
    page.get_by_role("button", name="Submit").click()
    print("退出登录成功")

def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()

    #商户注册
    register_email = "paylabs_merchant002@test.com" # Merchant Name商户名称，可自定义
    # paylabs_merchant_register(playwright, register_email)

    # sales端提交资料
    sales_login_name = '15318544153'# sales端登录用户，可自定义
    page = context.new_page()
    sales_login(page, sales_login_name)

    # 方法一：自动获取刚注册后的商户id
    page.get_by_role("link", name="ﱖ Merchant ").click()
    page.get_by_role("link", name="Merchant", exact=True).click()
    merchant_id = page.locator('//*[@id="merchant-datatable"]/tbody/tr[1]/td[1]').text_content()
    print(f"刚注册的商户id:{merchant_id}")

    # 方法二：指定merchant_id  如果想指定审核某商户，获取该商户merchant_id后，注释方法一后面的代码
    merchant_id = "010323"
    # sales_setting_sales(page,merchant_id) #设置销售人员
    # sales_submit_info(page,register_email,merchant_id) #提交销售资料

    # # 平台审核
    paylabs_operator_login_name = 'test001@qq.com'# 平台审核登录用户，可自定义
    paylabs_operator_login_name = 'Xander@sitch.paylabs.co.id'# 平台审核登录用户，可自定义
    page2 = context.new_page()
    platform_login(page2, paylabs_operator_login_name)#登录平台
    # platform_risk_control_audit(page2,merchant_id)# 风控审核
    # page2.wait_for_timeout(3000)
    # platform_legal_risk_audit(page2,merchant_id)#法律审核
    platform_request_activation(page2,merchant_id)# 激活请求审核
    platform_activation_audit(page2,merchant_id)# 激活审核


    context.close()
    browser.close()

if __name__ == '__main__':
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    DATA_DIR = os.path.join(BASE_DIR, '..', 'data')
    pdf_file_path = os.path.join(DATA_DIR, "合同.pdf")

    with sync_playwright() as playwright:
        run(playwright)
