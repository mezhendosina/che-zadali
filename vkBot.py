import os 
from vkbottle.bot import Bot, Message
from extractHomeworkFromHTML import selectHomework

bot = Bot(os.getenv('VK_API_TOKEN'))
@bot.on.message(text='Че задали')
async def sendHomework(message: Message):
    print('request homework')
    await message.answer(str(selectHomework()))

bot.run_forever()