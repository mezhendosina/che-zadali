import os
import telebot
from datetime import datetime

import psycopg2
import pytz

from Homework import select_homework
from sgo_login import new_sgo_login

token = os.getenv("TELEGRAM_API_TOKEN")
bot = telebot.TeleBot(token, parse_mode='html')
connection = psycopg2.connect(os.getenv('DATABASE_URL'), sslmode='require')
cursor = connection.cursor()  # connect to database
you_have_no_power_here_gif = "CgACAgIAAxkBAAIB_GJnx90AAaCKoY1VyIimxr-tEfj4SAACrgsAAjCpCUibArTOkV6_lCQE"


def current_pidor() -> str:
    cursor.execute("SELECT * FROM current_duty")
    time_now = datetime.now()
    current_duty = cursor.fetchall()[0]
    if time_now.strftime("%d.%m.%Y") > current_duty[1] and time_now.strftime("%w") != 0:
        if current_duty[0] > 14:
            a = 1
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
            '/che - домашка на завтра\n'
            '/lessons - расписание\n'
            '/pidors_today - дежурные сегодня'
        )

    @bot.message_handler(commands=['prev_pidor'])
    def prev_pidor(message):
        date = datetime.now(pytz.timezone('Asia/Yekaterinburg')).strftime('%Y.%m.%d %H:%M:%S')
        cursor.execute(
            f"INSERT INTO stats VALUES({message.from_user.id}, '{message.from_user.username}', '{message.text}', '{date}')")
        connection.commit()
        if message.from_user.id == 401311369:
            cursor.execute("SELECT * FROM current_duty")
            current_duty = cursor.fetchall()[0]
            if current_duty[0] == 0:
                a = 14
            else:
                a = current_duty[0] - 1
            cursor.execute(f"UPDATE current_duty SET id = {a}")
            connection.commit()
            bot.send_message(message.chat.id, f"Ок, дежурные сегодня:\n{current_pidor()}")
        else:
            gif = open("files/you_have_no_power_here.gif", 'rb')
            bot.send_document(message.chat.id, gif)

    @bot.message_handler(commands=['stats'])
    def send_stats(message):
        cursor.execute('SELECT COUNT(*) FROM stats')
        bot.reply_to(message, f'Количество использований c 25.01.2022 - <b>{cursor.fetchall()[0][0]}</b>')
        date = datetime.now(pytz.timezone('Asia/Yekaterinburg')).strftime('%Y.%m.%d %H:%M:%S')
        cursor.execute(
            f"INSERT INTO stats VALUES({message.from_user.id}, '{message.from_user.username}', '{message.text}', '{date}')")
        connection.commit()

    @bot.message_handler(commands=['next_pidor'])
    def send_next_pidor(message):
        date = datetime.now(pytz.timezone('Asia/Yekaterinburg')).strftime('%Y.%m.%d %H:%M:%S')
        cursor.execute(
            f"INSERT INTO stats VALUES({message.from_user.id}, '{message.from_user.username}', '{message.text}', '{date}')")
        connection.commit()
        if message.from_user.id == 401311369:
            cursor.execute("SELECT * FROM current_duty")
            current_duty = cursor.fetchall()[0]
            if current_duty[0] > 14:
                a = 1
            else:
                a = current_duty[0] + 1
            cursor.execute(f"UPDATE current_duty SET id = {a}")
            connection.commit()
            bot.send_message(message.chat.id, f"Ок, дежурные сегодня:\n{current_pidor()}")
        else:
            gif = open("files/you_have_no_power_here.gif", 'rb')
            bot.send_document(message.chat.id, gif)

    @bot.message_handler(commands=['che', 'Che'])
    def send_che(message):
        date = datetime.now(pytz.timezone('Asia/Yekaterinburg')).strftime('%Y.%m.%d %H:%M:%S')
        cursor.execute(
            f"INSERT INTO stats VALUES({message.from_user.id}, '{message.from_user.username}', '{message.text}', '{date}')")
        connection.commit()

        bot.send_message(message.chat.id, new_sgo_login())

    @bot.message_handler(commands=['pidors_today'])
    def send_pidor_day(message):
        try:
            pidor_today = current_pidor()
            date = datetime.now(pytz.timezone('Asia/Yekaterinburg')).strftime('%Y.%m.%d %H:%M:%S')
            cursor.execute(
                f"INSERT INTO stats VALUES({message.from_user.id}, '{message.from_user.username}', '{message.text}', '{date}')")
            connection.commit()

            bot.send_message(message.chat.id, f'<s>Пидоры дня</s> Дежурные сегодня (Beta):\n{pidor_today}')
        except BaseException as e:
            bot.send_message(message.chat.id, f'@mezhendosina дурак: код с ошибкой написал. <i>{str(e)}</i>')

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
