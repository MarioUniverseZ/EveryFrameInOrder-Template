import time
from apscheduler.schedulers.background import BackgroundScheduler
from job import job
from config import POST_INTERVAL
from datetime import datetime, timedelta

def job_wrapper():
    result = job()

    if result == "ERROR":
        print("Pausing scheduler due to error.")
        job_scheduler.pause()

    elif result == "DONE":
        print("All tasks completed.")
        job_scheduler.pause()

job_scheduler = BackgroundScheduler()
job_scheduler.add_job(job_wrapper, 'interval', seconds=POST_INTERVAL, next_run_time=datetime.now() + timedelta(seconds=2))


if __name__ == '__main__':
    job_scheduler.start()

    print("Bot started...")

    # Keep process alive
    try:
        while True:
            time.sleep(3600)
    except (KeyboardInterrupt, SystemExit):
        job_scheduler.shutdown()