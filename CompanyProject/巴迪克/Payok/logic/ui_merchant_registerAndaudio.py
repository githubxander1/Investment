import os
from os.path import exists

from playwright.sync_api import Playwright, sync_playwright, expect

from CompanyProject.巴迪克.Payok.logic.merchant_register import payok_register
from CompanyProject.巴迪克.Payok.logic.platform_login import platform_login


def platform_merchant_go_live(page, merchant_name):
    # 开始审核,上线
    page.get_by_role("link", name="ﶇ 商户 ").click()
    page.get_by_role("link", name="商户列表").click()

    # 审核100 生效105 审核驳回110 禁用130
    page.get_by_label("商户状态", exact=True).select_option("100")
    page.get_by_role("button", name=" 查找").click()
    page.wait_for_timeout(1000)

    # page.locator("td").first.click() #选择第一个商户
    page.get_by_role("gridcell", name=f"+ {merchant_name}").first.click()
    page.get_by_role("button", name="上线").click()
    page.get_by_role("dialog", name="商户信息").locator("b").nth(1).click()
    page.get_by_role("treeitem", name="梅总-[082211366666]").click()
    page.get_by_role("combobox", name="不参与分润").locator("b").click()
    page.get_by_role("treeitem", name="test-定时任务 -").click()
    page.get_by_text("确定切换").click()
    page.get_by_role("dialog", name="商户信息").locator("b").nth(3).click()
    page.get_by_role("treeitem", name="-日出东方-[120200916152641588]").click()
    page.pause()
    page.get_by_label("商户信息").get_by_role("combobox", name="选择").locator("b").click()
    page.get_by_role("treeitem").filter(has_text="hfdgd -").click()
    # page.locator('//*[@id="select2-agentProfitRules-result-n0uk-1116423140388933632"]').click()
    page.get_by_text("确定切换").click()
    page.get_by_role("listitem").filter(has_text="MCPPay-izpocket-wallet").locator("label").click()
    page.get_by_role("button", name="H5支付隐藏").click()
    page.on('filechooser', lambda file_chooser: file_chooser.set_files(pdf_file_path))
    page.get_by_role("heading", name="文件上传").click()
    page.wait_for_timeout(2000)
    page.get_by_role("button", name="生效").click()

    #断言toast是否包含‘成功’，如果没有就报错
    try:
        expect(page.get_by_text("成功")).to_be_visible()
        print("审核上线成功")
    except:
        print("审核上线失败")
        page.pause()


def run(playwright: Playwright) -> None:
    # browser = playwright.chromium.launch(headless=False,args=["--start-maximized"])
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.set_viewport_size({"width": 1920, "height": 1040})
    # next_button = page.locator("text=Next")
    # page.wait_for_selector("text=Next", state="visible")

    #商户注册
    register_email = "2@linshiyou.com"
    merchant_password = "A123456@test"
    merchant_name = register_email
    # merchant_name = '1'
    # payok_register(playwright, register_email, merchant_name) #商户注册

    # operator_login_name = 'Xander@test.com'
    # operator_password = 'QWEqwe@123456'
    # platform_login(playwright,operator_login_name, operator_password) #平台端登录
    # page.pause()

    # platform_merchant_go_live(page,merchant_name) # 审核上线

    # merchant_login(playwright, merchant_name, merchant_password) #商户端登录

    context.close()
    browser.close()

if __name__ == '__main__':
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    DATA_DIR = os.path.join(BASE_DIR, '../..', 'data')
    pdf_file_path = os.path.join(DATA_DIR, "合同.pdf")
    if pdf_file_path is exists:
        print('文件存在')

    with sync_playwright() as playwright:
        run(playwright)
