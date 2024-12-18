import cv2
import dlib
import numpy as np
import winsound
from datetime import datetime, timedelta

# 常量定义
KNOWN_WIDTH = 6.0  # cm - 平均人眼宽度
FOCAL_LENGTH = 875  # 需要根据你的摄像头进行校准
DISTANCE_THRESHOLD = 30  # 距离阈值，单位为厘米
SCREEN_TIME_LIMIT = timedelta(minutes=20)  # 屏幕时间限制
BREAK_DURATION = timedelta(seconds=20)  # 休息间隔时间

# 初始化变量
detector = dlib.get_frontal_face_detector()
last_break_time = datetime.min
is_on_break = False


def distance_to_camera(known_width, focal_length, pixel_width):
    return (known_width * focal_length) / pixel_width


def detect_faces(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = detector(gray)
    return faces


def play_warning_sound():
    frequency = 2500  # 设置声音频率
    duration = 1000  # 持续时间，单位毫秒
    winsound.Beep(frequency, duration)


def check_screen_time():
    global last_break_time, is_on_break
    current_time = datetime.now()
    if not is_on_break and current_time - last_break_time >= SCREEN_TIME_LIMIT:
        is_on_break = True
        print("It's time for a break!")
        play_warning_sound()
        last_break_time = current_time
        return True
    elif is_on_break and current_time - last_break_time >= BREAK_DURATION:
        is_on_break = False
        print("Break over, you can continue using the screen.")
    return is_on_break


def main():
    cap = cv2.VideoCapture(0)

    while True:
        ret, frame = cap.read()
        if not ret:
            print("无法获取摄像头数据")
            break

        faces = detect_faces(frame)
        too_close = False

        for rect in faces:
            x, y, w, h = rect.left(), rect.top(), rect.width(), rect.height()
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

            dist = distance_to_camera(KNOWN_WIDTH, FOCAL_LENGTH, w)
            text = f"Distance: {dist:.2f}cm"
            cv2.putText(frame, text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

            if dist < DISTANCE_THRESHOLD:
                too_close = True
                play_warning_sound()
                cv2.putText(frame, "WARNING: Too Close!", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

        if not too_close:
            if check_screen_time():
                cv2.putText(frame, "Take a Break!", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

        cv2.imshow('Camera Feed', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()