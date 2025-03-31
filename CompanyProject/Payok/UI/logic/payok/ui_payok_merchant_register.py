import os
from playwright.sync_api import Playwright, sync_playwright, expect

from CompanyProject.Payok.UI.logic.get_email_code import get_email_code
def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False,devtools=False) #slow_mo=10
    context = browser.new_context()
    page = context.new_page()

    # payok商户入口
    page.goto("http://payok-test.com/merchant/payok-register-register.html")
    #切换语言
    page.locator("span").filter(has_text="English").first.click()
    page.get_by_role("link", name="中文").click()

    page.get_by_role("textbox", name="公司名称 *").fill("公司001")
    page.get_by_role("textbox", name="纳税人号 *").fill("002")
    page.get_by_role("textbox", name="公司品牌名").fill("公司品牌名001")
    page.get_by_role("textbox", name="公司简称").fill("公司简称001")

    '''公司类型：印尼本地公司，越南本地公司，巴西本地公司，泰国本地公司，士耳其本地公司，哥伦比亚本地公司，印度本地公司，孟加拉国本地公司，中国本地公司，其他海外公司
    100印尼 106越南 107巴西 108泰国 109土耳其 110哥伦比亚 111印度 112孟加拉 101中国 105其他海外'''
    page.get_by_label("公司类型 *").select_option("100")
    page.get_by_role("textbox", name="公司官网 *").fill("")
    page.get_by_role("textbox", name="公司官网 *").fill("http://www.baidu.com")
    page.get_by_role("textbox", name="公司地址 *").fill('广东省深圳市南山区桃源街道1号')
    page.get_by_role("textbox", name="公司法人(责任人) *").fill("法定责任人001")
    page.get_by_role("textbox", name="法人(责任人)联系电话 *").fill("15318544154")
    page.get_by_role("textbox", name="法人(责任人)邮箱 *").fill("1@linshiyou.com")
    page.get_by_role("textbox", name="法人（责任人）住址 商品服务 *").fill("法定责任人地址")

    '''商户类型：Live Streaming，Oline Gambling,Forex Trading,Fintech,Binary Option,Crypto Platform,Dating Apps,Other
    1直播 2线上博弈 3外汇交易 4金融行业 5二元期货 6加密平台 7线上约会 9本地商户 10本地聚合支付 8其他'''
    page.get_by_label("商户类型 *").select_option("7")
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

    '''账户类型：1对公，2对私'''
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
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    # 文件路径配置
    DATA_DIR = os.path.join(BASE_DIR, '../..', 'data')
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
    page.get_by_role("textbox", name="业务归属地 * 邮箱 *").fill("5@qq.com")
    page.get_by_role("button", name="发送验证码").click()

    # 等待滑动解锁弹窗出现
    # page.wait_for_selector("#mpanel4", state='visible')
    # page.wait_for_timeout(5000)
    page.pause()#暂停

    '''复制粘贴：
        cd /data/logs/tomcat/merchart
        grep "发邮件结束 getVerificationCode 登录邮箱" *
        '''
    get_email_code(playwright, 'xiaozehua' ,'8qudcQifW7cjydglydm{')

    page.get_by_role("textbox", name="密码 *").fill("A123456@test")
    page.get_by_role("textbox", name="密码（确认） *").fill("A123456@test")
    page.get_by_role("button", name="提交").click()

    # 等待并捕获 alert
    # alert = page.wait_for_alert()
    #
    # # 获取 alert 的文本内容
    # alert_text = alert.text
    #
    # print(alert_text)
    # # 进行断言，这里假设预期的文本是 "这是一个测试 alert"，需要替换为实际的预期文本
    # assert alert_text == "这是一个测试 alert", f"Alert 文本不正确，实际文本是: {alert_text}"
    #
    # # 接受 alert（关闭 alert 弹窗）
    # alert.accept()

    # 断言弹窗里账户邮箱已存在提示
    page.wait_for_timeout(1000)
    # toast = page.get_by_role("alert")
    toast = page.locator("text=×提示账户邮箱已存在")
    # expect(toast).to_be_visible()
    if toast.is_visible():
        print("注册失败：邮箱已存在")
    else:
        print("邮箱可以注册")

    # page.get_by_role("button", name="继续注册").click()
    # page.get_by_role("button", name="去登录").click()

    # page.wait_for_timeout(5000)
    page.pause()#暂停

    # ---------------------
    context.close()
    browser.close()


with sync_playwright() as playwright:
    run(playwright)
