import tkinter as tk

import winsound  # Windows系统下播放声音


class CountdownApp:
    def __init__(self, root):
        self.root = root
        self.root.title("倒计时应用")

        self.time_label = tk.Label(root, text="倒计时: 0 秒", font=("Arial", 24))
        self.time_label.pack(pady=20)

        self.start_button = tk.Button(root, text="开始倒计时", command=self.start_countdown)
        self.start_button.pack(pady=10)

        self.continue_button = tk.Button(root, text="继续", command=self.continue_countdown)
        self.continue_button.pack(pady=10)

        self.stop_button = tk.Button(root, text="停止", command=self.stop_countdown)
        self.stop_button.pack(pady=10)

        self.countdown_running = False
        self.countdown_time = 0
        self.default_countdown_time = 3  # 默认倒计时时间（秒）

        # 设置默认倒计时时间为3秒后自动开始
        self.root.after(3000, self.start_countdown)

    def start_countdown(self):
        if not self.countdown_running:
            self.countdown_time = self.default_countdown_time
            self.countdown_running = True
            self.update_countdown()

    def continue_countdown(self):
        if self.countdown_running:
            self.countdown_time = self.default_countdown_time
            self.update_countdown()

    def stop_countdown(self):
        self.countdown_running = False

    def update_countdown(self):
        if self.countdown_running:
            if self.countdown_time > 0:
                self.time_label.config(text=f"倒计时: {self.countdown_time} 秒")
                self.countdown_time -= 1
                self.root.after(1000, self.update_countdown)
            else:
                self.time_label.config(text="时间到！")
                self.countdown_running = False
                self.play_alarm()  # 播放闹铃
                self.root.after(3000, self.start_countdown)  # 3秒后自动开始倒计时

    def play_alarm(self):
        # 播放闹铃
        frequency = 2500  # Set Frequency To 2500 Hertz
        duration = 1000  # Set Duration To 1000 ms == 1 second
        winsound.Beep(frequency, duration)

if __name__ == "__main__":
    root = tk.Tk()
    app = CountdownApp(root)
    root.mainloop()
