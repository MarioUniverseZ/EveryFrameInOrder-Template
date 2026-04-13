import time
from apscheduler.schedulers.background import BackgroundScheduler
from job import job
from config import POST_INTERVAL

scheduler = BackgroundScheduler()
scheduler.add_job(job, 'interval', seconds=POST_INTERVAL)

scheduler.start()

print("Bot started...")

# Keep process alive
try:
    while True:
        time.sleep(3600)
except (KeyboardInterrupt, SystemExit):
    scheduler.shutdown()