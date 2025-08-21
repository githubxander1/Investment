import os
import json
import time
from playwright.sync_api import Playwright, sync_playwright
import logging

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class JrttActivityCrawler:
    def __init__(self):
        self.url = 'https://mp.toutiao.com/profile_v4/activity/task-list'
        self.storage_state_path = os.path.join(os.path.dirname(__file__), 'jrtt_storage_state_c.json')
        self.max_pages = 3  # 爬取前三页

    def load_storage_state(self):
        """加载存储状态以保持登录"""
        if os.path.exists(self.storage_state_path):
            logger.info(f"加载存储状态: {self.storage_state_path}")
            return self.storage_state_path
        else:
            logger.warning("存储状态文件不存在，将以未登录状态访问")
            return None

    def save_storage_state(self, context):
        """保存存储状态以便后续使用"""
        context.storage_state(path=self.storage_state_path)
        logger.info(f"保存存储状态到: {self.storage_state_path}")

    def crawl_activities(self):
        """爬取活动页面的前三页活动"""
        activities = []

        with sync_playwright() as playwright:
            # 启动浏览器
            browser = playwright.chromium.launch(
                headless=False,  # 非无头模式，便于查看
                args=[
                    '--disable-blink-features=AutomationControlled',
                    '--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36'
                ]
            )

            # 创建上下文
            storage_state = self.load_storage_state()
            context = browser.new_context(storage_state=storage_state) if storage_state else browser.new_context()

            # 创建页面
            page = context.new_page()

            try:
                # 访问目标页面
                logger.info(f"访问页面: {self.url}")
                page.goto(self.url, wait_until='networkidle')
                time.sleep(5)  # 增加等待时间

                # 检查当前页面状态
                current_url = page.url
                page_title = page.title()
                logger.info(f"当前页面URL: {current_url}")
                logger.info(f"当前页面标题: {page_title}")

                # 如果页面不是目标页面，可能是重定向到了其他页面
                if 'activity/task-list' not in current_url:
                    logger.warning(f"当前页面不是活动列表页面，可能需要手动检查: {current_url}")
                    return activities

                # 检查是否需要登录
                if 'login' in page.url.lower():
                    logger.warning("需要登录，请在浏览器中完成登录")
                    input("登录完成后按Enter键继续...")
                    # 保存登录状态
                    self.save_storage_state(context)
                    # 重新访问目标页面
                    page.goto(self.url, wait_until='networkidle')
                    time.sleep(3)

                # 爬取前三页
                for page_num in range(1, self.max_pages + 1):
                    logger.info(f"爬取第 {page_num} 页")

                    # 提取活动信息
                    page_activities = self.extract_activities(page)
                    activities.extend(page_activities)
                    logger.info(f"第 {page_num} 页提取了 {len(page_activities)} 个活动")

                    # 如果不是最后一页，点击下一页
                    if page_num < self.max_pages:
                        if not self.click_next_page(page):
                            logger.warning("无法找到下一页按钮，爬取结束")
                            break

            except Exception as e:
                logger.error(f"爬取过程中出错: {e}")
            finally:
                # 关闭浏览器
                browser.close()

        logger.info(f"总共爬取了 {len(activities)} 个活动")
        return activities

    def extract_activities(self, page):
        """从当前页面提取活动信息"""
        activities = []

        try:
            # 等待页面加载完成
            page.wait_for_load_state('networkidle')
            time.sleep(2)

            # 根据日志分析，页面上有.card-title类的元素
            logger.info("尝试使用.card-title选择器提取活动项")
            try:
                # 等待卡片标题元素出现
                page.wait_for_selector('.card-title', timeout=5000)
                logger.info("找到.card-title元素")

                # 获取所有卡片元素（假设每个活动项是.card-title的父元素）
                title_elements = page.locator('.card-title').all()
                logger.info(f"找到{len(title_elements)}个标题元素")

                # 遍历每个标题元素，获取其父元素作为活动项
                activity_items = []
                for title_element in title_elements:
                    # 获取父元素（假设活动项是标题的直接父元素或祖父元素）
                    activity_item = title_element.locator('..').locator('..')
                    if activity_item.count() > 0:
                        activity_items.append(activity_item)

                logger.info(f"提取到{len(activity_items)}个活动项")

                for item in activity_items:
                    # 提取活动标题
                    title = item.locator('.card-title').text_content().strip() if item.locator('.card-title').count() > 0 else ''
                    logger.info(f"活动标题: {title}")

                    # 提取活动描述（尝试多种可能的选择器）
                    description = ''
                    for desc_selector in ['.card-desc', 'p', 'div[class*="desc"]']:
                        if item.locator(desc_selector).count() > 0:
                            description = item.locator(desc_selector).text_content().strip()
                            break

                    # 提取活动时间
                    time_info = ''
                    for time_selector in ['.card-time', 'span[class*="time"]', 'div[class*="time"]']:
                        if item.locator(time_selector).count() > 0:
                            time_info = item.locator(time_selector).text_content().strip()
                            break

                    # 提取活动链接
                    link = ''
                    if item.locator('a').count() > 0:
                        link = item.locator('a').get_attribute('href')
                        if link and not link.startswith('http'):
                            link = f'https://mp.toutiao.com{link}'

                    # 提取活动状态
                    status = ''
                    for status_selector in ['.card-status', 'span[class*="status"]', 'div[class*="status"]']:
                        if item.locator(status_selector).count() > 0:
                            status = item.locator(status_selector).text_content().strip()
                            break

                    # 只添加有标题的活动
                    if title:
                        activities.append({
                            'title': title,
                            'description': description,
                            'time': time_info,
                            'link': link,
                            'status': status
                        })
            except TimeoutError:
                logger.warning(".card-title选择器未找到匹配元素")

        except Exception as e:
            logger.error(f"提取活动信息出错: {e}")

        return activities

    def click_next_page(self, page):
        """点击下一页按钮"""
        try:
            # 尝试多种方式查找下一页按钮
            next_page_buttons = [
                page.locator('.pagination-item.next'),
                page.locator('button:has-text("下一页")'),
                page.locator('a:has-text("下一页")'),
                page.locator('span[class*="next"]'),
                page.locator('div:has-text("下一页")')
            ]

            for btn in next_page_buttons:
                if btn.count() > 0:
                    logger.info(f"找到下一页按钮: {btn}")
                    # 检查按钮是否可见且可点击
                    if btn.is_visible() and btn.is_enabled():
                        btn.click()
                        time.sleep(5)  # 增加等待时间
                        return True
                    else:
                        logger.warning("下一页按钮不可见或不可点击")

            # 尝试使用键盘翻页
            logger.info("尝试使用键盘翻页")
            page.keyboard.press('PageDown')
            time.sleep(3)
            return True

        except Exception as e:
            logger.error(f"点击下一页出错: {e}")
            return False

if __name__ == '__main__':
    crawler = JrttActivityCrawler()
    activities = crawler.crawl_activities()

    # 打印爬取结果
    for i, activity in enumerate(activities, 1):
        print(f"活动 {i}:")
        print(f"标题: {activity['title']}")
        print(f"描述: {activity['description']}")
        print(f"时间: {activity['time']}")
        print(f"链接: {activity['link']}")
        print(f"状态: {activity['status']}")
        print('-' * 50)

    # 保存到文件
    with open('jrtt_activities.json', 'w', encoding='utf-8') as f:
        json.dump(activities, f, ensure_ascii=False, indent=4)
    print(f"活动数据已保存到 jrtt_activities.json 文件")