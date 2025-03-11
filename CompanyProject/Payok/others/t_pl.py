from playwright.sync_api import sync_playwright


def slide_verification():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)  # 设置为 headless=False 便于查看执行过程，可按需修改为 True
        page = browser.new_page()
        page.goto("http://paylabs-test.com/platform/paylabs-user-login.html")

        # 定位滑块元素
        slider = page.locator('.verify-move-block')
        # 定位滑块轨道元素（这里假设滑块轨道是包含滑块的父元素）
        track = page.locator('.verify-bar-area')

        # 获取滑块和轨道的边界信息
        slider_bounding_box = slider.bounding_box()
        track_bounding_box = track.bounding_box()

        if slider_bounding_box and track_bounding_box:
            start_x = slider_bounding_box['x'] + slider_bounding_box['width'] / 2
            start_y = slider_bounding_box['y'] + slider_bounding_box['height'] / 2
            end_x = track_bounding_box['x'] + track_bounding_box['width'] - 10  # 减去一定值，避免滑出边界
            end_y = start_y

            # 模拟按下鼠标左键
            page.mouse.down(x=start_x, y=start_y)
            # 模拟拖动滑块
            page.mouse.move(x=end_x, y=end_y)
            # 模拟释放鼠标左键
            page.mouse.up(x=end_x, y=end_y)

        page.wait_for_timeout(3000)  # 等待验证完成，可根据实际情况调整时间
        browser.close()


if __name__ == "__main__":
    slide_verification()