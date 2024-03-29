from datetime import datetime

import psycopg2
import pytz
from telebot.async_telebot import AsyncTeleBot
from telebot.types import Message

import config as config
from bot.bot_utils import BotUtils
from bot.homework import Homework

connection = psycopg2.connect(config.bot_database_url)  # init sql database

utils = BotUtils(connection)
homework = Homework(connection)

bot = AsyncTeleBot(config.telegram_token, parse_mode="html")


@bot.message_handler(commands=["help", "start"])
async def send_help(message: Message):
    utils.report_activity(message)
    await bot.send_message(
        message.chat.id,
        'Это бот, который скидывает д\з \n'
        '<b>Список команд</b>\n'
        '/che - домашка на завтра\n'
        '/lessons - расписание\n'
        '/p_today - дежурные сегодня\n'
        '/when_ege - когда егэ по матану?'
    )


@bot.message_handler(commands=["che"])
async def send_che(message):
    a = homework.select_homework()
    await bot.send_message(message.chat.id, a)
    utils.report_activity(message)


@bot.message_handler(commands=["p_today"])
async def send_p_today(message):
    p_today = utils.p_today.current_p()
    await bot.send_message(message.chat.id, f"Дежурные сегодня <i>(Вета)</i>:\n{p_today}")
    utils.report_activity(message)


@bot.message_handler(commands=["lessons"])
async def send_lessons(message):
    photo = open("../files/img.png", 'rb')
    await bot.send_photo(message.chat.id, photo)
    utils.report_activity(message)


@bot.message_handler(commands=["when_ege"])
async def send_ege(message):
    time_now = datetime.now(pytz.timezone('Asia/Yekaterinburg'))

    math_ege = datetime(2023, 6, 1, tzinfo=pytz.timezone('Asia/Yekaterinburg')) - time_now
    russ_ege = datetime(2023, 5, 29, tzinfo=pytz.timezone('Asia/Yekaterinburg')) - time_now
    inf_ege = datetime(2023, 6, 19, tzinfo=pytz.timezone('Asia/Yekaterinburg')) - time_now
    phys_ege = datetime(2023, 6, 5, tzinfo=pytz.timezone('Asia/Yekaterinburg')) - time_now
    bio_ege = datetime(2023, 6, 13, tzinfo=pytz.timezone('Asia/Yekaterinburg')) - time_now
    text = f"До ЕГЭ по математике <tg-spoiler>{math_ege.days} дней</tg-spoiler>\n" \
           f"До ЕГЭ по русскому <tg-spoiler>{russ_ege.days} дней</tg-spoiler>\n" \
           f"До ЕГЭ по информатике <tg-spoiler>{inf_ege.days} дней</tg-spoiler>\n" \
           f"До <del>смерти Мишани</del> ЕГЭ по физике <tg-spoiler>{phys_ege.days} дней</tg-spoiler>\n" \
           f"До ЕГЭ по биологии <tg-spoiler>{bio_ege.days} дней</tg-spoiler>\n"

    await bot.reply_to(message, text)
    utils.report_activity(message)


@bot.message_handler(commands=["некит"])
async def n(message):
    voice = open('/files/voice.ogg', 'rb')
    await bot.send_voice(message.chat.id, voice)
    utils.report_activity(message)


@bot.message_handler(commands=["prev_p"])
async def set_prev_p(message):
    if message.from_user.id == config.admin_id:
        utils.p_today.set_prev_p()
    current_p = f"Ок, дежурные сегодня:\n{utils.p_today.current_p()}"
    await bot.send_message(message.chat.id, current_p)
    utils.report_activity(message)


@bot.message_handler(commands=["next_p"])
async def set_next_p(message):
    if message.from_user.id == config.admin_id:
        utils.p_today.set_next_p()
    current_p = f"Ок, дежурные сегодня:\n{utils.p_today.current_p()}"
    await bot.send_message(message.chat.id, current_p)
    utils.report_activity(message)


async def run():
    await bot.polling(non_stop=True)
