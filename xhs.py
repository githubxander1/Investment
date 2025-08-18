import re
from playwright.sync_api import Playwright, sync_playwright, expect


def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("https://creator.xiaohongshu.com/login?source=&redirectReason=401&lastUrl=%252Fnew%252Fnote-manager")
    page.get_by_role("textbox", name="手机号").click()
    page.get_by_role("textbox", name="手机号").fill("19918754473")
    page.get_by_text("发送验证码").click()
    page.get_by_text("发送验证码").click()
    page.get_by_role("textbox", name="验证码").click()
    page.get_by_role("textbox", name="验证码").fill("652242")
    page.get_by_role("button", name="登 录").click()
    page.get_by_text("发布笔记").click()
    page.locator("div").filter(has_text=re.compile(r"^上传视频$")).locator("span").click()
    page.get_by_text("上传图文").nth(1).click()
    page.get_by_text("导入长文").click()
    page.get_by_text("上传图文").nth(1).click()
    page.get_by_role("button", name="Choose File").click()
    page.get_by_role("button", name="Choose File").set_input_files("Capture001.png")
    page.get_by_role("textbox", name="填写标题会有更多赞哦～").click()
    page.get_by_role("textbox", name="填写标题会有更多赞哦～").fill("test")
    page.locator("#quillEditor div").click()
    page.get_by_role("textbox", name="填写标题会有更多赞哦～").fill("testt")
    page.locator("#quillEditor div").fill("EST")
    page.locator("#quillEditor").get_by_text("EST").click()
    page.locator("#quillEditor div").fill("EST第三方第三方斯蒂芬")
    page.get_by_role("button", name="话题").click()
    page.get_by_text("#有想法轻松发").click()
    page.get_by_text("添加合集").nth(1).click()
    page.get_by_text("添加合集").nth(1).click()
    page.locator("form").filter(has_text="允许正文复制").locator("span").nth(1).click()
    page.locator("form").filter(has_text="允许合拍").locator("span").nth(1).click()
    page.get_by_role("button", name="发布").click()
    page.get_by_text("发布成功").click()

    # ---------------------
    context.close()
    browser.close()


with sync_playwright() as playwright:
    run(playwright)
