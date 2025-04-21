import re
from os.path import exists

from playwright.sync_api import Playwright, sync_playwright, expect

from CompanyProject.Payok.UI.utils.get_email_code import get_email_code


def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("http://payok-test.com/merchant/payok-register-register.html")
    page.get_by_role("textbox", name="Company Name *").fill("公司名称")
    page.get_by_role("textbox", name="Company Name *").fill("Payok公司名称")
    page.get_by_role("textbox", name="Taxpayer Number *").fill("纳税人号码")
    page.get_by_role("textbox", name="Company Brand Name").fill("公司品牌名")
    page.get_by_role("textbox", name="Company Abbreviation").fill("公司东方闪电")
    page.locator("#select2-companyLocationType-container").click()
    page.get_by_role("treeitem", name="Indonesia Local Company").click()
    page.get_by_role("textbox", name="Official Website *").fill("www.baidu.com")
    page.get_by_role("textbox", name="Company Address *").fill("深圳市宝安区烦死了地方撒发大水")
    page.get_by_role("textbox", name="Corporate Legal Person (").fill("公司法人")
    page.get_by_role("textbox", name="Legal Person Contact Number *").fill("15318544154")
    page.get_by_role("textbox", name="Email of Legal Person *").fill("1@linshiyou.com")
    page.get_by_role("textbox", name="Address of Legal Person Type").fill("法人地址")
    page.get_by_role("textbox", name="Choose").click()
    page.get_by_role("treeitem", name="Live Streaming").click()
    page.get_by_role("textbox", name="Please enter").fill("直播")
    page.get_by_role("textbox", name="Amount Range *").fill("1")
    page.get_by_role("textbox", name="The Maximum Amount Per").fill("6")
    page.get_by_role("button", name="Next").click()
    page.get_by_role("textbox", name="Business Contact *").fill("15318544154")
    page.get_by_role("textbox", name="Business Contact Number *").fill("15318544154")
    page.get_by_role("textbox", name="Business Contact Email *").fill("1@linshiyou.com")
    page.get_by_role("textbox", name="Technical Contact *").fill("15318544154")
    page.get_by_role("textbox", name="Technical Contact Number *").fill("15318544154")
    page.get_by_role("textbox", name="Technical Contact Email *").fill("1@linshiyou.com")
    page.get_by_role("textbox", name="Technical Contact Number *").fill("15318544154")

    page.get_by_role("button", name="Next").click()
    page.get_by_role("textbox", name="Account Number *").fill("1531854415415318544154")
    page.get_by_role("textbox", name="Account Name *").fill("15318544154")
    page.get_by_role("textbox", name="Bank Name *").fill("银行名称")
    page.get_by_role("textbox", name="Choose").click()
    page.get_by_role("treeitem", name="By Corporate").click()
    page.get_by_role("textbox", name="SWIFT Code *").fill("第三方第三发所发生的")
    page.get_by_role("textbox", name="Secure Email for fund account").fill("1@linshiyou.com")
    page.get_by_role("button", name="Next").click()

    filepath = "../../data/合同.pdf"
    if filepath is None or not exists(filepath):
        print("文件不存在")
        exit(1)
    page.on("filechooser", lambda f: f.set_files(filepath))
    page.locator("#form1").click()
    page.on("filechooser", lambda f: f.set_files(filepath))
    page.locator("#form2").click()
    page.on("filechooser", lambda f: f.set_files(filepath))
    page.locator("#form3").click()


    page.get_by_role("button", name=" Add a row").click()
    page.get_by_role("combobox", name="Please Choose").locator("span").nth(1).click()
    page.get_by_role("treeitem", name="H5").click()
    page.get_by_role("textbox", name="Registration Address").fill("www.baidu.com")
    page.get_by_role("textbox", name="Test Account", exact=True).fill("托尔斯泰")
    page.get_by_role("textbox", name="Test Account Password").fill("A123456@test")
    page.get_by_role("button", name="Next").click()

    page.locator("span").filter(has_text=re.compile(r"^Indonesia$")).click()
    page.get_by_role("link", name="Indonesia").click()
    page.get_by_role("textbox", name="E-mail *").fill("9@linshiyou.com")
    page.get_by_role("button", name="Send the verification code").click()
    page.pause()
    '''复制粘贴：
            cd /data/logs/tomcat/merchart
            grep "发邮件结束 getVerificationCode 登录邮箱" *
            '''
    # get_email_code(playwright, 'xiaozehua', '8qudcQifW7cjydglydm{')
    # page.locator("#registerAccount span").filter(has_text="Indonesia").first.click()
    # page.get_by_role("textbox", name="Email Verification Code *").fill("5@linshiyou.com")
    # page.locator("#mpanel4 div").filter(has_text="Slide right to unlock").locator("i").click()
    # page.get_by_role("textbox", name="Email Verification Code *").fill("123654")
    page.get_by_role("textbox", name="Password*").fill("A123456@test")
    page.get_by_role("textbox", name="Comfirm Password *").fill("A123456@test")
    page.get_by_role("button", name="Submit").click()
    page.pause()

    # ---------------------
    context.close()
    browser.close()


with sync_playwright() as playwright:
    run(playwright)
