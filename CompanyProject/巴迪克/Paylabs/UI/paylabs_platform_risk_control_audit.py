import logging
from playwright.sync_api import Page
from CompanyProject.巴迪克.utils.logger import get_logger
from CompanyProject.巴迪克.utils.retry import default_retry
# from CompanyProject.巴迪克.utils.generate_google_code import GoogleAuth
from CompanyProject.巴迪克.utils.perform_slider_unlock import perform_block_slider_verification


def platform_risk_control_audit(page, merchant_id, pdf_file_path):
    # 开始风险审核
    page.get_by_role("link", name=" Risk Control ").click()
    page.get_by_role("link", name="Risk Control", exact=True).click()
    # page.pause()
    # page.locator(".DTFC_RightBodyLiner > .table > tbody > tr:nth-child(3) > td > .mb-2 > .btnAudit").click()

    # 移动滑块
    scroll_div = page.wait_for_selector('#scrollDiv')  # 等待目标 div 加载
    scroll_div_table = page.query_selector('#scrollDivTable')  # 获取 scrollDivTable 的宽度
    scroll_width = scroll_div_table.evaluate('(element) => element.offsetWidth')
    scroll_div.evaluate(f'(element) => element.scrollLeft = {scroll_width}')  # 滚动到最右侧

    # row = page.locator(f"tbody tr").filter(has_text=merchant_id)
    # #
    # # # 查找该行中的 Setting Sales 按钮
    # setting_sales_button = row.locator("button[name='btnSetSales']")
    # risk_control_audit_button = row.locator("#btnAudit").first
    #文本含‘Risk Control Audit’,含data属性的按钮
    # page.pause()
    # risk_control_audit_button = row.get_by_role("button", name="Risk Control Audit", exact=True)
    # 在某个具体的 <tr> 中查找按钮
    # risk_control_audit_button = page.locator("tbody tr").filter(has_text=merchant_id).get_by_role("button", name="Risk Control Audit")

    # risk_control_audit_button = page.locator(".DTFC_RightBodyLiner > .table > tbody > tr > td > .mb-2 > .btnAudit").first.click()
    try:
        # 等待按钮可点击
        # page.pause()
        # 尝试直接使用 JavaScript 点击按钮
        # page.evaluate('(button) => button.click()', risk_control_audit_button.element_handle())
        # page.get_by_role("button", name="Risk Control Audit").filter(has_text=merchant_id).click()
        # 或者使用 data 属性中的 merchantNo 进行筛选
        page.locator("tbody tr").filter(has_text=merchant_id).get_by_role("button", name="Risk Control Audit").click()

    except Exception as e:
        print(f"Risk Control Audit按钮点击失败：{e}")
    # page.locator(".DTFC_RightBodyLiner > .table > tbody > tr > td > .mb-2 > .btnAudit").first.click()

    page.get_by_role("textbox", name="Max 200 characters can be").fill("评论：风险控制审计通过")
    page.locator("#toRiskAudit").click()

    page.get_by_role("link", name="None").click()

    # 上传风控报告
    page.on('filechooser', lambda file_chooser: file_chooser.set_files(pdf_file_path))
    page.locator("#reportForm1").click()

    page.get_by_role("textbox", name="Max 200 characters can be").fill("评论：风控报告上传成功，风险控制审计通过2")
    page.get_by_role("button", name="Approve").click()
    page.locator("#btnSubmitSure").click()
    # page2.get_by_role("button", name="Approve").click()
    print("风险审核通过")