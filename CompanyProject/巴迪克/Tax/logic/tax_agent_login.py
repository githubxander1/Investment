# tax_agent_login.py
import asyncio
from playwright.async_api import async_playwright  # 使用异步API
from CompanyProject.巴迪克.utils.generate_google_code import GoogleAuthenticator
# from CompanyProject.巴迪克.utils.perform_slider_unlock import perform_block_slider_verification
from tenacity import retry, stop_after_attempt

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


async def agent_login(login_email: str) -> None:
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context()
        page = await context.new_page()

        await page.goto("http://balitax-test.com/tax-agent/balitax-user-login.html")
        # await page.goto("http://balitax-test.com/tax-platform/balitax-user-login.html")
        await page.locator("span").filter(has_text="Bahasa").first.click()
        await page.get_by_role("link", name="English").click()

        await page.get_by_role("textbox", name="Email").fill(login_email)
        await page.get_by_role("textbox", name="Password").fill("A123456@test")

        await page.pause()
        # 异步滑块验证

        await perform_block_slider_verification(page)

        await page.get_by_role("button", name="Log In").click()
        await page.wait_for_timeout(1000)  # 替代pause()

        @retry(stop=stop_after_attempt(3))
        async def get_google_code():
            agent_google_code = GoogleAuthenticator.generate(
                environment='test',
                project='tax',
                table='agent_operator',
                login_name=login_email
            )
            # await page.get_by_role("textbox", name="Google Verification Code").fill(agent_google_code)
            await page.locator("#googleCode").fill(agent_google_code)

            # 更可靠的错误检测
            if await page.query_selector(".error-message:visible"):
                await page.get_by_role("textbox", name="Google Verification Code").clear()
                raise ValueError("谷歌验证码错误")

        await get_google_code()
        await page.get_by_role("button", name="Log In").click()
        await page.pause()

        # 关闭浏览器
        await context.close()
        await browser.close()

if __name__ == '__main__':
    login_email  = "1@qq.com"
    asyncio.run(agent_login(login_email))
    print("登录成功")
