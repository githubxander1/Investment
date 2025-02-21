# from playwright.sync_api import sync_playwright
#
# with sync_playwright() as p:
#     # 如果使用参数headless = False，那么浏览器不会启动，会以无头模式运行脚本。
#     browser = p.chromium.launch(channel="msedge",headless=False)
#     # browser = p.chromium.launch(channel="chrome"，headless = False)
#     # browser = p.webkit.launch(headless=False)
#     pom = browser.new_page()
#     pom.goto('http://www.baidu.com')
#     print(pom.title)
#     # browser.close()

# 同步模式:
# with sync_playwright() as p:
#     brower=p.chromium.launch(channel='msedge',headless=False)
#     page =brower.new_page()
#     page.goto('http://www.163.com')
#     print(page.title)
#     brower.close()
#
# async def main():
#     async with sync_playwright() as p:
#         brower=p.chromium.launch(channel='msedge',headless=False)
#         page = brower.new_page()
#         page.goto('http://www.163.com')
#         brower.close()
# asyncio.run(main())

from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()
    page.goto('https://www.baidu.com')

    # 在这里可以暂停脚本执行，以便在 UI 中进行元素定位
    page.pause()

    browser.close()