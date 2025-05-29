# paylabs_full_flow.py - Paylabs 完整业务流程入口

import os

from playwright.sync_api import sync_playwright

# 从项目结构中导入相关模块
#     paylabs_merchant_register,
from CompanyProject.巴迪克.Paylabs.UI.paylabs_MerchantRegisterAndaudio import (
    sales_login,
    sales_setting_sales,
    sales_submit_info,
    platform_login,
    platform_risk_control_audit,
    platform_legal_risk_audit,
    platform_request_activation,
    platform_activation_audit
)
from CompanyProject.巴迪克.Paylabs.UI.paylabs_merchant_register import paylabs_merchant_register


def run_paylabs_full_flow(
    register_email: str,
    sales_login_name: str,
    operator_login_name: str,
    pdf_file_path: str,
    do_register_agent: bool = True,
    do_sales_login: bool = True,
    do_sales_setting: bool = True,
    do_submit_info: bool = True,
    do_platform_login: bool = True,
    do_risk_audit: bool = True,
    do_legal_audit: bool = True,
    do_request_activation: bool = True,
    do_activation_audit: bool = True
):
    """
    Paylabs 完整业务流程：
    注册Agent → Sales登录 → Sales提交资料 → 平台登录 → 风控审核 → 法律审核 → 激活请求 → 激活审核
    """

    with sync_playwright() as p:
        browser =  p.chromium.launch(headless=False)
        context =  browser.new_context()
        page =  context.new_page()

        try:
            merchant_id = "010329"  # 初始化 merchant_id

            # 1️⃣ 注册 Agent（可选）
            if do_register_agent:
                print("🔄 开始注册 Agent")
                paylabs_merchant_register(p, register_email, pdf_file_path)
                print("✅ Agent 注册完成\n")

            # 2️⃣ Sales 登录（可选）
            if do_sales_login:
                print("🔄 开始 Sales 登录")
                sales_login(page, sales_login_name)
                print("✅ Sales 登录成功\n")

            # 3️⃣ 获取 Merchant ID 并设置 Sales（可选）
            if do_sales_setting:
                print("🔄 开始设置 Sales")
                with page.expect_popup() as popup_info:
                    page.get_by_role("link", name=" Merchant ").click()
                    page.locator("#left-bar-menu").get_by_role("link", name="Merchant", exact=True).click()
                    page.wait_for_timeout(1000)

                page = popup_info.value
                merchant_id =  page.locator('//*[@id="merchant-datatable"]/tbody/tr[1]/td[1]').text_content()
                print(f"✅ 获取 Merchant ID: {merchant_id}")

                sales_setting_sales(page, merchant_id)
                print("✅ Sales 设置完成\n")

            # 4️⃣ 提交商户资料（可选）
            if do_submit_info:
                print("🔄 开始提交商户资料")
                sales_submit_info(page, register_email, merchant_id,  pdf_file_path)
                print("✅ 商户资料提交成功\n")

            # 5️⃣ 平台登录（可选）
            if do_platform_login:
                print("🔄 开始平台登录")
                platform_login(page, operator_login_name)
                print("✅ 平台登录成功\n")

            # 6️⃣ 风险审核（可选）
            if do_risk_audit:
                print("🔄 开始风险审核")
                platform_risk_control_audit(page, merchant_id, pdf_file_path)
                print("✅ 风险审核完成\n")

            # 7️⃣ 法律风控审核（可选）
            if do_legal_audit:
                print("🔄 开始法律风控审核")
                platform_legal_risk_audit(page, merchant_id, pdf_file_path)
                print("✅ 法律风控审核完成\n")

            # 8️⃣ 激活请求（可选）
            if do_request_activation:
                print("🔄 开始激活请求")
                platform_request_activation(page, merchant_id)
                print("✅ 激活请求提交成功\n")

            # 9️⃣ 激活审核（可选）
            if do_activation_audit:
                print("🔄 开始激活审核")
                platform_activation_audit(page, merchant_id)
                print("✅ 激活审核通过，商户入驻完成！\n")

        finally:
            context.close()
            browser.close()


if __name__ == '__main__':
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    DATA_DIR = os.path.join(BASE_DIR, '../../common', 'data')
    pdf_file_path = os.path.join(DATA_DIR, "合同.pdf")

    run_paylabs_full_flow(
        register_email="tax_agent0010@linshiyou.com",
        sales_login_name="15318544153",
        operator_login_name="Xander@sitch.paylabs.co.id",
        pdf_file_path=pdf_file_path,

        do_register_agent=False,
        do_sales_login=False,
        do_sales_setting=False,
        do_submit_info=False,
        do_platform_login=True,
        do_risk_audit=False,
        do_legal_audit=True,
        do_request_activation=True,
        do_activation_audit=True
    )
