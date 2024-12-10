import asyncio
from crawl4ai import AsyncWebCrawler
from tabulate import tabulate  # 用于格式化表格输出
from bs4 import BeautifulSoup  # 用于解析HTML内容

# 定义异步主函数
async def main():
    results = []  # 用于存储所有爬取的结果
    timeout = 10  # 设置超时时间为10秒
    start_time = asyncio.get_event_loop().time()  # 获取当前时间

    try:
        # 初始化爬虫
        async with AsyncWebCrawler(verbose=True) as crawler:
            # 执行爬取任务
            result = await crawler.arun(url="https://top.baidu.com/board?platform=wise&tab=realtime")

            # 假设 result.html 是一个包含HTML内容的字符串
            if hasattr(result, 'html'):
                html_content = result.html
            elif hasattr(result, 'content'):
                html_content = result.content
            else:
                raise ValueError("No HTML content found in the result")

            soup = BeautifulSoup(html_content, 'html.parser')

            # 查找所有的榜单容器
            boards = soup.find_all('div', class_='_23KXyWDm2k2IInG-ul6YB-')
            print('查找所有的榜单')
            print(f"Found {len(boards)} boards")  # 调试信息

            for board in boards:
                # 获取榜单名称
                board_name_tag = board.find('span', class_='_2J4Ry1eOiqfvLWaAftNzNy')
                if board_name_tag:
                    board_name = board_name_tag.text.strip()
                    # print(f"Board name: {board_name}")
                else:
                    print("榜单名称未找到，跳过")
                    continue

                news_list = soup.find_all('div', class_='row-start-center zkwvwdF0VfxBzs7BSEZ1A')
                # print(f"Found {len(news_list)} news items in board: {board_name}")
                for news in news_list:
                    order_num_tag = news.find('span', class_='_1DHjV0lKKB9gt0NdIKD2iH')
                    news_title_tag = news.find('span', class_='_38vEKmzrdqNxu0Z5xPExcg')

                    if order_num_tag and news_title_tag:
                        order_num = order_num_tag.text.strip()
                        news_title = news_title_tag.text.strip()
                        results.append([board_name, order_num, news_title])
                    else:
                        print("Order number or news title not found, skipping this item")

                # 检查是否超过10秒
    #             current_time = asyncio.get_event_loop().time()
    #             if current_time - start_time > timeout:
    #                 print("Timeout reached, stopping further processing")
    #                 break

    except Exception as e:
        # 捕获并打印异常
        print(f"Error occurred: {e}")

    # 使用 tabulate 格式化结果并打印
    headers = ["榜单名称", "排名", "新闻标题"]
    print(tabulate(results, headers=headers, tablefmt="grid"))

if __name__ == "__main__":
    # 运行异步主函数
    asyncio.run(main())
