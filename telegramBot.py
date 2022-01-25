
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


def telegram_bot():
    @bot.message_handler(commands=['help', 'start'])
    def send_help(message):
        date = datetime.now(pytz.timezone('Asia/Yekaterinburg')).strftime('%Y.%m.%d %H:%M:%S')
        cursor.execute(
            f"INSERT INTO stats VALUES({message.from_user.id}, '{message.from_user.username}', '{message.text}', '{date}')")
        connection.commit()
        bot.reply_to(
            message,
            'Это бот, который скидывает д\з \n<b>Список команд</b>\n/che - д\з на завтра\n/lessons - расписание\n/all_week - д\з на неделю'
        )

    @bot.message_handler(commands=['che', 'Che'])
    def send_che(message):
        date = datetime.now(pytz.timezone('Asia/Yekaterinburg')).strftime('%Y.%m.%d %H:%M:%S')
        cursor.execute(
            f"INSERT INTO stats VALUES({message.from_user.id}, '{message.from_user.username}', '{message.text}', '{date}')")
        connection.commit()

        bot.send_message(message.chat.id, select_homework())

    @bot.message_handler(commands=['all_week'])
    def send_all_week(message):
        date = datetime.now(pytz.timezone('Asia/Yekaterinburg')).strftime('%Y.%m.%d %H:%M:%S')
        cursor.execute(
            f"INSERT INTO stats VALUES({message.from_user.id}, '{message.from_user.username}', '{message.text}', '{date}')")
        connection.commit()
        bot.send_message(message.chat.id, select_homework('all_week'))

    @bot.message_handler(commands=['lessons'])
    def send_list_of_lessons(message):
        date = datetime.now(pytz.timezone('Asia/Yekaterinburg')).strftime('%Y.%m.%d %H:%M:%S')
        cursor.execute(
            f"INSERT INTO stats VALUES({message.from_user.id}, '{message.from_user.username}', '{message.text}', '{date}')")
        connection.commit()
        text = open('files/lessons.txt', 'r', encoding='utf-8').read()
        bot.reply_to(
            message,
            text
        )

    @bot.message_handler(commands=['некит'])
    def n(message):
        date = datetime.now(pytz.timezone('Asia/Yekaterinburg')).strftime('%Y.%m.%d %H:%M:%S')
        cursor.execute(
            f"INSERT INTO stats VALUES({message.from_user.id}, '{message.from_user.username}', '{message.text}', '{date}')")
        connection.commit()
        voice = open('files/voice.ogg', 'rb')
        bot.send_voice(message.chat.id, voice)

    @bot.inline_handler(func=lambda query: len(query.query) > 0)
    def query_text(message):
        try:
            che = types.InlineQueryResultArticle(
                id='1', title="Че",
                description='узнать домаху на завтра',
                input_message_content=types.InputTextMessageContent(
                    message_text=select_homework(),
                    parse_mode='Markdown'
                )
            )
            lessons = types.InlineQueryResultArticle(
                id='2', title='расписание',
                description='узнать расписание',
                input_message_content=types.InputTextMessageContent(
                    message_text='Расписание\n' + open('files/lessons.txt', 'r', encoding='utf-8').read(),
                    parse_mode='Markdown'
                )
            )
            all_week = types.InlineQueryResultArticle(
                id='2', title='вся неделя',
                description='узнать д/з на всю неделю',
                input_message_content=types.InputTextMessageContent(
                    message_text=select_homework(day='all_week'),
                    parse_mode='Markdown'
                )
            )
            bot.answer_inline_query(message.id, [che, lessons, all_week])
        except Exception as e:
            print(e)

    bot.polling(non_stop=True)


if __name__ == '__main__':
    telegram_bot()
