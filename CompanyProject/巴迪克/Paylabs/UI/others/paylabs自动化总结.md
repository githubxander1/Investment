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
    if merchant_status_content != "New Merchant":
        print("⚠️提示：商户状态不是New Merchant，不需要再设置销售")
    else:
        setting_sales_button = row.locator("#btnSetSales").first
        try:
            # page.evaluate('(button) => button.click()', setting_sales_button.element_handle())
            setting_sales_button.click()
        except Exception as e:
            print(f"点击设置sales按钮失败：{e}")

第二种：分左右wrapper
row = page.locator("tbody tr").filter(has_text=merchant_id)
    merchant_status = row.locator("td").nth(2)
    merchant_status_content = merchant_status.text_content()
    left_wrapper = page.locator(".dataTables_scrollBody")
    left_row = left_wrapper.locator("tbody tr").filter(has_text=merchant_id)
    left_row.wait_for(state="visible",timeout=3000)
    row_index = left_row.evaluate('(row) => Array.from(row.parentNode.children).indexOf(row)')
    right_wrapper = page.locator(".DTFC_RightBodyLiner")
    corresponding_right_row = right_wrapper.locator("tbody tr").nth(row_index)
    submit_button = corresponding_right_row.get_by_text("Submit")
    # submit_button = corresponding_right_row.locator('button',has_text="Submit")
        # page.get_by_text("Submit").click()
        # page.get_by_text("Submit").nth()
    if merchant_status_content == "Pending complete the information":
        with page.expect_popup() as popup_info:
            submit_button.click()