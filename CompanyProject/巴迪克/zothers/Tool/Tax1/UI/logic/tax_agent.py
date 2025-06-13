from playwright.async_api import async_playwright, expect

from CompanyProject.巴迪克.zothers.generate_google_code import GoogleAuthenticator
from tenacity import retry, stop_after_attempt

@retry(stop=stop_after_attempt(3))
async def perform_block_slider_verification_new(page):
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

async def agent_login(page, login_email: str) -> None:
    await page.goto("http://balitax-test.com/tax-agent/balitax-user-login.html")
    await page.locator("span").filter(has_text="Bahasa").first.click()
    await page.get_by_role("link", name="English").click()
    await page.get_by_role("textbox", name="Email").fill(login_email)
    await page.get_by_role("textbox", name="Password").fill("A123456@test")

    await perform_block_slider_verification_new(page)
    await page.get_by_role("button", name="Log In").click()
    await page.wait_for_timeout(1000)

    @retry(stop=stop_after_attempt(3))
    async def get_google_code():
        google_code = GoogleAuthenticator.generate(
            environment='test',
            project='tax',
            table='agent_operator',
            login_name=login_email
        )
        await page.locator("#googleCode").fill(google_code)

        if await page.query_selector(".error-message:visible"):
            await page.get_by_role("textbox", name="Google Verification Code").clear()
            raise ValueError("谷歌验证码错误")

    await get_google_code()
    await page.get_by_role("button", name="Log In").click()


async def create_merchant(page) -> None:
    # await page.goto("http://balitax-test.com/tax-agent/balitax-user-login.html")
    # await page.locator("span").filter(has_text="Bahasa").first.click()
    # await page.get_by_role("link", name="English").click()

    # 注册商户流程
    # await page.pause()
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
    file_path = '../../../../../common/data/合同.pdf'
    page.on("filechooser", lambda file_chooser: file_chooser.set_files(file_path))
    await page.locator("#form1 i").click()
    await page.locator("#form2 i").click()
    await page.locator("#form3 i").click()

    await page.wait_for_timeout(3000)
    try:
        await page.get_by_role("button", name="Submit Registration").click()
        await expect(page.locator("h3")).to_contain_text("Registration submitted successfully")
        await page.get_by_role("button", name="I Understand").click()
        # 获取注册后的信息
        merchant_id = await page.locator('//*[@id="profit-datatable"]/tbody/tr[1]/td[1]').text_content()
        merchant_name = await page.locator('//*[@id="profit-datatable"]/tbody/tr[1]/td[2]').text_content()
        merchant_status = await page.locator('//*[@id="profit-datatable"]/tbody/tr[1]/td[4]/span').text_content()
        print(f"merchant注册成功：名称：{merchant_name}，id: {merchant_id}，状态：{merchant_status}")
        # print("✅ ")
        return merchant_id
    except Exception as e:
        print(f"merchant注册失败: {str(e)}")
        await page.screenshot(path='merchant_create_failure.png')
        raise



async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context()
        page = await context.new_page()

        try:
            await agent_login(page, "tax_agent009@linshiyou.com")
            await create_merchant(page)
        finally:
            await context.close()
            await browser.close()


# if __name__ == '__main__':
#     asyncio.run(main())
