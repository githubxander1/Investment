import schedule
import time
import subprocess
import pandas as pd
from plyer import notification

# 定义文件路径
zuhe_file_path = r'D:\1document\1test\PycharmProject_gitee\others\量化投资\THS\组合\保存的数据\组合_持仓_今天调仓_历史调仓.py'
celue_file_path = r'D:\1document\1test\PycharmProject_gitee\others\量化投资\THS\策略\策略_最新调仓和持仓_今天.py'

# 上一次交易信息的缓存
last_trade_info = pd.DataFrame()

def run_celue_script():
    print("Running celue_file_path script...")
    subprocess.run(['python', celue_file_path])

def run_zuhe_script():
    global last_trade_info
    print("Running zuhe_file_path script...")
    subprocess.run(['python', zuhe_file_path])

    # 加载最新的交易信息
    new_trade_info = load_trade_info()

    # 检查是否有新的交易信息
    if not new_trade_info.empty and not last_trade_info.equals(new_trade_info):
        notify_new_trades(new_trade_info)
        last_trade_info = new_trade_info

def load_trade_info():
    # 假设交易信息保存在 Excel 文件中
    file_path = r'D:\1document\1test\PycharmProject_gitee\others\量化投资\THS\策略\策略保存的数据\策略今天调仓_所有.xlsx'
    try:
        df = pd.read_excel(file_path, sheet_name='策略今天调仓')
        return df
    except Exception as e:
        print(f"Error loading trade info: {e}")
        return pd.DataFrame()

def notify_new_trades(trade_info):
    message = trade_info.to_string(index=False)
    notification.notify(
        title="New Trading Information",
        message=message,
        app_icon=None,  # 可以设置一个图标路径
        timeout=10
    )

# 设置定时任务
schedule.every().day.at("09:32").do(run_celue_script)
schedule.every().hour.do(run_zuhe_script)

print("Scheduler started...")

while True:
    schedule.run_pending()
    time.sleep(60)  # 每分钟检查一次任务
