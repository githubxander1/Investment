import tkinter as tk
from tkinter import ttk
import datetime

class TradeCalculatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Trade Calculator")
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)

        # Upper part: User input
        self.top_frame = ttk.Frame(self.root, padding="10")
        self.top_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        ttk.Label(self.top_frame, text="Product Name:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.product_name_entry = ttk.Entry(self.top_frame)
        self.product_name_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=5, pady=5)

        ttk.Label(self.top_frame, text="Mode:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        self.mode_var = tk.StringVar(value="正T")
        ttk.Radiobutton(self.top_frame, text="正T", variable=self.mode_var, value="正T").grid(row=1, column=1, sticky=tk.W, padx=5, pady=5)
        ttk.Radiobutton(self.top_frame, text="倒T", variable=self.mode_var, value="倒T").grid(row=1, column=2, sticky=tk.W, padx=5, pady=5)

        ttk.Label(self.top_frame, text="Price:").grid(row=2, column=0, sticky=tk.W, padx=5, pady=5)
        self.price_entry = ttk.Entry(self.top_frame)
        self.price_entry.grid(row=2, column=1, sticky=(tk.W, tk.E), padx=5, pady=5)

        ttk.Label(self.top_frame, text="Increase Rate:").grid(row=2, column=2, sticky=tk.W, padx=5, pady=5)
        self.increase_rate_entry = ttk.Entry(self.top_frame)
        self.increase_rate_entry.grid(row=2, column=3, sticky=(tk.W, tk.E), padx=5, pady=5)

        ttk.Button(self.top_frame, text="Calculate", command=self.calculate).grid(row=3, column=1, sticky=tk.W, padx=5, pady=5)

        # Lower part: Record data
        self.bottom_frame = ttk.Frame(self.root, padding="10")
        self.bottom_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        self.tree = ttk.Treeview(self.bottom_frame, columns=('序号', '时间', '品种名', '模式', '基础价格', '计算结果', '差价'), show='headings')
        self.tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=5, pady=5)
        self.tree.heading('序号', text='序号')
        self.tree.heading('时间', text='时间')
        self.tree.heading('品种名', text='品种名')
        self.tree.heading('模式', text='模式')
        self.tree.heading('基础价格', text='基础价格')
        self.tree.heading('计算结果', text='计算结果')
        self.tree.heading('差价', text='差价')

        self.scroll = ttk.Scrollbar(self.bottom_frame, orient="vertical", command=self.tree.yview)
        self.scroll.grid(row=0, column=1, sticky='ns', padx=5, pady=5)
        self.tree.configure(yscrollcommand=self.scroll.set)

    def calculate(self):
        product_name = self.product_name_entry.get()
        mode = self.mode_var.get()
        price = float(self.price_entry.get())
        increase_rate = float(self.increase_rate_entry.get())

        if mode == "正T":
            sell_price = price * (1 + increase_rate / 100)
            difference = sell_price - price
            result = f"Sell Price: {sell_price:.3f}"
        else:  # 倒T
            sell_price = price / (1 + increase_rate / 100)
            difference = price - sell_price
            result = f"Buy Price: {sell_price:.3f}"

        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.tree.insert("", "end", values=(self.tree.size() + 1, current_time, product_name, mode, price, result, difference))

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("600x400")  # Set initial size
    app = TradeCalculatorApp(root)
    root.mainloop()