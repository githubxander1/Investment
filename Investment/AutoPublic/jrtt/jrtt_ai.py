from openai import OpenAI
import json
import os
import pickle
import random
import re
import time
from datetime import datetime, timedelta
from plyer import notification

from playwright.sync_api import Playwright, sync_playwright

def get_hot_topics_from_ai():
    """
    使用Qwen大模型获取当前热门话题
    """
    # Qwen API配置
    qwen_client = OpenAI(
        base_url='https://api-inference.modelscope.cn/v1',
        api_key='ms-04756442-433d-4c9c-88c3-095de9dc36d3', # ModelScope Token
    )
    try:
        prompt = """
        请提供10个当前在中文互联网上热门、高关注度且贴近生活的话题，要求：
        1. 话题要具体、细化，避免过于宽泛，如"旅行"应具体为"周末短途旅行推荐"等
        2. 贴近普通人日常生活，如职场、家庭、情感、消费、教育等具体场景
        3. 具有实用价值或情感共鸣，能引起读者兴趣
        4. 每个话题简洁明了，不超过15个字
        5. 直接列出话题，每行一个，不要序号和其他说明
        
        示例格式：
        周末短途旅行推荐
        家庭收纳小妙招
        职场新人沟通技巧
        ...
        """

        response = qwen_client.chat.completions.create(
            model='Qwen/Qwen3-Coder-480B-A35B-Instruct',
            messages=[
                {
                    "role": "system",
                    "content": "你是一个专业的热点话题分析师，擅长发现和总结当前热门且贴近普通人生活的话题。"
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.7,
            max_tokens=500
        )

        # 解析AI返回的话题列表
        topics_text = response.choices[0].message.content.strip()
        topics = [topic.strip() for topic in topics_text.split('\n') if topic.strip()]

        # 过滤掉太长或无效的话题
        topics = [topic for topic in topics if len(topic) <= 20 and len(topic) > 2]

        if topics:
            print(f"AI推荐的热门话题: {topics}")
            return topics
        else:
            print("AI未返回有效话题，使用默认话题")
            return get_default_topics()

    except Exception as e:
        print(f"获取AI推荐话题失败: {e}")
        return get_default_topics()

def get_default_topics():
    """
    默认话题列表，当AI无法提供时使用
    """
    return [
        "周末短途旅行推荐", "家庭收纳小妙招", "职场新人沟通技巧", "家庭理财小窍门",
        "亲子教育心得", "健康饮食搭配", "情感关系维护", "个人成长感悟",
        "城市生活小确幸", "兴趣爱好培养"
    ]

# 添加已使用话题的记录文件
USED_TOPICS_FILE = "used_topics.pkl"

def load_used_topics():
    """加载已使用过的话题列表"""
    if os.path.exists(USED_TOPICS_FILE):
        try:
            with open(USED_TOPICS_FILE, "rb") as f:
                return pickle.load(f)
        except:
            return []
    return []

def save_used_topics(used_topics):
    """保存已使用过的话题列表"""
    with open(USED_TOPICS_FILE, "wb") as f:
        pickle.dump(used_topics, f)

def select_unique_topic(topics=None, max_history=20):
    """
    从话题列表中选择一个未使用过的话题
    :param topics: 可选择的话题列表，如果为None则从AI获取
    :param max_history: 保留最近使用过的话题数量
    :return: 选中的话题
    """
    # 如果没有提供话题列表，则从AI获取
    if topics is None or len(topics) == 0:
        topics = get_hot_topics_from_ai()

    used_topics = load_used_topics()

    # 优先选择未使用过的话题
    unused_topics = [topic for topic in topics if topic not in used_topics]

    if unused_topics:
        selected_topic = random.choice(unused_topics)
    else:
        # 如果所有话题都使用过，则从所有话题中随机选择
        selected_topic = random.choice(topics)

    # 更新已使用话题列表
    used_topics.append(selected_topic)
    # 保持历史记录在合理范围内
    if len(used_topics) > max_history:
        used_topics = used_topics[-max_history:]

    save_used_topics(used_topics)
    return selected_topic

def schedule_posts():
    """
    安排一天的发文时间（早上7点到晚上11点之间随机发送10篇）
    """
    # 定义时间范围
    start_hour = 7   # 早上7点
    end_hour = 23    # 晚上11点
    posts_count = 10 # 发送10篇

    # 生成随机时间点
    times = []
    for i in range(posts_count):
        # 在时间范围内生成随机小时和分钟
        hour = random.randint(start_hour, end_hour-1)
        minute = random.randint(0, 59)
        times.append((hour, minute))

    # 按时间排序
    times.sort()
    return times

def send_notification(message):
    if len(message) > 256:
        message = message[:256 - 3] + '...'
    notification.notify(
        title="trade通知",
        message=message,
        app_name="THS",
        timeout=10
    )
# 定义存储状态的文件路径
STORAGE_STATE_FILE = "jrtt_storage_state_c.json"
# STORAGE_STATE_FILE = "jrtt_storage_state_h.json"

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
    爬取创作热点推荐内容（保留原有功能作为备选）

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

def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False,args=['--start-maximized'])

    # 尝试加载已保存的登录状态
    storage_state = load_storage_state()

    if storage_state:
        # 如果有保存的登录状态，则直接使用
        context = browser.new_context(storage_state=storage_state,no_viewport=True)
        page = context.new_page()
        page.goto("https://mp.toutiao.com/auth/page/login?redirect_url=JTJGcHJvZmlsZV92NCUyRmluZGV4")
        # page.pause()

        # 检查是否已成功登录（通过检查页面是否存在特定元素）
        try:
            # page.wait_for_selector("text=文章", timeout=5000)
            page.wait_for_selector("text=Xander", timeout=5000)
            #'#masterRoot > div > div.garr-header > div > div > div.user-panel > div.information > a > span > div > div > div.auth-avator-name"
            print("使用已保存的登录状态成功登录")
        except:
            print("保存的登录状态已失效，重新登录")
            # context.close()
            # context = browser.new_context()
            # page = context.new_page()
            login_and_save_state(page, context)
    else:
        # 没有保存的登录状态，需要重新登录
        context = browser.new_context()
        page = context.new_page()
        login_and_save_state(page, context)

    # 安排一天的发文时间
    # post_times = schedule_posts()
    # print(f"今日发文计划时间: {[f'{h:02d}:{m:02d}' for h, m in post_times]}")

    # 循环发送多篇文章
    # for i, (hour, minute) in enumerate(post_times):
    #     # 计算下次发送时间
    #     now = datetime.now()
    #     next_post = now.replace(hour=hour, minute=minute, second=0, microsecond=0)
    #
    #     # 如果设定时间已过，则安排到明天
    #     if next_post <= now:
    #         next_post += timedelta(days=1)
    #
    #     # 等待到指定时间
    #     wait_seconds = (next_post - now).total_seconds()
    #     if wait_seconds > 0:
    #         print(f"等待到 {next_post.strftime('%Y-%m-%d %H:%M:%S')} 发送第 {i+1} 篇文章...")
    #         time.sleep(wait_seconds)

        # 执行发文操作
        # print(f"开始发送第 {i+1} 篇文章")
    send_article(page, playwright)

        # # 发送间隔，避免过于频繁
        # if i < len(post_times) - 1:
        #     interval = random.randint(300, 600)  # 5-10分钟间隔
        #     print(f"发送完成，{interval}秒后发送下一篇...")
        #     time.sleep(interval)

    # ---------------------
    context.close()
    browser.close()

def send_article(page, playwright):
    """发送单篇文章的函数"""
    # 继续执行其他操作
    start_creat = page.get_by_role("link", name="开始创作")
    if start_creat.is_visible():
        start_creat.click()
    page.get_by_role("link", name="文章").click()
    # page.get_by_role("link", name="视频").click()
    # page.get_by_role("link", name="微头条").click()
    # page.get_by_role("link", name="问答").click()
    # page.get_by_role("link", name="音频").click()

    # 优先使用AI推荐的热门话题，备选使用平台推荐话题
    try:
        print("正在获取AI推荐的热门话题...")
        topics = get_hot_topics_from_ai()
        if not topics:
            print("AI未返回有效话题，使用平台推荐话题...")
            topics = crawl_recommend_topics(page, batches=3)
    except Exception as e:
        print(f"获取话题失败: {e}，使用平台推荐话题...")
        topics = crawl_recommend_topics(page, batches=3)

    if not topics:
        print("未获取到任何话题，使用默认话题...")
        topics = get_default_topics()

    print(f"总共获取到 {len(topics)} 个话题:")
    for i, topic in enumerate(topics, 1):
        print(f"{i}. {topic}")

    # 选择一个未使用过的话题
    topic = select_unique_topic(topics)
    print(f"已选择话题：{topic}")

    # 主题
    content = (f"主题：{topic}"
               "写作要求："
               "1.语言风格：用轻松自然的口语化表达，就像和朋友聊天一样，避免书面语和官方腔调。可以适当加入一些网络热词或流行语，但不要过度使用。"
               "2.内容组织：不要拘泥于固定模式，根据主题自由发挥。可以分享个人见解、生活感悟，或者对事件的观察思考。段落长短结合，思路跳跃一些反而更真实。"
               "3.情感表达：加入真实的情绪和感受，可以是困惑、惊喜、感慨等，让文字有温度。不必每篇都正能量，适当展现复杂情绪。"
               "4.细节描写：根据主题加入生动的细节，比如当时的环境、人物的神态、自己的心理活动等。避免使用固定模板场景（如超市闲聊），要灵活应变。"
               "5.结构安排：文章结构可以灵活多样，不一定要有明确的开头、中间、结尾。可以是一个完整的故事，也可以是几个片段的组合，或者是一种情绪的渲染。"
               "6.个性化：展现你的个性和观点，可以有点小偏见、小固执，或者独特的观察角度。文字要有你自己的风格烙印。"
               "7.结尾处理：结尾可以引人思考、留有余味，或者戛然而止，或者来个神转折。避免套路式的总结或呼吁。"
               "8.标题要求：不要直接使用主题作为标题，要根据文章内容提炼出一个吸引人的标题，标题要有趣、有悬念或有共鸣点。"
               "请根据以上要求，围绕主题写一篇有血有肉、真实自然的文章，标题要从文章内容中提炼。")

    # 更准确地定位输入框和发送按钮
    textarea = page.locator(".ai-input .byte-textarea.inner-input")
    send_button = page.locator(".ai-input .btn")

    # 填入内容
    textarea.fill(content)

    # 等待发送按钮变为可用状态（移除disabled类）
    page.wait_for_function("""
        () => {
            const button = document.querySelector('.ai-input .btn');
            return button && !button.classList.contains('disabled');
        }
    """, timeout=10000)

    # 点击发送按钮
    send_button.click()

    # 等待响应或页面更新
    # 智能等待：等待添加到正文按钮出现或超时
    add_to_content_visible = False
    for i in range(60):  # 最多等待60秒
        try:
            add_to_content = page.get_by_text("添加到正文")
            if add_to_content.is_visible():
                add_to_content_visible = True
                break
        except:
            pass
        time.sleep(1)

    if not add_to_content_visible:
        # 如果智能等待失败，使用固定等待
        page.wait_for_timeout(60000)

    # 提取AI生成的标题
    try:
        ai_title = ""

        # 尝试从活跃的markdown-body中提取标题
        active_markdown = page.locator(".markdown-body.active")
        if active_markdown.is_visible(timeout=5000):
            title_element = active_markdown.locator("h1")
            if title_element.count() > 0:
                ai_title = title_element.first.text_content().strip()

        # 如果从active markdown中找不到，尝试查找所有markdown-body中的第一个h1
        if not ai_title:
            all_markdowns = page.locator(".markdown-body")
            if all_markdowns.count() > 0:
                for i in range(all_markdowns.count()):
                    markdown = all_markdowns.nth(i)
                    title_element = markdown.locator("h1")
                    if title_element.count() > 0:
                        ai_title = title_element.first.text_content().strip()
                        if ai_title:
                            break

        # 如果还是找不到，尝试直接查找页面上的h1标签
        if not ai_title:
            h1_elements = page.locator("h1")
            if h1_elements.count() > 0:
                for i in range(min(h1_elements.count(), 5)):  # 检查前5个h1元素
                    title_text = h1_elements.nth(i).text_content().strip()
                    if title_text and len(title_text) > 0:
                        ai_title = title_text
                        break

        # 如果找到了标题且不为空，则使用该标题
        if ai_title and len(ai_title) > 0:
            # 确保标题长度符合要求（2-30个字）
            if len(ai_title) > 30:
                ai_title = ai_title[:30]
            page.get_by_role("textbox", name="请输入文章标题（2～30个字）").fill(ai_title)
            print(f"使用AI生成的标题：{ai_title}")
        else:
            # 如果没有生成标题，则使用原主题
            page.get_by_role("textbox", name="请输入文章标题（2～30个字）").fill(topic)
            print(f"未找到AI生成的标题，使用原主题：{topic}")
    except Exception as e:
        print(f"提取标题失败: {e}，使用原主题")
        page.get_by_role("textbox", name="请输入文章标题（2～30个字）").fill(topic)

    # 点击添加到正文按钮
    add_to_content = page.get_by_text("添加到正文")
    if add_to_content.is_visible(timeout=60000):
        add_to_content.click()
        print("点击添加到正文按钮")
    else:
        print("没有添加到正文按钮")
    # page.pause()

    page.get_by_text('内容建议').click()
    no_suggestion = page.get_by_role("paragraph").filter(has_text=re.compile(r"^暂无建议$")).locator("span")
    no_suggestion2 = page.get_by_text("检测成功，暂无建议")

    if no_suggestion.is_visible():
        page.get_by_text("重新检测").click()
        time.sleep(5)
        page.pause()
        if no_suggestion2.is_visible():
            print("检测成功，暂无建议")
            page.get_by_text("AI 创作").click()
        else:
            pass
    else:
        print("有内容建议")


    # page.locator(".byte-drawer-mask").click()    # page.get_by_role("paragraph").click()
    # page.locator("div").filter(has_text=re.compile(r"^请输入正文$")).fill(content)
    # page.locator("label").filter(has_text="单图").locator("div").click()
    # page.locator("label").filter(has_text="三图").locator("div").click()

    # 点击关闭头条创作助手
    # ai_avg = page.get_by_role("heading", name="头条创作助手").locator("svg")
    # if ai_avg.is_visible():
    #     ai_avg.click()
    # 展示封面
    page.mouse.wheel(0, 500)
    # page.pause()
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
    # page.get_by_role("button", name="添加至合集").click()
    # select_collection_by_name(page, "所思所想集")

    # page.locator("li").filter(has_text="所思所想集2023-05-28 20:44展现 24,960阅读").locator("label div").click()
    page.locator("button").filter(has_text="确定").click()
    # page.get_by_text("个人观点，仅供参考").click()
    page.get_by_role("button", name="预览并发布").click()
    time.sleep(1)
    # page.pause()
    # 在点击确认发布前添加监听器
    def handle_dialog(dialog):
        print(f"Dialog message: {dialog.message}")
        assert "提交成功" in dialog.message
        print("断言成功，发布成功")
        dialog.accept()

    page.on("dialog", handle_dialog)
    page.pause()
    page.get_by_role("button", name="确认发布").click()
    print("发布成功")
    page.pause()

    # # ---------------------
    # context.close()
    # browser.close()

def login_and_save_state(page, context):
    """执行登录流程并保存状态"""
    page.goto("https://mp.toutiao.com/auth/page/login?redirect_url=JTJGcHJvZmlsZV92NCUyRmluZGV4")
    reload_notice = page.get_by_role("alert", name="警告:为保证账号安全，请使用手机验证码登录")
        # expect(page.get_by_label("警告:为保证账号安全，请使用手机验证码登录")).to_contain_text(
        #     "为保证账号安全，请使用手机验证码登录")
    page.get_by_role("button", name="账密登录").click()
    page.get_by_role("textbox", name="请输入手机号或邮箱").click()
    page.get_by_role("textbox", name="请输入手机号或邮箱").fill("19918754473")
    page.get_by_role("textbox", name="请输入密码").click()
    page.get_by_role("textbox", name="请输入密码").fill("tth0520@XL")
    page.get_by_role("checkbox", name="协议勾选框").click()
    page.get_by_role("button", name="登录", exact=True).click()
    if reload_notice.is_visible():
        # 系统通知
        send_notification("请使用手机验证码登录")
        # page.pause()
        # continue
    # else:

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
        run(playwright)
