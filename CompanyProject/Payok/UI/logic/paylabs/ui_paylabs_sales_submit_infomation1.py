import os
import re
import time

from playwright.sync_api import Playwright, sync_playwright, expect

from CompanyProject.Payok.UI.logic.paylabs.ui_paylabs_merchant_register import paylabs_merchant_register
from CompanyProject.Payok.UI.utils.GoogleSecure import CalGoogleCode
# from CompanyProject.Payok.UI.utils.get_email_code import cookies
from CompanyProject.Payok.UI.utils.perform_slider_unlock import perform_slider_verification
from CompanyProject.Payok.UI.utils.sql_handler import SQLHandler

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, '../..', 'data')
pdf_file_path = os.path.join(DATA_DIR, "合同.pdf")

def generate_google_code(host, port, user, password, database, table_name, login_name):
    db_handler = SQLHandler(host, port, user, password, database)
    db_handler.connect()

    secret_key = db_handler.get_google_secret_key(table_name, login_name)
    if secret_key:
        print("谷歌私钥:", secret_key)
    else:
        print("未发现给定邮箱的记录")
        return None

    db_handler.disconnect()
    try:
        current_time = int(time.time()) // 30
        generated_code = CalGoogleCode.cal_google_code(secret_key, current_time)
        print(f"生成的谷歌验证码: {generated_code}")
        return generated_code
    except ValueError as e:
        print("错误:", e)
        return None

def client_login(page):
    # 客户端登录
    page.goto("http://paylabs-test.com/sales/paylabs-user-login.html")
    # 切换语言
    page.locator("span").filter(has_text="Bahasa").first.click()
    page.get_by_role("link", name="English").click()

    # sales 端登录
    merchant_login_name = '15318544153'
    page.get_by_role("textbox", name="Phone Number").fill(merchant_login_name)
    page.get_by_role("textbox", name="Password").fill("A123456@test")
    # page.get_by_role("textbox", name="Password").fill("Abc@123456789")

    perform_slider_verification(page)
    page.get_by_role("button", name="Login").click()

    paylabs_merchant_google_code = generate_google_code('192.168.0.233', 3306, 'paylabs_payapi', 'SharkZ@DBA666', 'paylabs', 'sales_operator', merchant_login_name)
    page.wait_for_timeout(1000)
    page.get_by_role("textbox", name="Google Verification Code").fill(paylabs_merchant_google_code)

    error_code = page.get_by_role("textbox", name="The Google verification code is incorrect, please reenter")
    if error_code.is_visible():
        page.get_by_role("textbox", name="Kode Verifikasi Google").fill(paylabs_merchant_google_code)
    page.get_by_role("button", name="Login").click()
    print("客户端登录成功")
def client_setting_sales(page):
    '''
    流程中，client_setting_sales按钮在左边，
    page.locator("tbody").filter(has_text="Submit Setting Sales Submit").locator("#btnSetSales").first.click()
    page.locator("tbody").filter(has_text="Submit Setting Sales Submit").locator("#btnSetSales").nth(1).click()
    page.locator("tbody").filter(has_text="Submit Setting Sales Submit").locator("#btnSetSales").nth(2).click()
    page.locator("tr").filter(has_text=re.compile(r"^Setting Sales$")).locator("#btnSetSales").click()
    setting在右边
    page.locator("tbody").filter(has_text="Submit Setting Sales Submit").locator("#btnSetSales").first.click()
    page.get_by_text("Setting Sales").nth(2).click()
    '''
    page.get_by_role("link", name="ﱖ Merchant ").click()
    page.locator("#left-bar-menu").get_by_role("link", name="Merchant", exact=True).click()

    page.locator("tbody").filter(has_text="Setting Sales View Store List").locator("#btnSetSales").first.click()
    # page.get_by_role("textbox", name="Please Choose...").click()
    page.locator('#select2-newSalesManModal-container').click()
    page.get_by_role("treeitem", name="111111").click()
    # page.locator("#select2-newSalesManModal-result-mtyr-920211025155300277").click()
    page.get_by_role("textbox", name="Remarks").fill("1设置sales")
    page.locator("#btnSureSaleModal").click()
    print("销售设置成功")
def client_submit_info(page,email):
    # 开始提交资料
    # with page.expect_popup() as page1_info:
        # page.get_by_text("Submit").nth(2).click()
    page.get_by_role("link", name="ﱖ Merchant ").click()
    page.locator("#left-bar-menu").get_by_role("link", name="Merchant", exact=True).click()


    with page.expect_popup() as page1_info:
        # page.locator("tbody").filter(has_text="Submit Setting Sales View").locator("#btnSubmitInfo").click()
        page.locator("tbody").filter(has_text="Submit Setting Sales View").locator("#btnSubmitInfo").nth(0).click()

    page = page1_info.value
    page.wait_for_timeout(1000)
    page.get_by_role("textbox", name="Company Name *").fill(email)
    page.get_by_role("textbox", name="Company Brand Name").fill(email)
    page.get_by_role("textbox", name="Company Abbreviation").fill("公司缩写")
    page.get_by_label("Types of Companies *").select_option("100")
    page.get_by_role("textbox", name="Official Website *").click()
    # page1.get_by_label("Types of Companies *").select_option("")
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
    
    # 上传文件
    def upload_file(file_path, form_id):
        if not os.path.exists(file_path):
            print(f"文件不存在: {file_path}")
            return
    
        print(f"文件存在: {file_path}")
    
        # 监听 file_chooser 事件
        # with page1.expect_file_chooser() as fc_info:
        #     upload_button.click()
        #
        # # 设置文件路径
        # file_chooser = fc_info.value
        # file_chooser.set_files(file_path)
    
        # 监听 file_chooser 事件
        page.on('filechooser', lambda file_chooser: file_chooser.set_files(file_path))
        page.locator(f"#btnUpload{form_id}").click()
        # page.wait_for_timeout(2000)
    
       # page1.evaluate(f"document.querySelector('#btnUpload{form_id}').click()")
    #
    # # 上传文件
    upload_file(pdf_file_path, "12")
    upload_file(pdf_file_path, "13")
    upload_file(pdf_file_path, "16")
    upload_file(pdf_file_path, "18")
    upload_file(pdf_file_path, "24")
    upload_file(pdf_file_path, "15")
    
    page.get_by_role("heading", name="").locator("i").click()
    page.locator("#select2-selTempsModal-container").click()
    page.get_by_role("treeitem", name="Copy of Bank Account Book").click()
    page.locator("#merFormModal i").click()
    
    #监听 file_chooser 事件
    page.on('filechooser', lambda file_chooser: file_chooser.set_files(pdf_file_path))
    page.locator("#temps-modal").click()
    page.wait_for_timeout(1000)
    page.locator("#btnSureTempModal").click()#id="btnSureTempModal"
    
    # page1.pause()
    # page1.get_by_role("textbox", name="Max 200 characters can be").fill("评论：提交资料完成")
    # page1.wait_for_timeout(1000)
    # # page1.get_by_role("button", name="Comment").click()
    # page1.locator("#btnComment").click()
    # page1.locator("#info-page div").filter(has_text="2025-03-19 14:27:27 test1").nth(2).click()
    page.get_by_text("I declare that the application information submitted by the merchant for").click()
    page.get_by_text("I declare that the above").click()
    
    page.get_by_role("button", name="Save").click()
    
    page.wait_for_timeout(1000)
    # page1.get_by_role("button", name="Submit Review").click()
    page.locator("#btnSubmit").click()
    # page1.get_by_text("OK Processing...").click()
    page.wait_for_timeout(2000)
    # page1.pause()
    page.get_by_role("link", name="I got it").click()
    print("客户端资料提交成功")

    # def upload_file(file_path, form_id):
    #     if not os.path.exists(file_path):
    #         print(f"文件不存在: {file_path}")
    #         return

    #     print(f"文件存在: {file_path}")
    #     page.on('filechooser', lambda file_chooser: file_chooser.set_files(file_path))
    #     page.locator(f"#btnUpload{form_id}").click()
    #     page.wait_for_timeout(2000)

    # # 上传文件
    # upload_file(pdf_file_path, "12")
    # upload_file(pdf_file_path, "13")
    # # ...

    # page.get_by_text("I declare that the application information submitted by the merchant for").click()
    # page.get_by_text("I declare that the above").click()

    # page.get_by_role("button", name="Save").click()
    # page.wait_for_timeout(1000)
    # page.locator("#btnSubmit").click()
    # page.wait_for_timeout(2000)
    # page.get_by_role("link", name="I got it").click()

def platform_login(page):
    # 平台登录
    page.goto("http://paylabs-test.com/platform/paylabs-user-login.html")
    page.locator("span").filter(has_text="Bahasa").first.click()
    page.get_by_role("link", name="English").click()

    # 登录
    paylabs_operator_login_name = 'test001@qq.com'
    page.get_by_role("textbox", name="E-mail").fill(paylabs_operator_login_name)
    page.get_by_role("textbox", name="Password Verification Code").fill("Abc@123456789")

    perform_slider_verification(page)
    page.get_by_role("button", name=" Login").click()
    # page.pause()
    # 如果有弹窗，点确定
    page.get_by_role("button", name="Confirm").click()
    paylabs_platform_google_code = generate_google_code('192.168.0.233', 3306, 'paylabs_payapi', 'SharkZ@DBA666', 'paylabs', 'operator', paylabs_operator_login_name)
    page.get_by_role("textbox", name="Google Verification Code").fill(paylabs_platform_google_code)

    error_code = page.get_by_role("textbox", name="The Google verification code is incorrect, please reenter")
    if error_code.is_visible():
        page.get_by_role("textbox", name="Google Verification Code").fill(paylabs_platform_google_code)

    page.get_by_role("button", name="Submit").click()
    print("平台端登录成功")

def platform_risk_audit(page):
    # 开始风险审核
    page.get_by_role("link", name=" Risk Control ").click()
    page.get_by_role("link", name="Risk Control", exact=True).click()
    # page.pause()
    # page.locator(".DTFC_RightBodyLiner > .table > tbody > tr:nth-child(3) > td > .mb-2 > .btnAudit").click()

    page.locator(".DTFC_RightBodyLiner > .table > tbody > tr > td > .mb-2 > .btnAudit").first.click()

    page.get_by_role("textbox", name="Max 200 characters can be").fill("评论：风险控制审计通过")
    page.locator("#toRiskAudit").click()

    page.get_by_role("link", name="None").click()

    # 上传风控报告
    page.on('filechooser', lambda file_chooser: file_chooser.set_files(pdf_file_path))
    page.locator("#reportForm1").click()

    page.get_by_role("textbox", name="Max 200 characters can be").fill("评论：风控报告上传成功，风险控制审计通过2")
    page.get_by_role("button", name="Approve").click()
    # page2.get_by_role("button", name="Approve").click()
    print("风险审核通过")

def platform_legal_risk_audit(page):
    # 法律风控
    page.get_by_role("link", name="ﶇ Merchant ").click()
    page.get_by_role("link", name="Merchant List").click()

    # page.pause()
    # page.locator("tbody").filter(
    #     has_text="DataConfiguration Status Store List System ConfigurationDataSystem").locator(
    #     "button[name=\"btnLagelCheck\"]").click()
    ##merchant-datatable_wrapper > div:nth-child(2) > div > div.DTFC_ScrollWrapper > div.DTFC_RightWrapper > div.DTFC_RightBodyWrapper > div > table > tbody > tr:nth-child(3) > td > div > button.btn.btn-blue.font-12.mr-1.w-53
    #//*[@id="merchant-datatable_wrapper"]/div[2]/div/div[1]/div[3]/div[2]/div/table/tbody/tr[3]/td/div/button[1]
    # page.locator("tbody").filter(
    #     has_text="DataConfiguration Status Store List System ConfigurationDataConfiguration").locator(
    #     "button[name=\"btnLagelCheck\"]").click()
    page.get_by_text("Legal Audit", exact=True).nth(1).click()

    page.on('filechooser', lambda file_chooser: file_chooser.set_files(pdf_file_path))
    page.locator("#reportForm2").click()
    page.on('filechooser', lambda file_chooser: file_chooser.set_files(pdf_file_path))
    page.locator("#reportForm3").click()

    # page.get_by_role("textbox", name="Max 200 characters can be").fill("评论：商户列表-法律审核通过")
    # page.get_by_role("button", name="Comment").click()

    page.get_by_role("button", name="Approve").click()
    # page.pause()
    page.wait_for_timeout(1000)
    # page.locator("#btnCancel2").click()
    page.locator("#btnSurePass").click()

    # page.locator("#btnSubmitSure").click()
    print("法律风控审核通过")

def platform_activation_request(page):
    # 激活请求
    page.get_by_role("link", name="ﶇ Merchant ").click()
    page.get_by_role("link", name="Merchant List").click()

    # page.locator("button[name=\"btnOnlineApply\"]").nth(2).click()
    page.locator("tbody").filter(
        has_text="DataRequest ActivationSystem ConfigurationDataConfiguration Status Store List").locator(
        "button[name=\"btnOnlineApply\"]").click()

    # page.get_by_role("button", name="H5 Display").click()
    page.locator("#nav_1 div").filter(has_text="DanamonVA Settlement Type").get_by_role("button").click()
    page.get_by_role("listitem").filter(has_text="Danamon Paylabs").locator("label").first.click()
    # page.locator("#nav_1 div").filter(has_text="DanamonVA Settlement Type").get_by_role("button").click()
    page.locator("#rate232").fill("5")
    page.locator("#fee232").fill('5000')
    page.locator("#transSharingRate232").fill("0")
    page.locator("#transSharingFee232").fill("0")
    # page.locator("#merVatSel1242").select_option("0")
    page.get_by_role("listitem").filter(has_text="Danamon Paylabs").locator("select[name=\"selMerVat\"]").select_option(
        "0.11")

    page.get_by_role("cell", name="Non-active").locator("label").click()
    page.get_by_role("cell", name="Active").get_by_role("list").click()

    # page.pause()
    page.get_by_role("button", name="Select all").click()
    # page.pause()
    page.get_by_role("cell", name="Merchant Cost ").click()
    # page.locator("button[name=\"btnSelectCancel\"]").click()
    page.get_by_role("cell", name="*Merchant Fee % Sample:0.7000").get_by_role("textbox").first.fill("4")
    page.get_by_role("textbox", name="1000").fill("4000")
    page.get_by_role("cell", name="*Merchant Fee 4 % Sample:0.").get_by_role("combobox").select_option("0.11")
    page.get_by_role("textbox", name="Merchant RSA Public Key").fill("123456789")

    # page.get_by_role("listitem").filter(has_text="Danamon Paylabs").locator("select[name=\"selMerVat\"]").select_option("0.11")
    # page.get_by_role("link", name="E-Money/Wallet").click()
    # page.get_by_role("listitem").filter(has_text="DANA Paylabs").locator("label").first.click()
    # page.locator("#nav_2 div").filter(has_text="DANABALANCE Settlement Type").get_by_role("button").click()
    # page.get_by_role("listitem").filter(has_text="DANA Paylabs").locator("select[name=\"selMerVat\"]").select_option("0.11")
    # page.get_by_role("link", name="CreditCard").click()
    # page.locator("#nav_3 > li > .form-row > div > .form-d-flex > .w-70-px > .pr-4").first.click()
    # page.locator("#nav_3 > li > .form-row > div:nth-child(3) > div > div:nth-child(5)").first.click()
    # page.locator("#nav_3 div").filter(has_text="CIMBCC Settlement Type").get_by_role("button").click()
    # page.get_by_role("link", name="QRIS", exact=True).click()
    # page.locator("#nav_4 div").filter(has_text="StaticQRIS Settlement Type").get_by_role("button").click()
    # page.locator("#nav_4 > li > .form-row > div > .form-d-flex > .w-70-px > .pr-4").first.click()
    # page.locator("#rate1231").fill("0.0001")
    # page.locator("#transSharingRate1231").fill("0.0001")
    # page.get_by_role("link", name="Payin Cash Outlet").click()
    # page.get_by_role("listitem").filter(has_text="POS Paylabs SettlementChannel").locator("label").first.click()
    # page.locator("#rate1239").fill("0.0001")
    # page.locator("#transSharingRate1239").fill("0.0001")
    # page.get_by_role("button", name="H5 Hidden").click()
    # page.get_by_role("link", name="CardlessCredit").click()
    # page.locator("#nav_6 div").filter(has_text="Indodana Settlement Type").get_by_role("button").click()
    # page.get_by_role("listitem").filter(has_text="TestBankVA Paylabs").locator("label").first.click()
    # page.locator("#transSharingRate1218").fill("0.0001")
    # page.get_by_role("cell", name="Non-active").locator("label").click()
    # page.get_by_role("cell", name="Active").get_by_role("list").click()
    # page.get_by_role("button", name="Select all").click()
    # page.locator("button[name=\"btnSelectCancel\"]").click()
    # page.get_by_role("cell", name="Active").get_by_role("list").click()
    # page.get_by_role("treeitem", name="BANK BNI", exact=True).locator("span").click()
    # page.get_by_role("cell", name="*Merchant Fee % Sample:0.7000").get_by_role("textbox").first.fill("0.01")
    # page.get_by_role("textbox", name="1000").fill("0.05")
    # page.get_by_role("textbox", name="Not involved in profit sharing").click()
    # page.get_by_role("treeitem", name="test-S -").click()
    # page.locator("#btnConfirm").click()
    # page.get_by_role("textbox", name="111111").click()
    # page.locator("#select2-agentMans-container").click()
    # page.get_by_role("treeitem", name="[667665] - dgadfag").click()
    # page.get_by_role("textbox", name="Choose...").click()
    # page.get_by_role("treeitem", name="test-A -").click()
    # page.locator("#btnConfirm").click()
    # page2.get_by_role("textbox", name="Max 200 characters can be").fill("request 审核通过")
    # page2.get_by_role("button", name="Comment").click()
    # page.pause()
    page.get_by_role("button", name="Submit Request").click()
    print("激活请求提交成功")

def platform_activation_audit(page):
    # 激活审核
    page.get_by_role("link", name="ﶇ Merchant ").click()
    page.get_by_role("link", name="Merchant List").click()

    page.locator("tr").filter(has_text=re.compile(r"^DataActivation AuditSystem Configuration$")).locator("button[name=\"btnOnlineApply\"]").click()
    page.get_by_role("textbox", name="Max 200 characters can be").fill("评论：激活审核通过")
    # page.pause()
    # page.get_by_role("button", name="Comment").click()#不能评论？
    page.get_by_role("button", name="Passed").click()
    print("激活审核通过")
    # expect(page.locator("#merchant-datatable")).to_match_aria_snapshot("- text: Active")
    print("商户入驻成功！")

def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()

    #商户注册
    email = "paylabs8@test.com"
    # paylabs_merchant_register(playwright, email)
    # 客户端操作
    page = context.new_page()
    client_login(page)
    client_setting_sales(page)
    client_submit_info(page,email)

    # 平台操作
    page2 = context.new_page()
    platform_login(page2)
    platform_risk_audit(page2)# 风控审核
    page2.wait_for_timeout(3000)
    platform_legal_risk_audit(page2)#法律风控审核

    platform_activation_request(page2)# 激活请求审核
    platform_activation_audit(page2)# 激活审核

    context.close()
    browser.close()

with sync_playwright() as playwright:
    run(playwright)
