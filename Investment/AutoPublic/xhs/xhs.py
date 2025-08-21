import re
import json
import os
from playwright.sync_api import Playwright, sync_playwright, expect

# 定义存储状态的文件路径
STORAGE_STATE_FILE = "xhs_storage_state_193_c.json"

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

def login_and_save_state(page, context):
    """执行登录流程并保存状态"""
    page.goto("https://creator.xiaohongshu.com/login?source=&redirectReason=401&lastUrl=%252Fnew%252Fnote-manager")
    page.pause()
    # page.get_by_role("textbox", name="手机号").click()
    # page.get_by_role("textbox", name="手机号").fill("19918754473")
    # page.get_by_text("发送验证码").click()
    # # 等待用户输入验证码
    # page.pause()  # 暂停以手动输入验证码
    # page.get_by_role("button", name="登 录").click()

    # 等待登录完成
    # page.wait_for_url("**/note-manager", timeout=30000)

    # 保存登录状态
    storage_state = context.storage_state()
    save_storage_state(storage_state)
    print("登录状态已保存")

def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)

    # 尝试加载已保存的登录状态
    storage_state = load_storage_state()

    if storage_state:
        # 如果有保存的登录状态，则直接使用
        context = browser.new_context(storage_state=storage_state)
        page = context.new_page()
        page.goto("https://creator.xiaohongshu.com/new/note-manager")

        # 检查是否已成功登录（通过检查页面是否存在特定元素）
        try:
            page.wait_for_selector("text=发布笔记", timeout=5000)
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

    page.pause()
    # 继续执行其他操作
    page.get_by_text("发布笔记").click()
    # page.locator("div").filter(has_text=re.compile(r"^上传视频$")).locator("span").click()
    page.get_by_text("上传图文").nth(1).click()
    # page.get_by_text("导入长文").click()
    # 监听上传
    file_path = '机器人图.png'
    page.on("filechooser", lambda file_chooser: file_chooser.set_files(file_path))
    page.get_by_text("上传图文").nth(1).click()
    page.get_by_role("textbox").click()
    # page.get_by_role("button", name="Choose File").click()
    # page.get_by_role("button", name="Choose File").set_input_files("Capture001.png")
    title = "机器人图"
    content = '机器人美女' * 100
    page.get_by_role("textbox", name="填写标题会有更多赞哦～").fill(title)
    page.locator("#quillEditor div").fill(content)
    page.pause()
    # page.get_by_role("button", name="话题").click()
    page.get_by_text("添加合集").nth(1).click()
    page.get_by_text("去声明").click()
    # page.locator(".d-checkbox-indicator > .d-icon > svg").click()
    page.locator(".d-checkbox-indicator").click()
    page.get_by_role("button", name="声明原创").click()
    page.locator("form").filter(has_text="允许正文复制").locator("span").nth(1).click()
    page.locator("form").filter(has_text="允许合拍").locator("span").nth(1).click()
    page.pause()
    page.get_by_role("button", name="发布").click()
    page.wait_for_timeout(1000)

    # 活动
    #详情图page.locator("iframe").content_frame.locator(".template-h5-mask")
    submit_sus = page.get_by_text("发布成功")
    if submit_sus.is_visible(timeout=3000):
        print("✅ 提交成功")
    else:
        print("❌ 提交失败")
    page.pause()

    # 等待并验证发布成功
    try:
        success_message = page.get_by_text("发布成功")
        success_message.wait_for(timeout=15000)
        assert success_message.is_visible()
        print("✅ 发布成功")
    except:
        print("❌ 未检测到发布成功的提示")
        page.screenshot(path="xhs_publish_error.png")

    # ---------------------
    context.close()
    browser.close()

with sync_playwright() as playwright:
    run(playwright)
