import psycopg2
import pytz
from telebot import types
from datetime import datetime
from Homework import select_homework
import os, telebot

token = os.getenv("TELEGRAM_API_TOKEN")
bot, salt = telebot.TeleBot(token, parse_mode='html'), os.urandom(32)
keyboard, inline_keyboard = types.ReplyKeyboardMarkup(), types.InlineKeyboardMarkup()
connection = psycopg2.connect(os.getenv('DATABASE_URL'), sslmode='require')
cursor = connection.cursor()  # connect to database


def current_pidor() -> str:
    cursor.execute("SELECT * FROM current_duty")
    time_now = datetime.now()
    current_duty = cursor.fetchall()[0]

    if time_now.strftime("%d.%m.%Y") > current_duty[1] and time_now.strftime("%w") != 0:
        if current_duty[0] > 14:
            a = 0
        else:
            a = current_duty[0] + 1
        cursor.execute(f"UPDATE current_duty SET id = {a}, date = '{time_now.strftime('%d.%m.%Y')}'")
        connection.commit()
        cursor.execute(f"SELECT people FROM duty WHERE id = {a}")
    else:
        cursor.execute(f"SELECT people FROM duty WHERE id = {current_duty[0]}")
    b = cursor.fetchall()[0][0].split(',')
    return f'<b>{b[0]}\n{b[1]}</b>'


def telegram_bot():
    @bot.message_handler(commands=['help', 'start'])
    def send_help(message):
        date = datetime.now(pytz.timezone('Asia/Yekaterinburg')).strftime('%Y.%m.%d %H:%M:%S')
        cursor.execute(
            f"INSERT INTO stats VALUES({message.from_user.id}, '{message.from_user.username}', '{message.text}', '{date}')")
        connection.commit()
        bot.reply_to(
            message,
            'Это бот, который скидывает д\з \n'
            '<b>Список команд</b>\n'
            '/che - д\з на завтра\n'
            '/lessons - расписание\n'
            '/all_week - д\з на неделю'
        )

    @bot.message_handler(commands=['stats'])
    def send_stats(message):
        cursor.execute('SELECT COUNT(*) FROM stats')
        bot.reply_to(message, f'Количество использований c 25.01.2022 - <b>{cursor.fetchall()[0][0]}</b>')
        date = datetime.now(pytz.timezone('Asia/Yekaterinburg')).strftime('%Y.%m.%d %H:%M:%S')
        cursor.execute(
            f"INSERT INTO stats VALUES({message.from_user.id}, '{message.from_user.username}', '{message.text}', '{date}')")
        connection.commit()

    @bot.message_handler(commands=['che', 'Che'])
    def send_che(message):
        date = datetime.now(pytz.timezone('Asia/Yekaterinburg')).strftime('%Y.%m.%d %H:%M:%S')
        cursor.execute(
            f"INSERT INTO stats VALUES({message.from_user.id}, '{message.from_user.username}', '{message.text}', '{date}')")
        connection.commit()

        bot.send_message(message.chat.id, select_homework())

    @bot.message_handler(commands=['pidors_today'])
    def send_pidor_day(message):
        pidor_today = current_pidor()
        date = datetime.now(pytz.timezone('Asia/Yekaterinburg')).strftime('%Y.%m.%d %H:%M:%S')
        cursor.execute(
            f"INSERT INTO stats VALUES({message.from_user.id}, '{message.from_user.username}', '{message.text}', '{date}')")
        connection.commit()

        bot.send_message(message.chat.id, f'<s>Пидоры дня</s> Дежурные сегодня (Beta):\n{pidor_today}')

    @bot.message_handler(commands=['lessons'])
    def send_list_of_lessons(message):
        date = datetime.now(pytz.timezone('Asia/Yekaterinburg')).strftime('%Y.%m.%d %H:%M:%S')
        cursor.execute(
            f"INSERT INTO stats VALUES({message.from_user.id}, '{message.from_user.username}', '{message.text}', '{date}')")
        connection.commit()
        text = open('files/lessons.txt', 'r', encoding='utf-8').read()
        bot.reply_to(message, text)

    @bot.message_handler(commands=['некит'])
    def n(message):
        date = datetime.now(pytz.timezone('Asia/Yekaterinburg')).strftime('%Y.%m.%d %H:%M:%S')
        cursor.execute(
            f"INSERT INTO stats VALUES({message.from_user.id}, '{message.from_user.username}', '{message.text}', '{date}')")
        connection.commit()
        voice = open('files/voice.ogg', 'rb')
        bot.send_voice(message.chat.id, voice)

    bot.polling(non_stop=True)


if __name__ == '__main__':
    telegram_bot()
