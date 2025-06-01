# agent_login_and_create_merchant.py

import asyncio
from playwright.async_api import async_playwright, expect
from CompanyProject.巴迪克.Tax.UI.common import get_google_code
from CompanyProject.巴迪克.Tax.UI.common import perform_block_slider_verification
from tenacity import retry, stop_after_attempt





async def agent_login_and_create_merchant(login_email: str) -> None:
    async with async_playwright() as p:
        # 启动浏览器
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context()
        page = await context.new_page()

        # 1️⃣ 登录部分
        await page.goto("http://balitax-test.com/tax-agent/balitax-user-login.html")
        await page.locator("span").filter(has_text="Bahasa").first.click()
        await page.get_by_role("link", name="English").click()
        await page.get_by_role("textbox", name="Email").fill(login_email)
        await page.get_by_role("textbox", name="Password").fill("A123456@test")

        await perform_block_slider_verification(page)
        await page.get_by_role("button", name="Log In").click()
        await page.wait_for_timeout(1000)

        # 填写谷歌验证码
        await get_google_code(page, login_email)
        await page.get_by_role("button", name="Log In").click()
        await page.wait_for_load_state("networkidle")
        print("✅ 登录成功")

        # 2️⃣ 注册商户部分
        await page.wait_for_timeout(1000)

        # 开始注册商户
        await page.get_by_role("link", name="* Merchant ").click()
        await page.get_by_role("link", name="Merchant", exact=True).click()
        await page.get_by_role("button", name=" Register Merchant").click()

        # 填写表单
        await page.get_by_role("textbox", name="Merchant Name *").fill("霸王茶姬")
        await page.get_by_role("textbox", name="Merchant Brand Name").fill("霸王")

        await page.locator("#full-width-modal b").click()
        await page.get_by_role("treeitem", name="[1520]Property").click()

        await page.get_by_role("textbox", name="Company Legal Person Name *").fill("张三")
        await page.get_by_role("textbox", name="NPWP *").fill("11.111.111.1-111.11111")
        await page.get_by_role("textbox", name="Merchant Address *").fill("美国白宫1号")
        await page.get_by_role("textbox", name="Contact Person *").fill("李四")
        await page.get_by_role("textbox", name="Contact phone number *").fill("11111111111111111111")

        # 文件上传
        file_path = '../../../common/data/合同.pdf'
        page.on("filechooser",  lambda file_chooser: file_chooser.set_files(file_path))
        await page.locator("#form1 i").click()
        await page.locator("#form2 i").click()
        await page.locator("#form3 i").click()
        # async with page.expect_file_chooser() as fc_info:
        #     await page.locator("#form1 i").click()
        # file_chooser = await fc_info.value
        # await file_chooser.set_files(file_path)

        await page.wait_for_timeout(3000)
        await page.get_by_role("button", name="Submit Registration").click()
        await expect(page.locator("h3")).to_contain_text("Registration submitted successfully")
        await page.get_by_role("button", name="I Understand").click()
        print("✅ 商户注册提交成功")

        #获取注册后的id
        merchant_id = await page.locator('//*[@id="profit-datatable"]/tbody/tr[1]/td[1]').text_content()
        # merchant_id = await page.locator('#profit-datatable tbody tr:first-child td:first-child').text_content()

        print(f"刚注册的merchant id: {merchant_id}")

        await page.pause()

        # 关闭资源
        await context.close()
        await browser.close()


if __name__ == '__main__':
    login_email = "tax_agent009@linshiyou.com"
    asyncio.run(agent_login_and_create_merchant(login_email))
