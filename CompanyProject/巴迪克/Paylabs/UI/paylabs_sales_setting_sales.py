import logging
from playwright.sync_api import Page
from CompanyProject.巴迪克.utils.logger import get_logger
from CompanyProject.巴迪克.utils.retry import default_retry
# from CompanyProject.巴迪克.utils.generate_google_code import GoogleAuth
from CompanyProject.巴迪克.utils.perform_slider_unlock import perform_block_slider_verification

def sales_setting_sales(page, merchant_id):
    page.get_by_role("link", name="ﱖ Merchant ").click()
    page.locator("#left-bar-menu").get_by_role("link", name="Merchant", exact=True).click()

    #选择要设置的sales
    page.wait_for_timeout(1000)
    page.pause()

    # if page.locator(f"tbody tr").filter(has_text=merchant_id).locator("//*[@id='merchant-datatable_wrapper']/div[2]/div/div[1]/div[2]/div[1]/div/table/thead/tr/th[11]").text_content() != "":
    #     print("销售设置成功")
    # else:
    #     print("销售设置失败")
    #     page.pause()

    # 移动滑块
    scroll_div = page.wait_for_selector('#scrollDiv')# 等待目标 div 加载
    scroll_div_table = page.query_selector('#scrollDivTable')# 获取 scrollDivTable 的宽度
    scroll_width = scroll_div_table.evaluate('(element) => element.offsetWidth')
    scroll_div.evaluate(f'(element) => element.scrollLeft = {scroll_width}')# 滚动到最右侧

    row = page.locator(f"tbody tr").filter(has_text=merchant_id)

    # seles_consultant_cell = row.locator("td").nth(10)
    # sales_consultant_content = seles_consultant_cell.text_content()
    # sales_consultant_content = merchant_status.text_content()
    # if sales_consultant_content != "":
    #     print("✅提示：销售设置成功,不需要再设置")
    # else:
    #     # print("销售设置失败")
    merchant_status = row.locator("td").nth(2)
    merchant_status_content = merchant_status.text_content()
    # print("商户状态：", merchant_status_content)
    if merchant_status_content != "New Merchant":
        print("⚠️提示：商户状态不是New Merchant，不需要再设置销售")
    else:
        setting_sales_button = row.locator("#btnSetSales").first
        try:
            page.evaluate('(button) => button.click()', setting_sales_button.element_handle())
        except Exception as e:
            print(f"点击设置sales按钮失败：{e}")
        page.locator('#select2-newSalesManModal-container').click()
        page.locator(".select2-results__option").nth(1).click()
        page.get_by_role("textbox", name="Remarks").fill("1设置sales")
        page.locator("#btnSureSaleModal").click()
        page.pause()
        #再次判断是否设置成功
        # sales_consultant_content = merchant_status_content.text_content()
        # if sales_consultant_content != "":
        #     print("✅销售设置成功")
        # else:
        #     print("销售设置失败")
        merchant_status_content = merchant_status.text_content()
        print("商户状态：", merchant_status_content)
        if merchant_status_content != "New Merchant":
            print("⚠️提示：商户状态不是New Merchant，设置成功")
        else:
            print("✅销售设置成功")
        #断言列表里merchantid这一行的sales consultant一列是否有内容，如果有，则设置成功
        # xpath='//*[@id="merchant-datatable_wrapper"]/div[2]/div/div[1]/div[2]/div[1]/div/table/thead/tr/th[11]'
