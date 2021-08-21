import psycopg2
import os 
from datetime import datetime, timedelta
import time
from vkbottle.bot import Bot, Message

def selectHomework():
    connection = psycopg2.connect(os.environ['DATABASE_URL'], sslmode='require')
    cursor = connection.cursor()
    if time.strftime('%w') == 6:
        date = datetime.now() + timedelta(days=2)
    else:
        date = datetime.now() + timedelta(days=1)
    if time.strftime('%m') == 6 or time.strftime('%m') == 7 or time.strftime('%m') == 8:
        return 'Какая домаха, лето жеж'
    cursor.execute(
            'SELECT lesson, homework FROM homeworktable WHERE dayname=%s and daymonth=%s and dayYear=%s;',
            (date.strftime('%d'), date.strftime('%m'), date.strftime('%Y'))
    )
    a = map(lambda x: '{}: {}'.format(x[0], x[1]), cursor.fetchall())
    return a 

bot = Bot(token=os.environ['VK_API_TOKEN'])
cheZadali = 'Че задали', 'Чё задали'
@bot.on.message(cheZadali)
def sendHomework(message: Message):
    message.answer(selectHomework())

bot.run_forever()