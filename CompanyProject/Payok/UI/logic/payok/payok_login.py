import re
from playwright.sync_api import Playwright, sync_playwright, expect

from CompanyProject.Payok.UI.utils.perform_slider_unlock import perform_block_slider_verification


def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("http://payok-test.com/merchant/payok-user-login.html")
    page.locator("span").filter(has_text="Indonesia").first.click()
    # page.get_by_role("link", name="Indonesia").click()
    page.get_by_role("link", name="Vietnam").click()
    page.get_by_role("textbox", name="Country E-mail").fill("11@qq.com")
    page.get_by_role("textbox", name="Password").fill("A123456@test")
    perform_block_slider_verification(page)
    page.get_by_role("button", name="Login").click()
    # page.get_by_role("textbox", name="Google Verification Code").fill("974661")
    page.get_by_role("button", name="Login").click()
    page.pause()

    # ---------------------
    context.close()
    browser.close()


with sync_playwright() as playwright:
    run(playwright)
