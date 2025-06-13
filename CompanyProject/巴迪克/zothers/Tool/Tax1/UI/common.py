from CompanyProject.巴迪克.zothers.generate_google_code import GoogleAuthenticator
from tenacity import retry, stop_after_attempt

@retry(stop=stop_after_attempt(3))
async def perform_block_slider_verification(page):
    """滑块验证逻辑"""
    await page.wait_for_selector('#mpanel2 .verify-move-block', state='visible')
    slider_handle = page.locator('#mpanel2 .verify-move-block')
    slider_track = page.locator('#mpanel2 .verify-bar-area')
    track_box = await slider_track.bounding_box()

    try:
        await slider_handle.drag_to(
            slider_handle,
            force=True,
            target_position={"x": track_box['width'] - 10, "y": track_box['height'] / 2},
            timeout=5000
        )

        success = await page.evaluate('''() => {
            const successElement = document.querySelector(
                '#mpanel2 .verify-left-bar .verify-msg[langkey="verify_successfully"]');
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


@retry(stop=stop_after_attempt(3))
async def get_google_code(page, login_email):
    """获取并填写谷歌验证码"""
    agent_google_code = GoogleAuthenticator.generate(
        environment='test',
        project='tax',
        table='agent_operator',
        login_name=login_email
    )
    await page.locator("#googleCode").fill(agent_google_code)

    if await page.query_selector(".error-message:visible"):
        await page.locator("#googleCode").clear()
        raise ValueError("谷歌验证码错误")