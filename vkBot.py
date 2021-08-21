import psycopg2
import os 
from datetime import datetime, timedelta
import time
from vkbottle.bot import Bot, Message

def selectHomework():
    if time.strftime('%m') == 6 or time.strftime('%m') == 7 or time.strftime('%m') == 8:
        return 'Какая домаха, лето жеж'
    if time.strftime('%w') == 6:
        date = datetime.now() + timedelta(days=2)
    else:
        date = datetime.now() + timedelta(days=1)
    
    connection = psycopg2.connect(os.getenv('DATABASE_URL'), sslmode='require')
    cursor = connection.cursor()
    
    cursor.execute(
            'SELECT lesson, homework FROM homeworktable WHERE daynum=%s and daymonth=%s and dayYear=%s;'
            (date.strftime('%d'), date.strftime('%m'), date.strftime('%Y'))
    )
    b = cursor.fetchall()
    print(b)
    return '\n'.join(map(lambda x: '{}: {}'.format(x[0], x[1]), b))

bot = Bot(os.getenv('VK_API_TOKEN'))
@bot.on.message(text='Че задали')
async def sendHomework(message: Message):
    print('request homework')
    await message.answer(str(selectHomework()))

bot.run_forever()