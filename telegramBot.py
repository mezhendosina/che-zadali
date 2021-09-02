 from telebot import types
from extractHomeworkFromHTML import addHomework, selectHomework
import os, re, telebot

bot, markup= telebot.TeleBot(os.getenv("TELEGRAM_API_TOKEN"), parse_mode='MarkdownV2'), types.ReplyKeyboardMarkup()

@bot.message_handler(commands=['help', 'start'])
def send_help(message):
    print(str(message.from_user.id) +' ' + str(message.from_user.username)+ ' '+ str(message.chat.id) + ' ' + str(message.text))
    bot.reply_to(
		message, 
		'Даров :)\nТы попал к боту, который достанет тебе домашку из Сетевого Города и скинет тебе.\nчтобы воспользоваться моей основной функцией напиши/che'
	)


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

@bot.message_handler(commands=['select'])
def s(message):
    print(str(message.from_user.id) +' ' + str(message.from_user.username)+ ' '+ str(message.chat.id) + ' ' + str(message.text))
    try:
	    bot.reply_to(
			message, 
			selectHomework(message.text.split(' ', maxsplit=1)[1]),
			parse_mode="MarkdownV2"
	    )
    except IndexError:
        bot.reply_to(
            message,
            'Чтобы воспользоваться этой командой, надо указать дату в формате ```день.месяц.год```\nP.S. Бот хранит домашку только за последние 7 дней',
            parse_mode="MarkdownV2"
        )

@bot.message_handler(commands=['add'])
def setHomework(message):
	try:
		lesson, homework, date = message.text.split(': ', maxsplit=1)[0], message.text.split(': ', maxsplit=1)[1], re.search(r'\d\d[.]\d\d[.]\d\d\d\d', message.text)
		addHomework(lesson, homework, date)
		bot.reply_to(message, 'Домашка сохранена')
		print(str(message.from_user.id) +' ' + str(message.from_user.username)+ ' '+ str(message.chat.id) + ' ' + str(message.text))
	except IndexError:
		print(str(message.from_user.id) +' ' + str(message.from_user.username)+ ' '+ str(message.chat.id) + ' ' + str(message.text) + 'Stupid human')
		bot.send_message(message.chat.id, 'Возможно ты не правильно заполнил домашку.\nПример заполнения домашки: \n```/add Урок: домашка :дата сдачи(дд.мм.гггг)```\n P.s. если домашка на завтра, можешь не писать дату')


@bot.message_handler(commands=['lessons'])
def sendListOfLessons(message):
    print(str(message.from_user.id) +' ' + str(message.from_user.username)+ ' '+ str(message.chat.id) + ' ' + str(message.text))
    bot.reply_to(
    	message,
    	open('lessons.txt', 'r', encoding= 'utf-8').read()
    )

@bot.message_handler(commands=['set'])
def setLessons(message):
	try:
		lessons = message.text.split(' ', maxsplit=1)[0]
		a = open('lessons.txt', 'w')
		a.write(lessons)
		a.close()
		bot.reply_to(message, 'Расписание сохранено')
		print(str(message.from_user.id) +' ' + str(message.from_user.username)+ ' '+ str(message.chat.id) + ' ' + str(message.text))
	except IndexError:
		bot.send_message(message, 'Возможно ты не правильно заполнил расписание.\n Пример сохранения расписания:\n```/set День недели\nвремя:урок\nвремя:урок```')
		print(str(message.from_user.id) +' ' + str(message.from_user.username)+ ' '+ str(message.chat.id) + ' ' + str(message.text) + 'Stupid human')



@bot.inline_handler(func=lambda query: len(query.query) >= 0)
def query_text(message):
    try:
        che = types.InlineQueryResultArticle(
            id='1', title="Че",
            description='узнать домаху на завтра',
            input_message_content=types.InputTextMessageContent(
                message_text=selectHomework(),
				parse_mode='MarkdownV2'
            )
        )
        today = types.InlineQueryResultArticle(
            id='3', title='сегодня',
            description='узнать домаху на сегодня',
            input_message_content=types.InputTextMessageContent(
                message_text=selectHomework(0),
				parse_mode='MarkdownV2'
            )
        )
        yesterday = types.InlineQueryResultArticle(
            id='4', title='вчера',
            description='узнать вчерашнюю домаху',
            input_message_content=types.InputTextMessageContent(
                message_text=selectHomework(-1),
				parse_mode='MarkdownV2'
            )
        )
        lessons = types.InlineQueryResultArticle(
        	id='2', title='расписание',
        	description='узнать расписание',
        	input_message_content=types.InputTextMessageContent(
				message_text=open('lessons.txt', 'r', encoding= 'utf-8').read(),
				parse_mode='MarkdownV2'
			)
        )
        bot.answer_inline_query(message.id, [che, lessons, today, yesterday])
    except Exception as e:
    	print(e)
    print(str(message.from_user.id) + ' ' + str(message.from_user.username)+ ' ' + str(message.chat.id) + ' ' + str(message.text))
    
bot.send_message(401311369, 'все ок')
bot.polling(non_stop=True)