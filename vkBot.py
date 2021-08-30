import os 
from vkbottle.bot import Bot, Message
from extractHomeworkFromHTML import selectHomework

bot = Bot(os.getenv('VK_API_TOKEN'))

@bot.on.message(text=['Кинг', 'Конг'])
async def sendYesterdayHomework(message: Message):
    await message.answer('Конг')
@bot.on.message(text=['Пинг', 'ПИНГ'])
async def sendYesterdayHomework(message: Message):
    await message.answer('Понг')
@bot.on.message(text=['Че задали', '/che'])
async def sendHomework(message: Message):
    print('request homework')
    await message.answer(str(selectHomework()))
@bot.on.message(text=['/yesterday'])
async def sendYesterdayHomework(message: Message):
    await message.answer(str(selectHomework(-1)))
@bot.on.message(text=['/today'])
async def sendTodayHomework(message: Message):
    await message.answer(str(selectHomework(0)))
'''
@bot.on.messag
async def sendTimeHomework():
    await bot.api.messages.send(peer_id=2000000163, random_id=0, message='.')
'''
bot.run_forever()