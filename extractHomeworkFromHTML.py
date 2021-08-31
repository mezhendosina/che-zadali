from bs4 import BeautifulSoup
import psycopg2
import os 
from datetime import datetime, timedelta
import pytz

summerHolidays = ['06', '07', '08']
holidays = [
	'27.10.2021', '28.10.2021', '29.03.2021,', '30.10.2021', '31.10.2021', 
	'01.11.2021', '02.11.2021', '03.11.2021', '29.12.2021', '30.12.2021', '31.12.2021', '01.01.2022', '02.01.2022', '03.01.2022', '04.01.2022', '05.01.2022', '06.01.2022', '07.01.2022', '08.01.2022', '09.01.2022', '10.01.2022', '11.01.2022', '12.01.2022', 
	'22.03.2022', '23.03.2022', '24.03.2022', '25.03.2022', '26.03.2022', '27.03.2022', '28.03.2022', '29.03.2022'
	]

def extractHomework(code):
	def months(month):
		return {
			'дек.': 12,'янв.': 1, 'февр.': 2,
			'мар.': 3,'апр.': 4,'мая': 5,
			'июн.': 6, 'июл.': 7, 'авг.': 8,
			'сент.': 9, 'окт.': 10, 'нояб.': 11
		}[month]
	connection = psycopg2.connect(os.getenv('DATABASE_URL'), sslmode='require')
	cursor = connection.cursor()
	'''
	cursor.execute('SELECT count(*) FROM homeworktable;'))
	'''
	soup =  BeautifulSoup(code, features = 'lxml')
	schoolJournal = soup.find('div', 'schooljournal_content column')
	dayTable = schoolJournal.find_all('div', class_ = 'day_table')
	for i in dayTable:
		day= i.find('span', 'ng-binding').get_text()
		dayName = None
		dayNum = int(day.split(' ')[1])
		dayMonth = months(day.split(' ')[2])
		dayYear = int(day.split(' ')[3])
		for a in i.find_all('tr', class_ = 'ng-scope'):
			try:
				lesson = a.find('a', 'subject ng-binding ng-scope').get_text()
				try:
					homework = a.find('a', 'ng-binding ng-scope').get_text()
				except AttributeError:
					homework = None
				cursor.execute(f"INSERT INTO homeworktable VALUES('{day}', '{lesson}', '{homework}', '{dayName}', {dayNum}, {dayMonth}, {dayYear})  ON CONFLICT DO NOTHING"
				)
			except AttributeError as e:
				print('AttributeError:', e)
	date = datetime.now(pytz.timezone('Asia/Yekaterinburg')) + timedelta(days=-7)
	#countLinesAfter = cursor.execute('SELECT count(*) FROM homeworktable;')
	cursor.execute("DELETE FROM homeworktable WHERE dayname=%s and daymonth=%s and dayYear=%s", (int(date.strftime(' %d').replace(' 0', '')), int(date.strftime(' %m').replace(' 0' '')), date.strftime('%Y'))
	)
	connection.commit()
	if countLines != countLinesAfter:
		return "New"
	else:
		return "Old"

def selectHomework(day=1):
	connection = psycopg2.connect(os.getenv('DATABASE_URL'), sslmode='require')
	cursor = connection.cursor()
	if len(str(day)) == 0:
		return 'Чтобы выбрать день нужно после команды указать дату в формате ```день.месяц.год```'
	elif len(str(day)) > 2:
		try: 
			cursor.execute(
				'SELECT lesson, homework FROM homeworktable WHERE daynum=%s and daymonth=%s and dayYear=%s;',
				(
					day.split('.')[0],
					day.split('.')[1],
					day.split('.')[2]
				)
			)
			date = f"{day.split('.')[0]}.{day.split('.')[1]}.{day.split('.')[2]}"
		except IndexError:
			return 'Неподдерживаемый формат даты. Пример даты:\n```/s день.месяц.год```'
		except psycopg2.Error as e:
			return 'Возможно вы пытаетесь получить слишком раннюю домаху, т.к. бот хранит только последние 7 дней домашки '
	else:
		date = datetime.now(pytz.timezone('Asia/Yekaterinburg')) + timedelta(days=int(day))
		for i in summerHolidays:
			if date.strftime('%m') == i:
				return 'Какая домаха, лето жеж'
		for i in holidays:
			if date.strftime('%d.%m.%Y') == i:
				return 'Какая домаха, каникулы жеж'
		if date.strftime('%w') == 0:
			date = datetime.now(pytz.timezone('Asia/Yekaterinburg')) + timedelta(days=2) 
		try:
			cursor.execute(
	            'SELECT lesson, homework FROM homeworktable WHERE daynum=%s and daymonth=%s and dayYear=%s;',
	            (int(date.strftime(' %d').replace(' 0', '')), int(date.strftime(' %m').replace(' 0' '')), date.strftime('%Y'))
			)
		except TypeError:
			cursor.execute(
				'SELECT lesson, homework FROM homeworktable WHERE daynum=%s and daymonth=%s and dayYear=%s;',
	            (date.strftime('%d'), date.strftime('%m'), date.strftime('%Y'))
			)
	d = date.strftime('%d.%m.%Y')
	a = f'Домаха на ```{d}```: \n' + '\n'.join(map(lambda x: f'**{x[0]}**: {x[1]}', cursor.fetchall()))
	return a

