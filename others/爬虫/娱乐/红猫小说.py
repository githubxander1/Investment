import asyncio

from playwright.async_api import async_playwright


async def main():
    async with async_playwright() as p:
        # 启动Chromium浏览器，headless=True表示无头模式
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        # 访问目标网页
        await page.goto('https://fylhfyullx.top:2568/txtdetail/9546226.html')
        # 提取class为nobdys元素的文本内容
        # content = await page.inner_text('.nobdys')
        # 定位css选择器定位下的文本
        title = await page.inner_text('#app_hm > div.layouts > div.newsbody > div.title')
        content = await page.inner_text('#app_hm > div.layouts > div.newsbody > div.nbodys')
        print(title)
        print(content)
        # 将内容保存为txt文件
        with open('小说1.txt', 'w', encoding='utf-8') as f:
            f.write(content)
        await browser.close()


if __name__ == '__main__':
    asyncio.run(main())