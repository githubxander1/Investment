import tkinter as tk
from tkinter import ttk
from datetime import datetime

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("计算器")
        self.root.geometry("600x400")  # 设置初始窗口大小
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        self.center_window()

        self.frame = ttk.Frame(self.root, padding="10")
        self.frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        self.create_widgets()

    def center_window(self):
        w = 600
        h = 400
        sw = self.root.winfo_screenwidth()
        sh = self.root.winfo_screenheight()
        x = (sw - w) / 2
        y = (sh - h) / 2
        self.root.geometry('%dx%d+%d+%d' % (w, h, x, y))

    def create_widgets(self):
        self.var_mode = tk.StringVar()
        self.var_variety = tk.StringVar()
        self.var_price = tk.StringVar()
        self.var_change_percent = tk.StringVar()

        ttk.Label(self.frame, text="品种名:").grid(row=0, column=0, sticky=tk.W)
        ttk.Entry(self.frame, textvariable=self.var_variety).grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(self.frame, text="模式:").grid(row=1, column=0, sticky=tk.W)
        ttk.Radiobutton(self.frame, text="正T", variable=self.var_mode, value="正T").grid(row=1, column=1, sticky=tk.W)
        ttk.Radiobutton(self.frame, text="倒T", variable=self.var_mode, value="倒T").grid(row=1, column=2, sticky=tk.W)

        ttk.Label(self.frame, text="价格:").grid(row=2, column=0, sticky=tk.W)
        ttk.Entry(self.frame, textvariable=self.var_price).grid(row=2, column=1, padx=5, pady=5)

        ttk.Label(self.frame, text="涨跌幅(%):").grid(row=3, column=0, sticky=tk.W)
        ttk.Entry(self.frame, textvariable=self.var_change_percent).grid(row=3, column=1, padx=5, pady=5)

        ttk.Button(self.frame, text="计算", command=self.calculate).grid(row=4, column=0, columnspan=3, pady=10)

        self.tree = ttk.Treeview(self.frame, columns=("序号", "时间", "品种名", "模式", "基础价格", "计算结果1", "计算结果2", "勾选框", "输入框"), show="headings")
        self.tree.heading("序号", text="序号")
        self.tree.heading("时间", text="时间")
        self.tree.heading("品种名", text="品种名")
        self.tree.heading("模式", text="模式")
        self.tree.heading("基础价格", text="基础价格")
        self.tree.heading("计算结果1", text="计算结果1")
        self.tree.heading("计算结果2", text="计算结果2")
        self.tree.heading("勾选框", text="勾选框")
        self.tree.heading("输入框", text="输入框")
        self.tree.grid(row=5, column=0, columnspan=3, padx=5, pady=5, sticky=(tk.W, tk.E, tk.N, tk.S))

    def calculate(self):
        variety = self.var_variety.get()
        mode = self.var_mode.get()
        price = float(self.var_price.get())
        change_percent = float(self.var_change_percent.get()) / 100

        if mode == "正T":
            sell_price = price * (1 + change_percent)
            base_price = price
            result1 = round(sell_price, 3)
            result2 = round(sell_price - price, 3)
        else:
            buy_price = price / (1 + change_percent)
            base_price = price
            result1 = round(buy_price, 3)
            result2 = round(price - buy_price, 3)

        index = len(self.tree.get_children()) + 1
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        item_id = self.tree.insert("", tk.END, values=(index, timestamp, variety, mode, round(base_price, 3), result1, result2, "", ""))

        checkbox = tk.BooleanVar()
        checkbox.set(False)
        checkbox_button = ttk.Checkbutton(self.frame, variable=checkbox)
        checkbox_button.grid(row=index+5, column=7, sticky=tk.W)
        self.tree.set(item_id, "勾选框", checkbox_button)

        textinput = tk.Text(self.frame, height=2, width=20)
        textinput.grid(row=index+5, column=8, padx=5, pady=5)
        self.tree.set(item_id, "输入框", textinput)

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()