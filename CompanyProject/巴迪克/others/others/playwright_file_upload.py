import asyncio
import os

from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()
        await page.goto('https://the-internet.herokuapp.com/upload')
        await page.wait_for_selector("#file-upload")

        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

        # 文件路径配置
        DATA_DIR = os.path.join(BASE_DIR, 'data')
        filepath = os.path.join(DATA_DIR, "法人护照.doc")
        print('文件存在' if os.path.exists(filepath) else '文件不存在')

        # 监听 file_chooser 事件
        async def handle_file_chooser(file_chooser):
            # 选择要上传的文件
            await file_chooser.set_files(filepath)

        # 设置文件选择器事件监听器
        page.on('filechooser', handle_file_chooser)

        # 触发文件选择框点击事件
        await page.locator("#file-upload").click()

        # 等待文件上传完成（可根据实际情况调整等待条件）
        await page.wait_for_timeout(5000)

        # 点击上传按钮
        await page.locator('input[type="submit"]').click()

        # 验证上传是否成功
        uploaded_file_name = await page.locator("#uploaded-files").text_content()
        if uploaded_file_name == "法人护照.doc":
            print("文件上传成功")
        else:
            print("文件上传失败")

        await page.pause()
        # 关闭浏览器
        # await browser.close()

asyncio.run(main())
