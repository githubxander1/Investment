from datetime import datetime, timedelta
import pandas as pd

# 定义计算工作时长和加班时长的函数
def calculate_work_and_overtime_v3(start_work, end_work, date):
    # 定义正常工作时间
    normal_work_start, normal_work_end = "08:30", "18:00"
    # 午休时间
    lunch_start, lunch_end = "12:00", "13:30"
    # 晚餐时间
    dinner_start, dinner_end = "18:00", "19:00"

    # 将时间字符串转换为 datetime 对象
    def time_to_datetime(t):
        h, m = map(int, t.split(':'))
        return datetime.combine(datetime.min.date(), datetime.min.time().replace(hour=h, minute=m))

    # 将日期字符串转换为 datetime 对象
    def date_to_datetime(d):
        return pd.to_datetime(d.split(" ")[0], format='%y-%m-%d')

    # 处理次日的情况
    if "次日" in end_work:
        day, end_work = end_work.split(" ")
        date = date_to_datetime(date) + timedelta(days=1)
        end_work = time_to_datetime(end_work) + timedelta(days=1)
    else:
        end_work = time_to_datetime(end_work)

    start_work = time_to_datetime(start_work)
    normal_work_start = time_to_datetime(normal_work_start)
    normal_work_end = time_to_datetime(normal_work_end)
    lunch_start = time_to_datetime(lunch_start)
    lunch_end = time_to_datetime(lunch_end)
    dinner_start = time_to_datetime(dinner_start)
    dinner_end = time_to_datetime(dinner_end)

    # 如果上班时间早于8:30，则按8:30算
    if start_work < normal_work_start:
        start_work = normal_work_start

    # 如果下午开始打上班卡，按13:30开始算
    if start_work <= lunch_end:
        start_work = lunch_end
        if end_work >= dinner_end:
            end_work = normal_work_end

    # 计算工作时长
    work_time = end_work - start_work

    # 计算午休时间
    lunch_duration = timedelta()
    if start_work < lunch_start and end_work > lunch_end:
        lunch_duration = lunch_end - lunch_start
    elif start_work < lunch_start and end_work <= lunch_end:
        lunch_duration = end_work - lunch_start
    elif start_work >= lunch_start and end_work > lunch_end:
        lunch_duration = lunch_end - start_work

    # 计算晚餐时间
    dinner_duration = timedelta()
    if start_work < dinner_start and end_work > dinner_end:
        dinner_duration = dinner_end - dinner_start
    elif start_work < dinner_start and end_work <= dinner_end:
        dinner_duration = end_work - dinner_start
    elif start_work >= dinner_start and end_work > dinner_end:
        dinner_duration = dinner_end - start_work

    # 总工作时长
    # if end_work > normal_work_end:
    total_work_time = work_time - lunch_duration - dinner_duration

    # 计算加班时长
    date_obj = date_to_datetime(date)
    is_weekend = date_obj.weekday() >= 5  # 5 表示周六，6 表示周日

    if is_weekend:
        overtime_time = total_work_time
    else:
        overtime_time = max(timedelta(), total_work_time - (normal_work_end - normal_work_start))

    # 转换为小时数
    work_hours = total_work_time.total_seconds() / 3600
    overtime_hours = overtime_time.total_seconds() / 3600

    return round(work_hours, 1), round(overtime_hours, 1)

# 创建 DataFrame
df = pd.DataFrame({
    '姓名': ['肖泽华', '肖泽华', '肖泽华', '肖泽华', '范德萨', '范德萨', '范德萨', '范德萨', '范德萨', '范德萨'],
    '日期': ['24-08-03 星期四', '24-08-02 星期五', '24-08-03 星期六', '24-08-02 星期五', '24-08-16 星期五',
             '24-08-17 星期六', '24-08-18 星期日', '24-08-19 星期一', '24-08-20 星期二', '24-08-21 星期三'],
    '考勤状态': ['早到', '正常', '弹性', '迟到', '早退', '上半天', '下半天', '上下晚餐补', '上下晚餐交补', '上到第二天'],
    '上班1打卡时间': ['12:20', '08:30', '09:00', '09:40', '08:30', '08:30', '13:30', '08:30', '08:30', '08:53'],
    '下班1打卡时间': ['次日 19:30', '18:00', '18:10', '19:10', '17:50', '12:00', '18:00', '20:00', '21:00', '次日 00:03'],
})

# 应用更新后的函数计算工作时长和加班时长
df[['工作时长', '加班时长']] = df.apply(
    lambda row: calculate_work_and_overtime_v3(row['上班1打卡时间'], row['下班1打卡时间'], row['日期'].split(" ")[0]),
    axis=1, result_type='expand'
)

# 重新计算餐补次数和交补次数
df['餐补次数'] = (df['工作时长'] > 9).astype(int)
df['交补次数'] = (df['工作时长'] > 10).astype(int)

print(df)
