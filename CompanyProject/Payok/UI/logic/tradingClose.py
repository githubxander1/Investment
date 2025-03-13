import re
from playwright.sync_api import Playwright, sync_playwright, expect


def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("http://192.168.0.224:8994/trade-close.html")
    page.get_by_role("link", name="PAYOK-api").click()
    page.get_by_role("button", name="Confirmation Successful").click()
    page.locator("#btnGenerateOrderNo").click()
    page.get_by_label("商户号").select_option("020069")
    page.get_by_label("版本号").select_option("3.2")
    page.get_by_role("button", name="Test").click()

    # 等待页面上id为"loading-spinner"的元素消失，最长等待时间为10000毫秒
    # page.wait_for_function("!document.querySelector('#spinnerBox')", timeout=10000)

    # 等待页面的网络请求结束，最长等待时间为15000毫秒
    # page.wait_for_load_state("networkidle", timeout=15000)
    # 等待 #spinnerBox 消失
    page.wait_for_selector("#spinnerBox", state="hidden")

    # 后续操作可以在这里添加
    print("Spinner 已消失，可以继续后续操作")

    # page.pause()
    # 断言第二个 #exeStatus 元素包含文本 "Success"
    # assert "Success" in page.locator("#exeStatus").nth(1).text_content()

    page.wait_for_timeout(10000)
    # 断言 #exeResult 元素包含文本 "Success"
    assert "Success" in page.locator("#exeResult").text_content()
    # if expect(page.locator("#exeResult")).to_contain_text("Success"):

    state = page.locator("#exeResult").text_content()
    if state == "Success":
        print(state)
        print("交易流程通畅")
    else:
        print("交易流程异常")
    # expect(page.locator("#exeResult")).to_match_aria_snapshot("- text: Success")

    # if expect(page.locator("#exeStatus")).to_contain_text("Completed") and expect(page.locator("#exeResult")).to_contain_text("Success"):
    # if expect(page.locator("#exeResult")).to_contain_text("Success"):
    #     print("交易流程通畅")
    # else:
    #     print("交易流程异常")
    page.pause()

    # ---------------------
    context.close()
    browser.close()


with sync_playwright() as playwright:
    run(playwright)
