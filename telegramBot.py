import telebot
from telebot import types
import os 
from extractHomeworkFromHTML import extractHomework, selectHomework

bot = telebot.TeleBot("1950280557:AAEGpmKCGIHZsoxzH5ndIJDTB5rMdGPoLN8", parse_mode=None)

@bot.message_handler(commands=['che'])
def send_welcome(message):
	bot.reply_to(message, selectHomework())
@bot.inline_handler(func=lambda query: len(query.query) > 0)
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
            id='2', title='сегодня',
            description='узнать домаху на сегодня',
            input_message_content=types.InputTextMessageContent(
                message_text=selectHomework(0)
            )
        )
        yesterday = types.InlineQueryResultArticle(
            id='3', title='вчера',
            description='узнать вчеранюю домаху',
            input_message_content=types.InputTextMessageContent(
                message_text=selectHomework(-1)
            )
        )
        bot.answer_inline_query(query.id, [che, today, yesterday])
    except Exception as e:
        print(e)
bot.polling()
