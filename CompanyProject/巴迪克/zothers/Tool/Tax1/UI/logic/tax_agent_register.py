from PIL import Image
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

async def agent_register(register_email,  pdf_file_path) -> None:
    async with async_playwright() as playwright:
        browser = await playwright.chromium.launch(headless=False)
        context = await browser.new_context()
        page = await context.new_page()
        await page.goto("http://balitax-test.com/tax-agent/balitax-user-register.html")
        await page.locator("span").filter(has_text="Bahasa").first.click()
        await page.get_by_role("link", name="English").click()
        await page.get_by_role("textbox", name="Company Name *").fill(register_email.split("@")[0])
        await page.get_by_role("textbox", name="Company Brand Name").fill("Company brand name")
        # await page.locator("b").click()
        await page.get_by_role("combobox", name="Please select").locator("span").nth(1).click()
        await page.get_by_role("treeitem", name="POS service providers").click()

        try:
            npwp = await generate_npwp()
            await page.get_by_role("textbox", name="NPWP *").fill(npwp)
            await page.keyboard.press("Tab")
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
        # await page.pause()
        page.on("filechooser", lambda f: f.set_files(pdf_file_path))
        await page.get_by_text("Business License").click()
        await page.get_by_text("Taxpayer Document (NPWP)").click()
        await page.get_by_text("Director Identity/Passport").click()
        await page.wait_for_timeout(3000)
        await page.get_by_role("button", name="Next").click()
    
        # 第二页
        await page.get_by_role("textbox", name="Admin Email *").fill(register_email)
        await page.get_by_role("button", name="Get Code").click()
    
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
    
        await get_email_code(username='xiaozehua',password='8qudcQifW7cjydglydm{')
        print('请填写邮箱验证码......')
        await page.pause()
        # await page.get_by_role("textbox", name="Email Verification Code *").fill("547099")
        await page.get_by_role("textbox", name="Password *", exact=True).fill("A123456@test")
        await page.get_by_role("textbox", name="Confirm Password *").fill("A123456@test")
        await page.evaluate('''() => {
                            const el = document.querySelector('input#customRadio3');
                            if(el) el.click() }''')

        await page.get_by_role("button", name="Confirm").click()
        # await page.get_by_role("button", name="I Understand").click()
        # 断言存在 i understand
        understand_button = page.get_by_role("button", name="I Understand")
        await expect(page.get_by_text("I Understand")).to_be_visible()
        if await understand_button.is_visible():
            await understand_button.click()
            print(f"agent {register_email} 注册成功")

        #删除‘email_code.png'文件
        # if os.path.exists("email_code.png"):
        #     os.remove("email_code.png")
        # else:
        #     print("email_code.png 文件不存在")
        # ---------------------
        await context.close()
        await browser.close()

# if __name__ == '__main__':
#     agent_register_email = "tax_agent0010@linshiyou.com"
#     BASE_DIR = os.path.dirname(os.path.abspath(__file__))
#     DATA_DIR = os.path.join(BASE_DIR, '../../../common', 'data')
#     pdf_file_path = os.path.join(DATA_DIR, "合同.pdf")
#
#     linux_username = 'xiaozehua'
#     linux_password = '8qudcQifW7cjydglydm{'
#
#     if not os.path.exists(pdf_file_path):
#         print('文件不存在')
#         exit()
#
#     asyncio.run(agent_register(agent_register_email))
    # 确保异步事件循环正确执行
    # try:
    #     asyncio.run(agent_register(agent_register_email))
    # except RuntimeError as e:
    #     if "Event loop is closed" in str(e):
    #         Windows系统需要特殊处理事件循环
            # asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
            # asyncio.run(agent_register(agent_register_email))
