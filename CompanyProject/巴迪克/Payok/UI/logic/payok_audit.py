from playwright.sync_api import Playwright

from CompanyProject.巴迪克.Payok.UI.others.old_ui_merchant_login import generate_google_code
from CompanyProject.巴迪克.utils.perform_slider_unlock import perform_block_slider_verification


# from CompanyProject.巴迪克.UI.utils.generate_google_code import generate_google_code
# from CompanyProject.巴迪克.UI.utils.perform_slider_unlock import perform_block_slider_verification


def payok_merchant_audio(playwright: Playwright, login_email, merchant_name) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("http://payok-test.com/platform/payok-user-login.html")
    page.get_by_text("Bahasa").click()
    page.get_by_role("link", name="中文").click()

    page.get_by_role("textbox", name="邮箱").fill(login_email)
    page.get_by_placeholder("请输入密码").fill("tktjBPB)eT4,]anz")
    # page.get_by_role("textbox", name="密码 验证码").click()
    # page.locator("div").filter(has_text="平台用户登录请输入您的电子邮箱和密码邮箱 密码 验证码向右滑动解锁登录您还未绑定谷歌验证码，为了您的账户和资金安全，请立即绑定。 请在 2:00").nth(2).click()
    # page.get_by_role("textbox", name="密码 验证码").click()
    # page.locator("#mpanel2 i").click()
    # page.goto("http://payok-test.com/platform/payok-user-login.html")
    perform_block_slider_verification(page)

    page.get_by_role("button", name=" 登录").click()
    google_code = generate_google_code('192.168.0.227', 3306, 'WAYANGPAY', 'Z43@Mon88', 'aesygo_test','operator', login_email)
    page.get_by_role("textbox", name="谷歌验证码").fill(google_code)
    page.get_by_role("button", name="确认").click()

    page.get_by_role("link", name="ﶇ 商户 ").click()
    page.get_by_role("link", name="商户列表").click()

    #审核100 生效105 审核驳回110 禁用130
    page.get_by_label("商户状态", exact=True).select_option("100")
    page.get_by_role("button", name=" 查找").click()
    page.wait_for_timeout(1000)
    page.pause()
    # 完全匹配文本 // * [text() = "theshy "]
    # 部分匹配文本 // * [contains(text(),“theshy”)]
    # page.get_by_role("gridcell", name=f"+{merchant_name}").click() #选择商户

    # page.locator("#merchant-datatable > tbody > tr:nth-child(2) > td.focus").click()
    # 使用 CSS 选择器定位元素
    element = page.locator('#merchant-datatable > tbody > tr:nth-child(2) > td.focus')
    if element:
        print("元素已找到")
        element.click()
    # page.get_by_text(text=f"{merchant_name}").click() #选择商户
    page.get_by_role("button", name="上线").click()

if __name__ == '__main__':
    login_email = "2695418206@qq.com"
    merchant_name = "公司001"
    with Playwright() as playwright:
        payok_merchant_audio(playwright, login_email, merchant_name)