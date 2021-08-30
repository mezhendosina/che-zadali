import telebot
from telebot import types
import os 
from extractHomeworkFromHTML import extractHomework, selectHomework

bot = telebot.TeleBot(os.getenv("TELEGRAM_API_TOKEN"), parse_mode=None)

listLessons = 'Расписание будет, когда его скажут'
markup = types.ReplyKeyboardMarkup()

@bot.message_handler(commands=['che', 'Che'])
def send_che(message):
	bot.reply_to(message, selectHomework(), parse_mode="Markdown")

@bot.message_handler(commands=['yesterday'])
def send_yesterday(message):
	bot.reply_to(message, selectHomework(-1), parse_mode="Markdown")

@bot.message_handler(commands=['today'])
def send_today(message):
	bot.reply_to(message, selectHomework(0), parse_mode="Markdown")
@bot.message_handler(commands=['lessons'])
def sendListOfLessons(message):
	bot.reply_to(message, listLesson)
@bot.message_handler(commands=['help', 'start'])
def send_help(message):
	bot.reply_to(message, 'Даров :)\nТы попал к боту, который достанет тебе домашку из Сетевого Города и скинет тебе.\nчтобы воспользоваться моей основной функцией напиши/che')

@bot.message_handler(commands=['select'])
def s(message):
    try:
	    bot.reply_to(
		message, 
		selectHomework(message.text.split(' ')[1]),
		parse_mode="Markdown"
	    )
    except IndexError:
        bot.reply_to(
            message,
            'Чтобы воспользоваться этой командой, надо указать дату в формате ```день.месяц.год```',
            parse_mode="Markdown"
            )
@bot.inline_handler(func=lambda query: len(query.query) >= 0)
def query_text(query):
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
        bot.answer_inline_query(query.id, [che, lessons, today, yesterday])
    except Exception as e:
    	bot.send_message(401311369, query + '\n\n' + e)
    	bot.reply_to(query, 'Упс, что то пошло не так :(')
    	print(e)
bot.polling()
