import os
import re
import time

from playwright.sync_api import Playwright, sync_playwright, expect

from CompanyProject.Payok.UI.utils.GoogleSecure import CalGoogleCode
from CompanyProject.Payok.UI.utils.get_email_code import cookies
from CompanyProject.Payok.UI.utils.perform_slider_unlock import perform_slider_verification
from CompanyProject.Payok.UI.utils.sql_handler import SQLHandler


def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()

    # cookies
    cookies = context.cookies()
    for cookie in cookies:
        if cookie['name'] == 'paylabs_session':
            session_cookie = cookie['value']
            print("session_cookie:", session_cookie)
            break

    #客户端-提交资料
    # page = context.new_page()
    # page.goto("http://paylabs-test.com/sales/paylabs-user-login.html")
    # #切换语言
    # page.locator("span").filter(has_text="Bahasa").first.click()
    # page.get_by_role("link", name="English").click()
    #
    # merchant_login_name = '15318544152'
    # page.get_by_role("textbox", name="Phone Number").fill(merchant_login_name)
    # page.get_by_role("textbox", name="Password").fill("A123456@test")
    #
    # perform_slider_verification(page)
    # page.get_by_role("button", name="Login").click()
    #
    # #如果出现了验证码错误提示，则重新输入验证码
    # # max_retries = 3
    # # retries = 0
    # # while retries < max_retries:
    # paylabs_merchant_google_code = generate_google_code('192.168.0.233', 3306, 'paylabs_payapi', 'SharkZ@DBA666', 'paylabs','sales_operator', merchant_login_name)
    # page.wait_for_timeout(1000)
    # page.get_by_role("textbox", name="Google Verification Code").fill(paylabs_merchant_google_code)
    #
    # # error_code  = page.get_by_role("textbox", name="Kode verifikasi Google salah, silakan masuk kembali")#.get_by_role("paragraph")
    # error_code  = page.get_by_role("textbox", name="The Google verification code is incorrect, please reenter")#.get_by_role("paragraph")
    # # error_code = page.get_by_role("paragraph").to_contain_text("Kode verifikasi Google salah, silakan masuk kembali")
    # if error_code.is_visible():
    #     page.get_by_role("textbox", name="Kode Verifikasi Google").fill(paylabs_merchant_google_code)
    # page.get_by_role("button", name="Login").click()
    # # page.get_by_text("Kode verifikasi Google salah").click()
    # # page.pause()
    # # page.get_by_role("textbox", name="Kode Verifikasi Google").fill("379881")
    # # page.get_by_role("button", name="Login").click()
    #
    # # 登录后
    # # page.get_by_role("button", name="user-image Bahasa ").click()
    # # page.get_by_role("link", name="user-image English").click()
    #
    # # page.get_by_role("link", name="ﱖ Merchant ").click()
    # # page.get_by_role("link", name="Merchant", exact=True).click()
    # page.get_by_role("link", name="ﱖ Merchant ").click()
    # page.locator("#left-bar-menu").get_by_role("link", name="Merchant", exact=True).click()
    #
    # page.pause()#如果没有 sales要补充setting sales
    # # page.locator("tbody").filter(has_text="Setting Sales View Store List").locator("#btnSetSales").first.click()
    # # # page.get_by_role("textbox", name="Please Choose...").click()
    # # page.locator('#select2-newSalesManModal-container').click()
    # # page.locator("#select2-newSalesManModal-result-mtyr-920211025155300277").click()
    # # # page.get_by_role("textbox", name="Remarks").click()
    # # # page.get_by_role("textbox", name="Remarks").fill("sales")
    # # # page.get_by_role("textbox", name="Remarks").press("Home")
    # # # page.get_by_role("textbox", name="Remarks").fill("设置sales")
    # # page.get_by_role("textbox", name="Remarks").press("Home")
    # # page.get_by_role("textbox", name="Remarks").fill("1设置sales")
    # # page.locator("#btnSureSaleModal").click()
    #
    # # page.get_by_role("gridcell", name="010387").click()
    # with page.expect_popup() as page1_info:
    #     # page.get_by_text("Submit").nth(2).click()
    #     page.locator("tbody").filter(has_text="Submit Setting Sales View").locator("#btnSubmitInfo").nth(1).click()
    # page1 = page1_info.value
    # page.wait_for_timeout(1000)
    # page1.get_by_role("textbox", name="Company Name *").fill("paylabs1@test.com公司名称1")
    # page1.get_by_role("textbox", name="Company Brand Name").fill("公司品牌名称")
    # page1.get_by_role("textbox", name="Company Abbreviation").fill("公司缩写")
    # page1.get_by_label("Types of Companies *").select_option("100")
    # page1.get_by_role("textbox", name="Official Website *").click()
    # # page1.get_by_label("Types of Companies *").select_option("")
    # page1.get_by_label("Types of Companies *").select_option("105")
    # # page1.get_by_label("Types of Companies *").select_option("100")
    # page1.get_by_role("textbox", name="Official Website *").fill("http://paylabs-test.com/sales/paylabs-merchant-info.html?k=1bdd7098b1cebd36e3d4be0028b9a7c3")
    # page1.get_by_role("textbox", name="Company Address *").fill("广东省深圳市南山区桃源街道中广时代广场001")
    # page1.get_by_role("textbox", name="PIC Name *").fill("PIC名称")
    # page1.get_by_role("textbox", name="PIC Contact Number *").fill("123456789")
    # page1.get_by_role("textbox", name="PIC Email *").fill("1@qq.com")
    # # page1.get_by_role("textbox", name="Company Address *").press("ControlOrMeta+a")
    # # page1.get_by_role("textbox", name="Company Address *").press("ControlOrMeta+c")
    # page1.get_by_role("textbox", name="PIC Address").fill("广东省深圳市南山区桃源街道中广时代广场001")
    # # page1.get_by_role("textbox", name="Choose...").click()
    # page1.locator("#select2-merchantType-container").click()
    # # page1.get_by_role("combobox", name="Choose...").locator("span").nth(1).click()
    # page1.get_by_role("treeitem", name="Advertising").click()
    # # page1.get_by_role("combobox", name="Advertising").locator("span").nth(1).click()
    # page1.get_by_role("textbox", name="Default Amount Range (Upper").fill("100")
    # page1.get_by_role("textbox", name="Default Amount Range", exact=True).fill("1000")
    # page1.get_by_role("textbox", name="Default Transaction Range (").fill("2147")
    # page1.get_by_role("textbox", name="Default Transaction Range", exact=True).fill("3000")
    # page1.get_by_role("textbox", name="Default Income Range (Upper").fill("100")
    # page1.get_by_role("textbox", name="Default Income Range", exact=True).fill("1000")
    # page1.get_by_role("textbox", name="##.###.###.#-###.###").fill("00.000.000.0-000.000")
    # page1.locator("#checkNPWP").click()
    # page1.get_by_role("textbox", name="LawanTransaksiID").fill("13546512456")
    # page1.get_by_role("textbox", name="NIK").fill("124")
    # page1.locator("#checkNIK").click()
    # page1.get_by_role("textbox", name="Account Number *").fill("15354879")
    # page1.get_by_role("textbox", name="Account Name *").fill("账户名称")
    # page1.get_by_role("textbox", name="Bank Name *").fill("中国人民银行")
    # page1.get_by_role("textbox", name="SWIFT Code *").fill("1236547")
    # page1.get_by_role("textbox", name="Business Contact *").fill("商务联系人")
    # page1.get_by_role("textbox", name="Technical Contact *").fill("技术联系人")
    # page1.get_by_role("textbox", name="Technical Contact Number *").fill("15318544154")
    # page1.get_by_role("textbox", name="Technical Contact Email *").fill("1@qq.com")
    # page1.get_by_role("textbox", name="Finance Contact *").fill("财务联系人")
    # page1.get_by_role("textbox", name="Finance Contact Number *").fill("15318544154")
    # # page1.get_by_role("textbox", name="##.###.###.#-###.###").press("ControlOrMeta+a")
    # # page1.get_by_role("textbox", name="##.###.###.#-###.###").fill("948409438036000")
    # # page1.get_by_role("button", name="Verification").click()
    # page1.get_by_role("textbox", name="Business Contact Number *").fill("15318544154")
    # page1.get_by_role("textbox", name="Business Contact Email *").fill("1@qq.com")
    # page1.get_by_role("textbox", name="Finance Contact Email *").fill("1@qq.com")
    # page1.get_by_role("textbox", name="CS Contact", exact=True).fill("CS联系人")
    # page1.get_by_role("textbox", name="CS Contact Number").fill("15318544154")
    # page1.get_by_role("textbox", name="CS Contact Email").fill("1@qq.com")
    #
    # # 上传文件
    # def upload_file(file_path, form_id):
    #     if not os.path.exists(file_path):
    #         print(f"文件不存在: {file_path}")
    #         return
    #
    #     print(f"文件存在: {file_path}")
    #
    #     # 监听 file_chooser 事件
    #     # with page1.expect_file_chooser() as fc_info:
    #     #     upload_button.click()
    #     #
    #     # # 设置文件路径
    #     # file_chooser = fc_info.value
    #     # file_chooser.set_files(file_path)
    #
    #     # 监听 file_chooser 事件
    #     page1.on('filechooser', lambda file_chooser: file_chooser.set_files(file_path))
    #
    #     page1.locator(f"#btnUpload{form_id}").click()
    #     page1.wait_for_timeout(2000)
    #
    #    # page1.evaluate(f"document.querySelector('#btnUpload{form_id}').click()")
    #
    # # 上传文件
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    DATA_DIR = os.path.join(BASE_DIR, '../..', 'data')
    pdf_file_path = os.path.join(DATA_DIR, "合同.pdf")
    #
    # upload_file(pdf_file_path, "12")
    # upload_file(pdf_file_path, "13")
    # upload_file(pdf_file_path, "16")
    # upload_file(pdf_file_path, "18")
    # upload_file(pdf_file_path, "24")
    # upload_file(pdf_file_path, "15")
    #
    # # page1.pause()
    # page1.get_by_role("heading", name="").locator("i").click()
    # # page1.get_by_role("textbox", name="Business License").click()
    # page1.locator("#select2-selTempsModal-container").click()
    # # page1.pause()
    # page1.get_by_role("treeitem", name="Copy of Bank Account Book").click()
    # page1.locator("#merFormModal i").click()
    #
    # #监听 file_chooser 事件
    # page1.on('filechooser', lambda file_chooser: file_chooser.set_files(pdf_file_path))
    # page1.locator("#temps-modal").click()
    # page1.wait_for_timeout(1000)
    # # page1.get_by_role("button", name="Upload").click()#id="btnSureTempModal"
    # page1.locator("#btnSureTempModal").click()#id="btnSureTempModal"
    #
    # # page1.pause()
    # # page1.get_by_role("textbox", name="Max 200 characters can be").fill("评论：可以通过")
    # # page1.wait_for_timeout(1000)
    # # # page1.get_by_role("button", name="Comment").click()
    # # page1.locator("#btnComment").click()
    # # page1.locator("#info-page div").filter(has_text="2025-03-19 14:27:27 test1").nth(2).click()
    # page1.get_by_text("I declare that the application information submitted by the merchant for").click()
    # page1.get_by_text("I declare that the above").click()
    #
    # page1.get_by_role("button", name="Save").click()
    #
    # page1.wait_for_timeout(1000)
    # # page1.get_by_role("button", name="Submit Review").click()
    # page1.locator("#btnSubmit").click()
    # # page1.get_by_text("OK Processing...").click()
    # page1.wait_for_timeout(2000)
    # # page1.pause()
    # page1.get_by_role("link", name="I got it").click()


    # 平台-审核
    page2 = context.new_page()
    page2.goto("http://paylabs-test.com/platform/paylabs-user-login.html")
    page2.locator("span").filter(has_text="Bahasa").first.click()
    page2.get_by_role("link", name="English").click()

    paylabs_operator_login_name = 'test001@qq.com'
    page2.get_by_role("textbox", name="E-mail").fill(paylabs_operator_login_name)
    page2.get_by_role("textbox", name="Password Verification Code").fill("Abc@123456789")

    perform_slider_verification(page2)
    page2.get_by_role("button", name=" Login").click()
    # page2.get_by_role("button", name="Confirm").click()
    paylabs_platform_google_code = generate_google_code('192.168.0.233', 3306, 'paylabs_payapi', 'SharkZ@DBA666', 'paylabs','operator', paylabs_operator_login_name)
    # page.wait_for_timeout(1000)
    page2.get_by_role("textbox", name="Google Verification Code").fill(paylabs_platform_google_code)
    page2.get_by_role("button", name="Submit").click()

    error_code = page2.get_by_role("textbox",
                                  name="The Google verification code is incorrect, please reenter")  # .get_by_role("paragraph")
    # error_code = page.get_by_role("paragraph").to_contain_text("Kode verifikasi Google salah, silakan masuk kembali")
    if error_code.is_visible():
        page2.get_by_role("textbox", name="Google Verification Code").fill(paylabs_platform_google_code)
        page2.get_by_role("button", name="Submit").click()


    # 风险控制
    # page2.get_by_role("link", name=" Risk Control ").click()
    # page2.get_by_role("link", name="Risk Control", exact=True).click()
    #
    # page2.get_by_role("gridcell", name="010388").click()

    # page2.locator(".DTFC_RightBodyLiner > .table > tbody > tr:nth-child(5) > td > .mb-2 > .btnAudit").click()
    # page2.get_by_role("dialog", name="Merchant Information").click()
    # page2.get_by_role("dialog", name="Merchant Information").locator("#btnCancel").click()
    # page2.locator("div").filter(has_text="English Bahasa English Clear").nth(1).click()

    # page2.locator(".DTFC_RightBodyLiner > .table > tbody > tr:nth-child(5) > td > .mb-2 > .btnAudit").click()
                # page2.locator(".DTFC_RightBodyLiner > .table > tbody > tr:nth-child(5) > td > .mb-2 > .watchDetail").click()
    # page2.get_by_role("textbox", name="Max 200 characters can be").click()


    # page2.get_by_role("textbox", name="Max 200 characters can be").fill("通过")
    # page2.get_by_role("textbox", name="Max 200 characters can be").press("Home")
    # page2.get_by_role("textbox", name="Max 200 characters can be").fill("审核通过")
    # page2.get_by_role("textbox", name="Max 200 characters can be").press("Home")
    # page2.get_by_role("textbox", name="Max 200 characters can be").fill("初审风控审核通过")
    # page2.get_by_role("button", name="Comment").click()
    # page2.locator("#toRiskAudit").click()
    # page2.get_by_role("dialog", name="Merchant Information").locator("label").first.click()
    # page2.locator("#btnOpenTransConfirm").click()
    # page2.get_by_role("dialog", name="Merchant Information").locator("label").nth(1).click()
    # page2.locator("#btnOpenTransConfirm").click()
    # page2.get_by_role("dialog", name="Merchant Information").locator("label").nth(2).click()
    # page2.locator("#btnOpenTransConfirm").click()
    # page2.get_by_role("dialog", name="Merchant Information").locator("label").nth(3).click()
    # page2.locator("#btnOpenTransConfirm").click()
    # page2.get_by_role("dialog", name="Merchant Information").locator("label").nth(4).click()
    # page2.locator("#btnOpenTransConfirm").click()
    # page2.get_by_role("link", name="None").click()

    #上传风控报告
    # page2.on('filechooser', lambda file_chooser: file_chooser.set_files(pdf_file_path))
    # # page2.locator("#reportForm1 div").filter(has_text="File Upload").click()
    # page2.locator("#reportForm1").click()
    #
    # # page2.get_by_role("dialog", name="Merchant Information").set_input_files("合同.pdf")
    # page2.get_by_role("textbox", name="Max 200 characters can be").fill("风控审核通过1")
    # # page2.get_by_role("button", name="Comment").click()#可能点击不了
    # page2.get_by_role("button", name="Approve").click()
    # page2.locator("#btnSubmitSure").click()
    # page2.locator("#btnSubmitCancel").click()
    # page2.get_by_role("dialog", name="Merchant Information").locator("label").first.click()
    # page2.locator("#btnCloseTransConfirm").click()
    # page2.get_by_role("dialog", name="Merchant Information").locator("label").nth(1).click()
    # page2.locator("#btnCloseTransConfirm").click()
    page2.get_by_role("link", name="ﶇ Merchant ").click()
    page2.get_by_role("link", name="Merchant List").click()
    page2.locator("tbody").filter(has_text="DataConfiguration Status Store List System ConfigurationDataSystem").locator("button[name=\"btnLagelCheck\"]").click()

    page2.on('filechooser', lambda file_chooser: file_chooser.set_files(pdf_file_path))
    page2.locator("#reportForm2").click()
    # page2.get_by_role("dialog", name="Merchant Status Change").set_input_files("合同.pdf")
    page2.on('filechooser', lambda file_chooser: file_chooser.set_files(pdf_file_path))
    page2.locator("#reportForm3").click()
    # page2.get_by_role("dialog", name="Merchant Status Change").set_input_files("合同.pdf")
    # page2.get_by_role("textbox", name="Max 200 characters can be").fill("法律风控审核通过")
    # page2.get_by_role("button", name="Comment").click()
    page2.get_by_role("button", name="Approve").click()
    page2.locator("#btnSurePass").click()


    page2.pause()
    #激活请求
    page2.wait_for_timeout(1000)
    page2.locator("button[name=\"btnOnlineApply\"]").nth(2).click()
    page2.get_by_role("listitem").filter(has_text="Danamon Paylabs").locator("label").first.click()
    page2.locator("#nav_1 div").filter(has_text="DanamonVA Settlement Type").get_by_role("button").click()
    page2.locator("#rate232").fill("0.0001")
    page2.locator("#transSharingRate232").fill("0.0001")
    page2.get_by_role("listitem").filter(has_text="Danamon Paylabs").locator("select[name=\"selMerVat\"]").select_option("0.11")
    page2.get_by_role("link", name="E-Money/Wallet").click()
    page2.get_by_role("listitem").filter(has_text="DANA Paylabs").locator("label").first.click()
    page2.locator("#nav_2 div").filter(has_text="DANABALANCE Settlement Type").get_by_role("button").click()
    page2.locator("#transSharingRate233").fill("0.0001")
    page2.get_by_role("listitem").filter(has_text="DANA Paylabs").locator("select[name=\"selMerVat\"]").select_option("0.11")
    page2.get_by_role("link", name="CreditCard").click()
    page2.locator("#nav_3 > li > .form-row > div > .form-d-flex > .w-70-px > .pr-4").first.click()
    page2.locator("#transSharingRate1242").fill("0.0001")
    page2.locator("#nav_3 > li > .form-row > div:nth-child(3) > div > div:nth-child(5)").first.click()
    page2.locator("#merVatSel1242").select_option("0.11")
    page2.locator("#nav_3 div").filter(has_text="CIMBCC Settlement Type").get_by_role("button").click()
    page2.get_by_role("link", name="QRIS", exact=True).click()
    page2.locator("#nav_4 div").filter(has_text="StaticQRIS Settlement Type").get_by_role("button").click()
    page2.locator("#nav_4 > li > .form-row > div > .form-d-flex > .w-70-px > .pr-4").first.click()
    page2.locator("#rate1231").fill("0.0001")
    page2.locator("#transSharingRate1231").fill("0.0001")
    page2.get_by_role("link", name="Payin Cash Outlet").click()
    page2.get_by_role("listitem").filter(has_text="POS Paylabs SettlementChannel").locator("label").first.click()
    page2.locator("#rate1239").fill("0.0001")
    page2.locator("#transSharingRate1239").fill("0.0001")
    page2.get_by_role("button", name="H5 Hidden").click()
    page2.get_by_role("link", name="CardlessCredit").click()
    page2.locator("#nav_6 div").filter(has_text="Indodana Settlement Type").get_by_role("button").click()
    page2.get_by_role("listitem").filter(has_text="TestBankVA Paylabs").locator("label").first.click()
    page2.locator("#transSharingRate1218").fill("0.0001")
    page2.get_by_role("cell", name="Non-active").locator("label").click()
    page2.get_by_role("cell", name="Active").get_by_role("list").click()
    page2.get_by_role("button", name="Select all").click()
    page2.locator("button[name=\"btnSelectCancel\"]").click()
    page2.get_by_role("cell", name="Active").get_by_role("list").click()
    page2.get_by_role("treeitem", name="BANK BNI", exact=True).locator("span").click()
    page2.get_by_role("cell", name="*Merchant Fee % Sample:0.7000").get_by_role("textbox").first.fill("0.01")
    page2.get_by_role("textbox", name="1000").fill("0.05")
    page2.get_by_role("textbox", name="Not involved in profit sharing").click()
    page2.get_by_role("treeitem", name="test-S -").click()
    page2.locator("#btnConfirm").click()
    page2.get_by_role("textbox", name="111111").click()
    page2.locator("#select2-agentMans-container").click()
    page2.get_by_role("treeitem", name="[667665] - dgadfag").click()
    page2.get_by_role("textbox", name="Choose...").click()
    page2.get_by_role("treeitem", name="test-A -").click()
    page2.locator("#btnConfirm").click()
    # page2.get_by_role("textbox", name="Max 200 characters can be").fill("request 审核通过")
    # page2.get_by_role("button", name="Comment").click()
    page2.get_by_role("button", name="Submit Request").click()
    page2.get_by_role("link", name="Bank").click()
    page2.get_by_role("link", name=" Risk Control ").click()
    page2.get_by_role("link", name="Risk Control", exact=True).click()
    page2.locator("tr").filter(has_text=re.compile(r"^DataActivation AuditSystem Configuration$")).locator("button[name=\"btnOnlineApply\"]").click()
    page2.get_by_role("textbox", name="Max 200 characters can be").fill("activation审核通过")
    page2.get_by_role("button", name="Passed").click()
    page2.get_by_role("button", name="Comment").click()
    # page3.locator("#checkNPWP").click()

    # ---------------------
    context.close()
    browser.close()

def generate_google_code(host, port, user, password, database, table_name, login_name):
    # db_handler = SQLHandler('192.168.0.233', 3306, 'paylabs_payapi', 'SharkZ@DBA666', 'paylabs')
    db_handler = SQLHandler(host, port, user, password, database)
    db_handler.connect()

    # secret_key = db_handler.get_google_secret_key('sales_operator', '15318544152')
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

# generate_google_code()
with sync_playwright() as playwright:
    run(playwright)
