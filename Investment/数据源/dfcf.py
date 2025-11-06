from playwright.sync_api import sync_playwright
import re
import json
import pandas as pd
import time
from datetime import datetime


class StockDailyCrawler:
    def __init__(self, stock_code, start_date=None, end_date=None, save_path="stock_daily_data.csv"):
        """
        初始化爬虫参数
        :param stock_code: 股票代码（如"000333"，深市自动加"sz"，沪市加"sh"）
        :param start_date: 起始日期（格式"YYYY-MM-DD"，默认爬取全部历史数据）
        :param end_date: 结束日期（格式"YYYY-MM-DD"，默认爬取到当前日期）
        :param save_path: 数据保存路径（默认CSV格式）
        """
        # 区分沪市（sh）/深市（sz）：000/002/300开头为深市，600/688开头为沪市
        if stock_code.startswith(("000", "002", "300")):
            self.stock_code = f"sz{stock_code}"
        elif stock_code.startswith(("600", "688")):
            self.stock_code = f"sh{stock_code}"
        else:
            raise ValueError("无效股票代码！请确认是沪市（600/688开头）或深市（000/002/300开头）")

        self.start_date = start_date
        self.end_date = end_date or datetime.now().strftime("%Y-%m-%d")
        self.save_path = save_path
        self.daily_data = []  # 存储所有日线数据
        self.base_url = f"https://quote.eastmoney.com/{self.stock_code}.html"  # 东方财富日K页面

    def _extract_daily_json(self, page):
        """从页面源码中提取日线数据JSON（东方财富数据存储在JS变量中）"""
        # 等待页面JS加载完成（关键数据在klData变量中）
        page.wait_for_selector("script:has-text('var klData')", timeout=10000)
        # 获取页面源码
        page_source = page.content()
        # 用正则表达式提取klData中的JSON数据（匹配var klData = {...};）
        pattern = r"var klData = (\{.*?\});"
        match = re.search(pattern, page_source, re.DOTALL)
        if not match:
            raise ValueError("未找到日线数据，请检查页面结构是否更新")

        # 解析JSON数据
        kl_data = json.loads(match.group(1))
        # 提取日线数据列表（klData.data为日线数据，每个元素对应一天）
        daily_list = kl_data.get("data", [])
        if not daily_list:
            print("当前页面无日线数据，可能已达历史最早数据")
            return False

        # 提取字段映射（确保字段与数据对应，不同网站字段名可能不同）
        field_map = {
            "date": "日期",
            "open": "开盘价",
            "close": "收盘价",
            "high": "最高价",
            "low": "最低价",
            "volume": "成交量(手)",
            "amount": "成交额(元)"
        }

        # 遍历数据，转换为DataFrame格式的字典
        for day_data in daily_list:
            # 东方财富日线数据格式：[日期戳, 开盘价, 收盘价, 最高价, 最低价, 成交量, 成交额, ...]
            # 转换日期戳为"YYYY-MM-DD"（如1728067200000 -> 2025-10-05）
            date_str = datetime.fromtimestamp(int(day_data[0]) / 1000).strftime("%Y-%m-%d")
            # 过滤日期范围（若用户指定了起始/结束日期）
            if self.start_date and date_str < self.start_date:
                return False  # 早于起始日期，停止爬取
            if date_str > self.end_date:
                continue  # 晚于结束日期，跳过

            # 提取关键字段
            daily_dict = {
                field_map["date"]: date_str,
                field_map["open"]: round(float(day_data[1]), 2),  # 保留2位小数
                field_map["close"]: round(float(day_data[2]), 2),
                field_map["high"]: round(float(day_data[3]), 2),
                field_map["low"]: round(float(day_data[4]), 2),
                field_map["volume"]: int(day_data[5]),  # 成交量单位：手
                field_map["amount"]: int(day_data[6])  # 成交额单位：元
            }
            self.daily_data.append(daily_dict)

        return True

    def _handle_pagination(self, page):
        """处理分页：点击“下一页”获取历史数据，直到达起始日期或无下一页"""
        page_num = 1
        while True:
            print(f"正在爬取第{page_num}页日线数据...")
            # 提取当前页数据
            has_more = self._extract_daily_json(page)
            if not has_more:
                break  # 无更多数据或已达起始日期，停止分页

            # 定位“下一页”按钮并点击（东方财富分页按钮CSS选择器：.next-page）
            try:
                # 等待下一页按钮可点击（避免动态加载延迟）
                next_btn = page.locator(".next-page")
                # 判断按钮是否禁用（禁用则无更多页）
                if next_btn.get_attribute("class") and "disabled" in next_btn.get_attribute("class"):
                    print("已爬取所有可用分页数据")
                    break
                # 点击下一页，等待页面加载（设置1-2秒间隔，避免反爬）
                next_btn.click()
                time.sleep(1.5)
                page_num += 1
            except Exception as e:
                print(f"分页失败：{str(e)}，停止爬取")
                break

    def run(self):
        """启动爬虫：初始化浏览器、导航页面、爬取数据、保存结果"""
        with sync_playwright() as p:
            # 启动无头Chrome浏览器（headless=True不显示界面，False用于调试）
            browser = p.chromium.launch(headless=True, args=["--no-sandbox"])
            page = browser.new_page()
            try:
                # 导航到目标股票日K线页面（设置超时时间30秒）
                page.goto(self.base_url, timeout=30000)
                # 等待页面加载完成（等待日K线标签激活，避免数据未加载）
                page.wait_for_selector(".tab-K", timeout=15000)
                print(f"成功进入{self.stock_code}（{self.stock_code[2:]}）日K线页面")

                # 处理分页并爬取数据
                self._handle_pagination(page)

                # 数据清洗与保存
                if self.daily_data:
                    # 转换为DataFrame，按日期降序排列（最新日期在前）
                    df = pd.DataFrame(self.daily_data)
                    df = df.sort_values(by="日期", ascending=False).drop_duplicates(subset="日期")
                    # 保存到CSV文件
                    df.to_csv(self.save_path, index=False, encoding="utf-8-sig")
                    print(f"\n爬取完成！共获取{len(df)}条日线数据")
                    print(f"数据已保存至：{self.save_path}")
                    print("数据预览：")
                    print(df.head(10))  # 打印前10条数据预览
                else:
                    print("未爬取到任何日线数据，请检查股票代码或日期范围")
            except Exception as e:
                print(f"爬虫运行失败：{str(e)}")
            finally:
                # 关闭浏览器
                browser.close()


# ------------------- 爬虫使用示例 -------------------
if __name__ == "__main__":
    # 爬取美的集团（000333，深市）2024-01-01至2025-10-10的日线数据
    crawler = StockDailyCrawler(
        stock_code="600030",  # 股票代码（无需加sz/sh，爬虫自动识别）
        start_date="2025-11-05",  # 起始日期（可选，默认爬全部历史）
        end_date="2025-11-06",  # 结束日期（可选，默认当前日期）
        save_path="中信证券日线数据_110506.csv"  # 保存路径
    )
    crawler.run()