import time
import tkinter as tk
from tkinter import messagebox

import winsound


class TimerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("倒计时/定时器")
        self.root.geometry("300x250")

        self.hours = tk.StringVar()
        self.minutes = tk.StringVar()
        self.seconds = tk.StringVar()
        self.mode = tk.StringVar(value="1")
        self.total_seconds = 0
        self.running = False
        self.alarm_running = False
        self.original_total_seconds = 0

        self.create_widgets()

    def create_widgets(self):
        # 输入框
        tk.Label(self.root, text="小时").grid(row=0, column=0)
        tk.Entry(self.root, textvariable=self.hours).grid(row=0, column=1)

        tk.Label(self.root, text="分钟").grid(row=1, column=0)
        tk.Entry(self.root, textvariable=self.minutes).grid(row=1, column=1)

        tk.Label(self.root, text="秒").grid(row=2, column=0)
        tk.Entry(self.root, textvariable=self.seconds).grid(row=2, column=1)

        # 选择模式
        tk.Radiobutton(self.root, text="倒计时", variable=self.mode, value="1").grid(row=3, column=0)
        tk.Radiobutton(self.root, text="定时", variable=self.mode, value="2").grid(row=3, column=1)

        # 开始按钮
        tk.Button(self.root, text="开始", command=self.start_timer).grid(row=4, column=0, columnspan=2)

        # 继续和停止按钮
        self.continue_button = tk.Button(self.root, text="继续", command=self.continue_timer, state=tk.DISABLED)
        self.continue_button.grid(row=5, column=0)
        self.stop_button = tk.Button(self.root, text="停止", command=self.stop_timer, state=tk.DISABLED)
        self.stop_button.grid(row=5, column=1)

    def start_timer(self):
        if self.running:
            return

        try:
            hours = int(self.hours.get())
            minutes = int(self.minutes.get())
            seconds = int(self.seconds.get())
            if hours < 0 or minutes < 0 or seconds < 0:
                raise ValueError
            self.total_seconds = hours * 3600 + minutes * 60 + seconds
            self.original_total_seconds = self.total_seconds

            if self.mode.get() == '1':
                self.countdown(self.total_seconds)
            else:
                self.timer(self.total_seconds)

            self.running = True
        except ValueError:
            messagebox.showerror("错误", "请输入有效的数字！")

    def countdown(self, total_seconds):
        while total_seconds > 0:
            mins, secs = divmod(total_seconds, 60)
            timeformat = '{:02d}:{:02d}'.format(mins, secs)
            self.root.title(f"倒计时 - {timeformat}")
            self.root.update()
            time.sleep(1)
            total_seconds -= 1
        self.show_popup()

    def timer(self, total_seconds):
        while total_seconds > 0:
            mins, secs = divmod(total_seconds, 60)
            timeformat = '{:02d}:{:02d}'.format(mins, secs)
            self.root.title(f"定时 - {timeformat}")
            self.root.update()
            time.sleep(1)
            total_seconds -= 1
        self.show_popup()

    def show_popup(self):
        self.running = False
        self.continue_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.NORMAL)
        self.play_alarm()

        self.root.after(5000, self.reset_and_start)

    def reset_and_start(self):
        if not self.running and not self.alarm_running:
            self.continue_button.config(state=tk.DISABLED)
            self.stop_button.config(state=tk.DISABLED)
            self.total_seconds = self.original_total_seconds
            self.start_timer()

    def play_alarm(self):
        self.alarm_running = True
        frequency = 2500  # Set Frequency To 2500 Hertz
        duration = 1000  # Set Duration To 1000 ms == 1 second
        for _ in range(10):  # 播放10秒
            winsound.Beep(frequency, duration)
            time.sleep(1)  # 间隔1秒播放一次
        self.alarm_running = False

    def continue_timer(self):
        self.running = True
        self.continue_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.DISABLED)
        self.start_timer()

    def stop_timer(self):
        self.running = False
        self.continue_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.DISABLED)

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    root = tk.Tk()
    app = TimerApp(root)
    app.run()
