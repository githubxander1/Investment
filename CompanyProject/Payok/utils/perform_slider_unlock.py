import re

import cv2
import numpy as np
import requests


def perform_slide_unlock(page):
    def get_dis(bj_rgb, hk_rgb):
        # 解析x距离
        # 灰度处理
        bj_gray = cv2.cvtColor(bj_rgb, cv2.COLOR_RGB2GRAY)
        # 读取滑块的rgb码
        hk_gray = cv2.cvtColor(hk_rgb, cv2.COLOR_RGB2GRAY)

        # 使用更精确的匹配方法，如SIFT或SURF
        sift = cv2.SIFT_create()
        kp1, des1 = sift.detectAndCompute(bj_gray, None)
        kp2, des2 = sift.detectAndCompute(hk_gray, None)

        bf = cv2.BFMatcher()
        matches = bf.knnMatch(des1, des2, k=2)

        good = []
        for m, n in matches:
            if m.distance < 0.75 * n.distance:
                good.append([m])

        if len(good) > 10:
            src_pts = np.float32([kp1[m.queryIdx].pt for m in good[0]]).reshape(-1, 1, 2)
            dst_pts = np.float32([kp2[m.trainIdx].pt for m in good[0]]).reshape(-1, 1, 2)

            M, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 5.0)
            h, w = hk_gray.shape
            pts = np.float32([[0, 0], [0, h - 1], [w - 1, h - 1], [w - 1, 0]]).reshape(-1, 1, 2)
            dst = cv2.perspectiveTransform(pts, M)
            x = dst[0][0][0]
            return x
        else:
            return 0

    for _ in range(5):  # 尝试5次
        try:
            # 获取验证码图片
            img_bj = page.locator(".verify-img-panel")
            img_hk = page.locator(".verify-move-block")

            # 获取原图下载地址
            src_bj = img_bj.evaluate("el => el.style.backgroundImage").split('"')[1]
            # 仅去掉第一个 .
            src_bj = re.sub(r'\.', '', src_bj, count=1)
            # src_bj = re.sub(r'\.\.', '', src_bj)

            src_hk = img_hk.locator(".verify-sub-block").evaluate("el => el.style.backgroundImage").split('"')[1]
            # 仅去掉第一个 .
            src_hk = re.sub(r'\.', '', src_hk, count=1)

            # 去除多余的点号
            src_bj = re.sub(r'\.\.', '', src_bj)
            src_hk = re.sub(r'\.\.', '', src_hk)

            base_url = 'http://payok-test.com/merchant'
            # 确保URL是完整的URL
            if not src_bj.startswith('http'):
                src_bj = base_url + src_bj
            if not src_hk.startswith('http'):
                src_hk = base_url + src_hk

            print(f"Background Image URL: {src_bj}")
            print(f"Slider Image URL: {src_hk}")

            # 通过requests下载图片的二进制码
            response_bj = requests.get(src_bj)
            response_bj.raise_for_status()  # 检查请求是否成功
            with open('bj.png', 'wb') as f:
                f.write(response_bj.content)

            response_hk = requests.get(src_hk)
            response_hk.raise_for_status()  # 检查请求是否成功
            with open('hk.png', 'wb') as f:
                f.write(response_hk.content)

            # 读取背景图片的rgb码
            bj_rgb = cv2.imread('bj.png')
            if bj_rgb is None:
                print("Failed to read background image")
                continue

            # 读取滑块的rgb码
            hk_rgb = cv2.imread('hk.png')
            if hk_rgb is None:
                print("Failed to read slider image")
                continue

            # 打印图像信息
            print(f"Background Image Shape: {bj_rgb.shape}, Type: {bj_rgb.dtype}")
            print(f"Slider Image Shape: {hk_rgb.shape}, Type: {hk_rgb.dtype}")

            # 确保图像类型和深度一致
            bj_rgb = cv2.cvtColor(bj_rgb, cv2.COLOR_BGR2RGB)
            hk_rgb = cv2.cvtColor(hk_rgb, cv2.COLOR_BGR2RGB)

            x = get_dis(bj_rgb, hk_rgb)
            if x == 0:
                print("Failed to find valid match position")
                continue

            slider = page.locator(".verify-move-block")
            slider_box = slider.bounding_box()
            target_x = slider_box['x'] + x
            target_y = slider_box['y'] + slider_box['height'] / 2

            page.mouse.move(slider_box['x'], slider_box['y'] + slider_box['height'] / 2, steps=10)
            page.mouse.down()
            page.mouse.move(target_x, target_y, steps=10)
            page.mouse.up()

            # 等待滑动解锁成功后的页面变化
            try:
                page.wait_for_selector(".success-message", state='visible', timeout=10000)
                return True
            except Exception as e:
                print(f"Waiting for success message failed: {e}")
                continue
        except Exception as e:
            print(f"滑动解锁失败，重试: {e}")
            page.wait_for_timeout(1000)
    return False
