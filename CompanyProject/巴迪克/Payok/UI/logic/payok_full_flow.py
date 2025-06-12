import os
from pathlib import Path

from playwright.sync_api import sync_playwright

# 导入各个步骤的函数
from CompanyProject.巴迪克.Payok.UI.logic.payok_merchant_register import payok_register
from CompanyProject.巴迪克.Payok.UI.logic.payok_merchant_login import merchant_login
from CompanyProject.巴迪克.Payok.UI.logic.payok_platform_login import platform_login
# from CompanyProject.巴迪克.Payok.UI.logic.payok_audit import payok_merchant_audio


def run_payok_full_flow(
    register_email: str,
    merchant_name: str,
    login_password: str,
    operator_login_name: str,
    upload_filepath: str,
    do_register_merchant: bool = True,
    do_merchant_login: bool = True,
    do_platform_login: bool = True,
    do_audit: bool = True
):
    """
    Payok 完整业务流程：
    注册 Merchant → 登录 Merchant → 登录 Platform → 审核商户 → 上线操作
    """

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context(no_viewport=True)
        page = context.new_page()
        page.set_default_timeout(10000)

        try:
            print("📄 开始执行 Payok 完整业务流程...")

            # 1️⃣ 注册商户
            if do_register_merchant:
                print("🔄 正在注册商户...")
                payok_register(page, register_email, merchant_name, PDF_FILE_PATH)
                print("✅ 商户注册完成\n")

            # 2️⃣ 商户登录
            if do_merchant_login:
                print("🔄 正在进行商户登录...")
                merchant_login(page, register_email, login_password)
                print("✅ 商户登录完成\n")

            # 3️⃣ 平台端登录
            if do_platform_login:
                print("🔄 正在进行平台端登录...")
                platform_login(page, operator_login_name, "A123456@test")
                print("✅ 平台端登录完成\n")

            # 4️⃣ 商户审核与上线
            # if do_audit:
            #     print("🔄 正在进行商户审核与上线操作...")
            #     with sync_playwright() as playwright:
            #         payok_merchant_audio(playwright, operator_login_name, merchant_name)
            #     print("✅ 商户审核与上线完成\n")

        finally:
            context.close()
            browser.close()


if __name__ == "__main__":
    # 设置基础路径和文件路径
    BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent
    PDF_FILE_PATH = os.path.join(BASE_DIR, "common", "data", "合同.pdf")
    if not os.path.exists(PDF_FILE_PATH):
        print(f"文件不存在: {PDF_FILE_PATH}")
        exit(1)

    # 测试参数配置
    REGISTER_EMAIL = "payok_merchant001@test.com"
    MERCHANT_NAME = REGISTER_EMAIL.split("@")[0]
    LOGIN_PASSWORD = "A123456@test"
    OPERATOR_LOGIN_NAME = "2695418206@qq.com"

    # 执行完整流程
    run_payok_full_flow(
        register_email=REGISTER_EMAIL,
        merchant_name=MERCHANT_NAME,
        login_password=LOGIN_PASSWORD,
        operator_login_name=OPERATOR_LOGIN_NAME,
        upload_filepath=PDF_FILE_PATH,

        do_register_merchant=True,
        do_merchant_login=False,
        do_platform_login=True,
        do_audit=False
    )
