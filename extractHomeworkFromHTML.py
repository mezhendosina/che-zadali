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
		'апреля': 4,
		'мая': 5
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
result = urlparse(os.environ.get('DATABASE_URL'))
connection = psycopg2.connect(
	user=result.password,
   	password=result.password,
   	database=result.path[1:],
	host=result.hostname,
    port = result.port
)
cursor = connection.cursor()
#with open('homework.html', 'r', encoding = 'utf-8') as f:
soup =  BeautifulSoup(sys.argv[1], features = 'lxml')
data = []
schoolJournal = soup.find('div', 'schooljournal_content column')
for i in schoolJournal.find_all('div', class_ = 'day_table')
:
    day= i.find('span', 'ng-binding').get_text()
    dayName = days(day.split(',')[0])
    dayNum = int(day.split(',')[1][:3])
    dayMonth = months(day.split(',')[1][4:].split(' ')[0])
    dayYear = day.split(',')[1][4:].split(' ')[1]
    
    for a in i.find_all('tr', class_ = 'ng-scope'):
        try:
            lesson = a.find('a', 'subject ng-binding ng-scope').get_text()
            try:
                homework = a.find('a', 'ng-binding ng-scope').get_text()
            except AttributeError:
                homework = None

            connection.execute('INSERT {}, {}, {}, {}, {}, {} INTO homeworktable ON CONFLICT DO NOTHING'.format(
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