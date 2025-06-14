from apscheduler.schedulers.blocking import BlockingScheduler
import datetime
import subprocess

def job():
    print(f"【定时任务触发】{datetime.datetime.now()}")
    print("执行 main.py 进行选股 + 回测 + 模拟交易")
    subprocess.run(["python", "main.py"])

if __name__ == '__main__':
    scheduler = BlockingScheduler()
    # 每天早上9:00执行一次
    scheduler.add_job(job, 'cron', hour=9, minute=0)
    try:
        scheduler.start()
    except KeyboardInterrupt:
        scheduler.shutdown()
