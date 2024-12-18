import kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.graphics.texture import Texture
from kivy.clock import Clock
import cv2
import numpy as np
import sqlite3
import time

# 加载人脸和眼睛检测模型
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')

# 距离阈值（单位：厘米）
distance_threshold = 30
# 使用时间阈值（单位：分钟）
time_threshold = 45

class MainScreen(BoxLayout):
    def __init__(self, **kwargs):
        super(MainScreen, self).__init__(**kwargs)
        self.cap = cv2.VideoCapture(0)  # 打开手机摄像头
        self.texture = Texture.create(size=(640, 480))
        self.start_time = None
        self.total_time = 0
        self.monitoring = False
        self.paused = False

        # 创建数据库连接和游标
        self.conn = sqlite3.connect('eye_health.db')
        self.cursor = self.conn.cursor()

        # 创建用眼数据表格（如果不存在）
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS eye_usage
                            (id INTEGER PRIMARY KEY AUTOINCREMENT,
                            start_time TEXT,
                            end_time TEXT,
                            distance REAL,
                            duration REAL)''')

    def start_monitoring(self):
        if not self.monitoring:
            print("开始监测...")
            self.monitoring = True
            self.start_time = time.time()
            Clock.schedule_interval(self.update, 1.0 / 30.0)  # 每1/30秒更新一次画面
            self.ids.pause_monitoring.disabled = False
            self.ids.start_monitoring.disabled = True

    def pause_monitoring(self):
        if self.monitoring and not self.paused:
            print("暂停监测...")
            self.paused = True
            Clock.unschedule(self.update)
            self.ids.pause_monitoring.text = "继续监测"
            self.ids.start_monitoring.disabled = False
        elif self.monitoring and self.paused:
            print("继续监测...")
            self.paused = False
            Clock.schedule_interval(self.update, 1.0 / 30.0)
            self.ids.pause_monitoring.text = "暂停监测"
            self.ids.start_monitoring.disabled = True

    def open_settings(self):
        print("打开设置...")

    def show_report(self):
        print("查看用眼报告...")
        generate_report()

    def update(self, dt):
        if self.monitoring and not self.paused:
            ret, frame = self.cap.read()
            if ret:
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

                # 检测人脸
                faces = face_cascade.detectMultiScale(gray, 1.3, 5)
                for (x, y, w, h) in faces:
                    # 在人脸区域检测眼睛
                    roi_gray = gray[y:y + h, x:x + w]
                    eyes = eye_cascade.detectMultiScale(roi_gray)

                    # 计算眼睛中心坐标
                    eye_centers = []
                    for (ex, ey, ew, eh) in eyes:
                        eye_centers.append((x + ex + ew // 2, y + ey + eh // 2))

                    if len(eye_centers) == 2:
                        # 计算眼睛间距
                        eye_distance = np.linalg.norm(np.array(eye_centers[0]) - np.array(eye_centers[1]))

                        # 根据眼睛间距估算距离（这里只是简单示例，实际需更精确校准）
                        estimated_distance = 50 * 3 / eye_distance

                        # 检查距离是否过近
                        if estimated_distance < distance_threshold:
                            print("距离过近！")
                            # 这里可以添加声音提醒等操作，例如使用 plyer 库播放声音
                            from plyer import notification
                            notification.notify(title='警告', message='眼睛距离屏幕过近，请保持适当距离！')

                        # 更新使用时间
                        self.total_time = time.time() - self.start_time
                        self.ids.time_label.text = time.strftime('%H:%M:%S', time.gmtime(self.total_time))

                        # 检查使用时间是否过长
                        if self.total_time > time_threshold * 60:
                            print("使用时间过长！")
                            # 这里可以添加限制使用等操作，例如暂停监测
                            self.pause_monitoring()
                            notification.notify(title='警告', message='使用时间过长，请休息一下！')

                        # 将用眼数据插入数据库
                        self.cursor.execute("INSERT INTO eye_usage (start_time, end_time, distance, duration) VALUES (?,?,?,?)",
                                            (self.start_time, time.time(), estimated_distance, self.total_time))
                        self.conn.commit()

                        # 更新距离显示
                        self.ids.distance_label.text = f"{estimated_distance:.2f} cm"

                # 将图像转换为纹理并显示在界面上
                buf = cv2.flip(frame, 0).tostring()
                self.texture.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
                self.ids.camera_view.texture = self.texture

class EyeHealthApp(App):
    def build(self):
        return MainScreen()

if __name__ == '__main__':
    EyeHealthApp().run()