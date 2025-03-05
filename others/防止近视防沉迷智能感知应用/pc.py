import cv2
import numpy as np
import threading
import winsound
from datetime import datetime
from tkinter import *
from tkinter import ttk


class EyeProtector:
    def __init__(self):
        # 加载人脸检测器
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        self.distance_threshold = 30  # 30厘米阈值
        self.is_running = False
        self.timer = None
        self.study_duration = 0  # 学习时长（分钟）
        self.reference_distance = 50  # 参考距离（厘米）
        self.reference_width = 300  # 参考人脸宽度（像素）

        # 创建GUI窗口
        self.root = Tk()
        self.root.title("智能防近视防沉迷助手")
        self.setup_gui()

    def setup_gui(self):
        # 创建定时器设置框架
        timer_frame = ttk.LabelFrame(self.root, text="定时器设置")
        timer_frame.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")

        # 添加时长选择
        ttk.Label(timer_frame, text="学习时长：").grid(row=0, column=0, padx=5, pady=5)
        self.duration_var = StringVar(value="15")
        duration_combo = ttk.Combobox(timer_frame, textvariable=self.duration_var)
        duration_combo['values'] = (15, 30, 45)
        duration_combo.grid(row=0, column=1, padx=5, pady=5)

        # 添加开始/停止按钮
        self.start_btn = ttk.Button(timer_frame, text="开始监测", command=self.toggle_monitoring)
        self.start_btn.grid(row=1, column=0, columnspan=2, pady=10)

        # 添加状态显示
        self.status_label = ttk.Label(self.root, text="状态：未开始")
        self.status_label.grid(row=1, column=0, pady=5)

        # 添加距离显示
        self.distance_label = ttk.Label(self.root, text="当前距离：--厘米")
        self.distance_label.grid(row=2, column=0, pady=5)

    def toggle_monitoring(self):
        if not self.is_running:
            self.start_monitoring()
            self.start_btn.config(text="停止监测")
            self.status_label.config(text="状态：监测中")
        else:
            self.stop_monitoring()
            self.start_btn.config(text="开始监测")
            self.status_label.config(text="状态：已停止")

    def start_monitoring(self):
        self.is_running = True
        self.study_duration = int(self.duration_var.get())

        # 启动摄像头监测线程
        self.camera_thread = threading.Thread(target=self.monitor_distance)
        self.camera_thread.daemon = True
        self.camera_thread.start()

        # 启动定时器
        self.start_timer()

    def stop_monitoring(self):
        self.is_running = False
        if self.timer:
            self.timer.cancel()
        self.distance_label.config(text="当前距离：--厘米")

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
            self.status_label.config(text="错误：未检测到可用的摄像头设备")
            self.stop_monitoring()
            return

        # 使用第一个可用的摄像头
        cap = cv2.VideoCapture(available_cameras[0])
        if not cap.isOpened():
            self.status_label.config(text="错误：无法打开摄像头设备")
            self.stop_monitoring()
            return

        while self.is_running:
            try:
                ret, frame = cap.read()
                if not ret:
                    self.status_label.config(text="错误：无法读取摄像头画面")
                    continue

                # 转换为灰度图
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

                # 检测人脸
                faces = self.face_cascade.detectMultiScale(
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

                    # 更新距离显示
                    self.root.after(0, lambda: self.distance_label.config(
                        text=f"当前距离：{estimated_distance:.1f}厘米"))

                    if estimated_distance < self.distance_threshold:
                        self.alert_distance()

                # 显示画面
                cv2.imshow('Monitor', frame)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break

            except Exception as e:
                self.status_label.config(text=f"错误：{str(e)}")
                break

        cap.release()
        cv2.destroyAllWindows()

    def start_timer(self):
        self.timer = threading.Timer(self.study_duration * 60, self.alert_time_up)
        self.timer.start()

    def alert_distance(self):
        # 发出提示音
        winsound.Beep(1000, 500)
        self.status_label.config(text="警告：请保持正确距离！")

    def alert_time_up(self):
        # 发出提示音
        winsound.Beep(2000, 1000)
        self.status_label.config(text=f"时间到！已经学习了{self.study_duration}分钟")
        self.stop_monitoring()

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    app = EyeProtector()
    app.run()