import asyncio
import logging
import random
import re
import time
from os.path import exists
import asyncio
from playwright.sync_api import Playwright, sync_playwright, expect
from playwright.sync_api import Playwright, sync_playwright, expect
from tenacity import stop_after_attempt

from CompanyProject.巴迪克.utils.get_email_code import get_email_code


def slide_verification(page):
    # 等待滑块验证元素出现
    slider = page.wait_for_selector('.verify-move-block', state='visible')  # 替换为实际滑块选择器

    # 获取滑块位置信息
    box = slider.bounding_box()
    if box:
        # 模拟人类行为的随机移动轨迹
        start_x = box["x"]
        start_y = box["y"]
        target_x = start_x + box["width"]  # 移动到滑块终点
        target_y = start_y

        # 创建随机移动轨迹
        steps = random.randint(15, 25)  # 随机步数
        points = [(start_x, start_y)]

        # 生成中间点
        for i in range(1, steps):
            progress = i / steps
            x = start_x + (target_x - start_x) * progress
            # 添加一些随机抖动
            y = start_y + random.randint(-5, 5)
            points.append((x, y))

        points.append((target_x, target_y))

        # 模拟鼠标按下
        page.mouse.move(start_x, start_y)
        page.mouse.down()

        # 按照轨迹移动鼠标
        for x, y in points[1:]:
            page.mouse.move(x, y)
            time.sleep(random.uniform(0.01, 0.03))  # 添加随机延迟

        # 释放鼠标
        page.mouse.up()
        time.sleep(1)  # 等待验证结果


def payok_register(page, register_email, merchant_name, upload_filepath) -> None:
    # browser = playwright.chromium.launch(headless=False)
    # context = browser.new_context(no_viewport=True)
    # page = context.new_page()
    page.goto("http://payok-test.com/merchant/payok-register-register.html") #测试环境
    # page.goto("https://m.payok.com/payok-register-register.html") #正式环境

    #第一页
    page.get_by_role("textbox", name="Company Name *").fill(merchant_name)
    page.get_by_role("textbox", name="Taxpayer Number *").fill("123456789012345")  # 印尼纳税人识别号格式
    page.get_by_role("textbox", name="Company Brand Name").fill("FutureTech Solutions")
    page.get_by_role("textbox", name="Company Abbreviation").fill("FTS")
    page.locator("#select2-companyLocationType-container").click()
    page.get_by_role("treeitem", name="Indonesia Local Company").click()
    page.get_by_role("textbox", name="Official Website *").fill("https://www.baidu.com")
    page.get_by_role("textbox", name="Company Address *").fill("Jl. Sudirman No.1, Jakarta 10220")
    page.get_by_role("textbox", name="Corporate Legal Person (").fill("Andi Wijaya")
    page.get_by_role("textbox", name="Legal Person Contact Number *").fill("628123456789")  # 印尼电话号码格式
    page.get_by_role("textbox", name="Email of Legal Person *").fill("1@linshiyou.com")
    page.get_by_role("textbox", name="Address of Legal Person Type").fill("Jl. Thamrin No.10, Jakarta 10350")
    page.get_by_role("textbox", name="Choose").click()
    page.get_by_role("treeitem", name="Live Streaming").click()
    page.get_by_role("textbox", name="Please enter").fill("直播")
    page.get_by_role("textbox", name="Amount Range *").fill("1")
    page.get_by_role("textbox", name="Maximum Amount").fill("6")
    page.get_by_role("button", name="Next").click()
    #第二页
    page.get_by_role("textbox", name="Business Contact *").fill("Budi Santoso")
    page.get_by_role("textbox", name="Business Contact Number *").fill("15318544154")
    page.get_by_role("textbox", name="Business Contact Email *").fill("1@linshiyou.com")
    page.get_by_role("textbox", name="Technical Contact *").fill("Rina Dewi")
    page.get_by_role("textbox", name="Technical Contact Number *").fill("15318544154")
    page.get_by_role("textbox", name="Technical Contact Email *").fill("1@linshiyou.com")
    page.get_by_role("button", name="Next").click()
    #第三页
    page.get_by_role("textbox", name="Account Number *").fill("1531854415415318544154")
    page.get_by_role("textbox", name="Account Name *").fill("华哥的账户")
    page.get_by_role("textbox", name="Bank Name *").fill("中国人民银行")
    page.get_by_role("textbox", name="Choose").click()
    page.get_by_role("treeitem", name="By Corporate").click()
    page.get_by_role("textbox", name="SWIFT Code *").fill("CENAIDJA")  # BCA的SWIFT代码示例
    page.get_by_role("textbox", name="Secure Email for fund account").fill("1@linshiyou.com")
    page.get_by_role("button", name="Next").click()
    # 第四页
    page.on("filechooser", lambda f: f.set_files(upload_filepath))
    page.locator("#form1").click()
    page.locator("#form2").click()
    page.locator("#form3").click()
    page.get_by_role("button", name=" Add a row").click()
    page.get_by_role("combobox", name="Please Choose").locator("span").nth(1).click()
    page.get_by_role("treeitem", name="H5").click()
    page.locator("input[name=\"txtMdRegisterAddress\"]").fill("www.baidu.com")
    page.locator("input[name=\"txtMdTestAccount\"]").fill("托尔斯泰")
    page.locator("input[name=\"txtMdTestPassword\"]").fill("1")
    page.get_by_role("button", name="Next").click()
    #第五页
    # page.pause()
    page.locator("span").filter(has_text=re.compile(r"^Indonesia$")).click()
    page.get_by_role("link", name="Indonesia").click()#Vietnam
    page.get_by_role("textbox", name="E-mail *").fill(register_email)
    page.get_by_role("button", name="Send the verification code").click()
    page.pause()

    # captcha_img = page.locator("#captchaImg")
    # captcha_text = get_captcha_text("ddddocr",captcha_img)

    from tenacity import retry
    # slide_verification(page)

    '''复制粘贴：
            cd /data/logs/tomcat/merchart
            grep "发邮件结束 getVerificationCode 登录邮箱" *
            '''
    get_email_code('xiaozehua', '8qudcQifW7cjydglydm{')
    page.get_by_role("textbox", name="Password*").fill("A123456@test")
    page.get_by_role("textbox", name="Comfirm Password *").fill("A123456@test")
    page.get_by_role("button", name="Submit").click()
    continue_register = page.get_by_role("button", name="Continue Registration")
    continue_register.click()
    # 断言如果继续注册存在，则打印注册成功
    if continue_register.is_visible():
        print("注册成功")
    else:
        print("注册失败")
    page.pause()

    # ---------------------
    # context.close()
    # browser.close()


if __name__ == '__main__':
    filepath = "../../../common/data/合同.pdf"
    if filepath is None or not exists(filepath):
        print("文件不存在")
        exit(1)

    with sync_playwright() as playwright:
        register_email = "payok3@test.com"
        merchant_name =  register_email.split("@")[0]
        payok_register(playwright, register_email, merchant_name,  filepath)

    asyncio.run(get_email_code('xiaozehua', '8qudcQifW7cjydglydm{'))
