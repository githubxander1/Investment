from apscheduler.schedulers.blocking import BlockingScheduler
import datetime

def job():
    print(f"【定时任务触发】{datetime.datetime.now()}")
    # 调用你已有的 get_stock_transaction_data 函数
    pass

if __name__ == '__main__':
    scheduler = BlockingScheduler()
    # 每天早上9:00执行一次
    scheduler.add_job(job, 'cron', hour=9, minute=0)
    try:
        scheduler.start()
    except KeyboardInterrupt:
        scheduler.shutdown()
