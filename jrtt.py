import re
from playwright.sync_api import Playwright, sync_playwright, expect


def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("https://mp.toutiao.com/auth/page/login?redirect_url=JTJGcHJvZmlsZV92NCUyRmluZGV4")
    page.get_by_role("button", name="账密登录").click()
    page.get_by_role("textbox", name="请输入手机号或邮箱").click()
    page.get_by_role("textbox", name="请输入手机号或邮箱").fill("19918754473")
    page.get_by_role("textbox", name="请输入密码").click()
    page.get_by_role("textbox", name="请输入密码").fill("tth0520@XL")
    page.get_by_role("checkbox", name="协议勾选框").click()
    page.get_by_role("button", name="登录", exact=True).click()
    page.get_by_role("link", name="文章").click()
    page.locator(".byte-drawer-mask").click()
    page.locator(".byte-drawer-mask").click()
    page.get_by_role("textbox", name="请输入文章标题（2～30个字）").fill("test标题")
    page.get_by_role("paragraph").click()
    page.locator("div").filter(has_text=re.compile(r"^请输入正文$")).fill("test正文\n\n\n")
    page.get_by_role("button", name="预览并发布").click()
    page.locator(".add-icon > path:nth-child(2)").click()
    page.get_by_text("免费正版图片").click()
    page.locator(".wall-rows > div > .list > li").first.click()
    page.get_by_role("button", name="确定").click()
    page.get_by_text("标记城市，让更多同城用户看到").click()
    page.get_by_text("深圳").click()
    page.locator("label").filter(has_text="头条首发").locator("div").click()
    page.get_by_text("test正文").click()
    page.locator("div").filter(has_text=re.compile(r"^test正文$")).fill("test正文嘎嘎嘎嘎嘎嘎嘎嘎嘎嘎嘎嘎嘎嘎嘎嘎嘎嘎嘎嘎嘎嘎嘎嘎嘎嘎嘎嘎嘎嘎嘎嘎嘎嘎嘎嘎更大地方孤寡孤寡孤寡嘎嘎嘎嘎嘎嘎嘎嘎嘎嘎嘎嘎嘎嘎嘎嘎嘎嘎嘎嘎嘎嘎嘎嘎嘎嘎嘎嘎嘎嘎嘎嘎嘎嘎嘎嘎嘎嘎嘎dfffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff\n\n\n")
    page.get_by_text("test正文g").click()
    page.locator("div").filter(has_text=re.compile(r"^test正文$")).fill("test正文嘎嘎嘎嘎嘎嘎嘎嘎嘎嘎嘎嘎嘎嘎嘎嘎嘎嘎嘎嘎嘎嘎嘎嘎嘎嘎嘎嘎嘎嘎嘎嘎嘎嘎嘎嘎更大地方孤寡孤寡孤寡嘎嘎嘎嘎嘎嘎嘎嘎嘎嘎嘎嘎嘎嘎嘎嘎嘎嘎嘎嘎嘎嘎嘎嘎嘎嘎嘎嘎嘎嘎嘎嘎嘎嘎嘎嘎嘎嘎嘎dfffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff灌灌灌灌孤寡孤寡孤寡嘎嘎嘎嘎嘎嘎嘎嘎嘎嘎嘎嘎嘎嘎嘎嘎嘎嘎dfddd\n\n\n")
    page.locator(".ProseMirror").fill("test正文嘎嘎嘎嘎嘎嘎嘎嘎嘎嘎嘎嘎嘎嘎嘎嘎嘎嘎嘎嘎嘎嘎嘎嘎嘎嘎嘎嘎嘎嘎嘎嘎嘎嘎嘎嘎更大地方孤寡孤寡孤寡嘎嘎嘎嘎嘎嘎嘎嘎嘎嘎嘎嘎嘎嘎嘎嘎嘎嘎嘎嘎嘎嘎嘎嘎嘎嘎嘎嘎嘎嘎嘎嘎嘎嘎嘎嘎嘎嘎嘎dfffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff灌灌灌灌孤寡孤寡孤寡嘎嘎嘎嘎嘎嘎嘎嘎嘎嘎嘎嘎嘎嘎嘎嘎嘎嘎东方大道的点点滴滴滴滴答答的哒哒哒哒哒哒哒哒哒哒哒哒哒哒哒哒哒哒哒哒哒哒哒哒哒哒哒哒哒哒哒哒哒哒哒哒\n\n\n")
    page.get_by_text("test正文g").click()
    page.locator(".exclusive-basic-select > .byte-checkbox > .byte-checkbox-wrapper > .byte-checkbox-mask").click()
    page.locator("button").filter(has_text="取消").click()
    page.get_by_role("button", name="添加至合集").click()
    page.locator("li").filter(has_text="所思所想集2023-05-28 20:44展现 24,960阅读").locator("label div").click()
    page.locator("button").filter(has_text="确定").click()
    page.get_by_role("button", name="预览并发布").click()

    # ---------------------
    context.close()
    browser.close()


with sync_playwright() as playwright:
    run(playwright)
