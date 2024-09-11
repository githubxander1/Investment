import tkinter as tk
from tkinter import filedialog, messagebox
from datetime import datetime, timedelta
import pandas as pd
import os

# 定义午休和晚餐时间
lunch_start = datetime.strptime('12:00', '%H:%M')
lunch_end = datetime.strptime('13:30', '%H:%M')
dinner_start = datetime.strptime('18:00', '%H:%M')
dinner_end = datetime.strptime('19:00', '%H:%M')

# 定义正常工作时间
work_start = datetime.strptime('08:30', '%H:%M')
work_end = datetime.strptime('18:00', '%H:%M')

# 定义计算时间差的函数
def calculate_work_duration(start_time, end_time, date):
    if pd.isna(start_time) or pd.isna(end_time):
        return None

    if isinstance(start_time, float):
        start_time = str(int(start_time))
    if isinstance(end_time, float):
        end_time = str(int(end_time))

    start = datetime.strptime(start_time, '%H:%M')
    if end_time.startswith('次日'):
        end_time = '00:00'  # 使用00:00表示第二天的午夜
        end = datetime.strptime(end_time, '%H:%M') + timedelta(days=1)
    else:
        end = datetime.strptime(end_time, '%H:%M')

    duration = end - start
    duration_format = '{:.1f}'.format(duration.total_seconds() / 3600)

    # 减去午休时间
    if start < lunch_end and end > lunch_start:
        duration -= (lunch_end - lunch_start)

    # 减去晚餐时间
    if start < dinner_end and end > dinner_end:
        duration -= (dinner_end - dinner_start)

    # 如果跨天工作，还需要减去第二天的正常工作时间
    if end_time.startswith('次日'):
        if end > work_end:
            duration -= (end - work_end).total_seconds() / 3600

    return duration.total_seconds() / 3600  # 返回小时数

# 定义判断是否为周末的函数
def is_weekend(date_str):
    day_of_week = datetime.strptime(date_str.split(' ')[0], '%y-%m-%d').weekday()
    return day_of_week >= 5  # 5是星期六，6是星期日

# 定义计算加班时长的函数
def calculate_overtime(duration, is_weekend):
    if duration is None:
        return None

    if is_weekend:
        overtime = duration
    else:
        overtime = max(duration - 8, 0)
    return round(overtime) if overtime < 0.5 else int(overtime)

# 定义计算餐补和交补次数的函数
def calculate_subsidy(duration):
    if duration is None:
        return 0, 0

    meal_subsidy = 1 if duration > 9 else 0
    traffic_subsidy = 1 if duration > 10 else 0
    return meal_subsidy, traffic_subsidy

# 遍历数据并计算结果
def process_excel(file_path, output_path):
    try:
        df = pd.read_excel(file_path)
        results = []
        for i in range(len(df)):
            name = df['姓名'][i]
            date = df['日期'][i]
            start_time = df['上班1打卡时间'][i]
            end_time = df['下班1打卡时间'][i]

            work_duration = calculate_work_duration(start_time, end_time, date)
            if work_duration is None:
                continue

            overtime_duration = calculate_overtime(work_duration, is_weekend(date))
            meal_subsidy, traffic_subsidy = calculate_subsidy(work_duration)

            results.append({
                '姓名': name,
                '考勤组': df['考勤组'][i],
                '部门': df['部门'][i],
                '职位': df['职位'][i],
                '日期': date,
                '班次': df['班次'][i],
                '上班1打卡时间': df['上班1打卡时间'][i],
                '下班1打卡时间': df['下班1打卡时间'][i],
                '下班1打卡结果': df['下班1打卡结果'][i],
                '工作时长': round(work_duration, 1),
                '加班时长': overtime_duration,
                '餐补次数': traffic_subsidy,
                '交补次数': meal_subsidy
            })

        df_results = pd.DataFrame(results)
        output_file_name = os.path.splitext(os.path.basename(file_path))[0] + '_processed.xlsx'
        output_path = os.path.join(os.path.dirname(file_path), output_file_name)
        df_results.to_excel(output_path, index=False)
        return "处理完成"
    except Exception as e:
        return f"处理失败：{str(e)}"

def select_input_file():
    file_path = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx")])
    if file_path:
        input_file_label.config(text=f"输入文件：\n{file_path}")
        selected_input_file.set(file_path)

def process_and_save():
    input_file = selected_input_file.get()
    if input_file:
        result = process_excel(input_file, "")
        result_label.config(text=result)

def open_file(file_path):
    if os.path.exists(file_path):
        os.startfile(file_path)

# GUI setup
root = tk.Tk()
root.title("考勤表处理工具")

selected_input_file = tk.StringVar()

input_file_label = tk.Label(root, text="选择文件：\n")
input_file_label.pack(pady=5)

input_button = tk.Button(root, text="选择输入文件", command=select_input_file)
input_button.pack(pady=5)

process_button = tk.Button(root, text="处理并保存", command=process_and_save)
process_button.pack(pady=10)

result_label = tk.Label(root, text="", fg="blue")
result_label.pack(pady=10)

open_input_button = tk.Button(root, text="打开要处理文件", command=lambda: open_file(selected_input_file.get()))
open_input_button.pack(pady=5)

# 添加打开已处理文件按钮
def open_processed_file():
    input_file = selected_input_file.get()
    if input_file:
        processed_file = os.path.splitext(input_file)[0] + '_processed.xlsx'
        open_file(processed_file)

open_processed_button = tk.Button(root, text="打开已处理文件", command=open_processed_file)
open_processed_button.pack(pady=5)

root.mainloop()
