import re
from os.path import exists

from playwright.sync_api import Playwright, sync_playwright, expect

from CompanyProject.Payok.UI.utils.get_email_code import get_email_code


def payok_register(playwright: Playwright, register_email, merchant_name) -> None:
    browser = playwright.chromium.launch(headless=False, args=["--start-maximized"])
    context = browser.new_context(no_viewport=True)
    # context = browser.new_context(viewport={"width": 1920, "height": 1080})
    page = context.new_page()
    page.set_viewport_size({"width": 1920, "height": 1080})
    page.goto("http://payok-test.com/merchant/payok-register-register.html")
    # page.evaluate("() => { document.documentElement.requestFullscreen(); }")

    #第一页
    page.get_by_role("textbox", name="Company Name *").fill(merchant_name)
    page.get_by_role("textbox", name="Taxpayer Number *").fill("纳税人号码")
    page.get_by_role("textbox", name="Company Brand Name").fill("公司品牌名：发达舒服")
    page.get_by_role("textbox", name="Company Abbreviation").fill("公司东方闪电")
    page.locator("#select2-companyLocationType-container").click()
    page.get_by_role("treeitem", name="Indonesia Local Company").click()
    page.get_by_role("textbox", name="Official Website *").fill("www.baidu.com")
    page.get_by_role("textbox", name="Company Address *").fill("深圳市宝安区宝安大道1号")
    page.get_by_role("textbox", name="Corporate Legal Person (").fill("公司法人：张三")
    page.get_by_role("textbox", name="Legal Person Contact Number *").fill("15318544154")
    page.get_by_role("textbox", name="Email of Legal Person *").fill("1@linshiyou.com")
    page.get_by_role("textbox", name="Address of Legal Person Type").fill("法人地址：范德萨范德萨发生大防守打法手打发撒")
    page.get_by_role("textbox", name="Choose").click()
    page.get_by_role("treeitem", name="Live Streaming").click()
    page.get_by_role("textbox", name="Please enter").fill("直播")
    page.get_by_role("textbox", name="Amount Range *").fill("1")
    page.get_by_role("textbox", name="The Maximum Amount Per").fill("6")
    page.get_by_role("button", name="Next").click()
    #第二页
    # page.pause()
    page.get_by_role("textbox", name="Business Contact *").fill("15318544154")
    page.get_by_role("textbox", name="Business Contact Number *").fill("15318544154")
    page.get_by_role("textbox", name="Business Contact Email *").fill("1@linshiyou.com")
    page.get_by_role("textbox", name="Technical Contact *").fill("15318544154")
    page.get_by_role("textbox", name="Technical Contact Number *").fill("15318544154")
    page.get_by_role("textbox", name="Technical Contact Email *").fill("1@linshiyou.com")
    page.get_by_role("textbox", name="Technical Contact Number *").fill("15318544154")
    page.get_by_role("button", name="Next").click()
    #第三页
    # page.pause()
    page.get_by_role("textbox", name="Account Number *").fill("1531854415415318544154")
    page.get_by_role("textbox", name="Account Name *").fill("15318544154")
    page.get_by_role("textbox", name="Bank Name *").fill("中国人民银行")
    page.get_by_role("textbox", name="Choose").click()
    page.get_by_role("treeitem", name="By Corporate").click()
    page.get_by_role("textbox", name="SWIFT Code *").fill("第三方第三发所发生的")
    page.get_by_role("textbox", name="Secure Email for fund account").fill("1@linshiyou.com")
    page.get_by_role("button", name="Next").click()
    # 第四页
    filepath = "../../data/合同.pdf"
    if filepath is None or not exists(filepath):
        print("文件不存在")
        exit(1)
    def set_files(number,filepath):
        page.on("filechooser", lambda f: f.set_files(filepath))
        page.locator(f"#form{number}").click()
    set_files("1",filepath)
    set_files("2",filepath)
    set_files("3",filepath)
    page.get_by_role("button", name=" Add a row").click()
    page.pause()
    page.get_by_role("combobox", name="Please Choose").locator("span").nth(1).click()
    page.get_by_role("treeitem", name="H5").click()
    page.locator("input[name=\"txtMdRegisterAddress\"]").fill("www.baidu.com")
    page.locator("input[name=\"txtMdTestAccount\"]").fill("托尔斯泰")
    page.locator("input[name=\"txtMdTestPassword\"]").fill("1")
    # page.get_by_role("textbox", name="Registration Address").fill("www.baidu.com")
    # page.get_by_role("textbox", name="Test Account", exact=True).fill("托尔斯泰")
    # page.get_by_role("textbox", name="Test Account Password").fill("A123456@test")
    page.get_by_role("button", name="Next").click()
    #第五页
    page.pause()
    page.locator("span").filter(has_text=re.compile(r"^Indonesia$")).click()
    # page.get_by_role("link", name="Indonesia").click()
    page.get_by_role("link", name="Vietnam").click()
    page.get_by_role("textbox", name="E-mail *").fill(register_email)
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


if __name__ == '__main__':
    with sync_playwright() as playwright:
        register_email = "12@linshiyou.com"
        payok_register(playwright, register_email)
