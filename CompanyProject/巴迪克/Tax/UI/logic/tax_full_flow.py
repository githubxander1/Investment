# main.py - 全流程主入口

import asyncio
import datetime
import os
from pprint import pprint

from faker import Faker
from playwright.async_api import async_playwright

from CompanyProject.巴迪克.Tax.UI.logic.tax_agent_register import agent_register
from CompanyProject.巴迪克.Tax.UI.logic.tax_agent import agent_login, create_merchant
from CompanyProject.巴迪克.Tax.UI.logic.tax_platform_audit import platform_login, audit_agent, audit_merchant
from CompanyProject.巴迪克.Tax.Api.create import CreateOrderAPI
from CompanyProject.巴迪克.Tax.Api.cancel import CancelOrderAPI

fake = Faker()

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
                print("✅ Agent注册完成\n")

            # 2️⃣ 登录平台并审核Agent（可选）
            if do_audit_agent:
                print("🔄 开始platform登录并审核Agent")
                await platform_login(page, login_email)
                await audit_agent(page, agent_email)
                print("✅ Agent审核完成\n")

            # 3️⃣ Agent登录并创建Merchant（可选）
            if do_create_merchant:
                print("🔄 开始Agent登录并创建merchant")
                await agent_login(page, agent_email)
                await create_merchant(page)
                print("✅ merchant创建完成\n")

            # 4️⃣ 登录平台并审核Merchant（可选）
            if do_audit_merchant:
                print("🔄 开始平台登录并审核merchant")
                await platform_login(page, login_email)
                merchant_id = await audit_merchant(page)
                print("✅ merchant审核完成\n")

            # 5️⃣ 创建订单（可选）
            if do_create_order:
                print("🔄 开始创建订单")
                if not merchant_id:
                    raise ValueError("merchant_id 未定义，请先执行 do_audit_merchant=True 获取 merchant_id")

                company_name = agent_email.split("@")[0]
                create_api = CreateOrderAPI(company_name)
                today = datetime.datetime.now().strftime("%Y%m%d")
                # order_suffix = f"{n:03d}"
                # agentOrderNo = f"AgentOrderNo{today}{n}"
                # payOrderNo = f"PayOrder{today}{n}"
                order_no = fake.random_int(min=1, max=1000)
                payload = {
                        "merchantId": merchant_id,
                        "paymentType": "StaticMandiriVA",
                        "amount": "999999999999.99",
                        "agentOrderNo": f"AgentOrderNo{today}{order_no}",
                        "payOrderNo": f"PayOrder{today}{order_no}",
                        "sourceAgentOrderNo": "AgentOrderNo20250516817",
                        "productName": fake.name(),
                        "requestId": "1"
                    }
                result = create_api.create_order(payload)
                AgentOrderNo = result["agentOrderNo"]
                print("✅ 订单创建成功\n")

            # 6️⃣ 撤销订单（可选）
            if do_cancel_order:
                print("🔄 开始撤销订单")
                cancel_api = CancelOrderAPI(company_name)
                cancel_payload = {
                    # "agentOrderNo": "AgentOrderNo20250516305",
                    "agentOrderNo": AgentOrderNo,
                    "requestId": "19999999999999999999"
                }
                result = cancel_api.cancel_order(cancel_payload)
                print("✅ 订单撤销成功\n")

        finally:
            await context.close()
            await browser.close()


if __name__ == '__main__':
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    DATA_DIR = os.path.join(BASE_DIR, '../../../common', 'data')
    pdf_file_path = os.path.join(DATA_DIR, "合同.pdf")

    asyncio.run(run_full_flow(
        login_email="tax_operator@test.com",
        agent_email="tax_agent002@linshiyou.com",
        do_register_agent=True,
        do_audit_agent=False,
        do_create_merchant=False,
        do_audit_merchant=False,
        do_create_order=False,
        do_cancel_order=False
    ))
