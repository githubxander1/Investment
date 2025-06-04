import random
import re
import time
from os.path import exists

from playwright.sync_api import Playwright, sync_playwright, expect
from tenacity import stop_after_attempt

from CompanyProject.巴迪克.utils.get_email_code import get_email_code

from tenacity import retry, stop_after_attempt

# @retry(stop=stop_after_attempt(3))
# def slide_verification(page):
#     """
#     滑动滑块验证
#
#     参数:
#     page: Playwright页面对象
#     """
#     # 等待滑动验证元素加载完成
#     page.wait_for_selector('.verify-move-block', state='visible')
#
#     # 获取滑块元素
#     slider = page.locator('.verify-move-block')
#
#     # 获取滑动条宽度
#     slider_bar = page.locator('.verify-left-bar')
#     bounding_box = slider_bar.bounding_box()
#     if bounding_box is None:
#         raise ValueError("滑动条元素未找到")
#
#     slider_width = bounding_box['width']
#
#     # 获取滑块的初始位置
#     slider_box = slider.bounding_box()
#     if slider_box is None:
#         raise ValueError("滑块元素未找到")
#
#     # 模拟鼠标按下滑块
#     slider.hover()
#     slider.evaluate('element => element.dispatchEvent(new MouseEvent("mousedown", { bubbles: true }))')
#
#     # 模拟鼠标移动并释放，这里使用更精确的移动距离
#     target_x = slider_box['x'] + slider_width - 10  # 减去10是为了避免滑过头
#     target_y = slider_box['y'] + slider_box['height'] / 2
#     page.mouse.move(target_x, target_y)
#     page.mouse.up()
#
#     # 等待验证结果
#     page.wait_for_timeout(2000)  # 等待2秒以检查验证是否成功
#
#     # 检查验证是否成功（这里可以根据实际情况调整）
#     success_message = page.locator('.verify-msg').inner_text()
#     if "success" in success_message:
#         print("滑动验证成功")
#     else:
#         print("滑动验证失败")
#         raise Exception("滑动验证失败")  # 触发重试机制
# from tenacity import retry, stop_after_attempt

# @retry(stop=stop_after_attempt(3))
# def slide_verification(page):
#     """
#     滑动滑块验证
#
#     参数:
#     page: Playwright页面对象
#     """
#     # 等待滑动验证元素加载完成
#     page.wait_for_selector('.verify-move-block', state='visible')
#
#     # 获取滑动条和滑块元素
#     slider_bar = page.locator('.verify-left-bar')
#     slider = page.locator('.verify-move-block')
#
#     # 获取滑动条的宽度
#     slider_bar_bounding_box = slider_bar.bounding_box()
#     if slider_bar_bounding_box is None:
#         raise ValueError("滑动条元素未找到")
#     slider_bar_width = slider_bar_bounding_box['width']
#
#     # 获取滑块的初始位置
#     slider_bounding_box = slider.bounding_box()
#     if slider_bounding_box is None:
#         raise ValueError("滑块元素未找到")
#
#     # 模拟鼠标按下滑块
#     slider.hover()
#     slider.evaluate('element => element.dispatchEvent(new MouseEvent("mousedown", { bubbles: true }))')
#
#     # 动态计算目标位置并进行滑动
#     target_x = slider_bounding_box['x'] + slider_bar_width - slider_bounding_box['width']
#     target_y = slider_bounding_box['y'] + slider_bounding_box['height'] / 2
#     page.mouse.move(target_x, target_y)
#     page.mouse.up()
#
#     # 等待验证结果
#     page.wait_for_timeout(2000)  # 等待2秒以检查验证是否成功
#
#     # 检查滑动后的状态是否成功
#     slider_bar_bounding_box_after = slider_bar.bounding_box()
#     if slider_bar_bounding_box_after is None:
#         raise ValueError("滑动条元素未找到（滑动后）")
#
#     slider_bounding_box_after = slider.bounding_box()
#     if slider_bounding_box_after is None:
#         raise ValueError("滑块元素未找到（滑动后）")
#
#     # 检查滑动条宽度和滑块左偏移量是否一致
#     if abs(slider_bar_bounding_box_after['width'] - slider_bounding_box_after['x']) < 5:
#         print("滑动验证成功")
#     else:
#         print("滑动验证失败")
#         raise Exception("滑动验证失败")  # 触发重试机制

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
# # 在 payok_register 函数中调用 slide_verification 方法
# def payok_register(playwright: Playwright, register_email, merchant_name) -> None:
#     # ... (之前的代码)
#
#     # 第五页
#     page.pause()
#     page.locator("span").filter(has_text=re.compile(r"^Indonesia$")).click()
#     page.get_by_role("link", name="Indonesia").click()
#     # page.get_by_role("link", name="Vietnam").click()
#     page.get_by_role("textbox", name="E-mail *").fill(register_email)
#     page.get_by_role("button", name="Send the verification code").click()
#     page.pause()
#
#     # 调用滑动验证方法
#     slide_verification(page)
#
#     # ... (之后的代码)
#
# if __name__ == '__main__':
#     with sync_playwright() as playwright:
#         register_email = "payok1@test.com"
#         merchant_name = register_email
#         payok_register(playwright, register_email, merchant_name)

def payok_register(playwright: Playwright, register_email, merchant_name) -> None:
    # browser = playwright.chromium.launch(headless=False, args=["--start-maximized"])
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context(viewport={"width": 1920, "height": 1040})
    #窗口放大
    page = context.new_page()
    # page.set_viewport_size({"width": 1920, "height": 1040})
    # context = browser.new_context(no_viewport=True)
    # context = browser.new_context(viewport={"width": 1920, "height": 1080})
    page.goto("http://payok-test.com/merchant/payok-register-register.html") #测试环境
    # page.goto("https://m.payok.com/payok-register-register.html") #正式环境
    # page.evaluate("() => { document.documentElement.requestFullscreen(); }")
    next_button = page.locator("text=Next")
    page.wait_for_selector("text=Next", state="visible")

    # 获取所有 "Next" 按钮
    # next_buttons = page.locator("text=Next").all()
    #
    # for button in next_buttons:
    #     try:
    #         # 检查按钮是否可见
    #         if button.is_visible():
    #             print(button.evaluate("node => node.style.display"))  # 检查 display 属性
    #             print(button.evaluate("node => node.style.visibility"))  # 检查 visibility 属性
    #
    #             # 点击按钮
    #             button.click()
    #             break
    #     except Exception as e:
    #         print(f"Button not clickable: {e}")

    page.wait_for_load_state("networkidle")  # 等待网络空闲状态

    #第一页
    # page.pause()
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
    # page.pause()
    page.get_by_role("textbox", name="Amount Range *").fill("1")
    page.get_by_role("textbox", name="Maximum Amount").fill("6")
    page.get_by_role("button", name="Next").click()
    #第二页
    # page.pause()

    page.get_by_role("textbox", name="Business Contact *").fill("Budi Santoso")
    page.get_by_role("textbox", name="Business Contact Number *").fill("15318544154")
    page.get_by_role("textbox", name="Business Contact Email *").fill("1@linshiyou.com")
    page.get_by_role("textbox", name="Technical Contact *").fill("Rina Dewi")
    page.get_by_role("textbox", name="Technical Contact Number *").fill("15318544154")
    page.get_by_role("textbox", name="Technical Contact Email *").fill("1@linshiyou.com")
    page.get_by_role("button", name="Next").click()
    #第三页
    # page.pause()
    page.get_by_role("textbox", name="Account Number *").fill("1531854415415318544154")
    page.get_by_role("textbox", name="Account Name *").fill("华哥的账户")
    page.get_by_role("textbox", name="Bank Name *").fill("中国人民银行")
    page.get_by_role("textbox", name="Choose").click()
    page.get_by_role("treeitem", name="By Corporate").click()
    page.get_by_role("textbox", name="SWIFT Code *").fill("CENAIDJA")  # BCA的SWIFT代码示例
    page.get_by_role("textbox", name="Secure Email for fund account").fill("1@linshiyou.com")
    page.get_by_role("button", name="Next").click()
    # 第四页
    # page.pause()
    filepath = "../../common/data/合同.pdf"
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
    page.get_by_role("combobox", name="Please Choose").locator("span").nth(1).click()
    page.get_by_role("treeitem", name="H5").click()
    page.locator("input[name=\"txtMdRegisterAddress\"]").fill("www.baidu.com")
    page.locator("input[name=\"txtMdTestAccount\"]").fill("托尔斯泰")
    page.locator("input[name=\"txtMdTestPassword\"]").fill("1")
    page.get_by_role("button", name="Next").click()
    #第五页
    page.pause()
    page.locator("span").filter(has_text=re.compile(r"^Indonesia$")).click()
    page.get_by_role("link", name="Indonesia").click()
    # page.get_by_role("link", name="Vietnam").click()
    page.get_by_role("textbox", name="E-mail *").fill(register_email)
    page.get_by_role("button", name="Send the verification code").click()
    page.pause()

    from tenacity import retry
    slide_verification(page)

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
    continue_register = page.get_by_role("button", name="Continue Registration")
    continue_register.click()
    # 断言如果继续注册存在，则打印注册成功
    if continue_register.is_visible():
        print("注册成功")
    else:
        print("注册失败")
    page.pause()

    # ---------------------
    context.close()
    browser.close()


if __name__ == '__main__':
    with sync_playwright() as playwright:
        register_email = "payok1@test.com"
        merchant_name =  register_email
        payok_register(playwright, register_email, merchant_name)
