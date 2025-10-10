import asyncio
from playwright.async_api import async_playwright
import json


async def crawl_stock_data(stock_code, stock_name):
    """
    使用Playwright爬取指定股票的日线数据和分时图数据
    
    Args:
        stock_code (str): 股票代码
        stock_name (str): 股票名称
    
    Returns:
        dict: 包含日线数据和分时图数据的字典
    """
    async with async_playwright() as p:
        # 启动浏览器
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()
        
        # 设置用户代理，模拟真实浏览器
        await page.set_user_agent("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36")
        
        # 访问目标网页
        url = f"https://gushitong.baidu.com/stock/ab-{stock_code}?name={stock_name}"
        await page.goto(url)
        
        # 等待页面加载完成
        await page.wait_for_timeout(5000)
        
        # 点击日K图按钮
        try:
            await page.click('div:has-text("日K")')
            await page.wait_for_timeout(3000)
            
            # 尝试获取日K数据
            # 注意：实际数据可能需要通过网络请求或页面元素解析获得
            print("已切换到日K图视图")
        except Exception as e:
            print(f"点击日K图按钮失败: {e}")
        
        # 点击分时图按钮
        try:
            await page.click('div:has-text("分时")')
            await page.wait_for_timeout(3000)
            
            # 尝试获取分时图数据
            print("已切换到分时图视图")
        except Exception as e:
            print(f"点击分时图按钮失败: {e}")
        
        # 尝试获取页面上的股票信息
        try:
            # 获取股票名称和代码
            stock_info = await page.text_content('.basicinfos >> text=美的集团')
            print(f"股票信息: {stock_info}")
            
            # 获取当前价格
            current_price = await page.text_content('.cur .price')
            print(f"当前价格: {current_price}")
            
            # 获取涨跌幅
            change_ratio = await page.text_content('.cur .ratio')
            print(f"涨跌幅: {change_ratio}")
        except Exception as e:
            print(f"获取股票信息失败: {e}")
        
        # 关闭浏览器
        await browser.close()
        
        # 返回示例数据结构
        return {
            "stock_code": stock_code,
            "stock_name": stock_name,
            "daily_data": "日K数据需要进一步解析",
            "minute_data": "分时图数据需要进一步解析"
        }


async def main():
    # 爬取美的集团的数据
    result = await crawl_stock_data("000333", "%E7%BE%8E%E7%9A%84%E9%9B%86%E5%9B%A2")
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    asyncio.run(main())