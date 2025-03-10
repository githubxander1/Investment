import os
import re
from playwright.sync_api import Playwright, sync_playwright, expect


def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False, slow_mo=50, devtools=False)
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

    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

    # 文件路径配置
    DATA_DIR = os.path.join(BASE_DIR, 'data')

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

    page.get_by_role("textbox", name="业务归属地 * 邮箱 *").fill("1@linshiyou.com")
    page.get_by_role("button", name="发送验证码").click()

    # 等待滑动解锁弹窗出现
    page.wait_for_selector("#mpanel4", state='visible')

    def perform_slide_unlock(page):
        for _ in range(3):  # 尝试3次
            try:
                slider = page.locator(".verify-move-block")
                slider_box = slider.bounding_box()
                target_x = slider_box['x'] + slider_box['width'] + 5  # 增加5像素的偏移量
                target_y = slider_box['y'] + slider_box['height'] / 2

                page.mouse.move(slider_box['x'], slider_box['y'] + slider_box['height'] / 2)
                page.mouse.down()
                page.mouse.move(target_x, target_y)
                page.mouse.up()

                # 等待滑动解锁成功后的页面变化
                page.wait_for_selector(".success-message", state='visible', timeout=5000)
                return True
            except Exception as e:
                print(f"滑动解锁失败，重试: {e}")
                page.wait_for_timeout(1000)  # 等待1秒后重试
        return False

    if not perform_slide_unlock(page):
        print("滑动解锁多次尝试后仍失败")
        context.close()
        browser.close()
        return


    page.get_by_role("textbox", name="密码 *").fill("A123456@test")
    page.get_by_role("textbox", name="密码（确认） *").fill("A123456@test")
    # page.get_by_role("button", name="提交").click()

    page.wait_for_timeout(5000)

    # ---------------------
    context.close()
    browser.close()


with sync_playwright() as playwright:
    run(playwright)
