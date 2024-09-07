import pandas as pd
from datetime import datetime, timedelta

# 定义数据
data = {
    '姓名': ['肖泽华', '肖泽华', '肖泽华', '肖泽华', '范德萨', '范德萨', '范德萨', '范德萨', '范德萨', '范德萨'],
    '日期': ['24-08-01 星期四', '24-08-02 星期五', '24-08-03 星期六', '24-08-02 星期五', '24-08-16 星期五',
           '24-08-17 星期六', '24-08-18 星期日', '24-08-19 星期一', '24-08-20 星期二', '24-08-21 星期三'],
    '考勤状态': ['早到', '正常', '弹性', '迟到', '早退', '上半天', '下半天', '上下晚餐补', '上下晚餐交补', '上到第二天'],
    '上班1打卡时间': ['08:20', '08:30', '09:00', '09:40', '08:30', '08:30', '13:30', '08:30', '08:30', '08:53'],
    '下班1打卡时间': ['18:30', '18:00', '18:10', '19:10', '17:50', '12:00', '18:00', '20:00', '21:00', '次日 00:03'],
}


# 定义转换日期格式的函数
def convert_date(date_str):
    return datetime.strptime(date_str.split(' ')[0], '%y-%m-%d')


# 定义计算工作时长和加班时长的函数
def calculate_work_and_overtime(start_time, end_time, date_str):
    # 计算工作时长
    start = datetime.strptime(start_time, '%H:%M')
    end = datetime.strptime(end_time, '%H:%M')
    work_start = datetime.strptime('08:30', '%H:%M')
    work_end = datetime.strptime('18:00', '%H:%M')
    lunch_start = datetime.strptime('12:00', '%H:%M')
    lunch_end = datetime.strptime('13:30', '%H:%M')
    dinner_start = datetime.strptime('18:00', '%H:%M')
    dinner_end = datetime.strptime('19:00', '%H:%M')

    # 减去午休和晚餐时间
    if start < lunch_end and end > lunch_start:
        work_duration = end - start - (lunch_end - lunch_start)
    elif start < dinner_end and end > dinner_start:
        work_duration = end - start - (dinner_end - dinner_start)
    else:
        work_duration = end - start

    # 计算加班时长
    overtime = max(0, work_duration.total_seconds() / 3600 - 8)
    if overtime >= 0.5:
        overtime = round(overtime)

    return work_duration.total_seconds() / 3600, overtime


# 定义计算餐补和交补的函数
def calculate_meal_and_traffic(work_duration, overtime):
    meal_subsidy = 0
    traffic_subsidy = 0
    if work_duration >= 9:
        meal_subsidy = 1
    if work_duration >= 10:
        traffic_subsidy = 1
    return meal_subsidy, traffic_subsidy


# 创建DataFrame
df = pd.DataFrame(data)

# 计算工作时长、加班时长、餐补次数和交补次数
df['工作时长'], df['加班时长'], df['餐补次数'], df['交补次数'] = zip(*df.apply(
    lambda row: calculate_work_and_overtime(row['上班1打卡时间'], row['下班1打卡时间'], row['日期']), axis=1))

# 显示结果
df[['姓名', '日期', '工作时长', '加班时长', '餐补次数', '交补次数']]
