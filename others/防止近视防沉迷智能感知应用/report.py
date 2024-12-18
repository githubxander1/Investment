import sqlite3
import matplotlib.pyplot as plt
import numpy as np

def generate_report():
    conn = sqlite3.connect('eye_health.db')
    cursor = conn.cursor()

    # 查询用眼数据
    cursor.execute("SELECT * FROM eye_usage")
    data = cursor.fetchall()

    distances = [row[3] for row in data]
    durations = [row[4] for row in data]

    # 绘制距离分布直方图
    plt.hist(distances, bins=10)
    plt.xlabel('距离（厘米）')
    plt.ylabel('频率')
    plt.title('用眼距离分布')
    plt.show()

    # 绘制使用时间折线图
    plt.plot(durations)
    plt.xlabel('使用次数')
    plt.ylabel('使用时间（秒）')
    plt.title('用眼时间变化趋势')
    plt.show()

    # 计算平均距离和平均使用时间
    average_distance = np.mean(distances) if distances else 0
    average_duration = np.mean(durations) if durations else 0

    print(f"平均用眼距离: {average_distance:.2f} cm")
    print(f"平均使用时间: {average_duration:.2f} 秒")

    conn.close()