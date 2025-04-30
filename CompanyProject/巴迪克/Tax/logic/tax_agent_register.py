import asyncio
import os
import re
from PIL import Image
# from numpy import error_message
from playwright.async_api import async_playwright, expect
import random
import pytesseract
from tenacity import retry, stop_after_attempt

from CompanyProject.巴迪克.utils.get_email_code import get_email_code

# 设置Tesseract路径
pytesseract.pytesseract.tesseract_cmd = r'D:\Xander\Applications\TesseractOCR\tesseract.exe'

@retry(stop=stop_after_attempt(3))
async def generate_npwp():
    """生成符合格式的随机NPWP"""
    parts = [
        f"{random.randint(10,99)}",          # 2位数字
        f"{random.randint(100,999)}",        # 3位数字
        f"{random.randint(100,999)}",        # 3位数字
        f"{random.randint(0,9)}",            # 1位数字
        f"{random.randint(0,999):03d}",      # 3位补零
        f"{random.randint(0,999):03d}"       # 3位补零
    ]
    return f"{parts[0]}.{parts[1]}.{parts[2]}.{parts[3]}-{parts[4]}.{parts[5]}"

async def recognize_captcha(image_path):
    """识别验证码"""
    image = Image.open(image_path)
    # 预处理图片
    image = image.convert('L')  # 灰度化
    threshold = 127
    table = []
    for i in range(256):
        if i < threshold:
            table.append(0)
        else:
            table.append(1)
    image = image.point(table, '1')  # 二值化

    # 使用pytesseract进行OCR识别
    captcha_text = pytesseract.image_to_string(image, config='--psm 7').strip()
    return captcha_text

async def agent_register(register_email) -> None:
    async with async_playwright() as playwright:
        browser = await playwright.chromium.launch(headless=False)
        context = await browser.new_context()
        page = await context.new_page()
        await page.goto("http://balitax-test.com/tax-agent/balitax-user-register.html")
        await page.locator("span").filter(has_text="Bahasa").first.click()
        await page.get_by_role("link", name="English").click()
        await page.get_by_role("textbox", name="Company Name *").fill(register_email)
        await page.get_by_role("textbox", name="Company Brand Name").fill("Company brand name")
        await page.locator("b").click()
        await page.get_by_role("treeitem", name="POS service providers").click()
    
        # max_retries = 5
        # for attempt in range(max_retries):
        npwp = await generate_npwp()
        await page.get_by_role("textbox", name="NPWP *").fill(npwp)

        # 触发验证（根据实际页面验证方式调整）
        await page.keyboard.press("Tab")

        try:
            # 检查错误提示是否存在（根据实际错误提示调整选择器）
            await expect(page.get_by_text("NPWP already exists")).not_to_be_visible(timeout=2000)
        except AssertionError:
            raise Exception("生成唯一NPWP失败，已达最大重试次数")

        await page.get_by_role("textbox", name="Official Website *").fill("www.baidu.com")
        await page.get_by_role("textbox", name="Company Address *").fill("广东省深圳市南山区桃源街道益田假日里1201")
        await page.get_by_role("textbox", name="Company Legal Person (").fill("张三")
        await page.get_by_role("textbox", name="Legal Person (Responsible Person) Contact Number *").fill("15318544154")
        await page.get_by_role("textbox", name="Legal Person (Responsible Person) Address *").fill("广东省深圳市南山区桃源街道法人地址001号")
        await page.get_by_role("textbox", name="Contact Person *").fill("李四")
        await page.get_by_role("textbox", name="Contact Person's Number *").fill("15318544154")
        page.on("filechooser", lambda f: f.set_files(pdf_file_path))
        await page.get_by_text("Business License").click()
        await page.get_by_text("Taxpayer Document (NPWP)").click()
        await page.get_by_text("Director Identity/Passport").click()
        await page.wait_for_timeout(1000)
        await page.get_by_role("button", name="Next").click()
    
        # 第二页
        await page.get_by_role("textbox", name="Admin Email *").fill(register_email)
        await page.get_by_role("button", name="Send Verification Code").click()
    
        print('请填写安全验证码......')
        await page.pause()
    
        # 捕获并识别验证码
        # captcha_img_path = "captcha.png"
        # await page.locator("#imgCode").screenshot(path=captcha_img_path)
        # captcha_text = recognize_captcha(captcha_img_path)
        # print("识别的验证码:", captcha_text)
        #
        # # 输入验证码
        # await page.locator("#txtVerificationCode").fill(captcha_text)
        #
        # await page.pause()
        await page.locator("#submitBtn").click()
        #
        # # 检查验证码是否正确
        # try:
        #     expect(await page.locator(".verification")).to_have_class("text-red verification d-none", timeout=2000)
        # except AssertionError:
        #     # error_message = expect(await page.locator("#verification")).to_contain_text("Incorrect CAPTCHA, please try again")
        #     # if error_message.is_visible():
        #         # raise ValueError("验证码输入错误")
        #     print("验证码输入错误，正在重新尝试...")
        #     # 如果验证码错误，清空输入框并重新识别
        #     await page.locator("#txtVerificationCode").clear()
        #     await page.locator("#imgCode").click()  # 刷新验证码图片
        #     await page.locator("#imgCode").screenshot(path=captcha_img_path)
        #     captcha_text = recognize_captcha(captcha_img_path)
        #     print("重新识别的验证码:", captcha_text)
        #     await page.locator("#txtVerificationCode").fill(captcha_text)
        #     await page.locator("#submitBtn").click()
    
        await get_email_code(linux_username,linux_password)
        print('请填写邮箱验证码......')
        await page.pause()
        # await page.get_by_role("textbox", name="Email Verification Code *").fill("547099")
        await page.get_by_role("textbox", name="Password *", exact=True).fill("A123456@test")
        await page.get_by_role("textbox", name="Confirm Password *").fill("A123456@test")
        # await page.locator('//*[@id="customCheck2"]').click()
        await page.evaluate('''() => {
                            const el = document.querySelector('input#customRadio3');
                            if(el) el.click() }''')
        # 勾选同意服务协议
        # checkbox = await page.query_selector('#customCheck2')
        # if checkbox:
        #     await page.evaluate('(element) => element.click()', checkbox)
        # else:
        #     print("元素未找到")
        # async def check_service_agreement(page):
        #     """勾选服务协议复选框"""
        #     # 组合定位策略
        #     checkbox_selector = """
        #         //div[contains(@class,'custom-radio')]
        #         /input[@id='customRadio3' and @name='customRadio1']
        #     """
        #
        #     try:
        #         # 等待元素可见
        #         await page.wait_for_selector(checkbox_selector, state="visible", timeout=5000)
        #
        #         # 更精确的定位方式
        #         checkbox = await page.locator(checkbox_selector).and_(
        #             page.get_by_label("I have read and agree to the")
        #         )
        #
        #         # 滚动到可视区域
        #         await checkbox.scroll_into_view_if_needed()
        #
        #         # 使用Playwright原生点击
        #         await checkbox.check(force=True)  # force参数确保绕过可见性检查
        #
        #         print("成功勾选服务协议")
        #         return True
        #     except Exception as e:
        #         print(f"勾选失败: {str(e)}")
        #         # 备用点击方案
        #         await page.evaluate('''() => {
        #             const el = document.querySelector('input#customRadio3');
        #             if(el) el.click();
        #         }''')
        #         return False
    
        # 在注册流程中调用
        # await check_service_agreement(page)
    
        # await page.get_by_role("button", name="Confirm").click()

        await page.get_by_role("button", name="I Understand").click()

        #删除同目录下的‘email_code.png'文件
        if os.path.exists("email_code.png"):
            os.remove("email_code.png")
        else:
            print("email_code.png 文件不存在")
        # ---------------------
        await context.close()
        await browser.close()

if __name__ == '__main__':
    agent_register_email = "tax_agent003@linshiyou.com"
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    DATA_DIR = os.path.join(BASE_DIR, '../../common', 'data')
    pdf_file_path = os.path.join(DATA_DIR, "合同.pdf")

    linux_username = 'xiaozehua'
    linux_password = '8qudcQifW7cjydglydm{'

    if not os.path.exists(pdf_file_path):
        print('文件不存在')
        exit()

    # 确保异步事件循环正确执行
    # try:
    asyncio.run(agent_register(agent_register_email))
    # except RuntimeError as e:
    #     if "Event loop is closed" in str(e):
    #         Windows系统需要特殊处理事件循环
            # asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
            # asyncio.run(agent_register(agent_register_email))
