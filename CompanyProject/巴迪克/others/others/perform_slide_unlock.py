import random

def perform_slide_unlock(page):
    adjustment = 0  # 初始化调整值为0

    for _ in range(5):  # 尝试5次
        try:
            # 获取 verify-gap 的 left 值和坐标
            gap_left = page.evaluate('''
                () => {
                    const gapElement = document.querySelector('.verify-gap');
                    const rect = gapElement.getBoundingClientRect();
                    return {
                        left: window.getComputedStyle(gapElement).getPropertyValue('left'),
                        x: rect.left,
                        y: rect.top
                    };
                }
            ''')
            gap_left_value = float(gap_left['left'].replace('px', ''))  # 转换为浮点数
            print(f"verify-gap coordinates: ({gap_left['x']}, {gap_left['y']})")
            print(f"verify-gap left value: {gap_left_value} px")

            slider = page.locator(".verify-move-block")
            slider_box = slider.bounding_box()
            print(f"Slider bounding box: {slider_box}")

            target_x = slider_box['x'] + gap_left_value + adjustment  # 计算目标位置并加上调整值
            target_y = slider_box['y'] + slider_box['height'] / 2

            print(f"Target position: ({target_x}, {target_y})")

            page.mouse.move(slider_box['x'], slider_box['y'] + slider_box['height'] / 2)
            page.mouse.down()

            # 分步骤移动滑块，模拟真实用户操作
            step_size = 10
            current_x = slider_box['x']
            while current_x < target_x:
                next_x = min(current_x + step_size + random.uniform(-2, 2), target_x)  # 添加随机偏移量
                page.mouse.move(next_x, target_y + random.uniform(-2, 2))  # 调整 y 坐标以模拟手抖
                current_x = next_x

            page.mouse.up()

            page.wait_for_timeout(5000)

            # 检查 verify-left-bar 的宽度是否与目标位置相等
            left_bar_width = page.evaluate('''
                () => {
                    const leftBarElement = document.querySelector('.verify-left-bar');
                    return window.getComputedStyle(leftBarElement).getPropertyValue('width');
                }
            ''')
            left_bar_width_value = float(left_bar_width.replace('px', ''))
            print(f"verify-left-bar width: {left_bar_width_value} px")

            difference = abs(left_bar_width_value - gap_left_value)
            print(f"Difference between left bar width and gap left: {difference} px")

            if difference <= 2:  # 允许一定的误差范围
                print("滑动解锁成功")
                return True
            else:
                print("滑动解锁未成功，重试")
                # 在下一次重试时加上差距的一半（逐步逼近）
                adjustment += (gap_left_value - left_bar_width_value) / 2
                continue
        except Exception as e:
            print(f"滑动解锁失败，重试: {e}")
            page.wait_for_timeout(3000)  # 等待3秒后重试
    return False


# if not perform_slide_unlock(page):
#     print("滑动解锁多次尝试后仍失败")
#     context.close()
#     browser.close()
#     return
