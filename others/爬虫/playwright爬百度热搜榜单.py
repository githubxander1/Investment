import asyncio
from bs4 import BeautifulSoup
from tabulate import tabulate
from playwright.async_api import async_playwright

# 定义异步主函数
async def main():
    results = []  # 用于存储所有爬取的结果
    timeout = 10  # 设置超时时间为10秒
    start_time = asyncio.get_event_loop().time()  # 获取当前时间

    try:
        # 初始化 Playwright
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=False)
            page = await browser.new_page()

            # 打开目标网站
            await page.goto('https://top.baidu.com/board?platform=wise&tab=realtime')

            # 查找所有的榜单项
            boards_locator = page.locator('._23KXyWDm2k2IInG-ul6YB-')
            boards_count = await boards_locator.count()
            print(f"发现 {boards_count} 榜单")  # 调试信息

            for i in range(boards_count):
                # 获取榜单名称
                board_name_locator = boards_locator.nth(i).locator('._2J4Ry1eOiqfvLWaAftNzNy')
                if await board_name_locator.count() > 0:
                    board_name = await board_name_locator.inner_text()
                    print(f"处理榜单: {board_name}")
                else:
                    print("榜单名称未找到，跳过")
                    continue

                # 点击跳转到具体的榜单页面
                await boards_locator.nth(i).click()
                await page.wait_for_load_state('networkidle')
                await asyncio.sleep(2)  # 增加延时，等待页面完全加载

                # 检查是否成功加载新的榜单内容
                if not await page.is_visible('.category-title'):
                    print("页面加载失败，跳过此榜单")
                    continue

                # 解析页面内容
                html_content = await page.content()
                soup = BeautifulSoup(html_content, 'html.parser')

                # 查找榜单中的新闻项目
                news_list = soup.find_all('div', class_='row-start-center zkwvwdF0VfxBzs7BSEZ1A')
                print(f"在榜单 {board_name} 中找到 {len(news_list)} 个新闻条目")

                for news in news_list:
                    order_num_tag = news.find('span', class_='_1DHjV0lKKB9gt0NdIKD2iH')
                    news_title_tag = news.find('span', class_='_38vEKmzrdqNxu0Z5xPExcg')

                    if order_num_tag and news_title_tag:
                        order_num = order_num_tag.text.strip()
                        news_title = news_title_tag.text.strip()
                        results.append([board_name, order_num, news_title])
                    else:
                        print("排名或新闻标题未找到，跳过此条目")

            await browser.close()

    except Exception as e:
        # 捕获并打印异常
        print(f"发生错误: {e}")

    # 使用 tabulate 格式化结果并打印
    headers = ["榜单名称", "排名", "新闻标题"]
    print(tabulate(results, headers=headers, tablefmt="grid"))

if __name__ == "__main__":
    # 运行异步主函数
    asyncio.run(main())