import re
from playwright.sync_api import Playwright, sync_playwright, expect
from pathlib import Path

import os

# 获取当前脚本所在目录
script_dir = os.path.dirname(os.path.abspath(__file__))
auth_file = os.path.join(script_dir, "deepseek_login_state.json")

# def wait_and_click_copy_after_thinking(page):
#     print("等待 '已深度思考' 内容出现...")

def wait_and_click_copy_after_thinking(page):
    print("等待 '已深度思考' 内容出现...")

    try:
        # 等待带有“已深度思考”文本的 div 可见
        page.wait_for_selector("div._58a6d71._19db599:has-text('已深度思考')", state="visible", timeout=120000)
        print("✅ 检测到 '已深度思考'")

        # 等待复制按钮可见
        # copy_button_selector = "#root > div > div > div.c3ecdb44 > div._7780f2e > div > div._3919b83 > div > div > div.dad65929 > div.ds-flex > div.ds-flex._965abe9 > div:nth-child(1) > div > svg"
        # 使用包含“已深度思考”的块，再往下找“复制”按钮
        copy_button_selector = page.locator("div._58a6d71._19db599:has-text('已深度思考')").locator("..").get_by_text("复制").click()

        page.wait_for_selector(copy_button_selector, state="visible", timeout=60000)

        # 点击复制按钮
        page.click(copy_button_selector)
        print("📌 已点击复制按钮")

    except TimeoutError as e:
        print(f"❌ 超时：未找到相关元素 - {str(e)}")

    # # 等待并点击复制按钮
    # page.wait_for_selector("div._58a6d71._19db599", timeout=120000)
    #
    # # 判断是否包含“已深度思考”文本
    # element = page.locator("div._58a6d71._19db599").first
    # text = element.text_content()
    #
    # if "已深度思考" in text:
    #     print("检测到已深度思考，准备点击复制按钮")
    #
    #     # 假设“复制”按钮在同级结构中
    #     # copy_button = element.locator("//following::button[.//span[text()='复制']]")
    #     copy_button = page.locator("//*[@id='root']/div/div/div[2]/div[3]/div/div[2]/div/div/div[1]/div[2]/div[5]/div[1]/div[1]/div/svg")
    #
    #     if copy_button.is_visible():
    #         copy_button.click()
    #         print("✅ 已成功点击复制按钮")
    #     else:
    #         print("❌ 未找到复制按钮")
    # else:
    #     print("⚠️ 文案未变为'已深度思考'")
    # page.wait_for_selector("div:has-text('已深度思考')", timeout=120000)
    # print("检测到深度思考完成，准备点击复制按钮")
    #
    # # 根据实际结构修改下面的选择器
    # # copy_button = page.locator("div:has-text('已深度思考')").locator("//following::button[.//span[text()='复制']]")
    # # copy_button = page.locator("#root > div > div > div.c3ecdb44 > div._7780f2e > div > div._3919b83 > div > div > div.dad65929 > div._4f9bf79.d7dc56a8._43c05b5 > div.ds-flex > div.ds-flex._965abe9 > div:nth-child(1)")
    # copy_button = page.locator("//*[@id='root']/div/div/div[2]/div[3]/div/div[2]/div/div/div[1]/div[2]/div[5]/div[1]/div[1]/div/svg")
    # if copy_button.is_visible():
    #     copy_button.click()
    #     print("✅ 已成功点击复制按钮")
    # else:
    #     print("❌ 未找到复制按钮")

def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    # auth_file = "deepseek_login_state.json"

    # 判断是否存在登录状态文件
    if Path(auth_file).exists():
        # 如果存在，则加载已保存的登录状态
        context = browser.new_context(storage_state=auth_file,permissions=["clipboard-read"])
        print("已加载登录状态")
    else:
        # 如果不存在，则进行登录操作
        context = browser.new_context()
        print("正在登录...")

    page = context.new_page()

    # 如果是首次运行或未登录状态，需要打开登录页面
    if not Path(auth_file).exists():
        page.goto("https://chat.deepseek.com/sign_in")
        page.get_by_text("密码登录").click()
        page.get_by_role("textbox", name="请输入手机号/邮箱地址").click()
        page.get_by_role("textbox", name="请输入手机号/邮箱地址").fill("19918754473")
        page.get_by_role("textbox", name="请输入密码").click()
        page.get_by_role("textbox", name="请输入密码").fill("ds0520@xl")
        page.get_by_role("button", name="登录").click()

        # 等待跳转到主页
        page.wait_for_url("https://chat.deepseek.com/")

        # 保存登录状态
        context.storage_state(path=auth_file)
        print("登录状态已保存")

    # 已登录状态下执行的操作
    page.goto("https://chat.deepseek.com/")
    page.get_by_role("button", name="深度思考 (R1)").click()
    page.get_by_role("button", name="联网搜索").click()
    page.get_by_role("textbox", name="给 DeepSeek 发送消息").fill("随机一个股票量化交易知识点")
    page.pause()
    page.get_by_role("button").filter(has_text=re.compile(r"^$")).click()

    wait_and_click_copy_after_thinking(page)
    # 打印剪贴板内容
    # 获取剪贴板内容
    # 获取剪贴板内容
    clipboard_content = page.evaluate("async () => await navigator.clipboard.readText()")
    print("剪贴板内容为:", clipboard_content)

    clipboard_content2 = page.evaluate("navigator.clipboard.readText()")
    print(clipboard_content2)

    # page.get_by_text("思考中").click()
    # 重新编辑问题
    # page.locator("div").filter(has_text=re.compile(r"^随机一个股票量化交易知识点思考中\.\.\.$")).get_by_role("img").nth(
    #     1).click()
    # page.get_by_text("复制").click()
    # page.locator(".ds-flex > .ds-flex > div > .ds-icon > svg").first.click()
    # page.locator(".ds-flex > .ds-flex > div").first.press("F12")

    # ---------------------
    context.close()
    browser.close()


with sync_playwright() as playwright:
    run(playwright)
