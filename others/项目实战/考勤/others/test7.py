from datetime import datetime, timedelta
import pandas as pd

# 读取 Excel 文件中的数据
df = pd.read_excel('考勤表.xlsx')

# 确保所有必要的列都存在
# required_columns = ['姓名', '日期', '考勤状态', '上班1打卡时间', '下班1打卡时间',
#                     '预期结果_工作时长', '预期结果_加班时长', '预期结果_餐补次数', '预期结果_交补次数']
# missing_columns = [col for col in required_columns if col not in df.columns]
# if missing_columns:
#     raise ValueError(f"缺少必要列：{missing_columns}")

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
    duration_format = '{:.1f}'.format(duration.total_seconds() / 3600)

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
for i in range(len(df)):
    name = df['姓名'][i]
    date = df['日期'][i]
    # date = df['考勤组'][i]
    start_time = df['上班1打卡时间'][i]
    end_time = df['下班1打卡时间'][i]

    work_duration = calculate_work_duration(start_time, end_time, date)
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

# 将结果转换为DataFrame
df_results = pd.DataFrame(results)

# 添加预期结果
# df_results['预期结果_工作时长'] = df['预期结果_工作时长']
# df_results['预期结果_加班时长'] = df['预期结果_加班时长']
# df_results['预期结果_餐补次数'] = df['预期结果_餐补次数']
# df_results['预期结果_交补次数'] = df['预期结果_交补次数']

# 添加实际结果与预期结果的差异
# df_results['工作时长差异'] = df_results['工作时长'] - df_results['预期结果_工作时长'].astype(float)
# df_results['加班时长差异'] = df_results['加班时长'] - df_results['预期结果_加班时长'].astype(float)
# df_results['餐补次数差异'] = df_results['餐补次数'] - df_results['预期结果_餐补次数'].astype(int)
# df_results['交补次数差异'] = df_results['交补次数'] - df_results['预期结果_交补次数'].astype(int)

# 输出表格
print(df_results)
df_results.to_excel('output111.xlsx', index=False)
