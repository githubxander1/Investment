import json
import os
import re
import time

from playwright.sync_api import Playwright, sync_playwright

# 定义存储状态的文件路径
STORAGE_STATE_FILE = "jrtt_storage_state_c.json"

def load_storage_state():
    """加载存储状态"""
    if os.path.exists(STORAGE_STATE_FILE):
        with open(STORAGE_STATE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return None

def save_storage_state(storage_state):
    """保存存储状态"""
    with open(STORAGE_STATE_FILE, "w", encoding="utf-8") as f:
        json.dump(storage_state, f, indent=2, ensure_ascii=False)

def scroll_page(page, direction="down", distance=500):
    """
    滑动页面函数
    :param page: Playwright页面对象
    :param direction: 滑动方向，"up" 或 "down"
    :param distance: 滑动距离
    """
    try:
        if direction == "down":
            page.evaluate(f"window.scrollBy(0, {distance})")
        else:
            page.evaluate(f"window.scrollBy(0, -{distance})")
        page.wait_for_timeout(1000)  # 等待页面渲染
        return True
    except Exception as e:
        print(f"页面滑动失败: {e}")
        return False

def select_collection_by_name(page, collection_name):
    """
    根据名称选择合集
    :param page: Playwright页面对象
    :param collection_name: 合集名称
    :return: 是否成功选择
    """
    try:
        # 等待合集列表加载
        page.wait_for_selector(".add-collection-list", timeout=10000)

        # 查找包含指定名称的合集项
        collection_items = page.query_selector_all(".add-collection-item")

        for item in collection_items:
            title_element = item.query_selector(".article-title")
            if title_element and collection_name in title_element.inner_text():
                # 找到匹配的合集，点击对应的复选框
                checkbox = item.query_selector(".byte-checkbox-wrapper")
                if checkbox:
                    checkbox.click()
                    print(f"成功选择合集: {collection_name}")
                    return True

        print(f"未找到合集: {collection_name}")
        return False
    except Exception as e:
        print(f"选择合集时出错: {e}")
        return False

def crawl_recommend_topics(page, batches=3):
    """
    爬取创作热点推荐内容

    Args:
        page: Playwright页面对象
        batches: 爬取批次数，默认为3批

    Returns:
        list: 所有爬取到的热点话题列表
    """
    all_topics = []

    # 确保在正确的页面
    # page.goto("https://mp.toutiao.com/profile_v4/graphic/publish")

    # 等待推荐列表加载
    try:
        page.wait_for_selector(".recommend-list", timeout=10000)
    except:
        print("未能找到推荐列表")
        return all_topics

    for i in range(batches):
        print(f"正在爬取第 {i+1} 批内容...")

        # 查找当前批次的所有话题
        topics_elements = page.query_selector_all(".recommend-list .topic .text")
        batch_topics = []

        for element in topics_elements:
            topic_text = element.inner_text().strip()
            if topic_text and topic_text not in batch_topics:
                batch_topics.append(topic_text)

        # 添加到总列表中（去重）
        for topic in batch_topics:
            if topic not in all_topics:
                all_topics.append(topic)

        print(f"第 {i+1} 批内容: {batch_topics}")

        # 如果不是最后一批，点击"换一换"按钮获取下一批
        if i < batches - 1:
            try:
                # 点击"换一换"按钮
                refresh_btn = page.query_selector(".refresh-btn")
                if refresh_btn:
                    refresh_btn.click()
                    # 等待新内容加载
                    time.sleep(2)
            except Exception as e:
                print(f"点击换一换按钮时出错: {e}")
                break

    return all_topics

def run(playwright: Playwright,title, content) -> None:
    browser = playwright.chromium.launch(headless=False)

    # 尝试加载已保存的登录状态
    storage_state = load_storage_state()

    if storage_state:
        # 如果有保存的登录状态，则直接使用
        context = browser.new_context(storage_state=storage_state)
        page = context.new_page()
        page.goto("https://mp.toutiao.com/auth/page/login?redirect_url=JTJGcHJvZmlsZV92NCUyRmluZGV4")
        # page.pause()

        # 检查是否已成功登录（通过检查页面是否存在特定元素）
        try:
            page.wait_for_selector("text=文章", timeout=5000)
            print("使用已保存的登录状态成功登录")
        except:
            print("保存的登录状态已失效，重新登录")
            context.close()
            context = browser.new_context()
            page = context.new_page()
            login_and_save_state(page, context)
    else:
        # 没有保存的登录状态，需要重新登录
        context = browser.new_context()
        page = context.new_page()
        login_and_save_state(page, context)



    # 继续执行其他操作
    page.get_by_role("link", name="文章").click()
    # page.get_by_role("link", name="视频").click()
    # page.get_by_role("link", name="微头条").click()
    # page.get_by_role("link", name="问答").click()
    # page.get_by_role("link", name="音频").click()



    # 爬取热点推荐内容
    # print("开始爬取创作热点推荐内容...")
    # topics = crawl_recommend_topics(page, batches=3)
    # print(f"总共爬取到 {len(topics)} 个独特话题:")
    # for i, topic in enumerate(topics, 1):
    #     print(f"{i}. {topic}")

    # page.locator(".byte-drawer-mask").click()    # page.get_by_role("paragraph").click()
    page.locator("div").filter(has_text=re.compile(r"^请输入正文$")).fill(content)
    # page.locator("label").filter(has_text="单图").locator("div").click()
    # page.locator("label").filter(has_text="三图").locator("div").click()
    # 点击关闭头条创作助手
    ai_avg = page.get_by_role("heading", name="头条创作助手").locator("svg")
    if ai_avg.is_visible():
        ai_avg.click()
    # 展示封面
    page.mouse.wheel(0, 500)
    page.pause()
    page.get_by_text("无封面").click()
    # page.locator("label").filter(has_text="无封面").locator("div").click()
    # 往下滑动一段距离
    # page.get_by_text("免费正版图片").click()
    # time.sleep(3)
    # page.locator(".wall-rows > div > .list > li").first.click()
    # page.get_by_role("button", name="确定").click()
    # 标记位置
    page.get_by_text("标记城市，让更多同城用户看到").click()
    page.get_by_text("深圳").click()
    # 申明头条首发
    page.locator("label").filter(has_text="头条首发").locator("div").click()
    # 添加合集
    page.get_by_role("button", name="添加至合集").click()
    page.pause()
    select_collection_by_name(page, "所思所想集")
    # page.locator("li").filter(has_text="所思所想集2023-05-28 20:44展现 24,960阅读").locator("label div").click()
    page.locator("button").filter(has_text="确定").click()
    page.pause()
    page.get_by_role("button", name="预览并发布").click()
    time.sleep(1)
    page.get_by_role("button", name="确认发布").click()

    # ---------------------
    context.close()
    browser.close()

def login_and_save_state(page, context):
    """执行登录流程并保存状态"""
    page.goto("https://mp.toutiao.com/auth/page/login?redirect_url=JTJGcHJvZmlsZV92NCUyRmluZGV4")
    # page.pause()
    page.get_by_role("button", name="账密登录").click()
    page.get_by_role("textbox", name="请输入手机号或邮箱").click()
    page.get_by_role("textbox", name="请输入手机号或邮箱").fill("19918754473")
    page.get_by_role("textbox", name="请输入密码").click()
    page.get_by_role("textbox", name="请输入密码").fill("tth0520@XL")
    page.get_by_role("checkbox", name="协议勾选框").click()
    page.get_by_role("button", name="登录", exact=True).click()

    # 等待登录完成
    page.wait_for_url("https://mp.toutiao.com/profile_v4/index?is_new_connect=0&is_new_user=0", timeout=10000)

    # 保存登录状态
    storage_state = context.storage_state()
    """保存存储状态"""
    with open(STORAGE_STATE_FILE, "w", encoding="utf-8") as f:
        json.dump(storage_state, f, indent=2, ensure_ascii=False)
    # save_storage_state(storage_state)
    print("登录状态已保存")

if __name__ == '__main__':
    title = "测试标题"
    content = "测试内容" * 100
    with sync_playwright() as playwright:
        run(playwright,title, content)
