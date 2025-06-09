from tenacity import retry, stop_after_attempt

# @retry(stop=stop_after_attempt(3))
# def slide_verification(page):
#     """
#     滑动滑块验证
#
#     参数:
#     page: Playwright页面对象
#     """
#     # 等待滑动验证元素加载完成
#     page.wait_for_selector('.verify-move-block', state='visible')
#
#     # 获取滑块元素
#     slider = page.locator('.verify-move-block')
#
#     # 获取滑动条宽度
#     slider_bar = page.locator('.verify-left-bar')
#     bounding_box = slider_bar.bounding_box()
#     if bounding_box is None:
#         raise ValueError("滑动条元素未找到")
#
#     slider_width = bounding_box['width']
#
#     # 获取滑块的初始位置
#     slider_box = slider.bounding_box()
#     if slider_box is None:
#         raise ValueError("滑块元素未找到")
#
#     # 模拟鼠标按下滑块
#     slider.hover()
#     slider.evaluate('element => element.dispatchEvent(new MouseEvent("mousedown", { bubbles: true }))')
#
#     # 模拟鼠标移动并释放，这里使用更精确的移动距离
#     target_x = slider_box['x'] + slider_width - 10  # 减去10是为了避免滑过头
#     target_y = slider_box['y'] + slider_box['height'] / 2
#     page.mouse.move(target_x, target_y)
#     page.mouse.up()
#
#     # 等待验证结果
#     page.wait_for_timeout(2000)  # 等待2秒以检查验证是否成功
#
#     # 检查验证是否成功（这里可以根据实际情况调整）
#     success_message = page.locator('.verify-msg').inner_text()
#     if "success" in success_message:
#         print("滑动验证成功")
#     else:
#         print("滑动验证失败")
#         raise Exception("滑动验证失败")  # 触发重试机制
# from tenacity import retry, stop_after_attempt

# @retry(stop=stop_after_attempt(3))
# def slide_verification(page):
#     """
#     滑动滑块验证
#
#     参数:
#     page: Playwright页面对象
#     """
#     # 等待滑动验证元素加载完成
#     page.wait_for_selector('.verify-move-block', state='visible')
#
#     # 获取滑动条和滑块元素
#     slider_bar = page.locator('.verify-left-bar')
#     slider = page.locator('.verify-move-block')
#
#     # 获取滑动条的宽度
#     slider_bar_bounding_box = slider_bar.bounding_box()
#     if slider_bar_bounding_box is None:
#         raise ValueError("滑动条元素未找到")
#     slider_bar_width = slider_bar_bounding_box['width']
#
#     # 获取滑块的初始位置
#     slider_bounding_box = slider.bounding_box()
#     if slider_bounding_box is None:
#         raise ValueError("滑块元素未找到")
#
#     # 模拟鼠标按下滑块
#     slider.hover()
#     slider.evaluate('element => element.dispatchEvent(new MouseEvent("mousedown", { bubbles: true }))')
#
#     # 动态计算目标位置并进行滑动
#     target_x = slider_bounding_box['x'] + slider_bar_width - slider_bounding_box['width']
#     target_y = slider_bounding_box['y'] + slider_bounding_box['height'] / 2
#     page.mouse.move(target_x, target_y)
#     page.mouse.up()
#
#     # 等待验证结果
#     page.wait_for_timeout(2000)  # 等待2秒以检查验证是否成功
#
#     # 检查滑动后的状态是否成功
#     slider_bar_bounding_box_after = slider_bar.bounding_box()
#     if slider_bar_bounding_box_after is None:
#         raise ValueError("滑动条元素未找到（滑动后）")
#
#     slider_bounding_box_after = slider.bounding_box()
#     if slider_bounding_box_after is None:
#         raise ValueError("滑块元素未找到（滑动后）")
#
#     # 检查滑动条宽度和滑块左偏移量是否一致
#     if abs(slider_bar_bounding_box_after['width'] - slider_bounding_box_after['x']) < 5:
#         print("滑动验证成功")
#     else:
#         print("滑动验证失败")
#         raise Exception("滑动验证失败")  # 触发重试机制