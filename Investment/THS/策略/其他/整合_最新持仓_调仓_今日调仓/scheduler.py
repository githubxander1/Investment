import time

import schedule
from business_logic import main
from datetime import datetime

def job():
    if datetime.now().weekday() < 5:  # 0-4 对应周一到周五
        main()

schedule.every().day.at("09:32").do(job)

if __name__ == '__main__':
    # while True:
    #     schedule.run_pending()
    #     time.sleep(1)
    main()
