import tkinter as tk
from tkinter import messagebox, ttk
from datetime import datetime

# 定义费用
commission_rate_stock = 0.000854  # 沪深股票交易佣金费率
commission_rate_etf_lof = 0.00005  # ETF/LOF交易佣金费率
minimum_fee = 0.1  # 最低费用
transfer_fee_rate = 0.00001  # 过户费率

# 存储历史记录
history_data = []

def calculate_profit_loss():
    try:
        # 获取用户输入的数据
        stock_name = entry_stock_name.get()
        mode = combo_mode.get()
        base_price = float(entry_base_price.get())
        price_change_percentage = float(entry_price_change.get())

        # 根据模式计算结果
        if mode == '正T':
            # 计算卖出价
            sell_price = base_price * (1 + price_change_percentage / 100)
            price_difference = round(sell_price - base_price, 3)

            # 更新结果显示
            label_result.config(text=f"模式：正T\n卖出价：{sell_price:.2f}\n差价：{price_difference:.3f}")

            # 添加到历史记录
            history_data.append((datetime.now().strftime("%H:%M:%S"), len(history_data) + 1, stock_name, mode, base_price, sell_price, price_difference, tk.BooleanVar(), ""))
            update_history_table()
        elif mode == '倒T':
            # 计算买入价
            buy_price = base_price * (1 - price_change_percentage / 100)
            price_difference = round(base_price - buy_price, 3)

            # 更新结果显示
            label_result.config(text=f"模式：倒T\n买入价：{buy_price:.2f}\n差价：{price_difference:.3f}")

            # 添加到历史记录
            history_data.append((datetime.now().strftime("%H:%M:%S"), len(history_data) + 1, stock_name, mode, base_price, buy_price, price_difference, tk.BooleanVar(), ""))
            update_history_table()
        else:
            raise ValueError("未知模式")

    except ValueError as e:
        messagebox.showerror("错误", str(e))

def update_history_table():
    # 清空表格
    for row in treeview.get_children():
        treeview.delete(row)

    # 添加历史记录到表格
    for i, data in enumerate(history_data):
        time_str, row_num, stock_name, mode, base_price, calculated_price, price_difference, selected_var, note = data
        item_id = treeview.insert('', 'end', values=(row_num, time_str, stock_name, mode, base_price, calculated_price, price_difference))

        # 添加单选框
        cb = ttk.Checkbutton(checkframe, variable=selected_var, onvalue=True, offvalue=False)
        cb.grid(row=i, column=0, sticky='w')

        # 添加备注输入框
        entry = tk.Text(checkframe, height=1, width=20)
        entry.insert(tk.END, note)
        entry.bind("<FocusOut>", lambda event, idx=i: on_text_focus_out(event, idx))
        entry.grid(row=i, column=1, sticky='w')

def on_text_focus_out(event, idx):
    # 当备注输入框失去焦点时更新备注
    new_note = event.widget.get("1.0", tk.END).strip()
    time_str, row_num, stock_name, mode, base_price, calculated_price, price_difference, selected_var, _ = history_data[idx]
    history_data[idx] = (time_str, row_num, stock_name, mode, base_price, calculated_price, price_difference, selected_var, new_note)
    update_history_table()

# 创建主窗口
root = tk.Tk()
root.title("买卖计算器")
root.geometry("800x600")  # 设置初始窗口大小
root.grid_rowconfigure(5, weight=1)  # 使表格所在行自适应高度
root.grid_columnconfigure(0, weight=1)  # 使表格所在列自适应宽度

# 创建标签和输入框
label_stock_name = tk.Label(root, text="品种名称:")
label_stock_name.grid(row=0, column=0)
entry_stock_name = tk.Entry(root)
entry_stock_name.grid(row=0, column=1)

# 创建下拉框选择模式
mode_options = ['正T', '倒T']
combo_mode = ttk.Combobox(root, values=mode_options)
combo_mode.set('正T')
combo_mode.grid(row=1, column=1)

label_mode = tk.Label(root, text="模式：")
label_mode.grid(row=1, column=0)

label_base_price = tk.Label(root, text="基础价格:")
label_base_price.grid(row=2, column=0)
entry_base_price = tk.Entry(root)
entry_base_price.grid(row=2, column=1)

label_price_change = tk.Label(root, text="涨跌幅(%)：")
label_price_change.grid(row=3, column=0)
entry_price_change = tk.Entry(root)
entry_price_change.grid(row=3, column=1)

# 创建结果显示标签
label_result = tk.Label(root, text="", justify=tk.LEFT)
label_result.grid(row=4, column=0, columnspan=2)

# 创建按钮
button_calculate = tk.Button(root, text="计算", command=calculate_profit_loss)
button_calculate.grid(row=6, column=1)

# 创建表格
treeview = ttk.Treeview(root, columns=("序号", "时间", "品种名称", "模式", "基础价格", "计算结果", "差价"), show="headings")
treeview.heading("序号", text="序号")
treeview.heading("时间", text="时间")
treeview.heading("品种名称", text="品种名称")
treeview.heading("模式", text="模式")
treeview.heading("基础价格", text="基础价格")
treeview.heading("计算结果", text="计算结果")
treeview.heading("差价", text="差价")
treeview.grid(row=5, column=0, sticky="nsew")

# 创建单选框和备注输入框的框架
checkframe = tk.Frame(root)
checkframe.grid(row=5, column=1, sticky="nsew")

# 运行主循环
root.mainloop()
