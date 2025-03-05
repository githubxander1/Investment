from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.spinner import Spinner
from kivy.clock import Clock
from kivy.core.window import Window

try:
    import cv2
except ImportError:
    # 尝试安装opencv-python包
    import subprocess
    import sys

    subprocess.check_call([sys.executable, "-m", "pip", "install", "opencv-python"])
    import cv2

import numpy as np
import threading
from datetime import datetime, timedelta
import os

# 加载人脸检测器
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')


class EyeProtectorMobile(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = 20
        self.spacing = 10

        # 初始化变量
        self.distance_threshold = 30
        self.is_running = False
        self.study_duration = 15  # 默认15分钟
        self.remaining_time = 0
        self.camera_thread = None
        self.reference_distance = 50  # 参考距离（厘米）
        self.reference_width = 300  # 参考人脸宽度（像素）

        # 创建UI组件
        self.setup_ui()

    def setup_ui(self):
        # 标题
        self.title_label = Label(
            text='智能防近视防沉迷助手',
            size_hint=(1, 0.2),
            font_size='20sp'
        )
        self.add_widget(self.title_label)

        # 时长选择
        duration_layout = BoxLayout(size_hint=(1, 0.2))
        duration_label = Label(
            text='学习时长：',
            size_hint=(0.4, 1)
        )
        self.duration_spinner = Spinner(
            text='15',
            values=('15', '30', '45'),
            size_hint=(0.6, 1)
        )
        duration_layout.add_widget(duration_label)
        duration_layout.add_widget(self.duration_spinner)
        self.add_widget(duration_layout)

        # 倒计时显示
        self.timer_label = Label(
            text='剩余时间：00:00',
            size_hint=(1, 0.2)
        )
        self.add_widget(self.timer_label)

        # 状态显示
        self.status_label = Label(
            text='状态：未开始',
            size_hint=(1, 0.2)
        )
        self.add_widget(self.status_label)

        # 开始/停止按钮
        self.start_button = Button(
            text='开始监测',
            size_hint=(1, 0.2)
        )
        self.start_button.bind(on_press=self.toggle_monitoring)
        self.add_widget(self.start_button)

    def toggle_monitoring(self, instance):
        if not self.is_running:
            self.start_monitoring()
            self.start_button.text = '停止监测'
            self.status_label.text = '状态：监测中'
        else:
            self.stop_monitoring()
            self.start_button.text = '开始监测'
            self.status_label.text = '状态：已停止'

    def start_monitoring(self):
        self.is_running = True
        self.study_duration = int(self.duration_spinner.text)
        self.remaining_time = self.study_duration * 60

        # 启动摄像头监测线程
        self.camera_thread = threading.Thread(target=self.monitor_distance)
        self.camera_thread.daemon = True
        self.camera_thread.start()

        # 启动倒计时
        Clock.schedule_interval(self.update_timer, 1)

    def stop_monitoring(self):
        self.is_running = False
        Clock.unschedule(self.update_timer)
        self.timer_label.text = '剩余时间：00:00'

    def update_timer(self, dt):
        if self.remaining_time > 0:
            self.remaining_time -= 1
            minutes = self.remaining_time // 60
            seconds = self.remaining_time % 60
            self.timer_label.text = f'剩余时间：{minutes:02d}:{seconds:02d}'
        else:
            self.alert_time_up()
            return False
        return True

    def estimate_distance(self, face_width):
        # 使用简单的反比例关系估算距离
        # distance = reference_distance * (reference_width / face_width)
        return self.reference_distance * (self.reference_width / face_width)

    def monitor_distance(self):
        # 尝试获取可用的摄像头列表
        available_cameras = []
        for i in range(5):  # 检查前5个摄像头设备
            cap = cv2.VideoCapture(i)
            if cap.isOpened():
                available_cameras.append(i)
                cap.release()

        if not available_cameras:
            Clock.schedule_once(lambda dt: setattr(self.status_label, 'text', '错误：未检测到可用的摄像头设备'))
            self.stop_monitoring()
            return

        # 使用第一个可用的摄像头
        cap = cv2.VideoCapture(available_cameras[0])
        if not cap.isOpened():
            Clock.schedule_once(lambda dt: setattr(self.status_label, 'text', '错误：无法打开摄像头设备'))
            self.stop_monitoring()
            return

        while self.is_running:
            try:
                ret, frame = cap.read()
                if not ret:
                    Clock.schedule_once(lambda dt: setattr(self.status_label, 'text', '错误：无法读取摄像头画面'))
                    continue

                # 转换为灰度图
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

                # 检测人脸
                faces = face_cascade.detectMultiScale(
                    gray,
                    scaleFactor=1.1,
                    minNeighbors=5,
                    minSize=(30, 30)
                )

                if len(faces) > 0:
                    # 使用最大的人脸
                    face = max(faces, key=lambda x: x[2] * x[3])
                    x, y, w, h = face

                    # 估算距离
                    estimated_distance = self.estimate_distance(w)

                    if estimated_distance < self.distance_threshold:
                        self.alert_distance()

            except Exception as e:
                Clock.schedule_once(lambda dt: setattr(self.status_label, 'text', f'错误：{str(e)}'))
                break

        cap.release()

    def alert_distance(self):
        # 在主线程中更新UI
        Clock.schedule_once(lambda dt: setattr(self.status_label, 'text', '警告：请保持正确距离！'))

    def alert_time_up(self):
        self.stop_monitoring()
        Clock.schedule_once(
            lambda dt: setattr(self.status_label, 'text', f'时间到！已经学习了{self.study_duration}分钟'))


class EyeProtectorMobileApp(App):
    def build(self):
        return EyeProtectorMobile()


if __name__ == '__main__':
    Window.size = (360, 640)  # 设置窗口大小模拟手机屏幕
    EyeProtectorMobileApp().run()