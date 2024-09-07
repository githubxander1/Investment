from datetime import datetime, timedelta
import pandas as pd

# 数据
data = {
    '姓名': ['肖泽华', '肖泽华', '肖泽华', '肖泽华', '范德萨', '范德萨', '范德萨', '范德萨', '范德萨', '范德萨'],
    '日期': ['24-08-01 星期四', '24-08-02 星期五', '24-08-03 星期六', '24-08-02 星期五', '24-08-16 星期五',
           '24-08-17 星期六', '24-08-18 星期日', '24-08-19 星期一', '24-08-20 星期二', '24-08-21 星期三'],
    '考勤状态': ['早到', '正常', '弹性', '迟到', '早退', '上半天', '下半天', '上下晚餐补', '上下晚餐交补', '上到第二天'],
    '上班1打卡时间': ['08:20', '08:30', '09:00', '09:40', '08:30', '08:30', '13:30', '08:30', '08:30', '08:53'],
    '下班1打卡时间': ['18:30', '18:00', '18:10', '19:10', '17:50', '12:00', '18:00', '20:00', '21:00', '次日 00:03'],
}

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
    start = datetime.strptime(start_time, '%H:%M')
    if end_time.startswith('次日'):
        end_time = '00:00'  # 使用00:00表示第二天的午夜
        end = datetime.strptime(end_time, '%H:%M') + timedelta(days=1)
    else:
        end = datetime.strptime(end_time, '%H:%M')

    duration = end - start

    # 减去午休时间
    if start < lunch_end and end > lunch_start:
        duration -= (lunch_end - lunch_start)

    # 减去晚餐时间
    if start < dinner_end and end > dinner_start:
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
    if is_weekend:
        overtime = duration
    else:
        overtime = max(duration - 8, 0)
    return round(overtime) if overtime < 0.5 else int(overtime)


# 定义计算餐补和交补次数的函数
def calculate_subsidy(duration):
    meal_subsidy = 1 if duration > 9 else 0
    traffic_subsidy = 1 if duration > 10 else 0
    return meal_subsidy, traffic_subsidy


# 遍历数据并计算结果
results = []
for i in range(len(data['姓名'])):
    name = data['姓名'][i]
    date = data['日期'][i]
    start_time = data['上班1打卡时间'][i]
    end_time = data['下班1打卡时间'][i]

    work_duration = calculate_work_duration(start_time, end_time, date)
    overtime_duration = calculate_overtime(work_duration, is_weekend(date))
    meal_subsidy, traffic_subsidy = calculate_subsidy(work_duration)

    results.append({
        '姓名': name,
        '日期': date,
        '工作时长': round(work_duration, 1),
        '加班时长': overtime_duration,
        '餐补次数': traffic_subsidy,
        '交补次数': meal_subsidy
    })

print(results)
# 将DataFrame转换为表格形式的字符串
table_str = pd.DataFrame(results)
# table_str = pd.to_string(index=False)

print(table_str)
