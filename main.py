import asyncio

from telebot.async_telebot import AsyncTeleBot

import config
from telegram_bot import send_help, send_p_today, set_prev_p, set_next_p, n, send_che, send_ege, send_lessons
from sgo import SGO

bot = AsyncTeleBot(config.telegram_token, parse_mode="html")

sgo = SGO()

bot.register_message_handler(send_help, commands=["help", "start"], pass_bot=True)
bot.register_message_handler(send_p_today, commands=["p_today"], pass_bot=True)
bot.register_message_handler(send_lessons, commands=["lessons"], pass_bot=True)
bot.register_message_handler(send_ege, commands=["when_ege"], pass_bot=True)
bot.register_message_handler(send_che, commands=["che"], pass_bot=True)
bot.register_message_handler(n, commands=["некит"], pass_bot=True)
bot.register_message_handler(set_prev_p, commands=["prev_p"], pass_bot=True)
bot.register_message_handler(set_next_p, commands=["next_p"], pass_bot=True)


async def observe_homework():
    while True:
        try:
            print("get homework")
            await sgo.get_homework()
            print("homework collected")
        except Exception as e:
            print(e)
        finally:
            await asyncio.sleep(1800)


ioloop = asyncio.new_event_loop()
tasks = [
    ioloop.create_task(bot.polling(non_stop=True)),
    ioloop.create_task(observe_homework())
]

ioloop.run_forever()
