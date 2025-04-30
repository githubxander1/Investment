import os
from playwright.sync_api import Playwright, sync_playwright, expect


def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()

    # 访问目标页面
    page.goto("https://the-internet.herokuapp.com/upload")
    # page.goto("http://payok-test.com/merchant/payok-register-register.html")

    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    # 文件路径配置
    DATA_DIR = os.path.join(BASE_DIR, 'data')
    filepath = os.path.join(DATA_DIR, "法人护照.doc")
    print('文件存在' if os.path.exists(filepath) else '文件不存在')

    # 监听 file_chooser 事件
    page.on('filechooser', lambda file_chooser: file_chooser.set_files(filepath))

    # 触发文件选择框点击事件
    page.locator("#file-upload").click()

    # 等待文件上传完成（可根据实际情况调整等待条件）
    page.wait_for_timeout(3000)

    # 点击上传按钮
    page.get_by_role("button", name="file-submit").click()

    # # 验证上传是否成功
    # uploaded_file_name = page.locator("#uploaded-files").text_content()
    # if uploaded_file_name == "合同.pdf":
    #     print("文件上传成功")
    # else:
    #     print("文件上传失败")

    # ---------------------
    context.close()
    browser.close()


with sync_playwright() as playwright:
    run(playwright)
