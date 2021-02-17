import schedule
import time
import os
from data.mongoconnect import connect


def job():
    os.system('python3 main.py')
    time.sleep(600)
    # MongoDB update
    connect()


# time
schedule.every().day.at("9:00").do(job)


while 1:
    schedule.run_pending()
    time.sleep(1)
