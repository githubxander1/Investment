import tkinter as tk
from tkinter import messagebox, ttk
from datetime import datetime
import json

# 存储历史记录
history_data = []

def load_history_data():
    """从本地文件加载历史记录"""
    try:
        with open('history1.json', 'r', encoding='utf-8') as f:
            content = f.read().strip()  # 读取文件内容并去除空白字符
            if not content:  # 如果文件为空
                return []
            loaded_data = json.loads(content)
            # 将布尔值转换为 BooleanVar 对象
            history_data = [(time_str, row_num, stock_name, mode, base_price, calculated_price, price_difference,
                            tk.BooleanVar(value=value), note) for
                           time_str, row_num, stock_name, mode, base_price, calculated_price, price_difference, value, note
                           in loaded_data]
            return history_data
    except FileNotFoundError:
        # 如果文件不存在，则创建一个空的 JSON 文件
        with open('history1.json', 'w', encoding='utf-8') as f:
            json.dump([], f)
        return []
    except json.JSONDecodeError:
        # 如果文件内容不是有效的 JSON 格式
        messagebox.showerror("错误", "历史记录文件格式错误，请确保文件内容为有效的 JSON 格式。")
        return []
    except Exception as e:
        messagebox.showerror("错误", f"加载历史记录失败: {e}")
        return []


def save_data(data):
    """保存历史数据"""
    with open('history1.json', 'w') as file:
        json.dump(data, file, indent=4)

def calculate_profit_loss():
    try:
        # 获取用户输入的数据
        stock_name = entry_stock_name.get()
        mode = combo_mode.get()
        base_price = float(entry_base_price.get())
        price_change_percentage = float(entry_price_change.get())
        shares = int(entry_shares.get())

        # 根据模式计算结果
        if mode == '正T':
            sell_price = base_price * (1 + price_change_percentage / 100)
            price_difference = round(sell_price - base_price, 3)

            label_result.config(text=f"模式：正T\n卖出价：{sell_price:.2f}\n差价：{price_difference:.3f}")
            history_data.append((datetime.now().strftime("%H:%M:%S"), len(history_data) + 1, stock_name, mode, base_price, sell_price, price_difference, shares, False, ""))
            update_history_table()
        elif mode == '倒T':
            buy_price = base_price * (1 - price_change_percentage / 100)
            price_difference = round(base_price - buy_price, 3)

            label_result.config(text=f"模式：倒T\n买入价：{buy_price:.2f}\n差价：{price_difference:.3f}")
            history_data.append((datetime.now().strftime("%H:%M:%S"), len(history_data) + 1, stock_name, mode, base_price, buy_price, price_difference, shares, False, ""))
            update_history_table()
        else:
            raise ValueError("未知模式")

    except ValueError as e:
        messagebox.showerror("错误", str(e))

def update_history_table():
    # 清空表格
    for row in treeview.get_children():
        treeview.delete(row)

    # 移除所有额外组件
    for widget in root.grid_slaves():
        if widget.grid_info()['column'] == 11:
            widget.grid_forget()

    # 添加历史记录到表格
    for i, data in enumerate(history_data):
        time_str, row_num, stock_name, mode, base_price, calculated_price, price_difference, shares, selected, note = data
        item_id = treeview.insert('', 'end', values=(row_num, time_str, stock_name, mode, base_price, calculated_price, price_difference, shares))

        # 创建容器
        frame = tk.Frame(root)
        frame.grid(row=i + 1, column=8, sticky='w')  # 将额外组件放在第8列

        # 添加单选框
        cb = ttk.Checkbutton(frame, variable=tk.BooleanVar(value=selected), onvalue=True, offvalue=False)
        cb.pack(side=tk.LEFT)

        # 添加备注输入框
        entry = tk.Text(frame, height=1, width=20)
        entry.insert(tk.END, note)
        entry.bind("<FocusOut>", lambda event, idx=i: on_text_focus_out(event, idx))
        entry.pack(side=tk.LEFT)

        # 添加删除按钮
        delete_button = tk.Button(frame, text="删除", command=lambda idx=i: delete_row(idx))
        delete_button.pack(side=tk.LEFT)

def on_text_focus_out(event, idx):
    # 当备注输入框失去焦点时更新备注
    new_note = event.widget.get("1.0", tk.END).strip()
    time_str, row_num, stock_name, mode, base_price, calculated_price, price_difference, shares, selected, _ = history_data[idx]
    history_data[idx] = (time_str, row_num, stock_name, mode, base_price, calculated_price, price_difference, shares, selected, new_note)
    update_history_table()
    save_data(history_data)

def delete_row(idx):
    # 删除指定行
    del history_data[idx]
    update_history_table()
    save_data(history_data)

# 加载历史数据
history_data = load_history_data()

# 创建主窗口
root = tk.Tk()
root.title("计算器")
root.geometry("800x600")

# 创建三个 Frame
input_frame = tk.Frame(root)
button_frame = tk.Frame(root)
result_frame = tk.Frame(root)

# 布局三个 Frame
input_frame.grid(row=0, column=0, padx=10, pady=10, sticky='nsew')
button_frame.grid(row=0, column=1, padx=10, pady=10, sticky='nsew')
result_frame.grid(row=0, column=2, padx=10, pady=10, sticky='nsew')

# 配置列权重
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)
root.grid_columnconfigure(2, weight=1)

# 创建标签和输入框
label_stock_name = tk.Label(input_frame, text="品种名称:")
label_stock_name.grid(row=0, column=0, sticky='e')
entry_stock_name = tk.Entry(input_frame)
entry_stock_name.grid(row=0, column=1, sticky='w')

combo_mode = ttk.Combobox(input_frame, values=['正T', '倒T'])
combo_mode.set('正T')
combo_mode.grid(row=1, column=1, sticky='w')

label_mode = tk.Label(input_frame, text="模式：")
label_mode.grid(row=1, column=0, sticky='e')

label_base_price = tk.Label(input_frame, text="基础价格:")
label_base_price.grid(row=2, column=0, sticky='e')
entry_base_price = tk.Entry(input_frame)
entry_base_price.grid(row=2, column=1, sticky='w')

label_shares = tk.Label(input_frame, text="股数:")
label_shares.grid(row=3, column=0, sticky='e')
entry_shares = tk.Entry(input_frame)
entry_shares.grid(row=3, column=1, sticky='w')

label_price_change = tk.Label(input_frame, text="涨跌幅(%)：")
label_price_change.grid(row=4, column=0, sticky='e')
entry_price_change = tk.Entry(input_frame)
entry_price_change.grid(row=4, column=1, sticky='w')

# 创建按钮
button_calculate = tk.Button(button_frame, text="计算", command=calculate_profit_loss)
button_calculate.pack(expand=True)

# 创建结果显示标签
label_result = tk.Label(result_frame, text="", justify=tk.RIGHT)
label_result.pack(expand=True)

# 创建表格
treeview = ttk.Treeview(root, columns=("序号", "时间", "品种名称", "模式", "基础价格", "计算结果", "差价", "股数"), show="headings")
treeview.heading("序号", text="序号")
treeview.heading("时间", text="时间")
treeview.heading("品种名称", text="品种名称")
treeview.heading("模式", text="模式")
treeview.heading("基础价格", text="基础价格")
treeview.heading("计算结果", text="计算结果")
treeview.heading("差价", text="差价")
treeview.heading("股数", text="股数")
treeview.grid(row=1, column=0, columnspan=3, sticky="nsew")

# 初始化表格
update_history_table()

# 运行主循环
root.mainloop()
