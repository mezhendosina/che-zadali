from apscheduler.schedulers.blocking import BlockingScheduler
from telegramBot import send_message
from Homework import select_homework
from login import sgo

sched = BlockingScheduler()

@sched.scheduled_job('interval', minutes=30)
def timed_job():
    sgo()
@sched.scheduled_job('cron', day_of_week='mon-sat', hour=14)
def sheduled_job():
    send_message(select_homework(), '-1001503742992', True)
sched.start()