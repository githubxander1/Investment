import asyncio
from playwright.async_api import async_playwright, expect
from tenacity import retry, stop_after_attempt
# from CompanyProject.巴迪克.Payok.api_framework.generate_orderId import merchant_id
from CompanyProject.巴迪克.utils.GoogleSecure import CalGoogleCode
from CompanyProject.巴迪克.utils.generate_google_code import GoogleAuthenticator


@retry(stop=stop_after_attempt(3))
async def perform_block_slider_verification(page):
    """适用于新版滑块验证的处理函数"""
    # 等待滑块组件加载
    await page.wait_for_selector('#mpanel2 .verify-move-block', state='visible')

    # 获取滑块元素和轨道
    slider_handle = page.locator('#mpanel2 .verify-move-block')
    slider_track = page.locator('#mpanel2 .verify-bar-area')

    # 获取轨道尺寸
    track_box = await slider_track.bounding_box()

    try:
        # 执行滑块拖动（横向移动）
        await slider_handle.drag_to(
            slider_handle,
            force=True,
            target_position={
                "x": track_box['width'] - 10,  # 移动到轨道右端
                "y": track_box['height'] / 2
            },
            timeout=5000
        )

        # 验证成功检查
        success = await page.evaluate('''() => {
            // 精确匹配成功状态的元素
            const successElement = document.querySelector(
                '#mpanel2 .verify-left-bar .verify-msg[langkey="verify_successfully"]'
            );

            // 双重验证机制
            return !!successElement && 
                (successElement.innerText.includes('Verify Successfully') || 
                 document.querySelector('#mpanel2 .verify-move-block').style.left === '280px');
        }''')

        if not success:
            raise Exception("滑块验证未成功")

    except Exception as e:
        print(f"滑块验证失败: {str(e)}")
        await page.screenshot(path='slider_failure.png')
        raise


async def platform_login(page, login_email: str):
    """平台登录逻辑"""
    await page.goto("http://balitax-test.com/tax-platform/balitax-user-login.html")
    # 如果不是英语环境，则切换为英语环境
    if await page.query_selector("span:has-text('Bahasa')"):
        await page.locator("span").filter(has_text="Bahasa").first.click()
        await page.get_by_role("link", name="English").click()
        # return
    await page.get_by_role("textbox", name="Email").fill(login_email)
    await page.get_by_role("textbox", name="Password").fill("A123456@test")
    await perform_block_slider_verification(page)
    await page.get_by_role("button", name="Log In").click()

    @retry(stop=stop_after_attempt(3))
    async def get_google_code():
        agent_google_code = GoogleAuthenticator.generate(
            environment='test',
            project='tax',
            table='tax_operator',
            login_name=login_email
        )
        await page.locator("#googleCode").fill(agent_google_code)

        if await page.query_selector(".error-message:visible"):
            await page.get_by_role("textbox", name="Google Verification Code").clear()
            raise ValueError("谷歌验证码错误")

    await get_google_code()
    await page.get_by_role("button", name="Log In").click()


async def audit_agent(page,  login_email: str):
    """审核 Agent 模块"""
    await page.get_by_role("link", name="* Merchant ").click()
    await page.get_by_role("link", name="Agent").click()


    # 审核agent
    # 获取agent状态
    agent_id = await page.locator("//*[@id='profit-datatable']/tbody/tr[1]/td[1]").text_content()
    agent_name = await page.locator("//*[@id='profit-datatable']/tbody/tr[1]/td[2]").text_content()
    agent_status = await page.locator('//*[@id="profit-datatable"]/tbody/tr[1]/td[4]/span').text_content()

    # print(f"商户 {agent_name}, id:{agent_id} 状态为: {agent_status}")
    # first_row = page.locator("//*[@id='profit-datatable']/tbody/tr[1]")
    # # 获取商户信息
    # # merchant_id = await first_row.locator("td[1]").text_content()
    # agent_id = await first_row.locator("td").nth(2).text_content()
    # # merchant_id = await first_row.locator("xpath=//td[1]").text_content()
    #
    # agent_name = await first_row.locator("td").nth(3).text_content()
    # # status_locator = first_row.locator("td[5]/span")
    # # merchant_status = await status_locator.text_content()
    # agent_status = await page.locator("//*[@id='profit-datatable']/tbody/tr[1]/td[5]/span").text_content()

    if agent_status == "Enable":
        print(f"agent {agent_name}, id:{agent_id} 状态为: {agent_status}，不需要审核")
        # return agent_id
    else:
        # 点击审核按钮
        # await page.locator(".DTFC_RightBodyLiner > .table > tbody > tr > td > button:nth-child(2)").first.click()

        # approve_button = page.get_by_role("button", name="Approve")
        try:
            await page.get_by_text("Review", exact=True).nth(1).click()
            await page.get_by_role("button", name="Approve").click()
        except Exception as e:
            print(f"审核失败: {str(e)}")
            await page.screenshot(path='audit_failure.png')
            raise
        # await approve_button.scroll_into_view_if_needed(timeout=2000)
        # await approve_button.click()

        # 验证审核成功提示
        await expect(page.get_by_text("Success", exact=True)).to_be_visible()

        # 重新获取更新后的商户状态
        updated_status = await page.locator('//*[@id="profit-datatable"]/tbody/tr[1]/td[4]/span').text_content()
        assert updated_status == "Enable", f"预期状态为 'Enable'，实际为 '{updated_status}'"
        print(f"agent {agent_name}, id:{agent_id} 状态为: {updated_status}")

        # print(f"商户 {agent_name}, id:{agent_id} 状态为: {agent_status}")
        # return merchant_id

        # 如果agent状态是Enable，则生成并数据库填入google_secret_key
        if updated_status == "Enable":
            CalGoogleCode.update_google_secret_key_in_db(
                environment='test',
                project='tax',
                table='agent_operator',
                login_name=login_email
            )
    # try:
    #     await page.get_by_text("Review", exact=True).nth(1).click()
    #     await page.get_by_role("button", name="Approve").click()
    # except Exception as e:
    #     print(f"审核失败: {str(e)}")
    #     await page.screenshot(path='audit_failure.png')
    #     raise
    # page.locator("tbody").filter(has_text="View Review View Blocked").locator("button[name=\"btnReview\"]").click()
    # await page.locator(".DTFC_RightBodyLiner > .table > tbody > tr > td > button").first.click()
    #
    # # 获取agent状态
    # agent_id = await page.locator("//*[@id='profit-datatable']/tbody/tr[1]/td[1]").text_content()
    # agent_name = await page.locator("//*[@id='profit-datatable']/tbody/tr[1]/td[2]").text_content()
    # agent_status = await page.locator('//*[@id="profit-datatable"]/tbody/tr[1]/td[4]/span').text_content()
    #
    # print(f"商户 {agent_name}, id:{agent_id} 状态为: {agent_status}")
    # assert agent_status == "Enable", f"预期状态为 'Enable'，实际为 '{agent_status}'"



async def audit_merchant(page):
    """审核 Merchant 模块"""
    await page.get_by_role("link", name="* Merchant ").click()
    await page.locator("#left-bar-menu").get_by_role("link", name="Merchant", exact=True).click()

    # merchant_id = await page.locator("//*[@id='profit-datatable']/tbody/tr[1]/td[1]").text_content()
    first_row = page.locator("//*[@id='profit-datatable']/tbody/tr[1]")

    # 获取商户信息
    # merchant_id = await first_row.locator("td[1]").text_content()
    merchant_id = await first_row.locator("td").nth(2).text_content()
    # merchant_id = await first_row.locator("xpath=//td[1]").text_content()

    merchant_name = await first_row.locator("td").nth(3).text_content()
    # status_locator = first_row.locator("td[5]/span")
    # merchant_status = await status_locator.text_content()
    merchant_status = await page.locator("//*[@id='profit-datatable']/tbody/tr[1]/td[5]/span").text_content()
    # merchant_status = page.locator("#profit-datatable tbody tr:first-child td:nth-child(5) span").text_content(

    if merchant_status == "Enable":
        print(f"商户 {merchant_name}, id:{merchant_id} 状态为: {merchant_status}，不需要审核")
        return merchant_id
    else:
        # 点击审核按钮
        await page.locator(".DTFC_RightBodyLiner > .table > tbody > tr > td > button:nth-child(2)").first.click()
        approve_button = page.get_by_role("button", name="Approve")
        await approve_button.scroll_into_view_if_needed(timeout=2000)
        await approve_button.click()

        await expect(page.get_by_text("Success", exact=True)).to_be_visible()

        # 重新获取更新后的商户状态
        await page.wait_for_timeout(1000)
        updated_status = await page.locator("//*[@id='profit-datatable']/tbody/tr[1]/td[5]/span").text_content()
        assert updated_status == "Enable", f"预期状态为 'Enable'，实际为 '{updated_status}'"
        print(f"商户 {merchant_name}, id:{merchant_id} 状态为: {merchant_status}")
        return merchant_id


# if __name__ == '__main__':
    # login_email = "tax_operator@test.com"

    # 自定义要执行的功能模块
    # asyncio.run(platform_login(
    #     login_email=login_email,
    #     do_login=True,
    #     do_audit_agent=True,
    #     do_audit_merchant=False
    # ))
