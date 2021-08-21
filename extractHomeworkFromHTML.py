from bs4 import BeautifulSoup
import psycopg2
import os 
from datetime import datetime, timedelta
def extractHomework(code):
	def months(month):
		return {
			'янв.': 1,
			'февр.': 2,
			'мар.': 3,
			'апр.': 4,
			'мая': 5,
			'сент.': 9,
			'окт.': 10,
			'нояб.': 11,
			'дек.': 12,
		}[month]
	def days(day):
		return {
			'Пн':1,
			'Вт': 2,
			'Ср': 3,
			'Чт': 4,
			'Пт': 5,
			'Сб': 6
		}[day]

	connection = psycopg2.connect(os.getenv('DATABASE_URL'), sslmode='require')
	cursor = connection.cursor()

	soup =  BeautifulSoup(code, features = 'lxml')
	schoolJournal = soup.find('div', 'schooljournal_content column')
	dayTable = schoolJournal.find_all('div', class_ = 'day_table')
	for i in dayTable:
		day= i.find('span', 'ng-binding').get_text()
		dayName = days(day.split(',')[0])
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
					day, 
					lesson, 
					homework, 
					dayName, 
					dayNum, 
					dayMonth, 
					dayYear
				))
			except AttributeError as e:
				print('AttributeError:', e)
	date = datetime.now() + timedelta(days=-7)
	cursor.execute("DELETE FROM homeworktable WHERE dayname=%s and daymonth=%s and dayYear=%s", 
	(date.strftime('%d'), date.strftime('%m'), date.strftime('%Y'))
	)
	connection.commit()
