import telebot
from telebot import types
from extractHomeworkFromHTML import extractHomework, selectHomework
import os

bot = telebot.TeleBot(os.getenv("TELEGRAM_API_TOKEN"), parse_mode='Markdown')

listLessons = '2 сентября будет: \nМатан\nОБЖ\nИстория\nРусский'
markup = types.ReplyKeyboardMarkup()

@bot.message_handler(commands=['che', 'Che'])
def send_che(message):
    print(str(message.from_user.id) +' ' + str(message.from_user.username)+ ' '+ str(message.chat.id) + ' ' + str(message.text))
    bot.reply_to(message, selectHomework())

@bot.message_handler(commands=['yesterday'])
def send_yesterday(message):
    print(str(message.from_user.id) +' ' + str(message.from_user.username)+ ' '+ str(message.chat.id) + ' ' + str(message.text))
    bot.reply_to(message, selectHomework(-1))

@bot.message_handler(commands=['today'])
def send_today(message):
    print(str(message.from_user.id) +' ' + str(message.from_user.username)+ ' '+ str(message.chat.id) + ' ' + str(message.text))
    bot.reply_to(message, selectHomework(0))

@bot.message_handler(commands=['lessons'])
def sendListOfLessons(message):
    print(str(message.from_user.id) +' ' + str(message.from_user.username)+ ' '+ str(message.chat.id) + ' ' + str(message.text))
    bot.reply_to(
    	message, 
    	open('lessons.txt', 'r', encoding= 'utf-8'.read()
    )

@bot.message_handler(commands=['set'])
def setLessons(message):
	open('lessons.txt', 'w').write(message.text.split(' ')[1])
	bot.send_message('Расписание сохранено')

@bot.message_handler(commands=['help', 'start'])
def send_help(message):
    print(str(message.from_user.id) +' ' + str(message.from_user.username)+ ' '+ str(message.chat.id) + ' ' + str(message.text
    bot.reply_to(message, 'Даров :)\nТы попал к боту, который достанет тебе домашку из Сетевого Города и скинет тебе.\nчтобы воспользоваться моей основной функцией напиши/che')

@bot.message_handler(commands=['select'])
def s(message):
    print(str(message.from_user.id) +' ' + str(message.from_user.username)+ ' '+ str(message.chat.id) + ' ' + str(message.text))
    try:
	    bot.reply_to(
		message, 
		selectHomework(message.text.split(' ')[1]),
		parse_mode="Markdown"
	    )
    except IndexError:
        bot.reply_to(
            message,
            'Чтобы воспользоваться этой командой, надо указать дату в формате ```день.месяц.год```\nP.S. Бот хранит домашку только за последние 7 дней',
            parse_mode="Markdown"
            )

@bot.inline_handler(func=lambda message: len(message.message) >= 0)
def query_text(message):
    try:
        che = types.InlineQueryResultArticle(
            id='1', title="Че",
            description='узнать домаху на завтра',
            input_message_content=types.InputTextMessageContent(
                message_text=selectHomework()
            )
        )
        today = types.InlineQueryResultArticle(
            id='3', title='сегодня',
            description='узнать домаху на сегодня',
            input_message_content=types.InputTextMessageContent(
                message_text=selectHomework(0)
            )
        )
        yesterday = types.InlineQueryResultArticle(
            id='4', title='вчера',
            description='узнать вчерашнюю домаху',
            input_message_content=types.InputTextMessageContent(
                message_text=selectHomework(-1)
            )
        )
        lessons = types.InlineQueryResultArticle(
        	id='2', title='расписание',
        	description='узнать расписание',
        	input_message_content=types.InputTextMessageContent(message_text=listLessons)
        	)
        bot.answer_inline_query(message.id, [che, lessons, today, yesterday])
    except Exception as e:
    	bot.send_message(401311369, message + '\n\n' + e)
    	bot.reply_to(message, 'Упс, что то пошло не так :(')
    	print(e)
    print(str(message.from_user.id) +' ' + str(message.from_user.username)+ ' '+ str(message.chat.id) + ' ' + str(message.text))
bot.send_message(401311369, 'все ок')
bot.polling()

def sendHomework(message=selectHomework()):
    print('send homework at 14:30')
    a = bot.send_message('-1001561236768', message)
    bot.pin_chat_message('-1001561236768', a.id, disable_notification=True)
