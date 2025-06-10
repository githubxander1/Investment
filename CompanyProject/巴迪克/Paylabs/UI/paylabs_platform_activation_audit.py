import logging
from playwright.sync_api import Page
from CompanyProject.巴迪克.utils.logger import get_logger
from CompanyProject.巴迪克.utils.retry import default_retry
# from CompanyProject.巴迪克.utils.generate_google_code import GoogleAuth
from CompanyProject.巴迪克.utils.perform_slider_unlock import perform_block_slider_verification


def platform_activation_audit(page,merchant_id):
    # 激活审核
    link_risk_control = page.get_by_role("link", name=" Risk Control ")
    if link_risk_control.get_attribute("class") != "active":
        page.get_by_role("link", name=" Risk Control ").click()
        page.get_by_role("link", name="Risk Control", exact=True).click()

    # 移动滑块
    scroll_div = page.wait_for_selector('#scrollDiv')  # 等待目标 div 加载
    scroll_div_table = page.query_selector('#scrollDivTable')  # 获取 scrollDivTable 的宽度
    scroll_width = scroll_div_table.evaluate('(element) => element.offsetWidth')
    scroll_div.evaluate(f'(element) => element.scrollLeft = {scroll_width}')  # 滚动到最右侧

    row = page.locator(f"tbody tr").filter(has_text=merchant_id)
    #
    # # 查找该行中的 Setting Sales 按钮
    # setting_sales_button = row.locator("button[name='btnSetSales']")
    # activate_audit_button = row.locator("#btnOnlineApply").first
    activate_audit_button = row.get_by_role('button', name="Activation Audit")
    try:
        # 等待按钮可点击
        # 尝试直接使用 JavaScript 点击按钮
        page.evaluate('(button) => button.click()', activate_audit_button.element_handle())
    except Exception as e:
        print(f"点击设置sales按钮失败：{e}")

    # page.locator("tr").filter(has_text=re.compile(r"^DataActivation AuditSystem Configuration$")).locator("button[name=\"btnOnlineApply\"]").click()
    page.get_by_role("textbox", name="Max 200 characters can be").fill("评论：激活审核通过")
    # page.get_by_role("button", name="Comment").click()#不能评论？
    page.get_by_role("button", name="Passed").click()
    print("激活审核通过")
    # expect(page.locator("#merchant-datatable")).to_match_aria_snapshot("- text: Active")
    print("商户入驻成功！")


    # 退出登录
    page.locator("#txtOperatorName").click()
    page.locator("a").filter(has_text="Log Out").click()
    page.get_by_role("button", name="Submit").click()
    print("退出登录成功")