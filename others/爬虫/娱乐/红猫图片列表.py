import asyncio

from playwright.async_api import async_playwright


async def crawl_with_playwright(url):
    """使用Playwright爬取动态加载内容"""
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        
        try:
            await page.goto(url, timeout=60000)
            # 等待主要内容加载
            await page.wait_for_selector('.vodlist.piclist.vertical', timeout=5000)
            
            # 获取整个页面内容
            content = await page.content()
            
            # 提取目标数据
            results = []
            vodlist = await page.query_selector('.vodlist.piclist.vertical')
            if vodlist:
                listpic_items = await vodlist.query_selector_all('.listpic')
                for item in listpic_items:
                    a_tag = await item.query_selector('a')
                    if not a_tag:
                        continue
                    
                    href = await a_tag.get_attribute('href')
                    vodname_div = await item.query_selector('.vodnane')
                    vodname = await vodname_div.inner_text() if vodname_div else '无相关名称'
                    results.append((href, vodname.strip()))
            
            return results
            
        except Exception as e:
            print(f"爬取过程中发生错误: {str(e)}")
            return None
        finally:
            await browser.close()

def save_results(data, filename='results.txt'):
    """保存结果到文件"""
    with open(filename, 'w', encoding='utf-8') as f:
        for idx, (href, name) in enumerate(data, 1):
            f.write(f"{idx}. 链接: {href}\n   名称: {name}\n\n")

async def main():
    target_url = "https://fylhfyullx.top:2568/piclist/45.html"
    
    # 执行爬取
    crawled_data = await crawl_with_playwright(target_url)
    
    # 处理结果
    if crawled_data:
        print(f"成功获取 {len(crawled_data)} 条数据")
        save_results(crawled_data)
        print("数据已保存到 results.txt")
    else:
        print("未能获取有效数据")

if __name__ == "__main__":
    asyncio.run(main())
