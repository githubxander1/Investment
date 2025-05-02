#登录滑块验证
def perform_block_slider_verification(page):
    slider = page.locator(".verify-move-block")
    slider_area = page.locator(".verify-bar-area")
    slider_area_bounding_box = slider_area.bounding_box()
    slider_bounding_box = slider.bounding_box()

    if not slider_area_bounding_box or not slider_bounding_box:
        raise Exception("无法获取滑块位置信息")

    slider_width = slider_bounding_box['width']
    slider_area_width = slider_area_bounding_box['width']
    distance_to_move = slider_area_width - slider_width

    # 拖拽操作
    page.mouse.move(slider_bounding_box['x'] + slider_width / 2, slider_bounding_box['y'] + slider_width / 2)
    page.mouse.down()
    page.mouse.move(slider_bounding_box['x'] + slider_width / 2 + distance_to_move, slider_bounding_box['y'] + slider_width / 2)
    page.mouse.up()

    page.wait_for_timeout(1000)  # 等待1秒观察情况