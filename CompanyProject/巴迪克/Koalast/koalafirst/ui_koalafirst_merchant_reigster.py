import os
import re
from playwright.sync_api import Playwright, sync_playwright, expect

from CompanyProject.巴迪克.UI.logic.get_email_code import get_email_code


def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False,slow_mo=100)
    context = browser.new_context()
    page = context.new_page()

    # koalafirst商户入口
    page.goto("http://koalafirst-test.com/merchant/koalafirst-register-register.html") #测试环境
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
    page.get_by_role("textbox", name="商品服务金额范围").fill("1")
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
    page.get_by_role("textbox", name="资金账户安全邮箱 *").fill("1@linshiyou.com")
    page.get_by_role("button", name=" 添加一行").click()
    page.locator("select[name=\"selMdPlatform\"]").select_option("H5")
    page.get_by_role("cell", name="https:// 1/").get_by_placeholder("请输入").fill("www.baidu.com")
    page.locator("input[name=\"txtMdTestAccount\"]").fill("测试账号001")
    page.locator("input[name=\"txtMdTestPassword\"]").fill("test001")
    page.get_by_role("button", name="保存").click()

    # 上传文件
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    # 文件路径配置
    DATA_DIR = os.path.join(BASE_DIR, '../..', 'data')  # 修正文件路径
    # 日志文件路径
    agreement = os.path.join(DATA_DIR, "合同.pdf")
    npwp = os.path.join(DATA_DIR, "纳税人号码.doc")
    passport = os.path.join(DATA_DIR, "法人护照.doc")

    def upload_file(file_path, form_id):
        if not os.path.exists(file_path):
            print(f"文件不存在: {file_path}")
            return

        print(f"文件存在: {file_path}")

        # 监听 file_chooser 事件
        page.on('filechooser', lambda file_chooser: file_chooser.set_files(file_path))

        # 触发文件选择弹窗
        page.locator(f"#form{form_id} .dz-message").click()

        # 等待文件上传完成（可根据实际情况调整等待条件）
        page.wait_for_timeout(3000)

    # 上传营业执照
    upload_file(agreement, "1")
    # 上传纳税人号码（NPWP）
    upload_file(npwp, "2")
    # 上传法人（责任人）护照
    upload_file(passport, "3")

    page.locator("span").filter(has_text="Indonesia").first.click()
    # 国家
    '''Indonesia,Vietnam,Brazil,Thailand,Turkey,Colombia,India,Bangladesh'''
    page.get_by_role("link", name="Indonesia").click()
    page.get_by_role("textbox", name="业务归属地 * 邮箱 *").fill("3@qq.com")
    page.get_by_role("button", name="发送验证码").click()

    # 等待滑动解锁弹窗出现
    # page.wait_for_selector("#mpanel4", state='visible')
    # page.wait_for_timeout(5000)
    page.pause()  # 暂停

    '''复制粘贴：
        cd /data/logs/tomcat/merchart
        grep "发邮件结束 getVerificationCode 登录邮箱" *'''
    get_email_code(playwright)

    page.get_by_role("textbox", name="密码 *").fill("A123456@test")
    page.get_by_role("textbox", name="密码（确认） *").fill("A123456@test")
    page.get_by_role("button", name="提交").click()

    # ---------------------
    context.close()
    browser.close()


with sync_playwright() as playwright:
    run(playwright)
