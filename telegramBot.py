from telebot import types
from Homework import select_homework, add_homework
import os, re, telebot, hashlib, psycopg2

token = os.getenv("TELEGRAM_API_TOKEN")
bot, markup, salt= telebot.TeleBot(token, parse_mode='Markdown'), types.ReplyKeyboardMarkup(), os.urandom(32)
connection = psycopg2.connect(os.getenv('DATABASE_URL'), sslmode='require')
cursor = connection.cursor()#connect to database
voice = open('voice.ogg', 'rb')

@bot.message_handler(commands=['help', 'start'])
def send_help(message):
    print(str(message.from_user.id) +' ' + str(message.from_user.username)+ ' '+ str(message.chat.id) + ' ' + str(message.text))
    bot.reply_to(
		message, 
		'Даров :)\nТы попал к боту, который достанет тебе домашку из Сетевого Города и скинет тебе.\nчтобы воспользоваться моей основной функцией напиши /che'
	)

@bot.message_handler(commands=['che', 'Che'])
def send_che(message):
    print(str(message.from_user.id) +' ' + str(message.from_user.username)+ ' '+ str(message.chat.id) + ' ' + str(message.text))
    bot.reply_to(message, select_homework())

@bot.message_handler(commands=['yesterday'])
def send_yesterday(message):
    print(str(message.from_user.id) +' ' + str(message.from_user.username)+ ' '+ str(message.chat.id) + ' ' + str(message.text))
    bot.reply_to(message, select_homework(-1))

@bot.message_handler(commands=['today'])
def send_today(message):
    print(str(message.from_user.id) +' ' + str(message.from_user.username)+ ' '+ str(message.chat.id) + ' ' + str(message.text))
    bot.reply_to(message, select_homework(0))

@bot.message_handler(commands=['select'])
def s(message):
    print(str(message.from_user.id) +' ' + str(message.from_user.username)+ ' '+ str(message.chat.id) + ' ' + str(message.text))
    try:
	    bot.reply_to(
			message, 
			select_homework(message.text.split(' ', maxsplit=1)[1])
	    )
    except IndexError:
        bot.reply_to(
            message,
            'Чтобы воспользоваться этой командой, надо указать дату в формате ```день.месяц.год```\nP.S. Бот хранит домашку только за последние 7 дней'
        )
@bot.message_handler(commands=['некит'])
def nekit(message):
   voice = open('voice.ogg', 'rb')
   bot.send_voice(message, voice)

@bot.message_handler(commands=['lessons'])
def sendListOfLessons(message):
	print(str(message.from_user.id) +' ' + str(message.from_user.username)+ ' '+ str(message.chat.id) + ' ' + str(message.text))
	text = open('lessons.txt', 'r', encoding= 'utf-8').read()
	bot.reply_to(
    	message,
    	text
    )

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
				message_text='Расписание\n' + open('lessons.txt', 'r', encoding= 'utf-8').read(),
				parse_mode='Markdown'
			)
        )
        nekit = types.InlineQueryResultArticle(
        	id='5', title='Некит',
        	description='Никита Лапшин попросил добавить',
        	input_message_content=voice
        )
        bot.answer_inline_query(message.id, [che, lessons, today, yesterday, nekit])
    except Exception as e:
    	print(e)
    #print(str(message.from_user.id) + ' ' + str(message.from_user.username) + ' ' + str(message.text))
'''
@bot.message_handler(commands=['login'], chat_types=['private'])
def login(message):
    bot.send_message(message, 'Выберите школу')
    
    bot.send_message(message, 'Введите логин от Сетевого города')   
'''
bot.send_message(401311369, 'все ок')
bot.polling(non_stop=True)