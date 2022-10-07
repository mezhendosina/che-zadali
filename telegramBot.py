import os
from datetime import datetime

import psycopg2
import pytz
import telebot

from Homework import select_homework

token = os.getenv("TELEGRAM_API_TOKEN")
bot = telebot.TeleBot(token, parse_mode='html')  # init bot
connection = psycopg2.connect(os.getenv('DATABASE_URL'), sslmode='require')  # init sql database
cursor = connection.cursor()  # connect to database
you_have_no_power_here_gif = "CgACAgIAAxkBAAIB_GJnx90AAaCKoY1VyIimxr-tEfj4SAACrgsAAjCpCUibArTOkV6_lCQE"


def current_pidor() -> str:
    """Getting class attendants for today"""

    cursor.execute("SELECT * FROM current_duty")
    time_now = datetime.now(pytz.timezone('Asia/Yekaterinburg'))
    current_duty = cursor.fetchall()[0]
    if time_now.strftime("%d.%m.%Y") > current_duty[1] and 0 < int(time_now.strftime("%w")) < 6:
        # get attendant ID
        a = current_duty[0] + 1

        if current_duty[0] > 14:
            a = 1

        cursor.execute(f"UPDATE current_duty SET id = {a}, date = '{time_now.strftime('%d.%m.%Y')}'")
        connection.commit()
        cursor.execute(f"SELECT people FROM duty WHERE id = {a}")
    else:
        cursor.execute(f"SELECT people FROM duty WHERE id = {current_duty[0]}")
    b = cursor.fetchall()[0][0].split(',')
    return f'<b>{b[0]}\n{b[1]}</b>'


def report_activity(message):
    """Log user activity into database"""

    date = datetime.now(pytz.timezone('Asia/Yekaterinburg')).strftime('%Y.%m.%d %H:%M:%S')
    cursor.execute(
        f"INSERT INTO stats VALUES({message.from_user.id}, '{message.from_user.username}', '{message.text}', '{date}')")
    connection.commit()


def telegram_bot():
    """Main bot function"""

    # send welcome message with list of commands
    @bot.message_handler(commands=['help', 'start'])
    def send_help(message):
        bot.reply_to(
            message,
            'Это бот, который скидывает д\з \n'
            '<b>Список команд</b>\n'
            '/che - домашка на завтра\n'
            '/lessons - расписание\n'
            '/pidors_today - дежурные сегодня\n'
            '/when_ege - когда егэ по матану?'
        )
        report_activity(message)

    # switch current attendant ID to previous ID (only for @mezhendosina)
    @bot.message_handler(commands=['prev_pidor'])
    def prev_pidor(message):
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
        report_activity(message)

    # # send usage statistic
    # @bot.message_handler(commands=['stats'])
    # def send_stats(message):
    #     cursor.execute('SELECT COUNT(*) FROM stats')
    #     bot.reply_to(message, f'Количество использований c 25.01.2022 - <b>{cursor.fetchall()[0][0]}</b>')
    #     report_activity(message)

    # switch current attendant ID to next ID (only for @mezhendosina)
    @bot.message_handler(commands=['next_pidor'])
    def send_next_pidor(message):
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

        report_activity(message)

    # send homework for next day (for monday if current week day is Saturday)
    @bot.message_handler(commands=['che', 'Che'])
    def send_che(message):
        bot.send_message(message.chat.id, select_homework())
        report_activity(message)

    # send current  attendants
    @bot.message_handler(commands=['pidors_today'])
    def send_pidor_day(message):
        try:
            pidor_today = current_pidor()
            bot.send_message(message.chat.id, f'<s>Пидоры дня</s> Дежурные сегодня (Beta):\n{pidor_today}')
        except BaseException as e:
            bot.send_message(message.chat.id, f'@mezhendosina дурак: код с ошибкой написал! <i>{str(e)}</i>')

        report_activity(message)

    # send schedule of lessons for the week
    @bot.message_handler(commands=['lessons'])
    def send_list_of_lessons(message):
        photo = open('files/img.png', 'rb')
        bot.send_photo(message.chat.id, photo)

        report_activity(message)

    @bot.message_handler(commands=["when_ege"])
    def send_ege(message):
        time_now = datetime.now(pytz.timezone('Asia/Yekaterinburg'))

        math_ege = datetime(2023, 6, 2, tzinfo=pytz.timezone('Asia/Yekaterinburg')) - time_now
        soch = datetime(2022, 12, 1, tzinfo=pytz.timezone('Asia/Yekaterinburg')) - time_now
        russ_ege = datetime(2022, 5, 30, tzinfo=pytz.timezone('Asia/Yekaterinburg')) - time_now
        inf_ege = datetime(2022, 6, 20, tzinfo=pytz.timezone('Asia/Yekaterinburg')) - time_now
        text = f"До ЕГЭ по математике <tg-spoiler>{math_ege.days} дней</tg-spoiler>\n" \
               f"До ЕГЭ по русскому <tg-spoiler>{russ_ege.days}</tg-spoiler>" \
               f"До ЕГЭ по информатике <tg-spoiler>наверное {inf_ege.days}</tg-spoiler>" \
               f"До итогового сочинения <tg-spoiler>{soch.days} дней</tg-spoiler>\n"

        bot.reply_to(message, text)

    # special command for my friend
    @bot.message_handler(commands=['некит'])
    def n(message):
        voice = open('files/voice.ogg', 'rb')
        bot.send_voice(message.chat.id, voice)

        report_activity(message)

    # start bot
    bot.polling(non_stop=True)


if __name__ == '__main__':
    telegram_bot()
