import subprocess
def take_screenshot(save_path):
    subprocess.run(f"adb shell screencap -p /sdcard/screen.png", shell=True)
    subprocess.run(f"adb pull /sdcard/screen.png {save_path}", shell=True)


import cv2


def find_element_coords(screenshot_path, step_desc):
    # 1. 调用通义千问分析元素特征
    prompt = f"这是同花顺APP的截图：{screenshot_path}，步骤是{step_desc}。请描述目标元素的颜色、形状、位置（如左上角/中间），用坐标范围表示（例如x1=100,y1=200,x2=300,y2=400）"
    element_desc = call_qianwen(prompt)  # 得到类似"红色按钮，x1=500,y1=800,x2=700,y2=900"

    # 2. 解析坐标（或用OpenCV模板匹配细化）
    # 简化：直接提取AI返回的坐标
    coords = parse_coords(element_desc)  # 自定义函数：从文本中提取x1,y1,x2,y2
    return (coords["x1"], coords["y1"])  # 返回点击中心点