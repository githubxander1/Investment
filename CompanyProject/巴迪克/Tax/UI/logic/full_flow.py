# main.py - 全流程主入口

import asyncio
import os

from playwright.async_api import async_playwright

from CompanyProject.巴迪克.Tax.UI.logic.tax_agent_register import agent_register
from CompanyProject.巴迪克.Tax.UI.logic.tax_agent import agent_login, create_merchant
from CompanyProject.巴迪克.Tax.UI.logic.tax_platform_audit import platform_login, audit_agent, audit_merchant
from CompanyProject.巴迪克.Tax.Api.create import CreateOrderAPI
from CompanyProject.巴迪克.Tax.Api.cancel import CancelOrderAPI


async def run_full_flow(
    agent_email,
    login_email,
    do_register_agent: bool = True,
    do_audit_agent: bool = True,
    do_create_merchant: bool = True,
    do_audit_merchant: bool = True,
    do_create_order: bool = True,
    do_cancel_order: bool = True
):
    """
    完整业务流程：
    注册Agent → 平台审核Agent → Agent登录并创建商户 → 平台审核商户 → 创建订单 → 撤销订单
    """

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context()
        page = await context.new_page()

        try:
            # 1️⃣ 注册Agent（可选）
            if do_register_agent:
                print("🔄 开始注册Agent")
                await agent_register(agent_email, pdf_file_path)
                print("✅ Agent注册完成")

            # 2️⃣ 登录平台并审核Agent（可选）
            if do_audit_agent:
                print("🔄 开始平台登录并审核Agent")
                await platform_login(page, login_email)
                await audit_agent(page, agent_email)
                print("✅ Agent审核完成")

            # 3️⃣ Agent登录并创建Merchant（可选）
            if do_create_merchant:
                print("🔄 开始Agent登录并创建商户")
                await agent_login(page, agent_email)
                await create_merchant(page)  # 注意：create_merchant 需要传入 page
                print("✅ 商户创建完成")

            # 4️⃣ 登录平台并审核Merchant（可选）
            if do_audit_merchant:
                print("🔄 开始平台登录并审核商户")
                await platform_login(page, login_email)
                await audit_merchant(page)
                print("✅ 商户审核完成")

            # 5️⃣ 创建订单（可选）
            if do_create_order:
                print("🔄 开始创建订单")
                create_api = CreateOrderAPI()
                payload = {
                    "merchantId": create_merchant(page),
                    "paymentType": "StaticMandiriVA",
                    "amount": "999999999999.99",
                    "agentOrderNo": "AgentOrderNo20250516305",
                    "payOrderNo": "PayOrder20250516305",
                    "productName": "Test Product",
                    "requestId": "1"
                }
                result = create_api.create_order(payload)
                print("✅ 订单创建成功", result)

            # 6️⃣ 撤销订单（可选）
            if do_cancel_order:
                print("🔄 开始撤销订单")
                cancel_api = CancelOrderAPI()
                cancel_payload = {
                    "agentOrderNo": "AgentOrderNo20250516305",
                    "requestId": "19999999999999999999"
                }
                result = cancel_api.cancel_order(cancel_payload)
                print("✅ 订单撤销成功", result)

        finally:
            await context.close()
            await browser.close()


if __name__ == '__main__':
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    DATA_DIR = os.path.join(BASE_DIR, '../../../common', 'data')
    pdf_file_path = os.path.join(DATA_DIR, "合同.pdf")

    asyncio.run(run_full_flow(
        login_email="tax_operator@test.com",
        agent_email="tax_agent0012@linshiyou.com",
        do_register_agent=False,
        do_audit_agent=True,
        do_create_merchant=True,
        do_audit_merchant=True,
        do_create_order=True,
        do_cancel_order=True
    ))
