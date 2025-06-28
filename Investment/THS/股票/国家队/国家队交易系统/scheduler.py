from apscheduler.schedulers.blocking import BlockingScheduler
import datetime
import subprocess
import traceback

def job():
    print(f"【定时任务触发】{datetime.datetime.now()}")
    print("执行 trade_main.py 进行选股 + 回测 + 模拟交易")
    try:
        result = subprocess.run(
            ["python", "trade_main.py"],
            capture_output=True,
            text=True,
            check=True
        )
        print("任务输出:\n", result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"任务执行失败: {e.returncode}")
        print("错误输出:\n", e.stderr)
    except Exception as e:
        print(f"未知错误: {str(e)}")
        traceback.print_exc()

if __name__ == '__main__':
    scheduler = BlockingScheduler()
    # 每天早上9:00执行一次
    scheduler.add_job(job, 'cron', hour=9, minute=0)
    try:
        print("定时任务已启动，按 Ctrl+C 退出")
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()
        print("定时任务已停止")
