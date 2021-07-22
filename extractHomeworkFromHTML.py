from bs4 import BeautifulSoup
import psycopg2
from urllib.parse import urlparse
import sys
import os 

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
#result = urlparse(os.environ.get('DATABASE_URL'))
connection = psycopg2.connect(
	user='xbwoosfturwnmu',#result.password,
   	password='4f3f0a25361cac11df1af8a3dfe11469029a422f85e055fa1f6072cb1c4b48c3',#result.password,
   	database='d4g1mkv1jennht',#result.path[1:],
	host='ec2-54-73-68-39.eu-west-1.compute.amazonaws.com',#result.hostname,
    port='5432'#result.port
)
cursor = connection.cursor()
with open('homework.html', 'r', encoding = 'utf-8') as f:
	soup =  BeautifulSoup(f, features = 'lxml')
data = []
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
            i = 0
connection.commit()
