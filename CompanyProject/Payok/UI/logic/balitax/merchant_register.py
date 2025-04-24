import os
import re
from PIL import Image
from playwright.sync_api import Playwright, sync_playwright, expect
import random
import pytesseract

# 设置Tesseract路径
pytesseract.pytesseract.tesseract_cmd = r'D:\Xander\Applications\TesseractOCR\tesseract.exe'

def generate_npwp():
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

def recognize_captcha(image_path):
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

def merchant_register(playwright: Playwright, register_email) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("http://balitax-test.com/tax-agent/balitax-user-register.html")
    page.locator("span").filter(has_text="Bahasa").first.click()
    page.get_by_role("link", name="English").click()
    page.get_by_role("textbox", name="Company Name *").fill(register_email)
    page.get_by_role("textbox", name="Company Brand Name").fill("Company brand name")
    page.locator("b").click()
    page.get_by_role("treeitem", name="POS service providers").click()

    max_retries = 5
    for attempt in range(max_retries):
        npwp = generate_npwp()
        page.get_by_role("textbox", name="NPWP *").fill(npwp)

        # 触发验证（根据实际页面验证方式调整）
        page.keyboard.press("Tab")

        try:
            # 检查错误提示是否存在（根据实际错误提示调整选择器）
            expect(page.get_by_text("NPWP already exists")).not_to_be_visible(timeout=2000)
            break
        except AssertionError:
            if attempt == max_retries - 1:
                raise Exception("生成唯一NPWP失败，已达最大重试次数")
            continue

    page.get_by_role("textbox", name="Official Website *").fill("www.baidu.com")
    page.get_by_role("textbox", name="Company Address *").fill("广东省深圳市南山区桃源街道xx号")
    page.get_by_role("textbox", name="Company Legal Person (").fill("张三")
    page.get_by_role("textbox", name="Legal Person (Responsible Person) Contact Number *").fill("15318544154")
    page.get_by_role("textbox", name="Legal Person (Responsible Person) Address *").fill("广东省深圳市南山区桃源街道法人地址001号")
    page.get_by_role("textbox", name="Contact Person *").fill("李四")
    page.get_by_role("textbox", name="Contact Person's Number *").fill("15318544154")
    page.pause()
    page.on("filechooser", lambda f: f.set_files(pdf_file_path))
    page.get_by_text("Business License").click()
    page.get_by_text("Taxpayer Document (NPWP)").click()
    page.get_by_text("Director Identity/Passport").click()
    page.wait_for_timeout(1000)
    page.pause()

    page.get_by_role("button", name="Next").click()

    # 第二页
    page.pause()
    page.get_by_role("textbox", name="Admin Email *").fill(register_email)
    page.get_by_role("button", name="Send Verification Code").click()

    # 捕获并识别验证码
    captcha_img_path = "captcha.png"
    page.locator("#imgCode").screenshot(path=captcha_img_path)
    captcha_text = recognize_captcha(captcha_img_path)
    print("识别的验证码:", captcha_text)

    # 输入验证码
    page.locator("#txtVerificationCode").fill(captcha_text)

    page.pause()
    page.locator("#submitBtn").click()

    # 检查验证码是否正确
    try:
        expect(page.locator(".verification")).to_have_class("text-red verification d-none", timeout=2000)
    except AssertionError:
        print("验证码输入错误，正在重新尝试...")
        # 如果验证码错误，清空输入框并重新识别
        page.locator("#txtVerificationCode").clear()
        page.locator("#imgCode").click()  # 刷新验证码图片
        page.locator("#imgCode").screenshot(path=captcha_img_path)
        captcha_text = recognize_captcha(captcha_img_path)
        print("重新识别的验证码:", captcha_text)
        page.locator("#txtVerificationCode").fill(captcha_text)
        page.locator("#submitBtn").click()

    page.get_by_role("textbox", name="Email Verification Code *").fill("547099")
    page.get_by_role("textbox", name="Password *", exact=True).fill("A123456@test")
    page.get_by_role("textbox", name="Confirm Password *").fill("A123456@test")
    page.get_by_role("button", name="Confirm").click()


    # ---------------------
    context.close()
    browser.close()

if __name__ == '__main__':
    merchant_register_email = "2@tax.com"

    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    DATA_DIR = os.path.join(BASE_DIR, '../..', 'data')
    pdf_file_path = os.path.join(DATA_DIR, "合同.pdf")
    # 判断文件是否存在
    if not os.path.exists(pdf_file_path):
        print('文件不存在')
        exit()

    with sync_playwright() as playwright:
        merchant_register(playwright, merchant_register_email)
