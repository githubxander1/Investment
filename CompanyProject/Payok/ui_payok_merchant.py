import os
import re
from playwright.sync_api import Playwright, sync_playwright, expect


def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False,slow_mo=200,devtools=False)
    context = browser.new_context()
    page = context.new_page()

    # payok商户入口
    page.goto("http://payok-test.com/merchant/payok-register-register.html")
    page.locator("span").filter(has_text="English").first.click()
    page.get_by_role("link", name="中文").click()

    page.get_by_role("textbox", name="公司名称 *").fill("公司名称002")
    page.get_by_role("textbox", name="纳税人号 *").fill("002")
    page.get_by_role("textbox", name="公司品牌名").fill("公司品牌名001")
    page.get_by_role("textbox", name="公司简称").fill("公司简称001")
    page.get_by_label("公司类型 *").select_option("100")
    page.get_by_role("textbox", name="公司官网 *").fill("")
    page.get_by_role("textbox", name="公司官网 *").fill("http://www.baidu.com")
    page.get_by_role("textbox", name="公司地址 *").fill("公司地址001")
    page.get_by_role("textbox", name="公司法人(责任人) *").fill("法定责任人001")
    page.get_by_role("textbox", name="法人(责任人)联系电话 *").fill("15318544154")
    page.get_by_role("textbox", name="法人(责任人)邮箱 *").fill("1@linshiyou.com")
    page.get_by_role("textbox", name="法人（责任人）住址 商品服务 *").fill("法定责任人地址")
    page.get_by_label("商户类型 *").select_option("2")
    page.get_by_role("textbox", name="商品服务", exact=True).fill("商品服务001")
    page.get_by_role("textbox", name="商品服务金额范围 *").fill("1")
    page.get_by_role("textbox", name="商品服务最大金额").fill("999999999")
    page.get_by_role("textbox", name="商务联系人 *").fill("商务联系人001")
    page.get_by_role("textbox", name="商务联系人电话 *").fill("15318544154")
    page.get_by_role("textbox", name="商务联系人邮箱 *").fill("1@linshiyou.com")
    page.get_by_role("textbox", name="商务联系人邮箱 *").fill("1@linshiyou.com")
    page.get_by_role("textbox", name="技术联系人 *").fill("技术联系人001")
    page.get_by_role("textbox", name="技术联系人电话 *").fill("15318544154")
    page.get_by_role("textbox", name="技术联系人邮箱 *").fill("1@linshiyou.com")
    page.get_by_role("textbox", name="结算卡号 *").fill("001")
    page.get_by_role("textbox", name="结算卡户名 *").fill("结算卡户名001")
    page.get_by_role("textbox", name="结算卡开户银行 *").fill("结算卡开户银行001")
    page.get_by_label("账户类型 *").select_option("1")
    page.get_by_role("textbox", name="银行国际代码 *").fill("001")
    page.get_by_role("textbox", name="资金账户安全邮箱（设置财务密码） *").fill("1@linshiyou.com")
    page.get_by_role("button", name=" 添加一行").click()
    page.locator("select[name=\"selMdPlatform\"]").select_option("H5")
    page.get_by_role("cell", name="https:// 1/").get_by_placeholder("请输入").fill("www.baidu.com")
    page.locator("input[name=\"txtMdTestAccount\"]").fill("测试账号001")
    page.locator("input[name=\"txtMdTestPassword\"]").fill("test001")
    page.get_by_role("button", name="保存").click()

    # 上传文件
    # 定位所有文件输入框元素
    # file_inputs = page.wait_for_selector('input[type="file"]').all()
    # file_inputs = page.query_selector_all('input[type="file"]')
    # #
    # if file_inputs:
    #     # 选择第一个文件输入框
    #     file_input = file_inputs[0]
    #     file_path = r"D:\Xander\测试\营业执照.doc"
    #     if not os.path.exists(file_path):
    #         print(f"文件不存在: {file_path}")
    #     else:
    #         print(f"文件存在: {file_path}")
    #         file_input.set_input_files(file_path)
    #         page.wait_for_load_state('networkidle')
    # else:
    #     print("没有找到文件输入框元素")
    # #在字符串中使用了反斜杠 \ 作为路径分隔符，而 Python 将其解释为转义字符。例如，\X 被解释为无效的转义序列
    # # 等待上传完成（可根据实际情况调整等待条件）
    # page.wait_for_load_state('networkidle')

    # page.locator("body").set_input_files(r"D:\Xander\测试\营业执照.doc")
    page.get_by_text("营业执照 *请上传pdf|xls|doc文件(文件必须小于").click()
    #等待3秒
    page.wait_for_timeout(3000)
    # page.locator("body").set_input_files("D:\\Xander\\测试\\营业执照.doc") #在字符串中使用了反斜杠 \ 作为路径分隔符，而 Python 将其解释为转义字符。例如，\X 被解释为无效的转义序列

    page.get_by_text("纳税人号码（NPWP) *请上传pdf|xls|doc").click()
    # page.locator("body").set_input_files(r"D:\Xander\测试\纳税人号码.doc")
    page.wait_for_timeout(3000)
    # page.locator("body").set_input_files("D:\\Xander\\测试\\纳税人号码.doc")
    page.get_by_text("法人（责任人）护照").click()
    # page.locator("body").set_input_files(r"D:\Xander\测试\法人护照.doc")
    page.wait_for_timeout(3000)
    # page.locator("body").set_input_files("D:\\Xander\\测试\\法人护照.doc")
    page.get_by_role("textbox", name="业务归属地 * 邮箱 *").fill("1@linshiyou.com")
    page.get_by_role("button", name="发送验证码").click()
    page.wait_for_timeout(3000)

    page.pause()

    # page.locator("#mpanel4 div").filter(has_text="向右滑动解锁").locator("i").click()
    page.locator(".verify-move-block").click()
    # page.locator("#mpanel4 div").filter(has_text="向右滑动解锁").locator("div").nth(1).click()
    page.get_by_text("×").click()
    page.get_by_role("textbox", name="密码 *").fill("A123456@test")
    page.get_by_role("textbox", name="密码（确认） *").fill("A123456@test")
    page.get_by_role("button", name="提交").click()

    # ---------------------
    context.close()
    browser.close()


with sync_playwright() as playwright:
    run(playwright)
