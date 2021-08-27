from bs4 import BeautifulSoup
import psycopg2
import os 
from datetime import datetime, timedelta
import time 

summerHolidays = ['06', '07', '08']
holidays = [
	'27.10.2021', '28.10.2021', '29.03.2021,', '30.10.2021', '31.10.2021', 
	'01.11.2021', '02.11.2021', '03.11.2021', '29.12.2021', '30.12.2021', '31.12.2021', '01.01.2022', '02.01.2022', '03.01.2022', '04.01.2022', '05.01.2022', '06.01.2022', '07.01.2022', '08.01.2022', '09.01.2022', '10.01.2022', '11.01.2022', '12.01.2022', 
	'22.03.2022', '23.03.2022', '24.03.2022', '25.03.2022', '26.03.2022', '27.03.2022', '28.03.2022', '29.03.2022'
	]

def extractHomework(code):
	def months(month):
		return {
			'янв.': 1,
			'февр.': 2,
			'мар.': 3,
			'апр.': 4,
			'мая': 5,
			'июн.': 6,
			'июл.': 7,
			'авг.': 8,
			'сент.': 9,
			'окт.': 10,
			'нояб.': 11,
			'дек.': 12,
		}[month]
	connection = psycopg2.connect(os.getenv('DATABASE_URL'), sslmode='require')
	cursor = connection.cursor()
	countLines = cursor.execute('SELECT count(*) FROM table;')
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
				cursor.execute("INSERT INTO homeworktable VALUES('{}', '{}', '{}', {}, {}, {}, {})  ON CONFLICT DO NOTHING".format(
					day, lesson, homework, dayName, dayNum, dayMonth, dayYear
				))
			except AttributeError as e:
				print('AttributeError:', e)
	date = datetime.now() + timedelta(days=-7)
	connection.commit()
	countLinesAfter = cursor.execute('SELECT count(*) FROM table;')
	if countLines != countLinesAfter:
		cursor.execute("DELETE FROM homeworktable WHERE dayname=%s and daymonth=%s and dayYear=%s", 
	(date.strftime('%d'), date.strftime('%m'), date.strftime('%Y'))
	)
		connection.commit()
		return "New"
	else:
		cursor.execute("DELETE FROM homeworktable WHERE dayname=%s and daymonth=%s and dayYear=%s", 
	(date.strftime('%d'), date.strftime('%m'), date.strftime('%Y'))
	)
		connection.commit()
		return "Old"

def selectHomework(day=1):
	date = datetime.now() + timedelta(days=day)
	
	for i in summerHolidays:
		if time.strftime('%m') == i:
			return 'Какая домаха, лето жеж'
	for i in holidays:
		if time.strftime('%d.%m.%Y') == i:
			return 'Какая домаха, каникулы жеж'
	if time.strftime('%w') == 6:
		date = datetime.now() + timedelta(days=2)

	connection = psycopg2.connect(os.getenv('DATABASE_URL'), sslmode='require')
	cursor = connection.cursor()
	cursor.execute(
            'SELECT lesson, homework FROM homeworktable WHERE daynum=%s and daymonth=%s and dayYear=%s;',
            (int(date.strftime(' %d').replace(' 0', '')), int(date.strftime(' %m').replace(' 0' '')), date.strftime('%Y'))
    )
	a = date.strftime('Домаха на %d.%m.%Y: \n')+'\n'.join(map(lambda x: '{}: {}'.format(x[0], x[1]), cursor.fetchall()))
	return a