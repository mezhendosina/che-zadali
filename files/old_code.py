'''Homework.py'''
summerHolidays = ['06', '07', '08'] #summer holidays month number  
holidays = [
	'27.10.2021', '28.10.2021', '29.10.2021', '30.10.2021', '31.10.2021',
	'01.11.2021', '02.11.2021', '03.11.2021', 
	'29.12.2021', '30.12.2021', '31.12.2021', '01.01.2022', '02.01.2022', '03.01.2022', '04.01.2022', 
	'05.01.2022', '06.01.2022', '07.01.2022', '08.01.2022', '09.01.2022', '10.01.2022', '11.01.2022', '12.01.2022',
	'22.03.2022', '23.03.2022', '24.03.2022', '25.03.2022', '26.03.2022', '27.03.2022', '28.03.2022', '29.03.2022'
	] #holidays days

for i in summerHolidays:
    if date.strftime('%m') == i:
        return 'Какая домаха, лето жеж'
for i in holidays:
    if date.strftime('%d.%m.%Y') == i:
        return 'Какая домаха, каникулы жеж'
'''telegrambot.py'''
@bot.message_handler(commands=['некит'])
    def n(message):
        print(str(message.from_user.id) +' ' + str(message.from_user.username)+ ' '+ str(message.chat.id) + ' ' + str(message.text))
        voice = open('files/voice.ogg', 'rb')
        bot.send_voice(message.chat.id, voice)