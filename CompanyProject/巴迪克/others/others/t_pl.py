from faker import Faker

faker=Faker(['zh_CN'])
print(faker.name())
print(faker.address())
print(faker.email())

# page.pause()
# 根据merchantid找到对应的行，这里假设merchantid在第一列
# merchant_id = "010407"
# rows =  page.query_selector_all('tbody[tr[role="row"]]')
# print(f"行数: {len(rows)}")
# for row in rows:
#     row_content = row.inner_text()
#     print(f"行内容: {row_content}")
#     cells =  row.query_selector_all('td')
#     print(f"列数: {len(cells)}")
#     print(f"内容：{[cell.text_content() for cell in cells]}")
#     first_cell_text =  cells[0].text_content()
#     print(f"第一列的内容: {first_cell_text}")
#     if first_cell_text == merchant_id:
#         # 找到对应的行后，点击Setting Sales按钮
#         setting_sales_button =  row.query_selector('button[name="btnSetSales"]')
#         if setting_sales_button:
#             expect(setting_sales_button).to_be_visible(timeout=5000)  # 等待5秒
#             setting_sales_button.click()
#             print(f"成功点击 {setting_sales_button} 按钮")
#             break
#         else:
#             print(f"未找到 {setting_sales_button} 按钮")
#             break