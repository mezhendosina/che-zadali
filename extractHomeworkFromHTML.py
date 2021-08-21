from bs4 import BeautifulSoup
import psycopg2
import sys
import os 
DATABASE_URL = os.environ['DATABASE_URL']
def extractHomework(code):
	def months(month):
		return {
			'января': 1,
			'февраля': 2,
			'марта': 3,
			'апр.': 4,
			'апреля': 4,
			'мая': 5,
			'инюня': 6,
			'июля': 7,
			'августа': 8,
			'сентября': 9,
			'октября': 10,
			'ноября': 11,
			'декабря': 12,
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

	connection = psycopg2.connect(DATABASE_URL, sslmode='require')
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
			except AttributeError:
				print('AttributeError')
	connection.commit()
