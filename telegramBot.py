from telebot import types
from Homework import select_homework 
import os, telebot, re, hashlib, psycopg2

token = os.getenv("TELEGRAM_API_TOKEN")
bot, salt= telebot.AsyncTeleBot(token, parse_mode='html'), os.urandom(32)
keyboard, inline_keyboard = types.ReplyKeyboardMarkup(), types.InlineKeyboardMarkup()
#connection = psycopg2.connect(os.getenv('DATABASE_URL'), sslmode='require')
#cursor = connection.cursor()#connect to database

def telegramBot():
    @bot.message_handler(commands=['help', 'start'])
    def send_help(message):
        print(str(message.from_user.id) +' ' + str(message.from_user.username)+ ' '+ str(message.chat.id) + ' ' + str(message.text))
        bot.reply_to(
            message, 
            'Даров :)\nТы попал к боту, который достанет тебе домашку из Сетевого Города и скинет тебе.\n<b>Список команд</b> \n /che - домашнее задание на завтра \n/today - домашнее задание на сегодня\n/yesterday - домашнее задание на вчерашний день\n/lessons - узнать расписание'
        )
   
    @bot.message_handler(commands=['che', 'Che'])
    def send_che(message):
        print(str(message.from_user.id) + ' ' + str(message.from_user.username)+ ' '+ str(message.chat.id) + ' ' + str(message.text))
        select_homework(bot, message)
    @bot.message_handler(commands=['yesterday'])
    def send_yesterday(message):
        print(str(message.from_user.id) +' ' + str(message.from_user.username)+ ' '+ str(message.chat.id) + ' ' + str(message.text))
        select_homework(bot, message, -1)

    @bot.message_handler(commands=['today'])
    def send_today(message):
        print(str(message.from_user.id) +' ' + str(message.from_user.username)+ ' '+ str(message.chat.id) + ' ' + str(message.text))
        select_homework(bot, message, 0)
    @bot.message_handler(commands=['all_week'])
    def send_all_week(message):
        print(str(message.from_user.id) +' ' + str(message.from_user.username)+ ' '+ str(message.chat.id) + ' ' + str(message.text))
        select_homework(bot, message, 'all_week')
    @bot.message_handler(commands=['некит'])
    def n(message):
        voice = open('files/voice.ogg', 'rb')
        bot.send_voice(message.chat.id, voice)
        voice.close()
    @bot.message_handler(commands=['lessons'])
    def send_list_of_Lessons(message):
        print(str(message.from_user.id) +' ' + str(message.from_user.username)+ ' '+ str(message.chat.id) + ' ' + str(message.text))
        text = open('files/lessons.txt', 'r', encoding= 'utf-8').read()
        bot.reply_to(
            message,
            text
        )
        text.close()
    @bot.inline_handler(func=lambda query: len(query.query) >= 0)
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
            today = types.InlineQueryResultArticle(
                id='3', title='сегодня',
                description='узнать домаху на сегодня',
                input_message_content=types.InputTextMessageContent(
                    message_text=select_homework(0),
                    parse_mode='Markdown'
                )
            )
            yesterday = types.InlineQueryResultArticle(
                id='4', title='вчера',
                description='узнать вчерашнюю домаху',
                input_message_content=types.InputTextMessageContent(
                    message_text=select_homework(-1),
                    parse_mode='Markdown'
                )
            )
            lessons = types.InlineQueryResultArticle(
                id='2', title='расписание',
                description='узнать расписание',
                input_message_content=types.InputTextMessageContent(
                    message_text='Расписание\n' + open('files/lessons.txt', 'r', encoding= 'utf-8').read(),
                    parse_mode='Markdown'
                )
            )
            all_week = types.InlineQueryResultArticle(
                id='5', title='вся неделя',
                description='узнать д/з на всю неделю',
                input_message_content=types.InputTextMessageContent(
                    message_text=select_homework(day='all_week'),
                    parse_mode='Markdown'
                )
            )
            bot.answer_inline_query(message.id, [che, lessons, today, yesterday, all_week])
        except Exception as e:
            print(e)
        #print(str(message.from_user.id) + ' ' + str(message.from_user.username) + ' ' + str(message.text))
    '''
    @bot.message_handler(commands=['login'], chat_types=['private'])
    def login(message):
        bot.send_message(message, 'Выберите школу')
        
        bot.send_message(message, 'Введите логин от Сетевого города')   
    '''
    
    bot.polling(non_stop=True)
if __name__ == '__main__':
    telegramBot() 
   
