from apscheduler.schedulers.blocking import BlockingScheduler
from telegramBot import send_homework, telegramBot
from Homework import select_homework
from sgoLogin import sgo

sched = BlockingScheduler()
@sched.scheduled_job('cron',  hour='4-18')
def sheduled_job():
    telegramBot()
@sched.scheduled_job('interval', minutes=30)
def timed_job():
    sgo()
@sched.scheduled_job('cron', day_of_week='mon-sat', hour=9)
def sheduled_job():
    send_homework(select_homework(), '-1001503742992', False)

sched.start()
