import re
from playwright.sync_api import Playwright, sync_playwright, expect


def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("http://payok-test.com/merchant/payok-user-login.html")
    page.locator("span").filter(has_text="Indonesia").first.click()
    page.get_by_role("link", name="Indonesia").click()
    page.get_by_role("textbox", name="Country E-mail").fill("3@qq.com")
    page.get_by_role("textbox", name="Password").fill("A123456@test")
    page.get_by_role("button", name="Login").click()
    page.get_by_role("textbox", name="Google Verification Code").fill("974661")
    page.get_by_role("button", name="Login").click()

    # ---------------------
    context.close()
    browser.close()


with sync_playwright() as playwright:
    run(playwright)
