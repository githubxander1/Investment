import tkinter as tk
from tkinter import ttk
import datetime

class TradeCalculatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Trade Calculator")
        self.root.geometry("800x600")  # 设置初始大小

        # 上半部分：用户输入
        self.top_frame = ttk.Frame(self.root, padding="10")
        self.top_frame.pack(pady=10)

        ttk.Label(self.top_frame, text="品种名：").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.product_name_entry = ttk.Entry(self.top_frame)
        self.product_name_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=5, pady=5)

        ttk.Label(self.top_frame, text="模式：").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        self.mode_var = tk.StringVar(value="正T")
        ttk.Radiobutton(self.top_frame, text="正T", variable=self.mode_var, value="正T").grid(row=1, column=1, sticky=tk.W, padx=5, pady=5)
        ttk.Radiobutton(self.top_frame, text="倒T", variable=self.mode_var, value="倒T").grid(row=1, column=2, sticky=tk.W, padx=5, pady=5)

        ttk.Label(self.top_frame, text="价格：").grid(row=2, column=0, sticky=tk.W, padx=5, pady=5)
        self.price_entry = ttk.Entry(self.top_frame)
        self.price_entry.grid(row=2, column=1, sticky=(tk.W, tk.E), padx=5, pady=5)

        ttk.Label(self.top_frame, text="涨跌幅：").grid(row=2, column=2, sticky=tk.W, padx=5, pady=5)
        self.increase_rate_entry = ttk.Entry(self.top_frame)
        self.increase_rate_entry.grid(row=2, column=3, sticky=(tk.W, tk.E), padx=5, pady=5)

        ttk.Button(self.top_frame, text="计算", command=self.calculate).grid(row=3, column=1, sticky=tk.W, padx=5, pady=5)

        # 下半部分：记录数据
        self.bottom_frame = ttk.Frame(self.root, padding="10")
        self.bottom_frame.pack(fill=tk.BOTH, expand=True)

        self.tree = ttk.Treeview(self.bottom_frame, columns=('序号', '时间', '品种名', '模式', '基础价格', '交易价格', '差价', '状态', '备注'), show='headings')
        self.tree.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        self.tree.heading('序号', text='序号')
        self.tree.heading('时间', text='时间')
        self.tree.heading('品种名', text='品种名')
        self.tree.heading('模式', text='模式')
        self.tree.heading('基础价格', text='基础价格')
        self.tree.heading('交易价格', text='交易价格')
        self.tree.heading('差价', text='差价')
        self.tree.heading('状态', text='状态')
        self.tree.heading('备注', text='备注')

        self.scroll = ttk.Scrollbar(self.bottom_frame, orient="vertical", command=self.tree.yview)
        self.scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.configure(yscrollcommand=self.scroll.set)

        self.status_var = tk.IntVar()

    def calculate(self):
        product_name = self.product_name_entry.get()
        mode = self.mode_var.get()
        try:
            price = float(self.price_entry.get())
            increase_rate = float(self.increase_rate_entry.get())
        except ValueError:
            self.root.bell()
            return

        if mode == "正T":
            sell_price = price * (1 + increase_rate / 100)
            difference = sell_price - price
            trade_price = "卖出价"
        else:  # 倒T
            buy_price = price / (1 + increase_rate / 100)
            difference = price - buy_price
            trade_price = "买入价"

        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.tree.insert("", "end", values=(self.tree.size() + 1, current_time, product_name, mode, price,
                                            f"{trade_price}: {sell_price if mode == '正T' else buy_price:.3f}",
                                            difference, self.status_var, ''))

        self.update_remarks()

    def update_remarks(self):
        for i in range(self.tree.size()):
            item = self.tree.item(self.tree.get_children()[-1], "values")
            remark_frame = ttk.Frame(self.tree)
            remark_entry = tk.Text(remark_frame, height=1, width=20)
            remark_entry.pack()
            remark_entry.insert(tk.END, item[8])
            self.tree.set(self.tree.get_children()[-1], '备注', remark_frame)

if __name__ == "__main__":
    root = tk.Tk()
    app = TradeCalculatorApp(root)
    root.mainloop()