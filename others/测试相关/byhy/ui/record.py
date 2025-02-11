import re

from playwright.sync_api import Playwright, sync_playwright, expect


def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    #登录
    page.goto("http://127.0.0.1:8047/mgr/sign.html")
    page.get_by_placeholder("用户名").fill("byhy")
    page.get_by_placeholder("密码").fill("88888888")
    page.get_by_role("button", name="登录").click()

    #等待2秒
    page.wait_for_timeout(2000)
    # 添加客户
    page.get_by_role("button", name="+ 添加客户").click()
    page.locator("div").filter(has_text=re.compile(r"^客户名$")).get_by_role("textbox").fill("新增1")
    page.locator("div").filter(has_text=re.compile(r"^联系电话$")).get_by_role("textbox").fill("15319548754")
    page.locator("textarea").fill("广东省深圳市罗湖区士大夫士大夫士大夫")
    page.get_by_role("button", name="创建").click()

    page.once("dialog", lambda dialog: dialog.dismiss())

    #删除客户
    page.get_by_text("删除").nth(1).click()

    # 药品
    #添加药品
    page.get_by_role("link", name=" 药品").click()
    page.get_by_role("button", name="+ 添加药品").click()
    page.locator("div").filter(has_text=re.compile(r"^药品名称$")).get_by_role("textbox").fill("新增药品1")
    page.locator("div").filter(has_text=re.compile(r"^编号$")).get_by_role("textbox").fill("001")
    page.locator("textarea").fill("描述随风倒随风倒十分")
    page.get_by_role("button", name="创建").click()

    #订单
    #添加订单
    page.get_by_role("link", name=" 订单").click()
    page.get_by_role("button", name="+ 添加订单").click()
    page.locator("div").filter(has_text=re.compile(r"^订单名称$")).get_by_role("textbox").fill("订单1")
    page.get_by_role("listbox").first.select_option("80")
    page.get_by_placeholder("请输入关键字查找").nth(1).fill("11")
    page.get_by_role("button", name="创建").click()

    # ---------------------
    context.close()
    browser.close()


with sync_playwright() as playwright:
    run(playwright)
