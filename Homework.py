"""
This file works with homework recived from https://sgo.edu-74.ru/
"""

import psycopg2, pytz, os, requests
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
from isoweek import Week
from telebot import types
from yadisk.yadisk import YaDisk
#global variables
connection = psycopg2.connect(os.getenv('DATABASE_URL'), sslmode='require')
cursor = connection.cursor()#connect to database
summerHolidays = ['06', '07', '08'] #summer holidays month number  
holidays = [
	'27.10.2021', '28.10.2021', '29.10.2021', '30.10.2021', '31.10.2021',
	'01.11.2021', '02.11.2021', '03.11.2021', 
	'29.12.2021', '30.12.2021', '31.12.2021', '01.01.2022', '02.01.2022', '03.01.2022', '04.01.2022', 
	'05.01.2022', '06.01.2022', '07.01.2022', '08.01.2022', '09.01.2022', '10.01.2022', '11.01.2022', '12.01.2022',
	'22.03.2022', '23.03.2022', '24.03.2022', '25.03.2022', '26.03.2022', '27.03.2022', '28.03.2022', '29.03.2022'
	] #holidays days

def months(month : int):
	"""This function compare month name with his number"""
	return {
		'дек.': 12,'янв.': 1, 'февр.': 2,
		'мар.': 3,'апр.': 4,'мая': 5,
		'июн.': 6, 'июл.': 7, 'авг.': 8,
		'сент.': 9, 'окт.': 10, 'нояб.': 11
	}[month]
def new_old() -> list:
	i, result = 0, []
	for i in range(2):
		if i == 2:	
			break
		date = datetime.now(pytz.timezone('Asia/Yekaterinburg')) + timedelta(days=i)
		cursor.execute(f"SELECT * FROM homeworktable WHERE daynum={date.strftime('%d')} AND daymonth={date.strftime('%m')} AND dayyear={date.strftime('%Y')};") 
		result.append(cursor.fetchall())
		i+1
	return result


def extract_homework(code : str) -> list:
	"""This function parses code in search homework and delete old homework"""
	
	soup, old_list =  BeautifulSoup(code, features = 'lxml'), new_old()
	schoolJournal = soup.find('div', 'schooljournal_content column')
	dayTable = schoolJournal.find_all('div', class_ = 'day_table')
	
	for i in dayTable:
		day= i.find('span', 'ng-binding').get_text()
		dayNum = int(day.split(' ')[1])
		dayMonth = months(day.split(' ')[2])
		dayYear = int(day.split(' ')[3])

		for a in i.find_all('tr', class_ = 'ng-scope'):
			try:
				lesson = a.find('a', class_='subject ng-binding ng-scope').get_text()
				try:
					homework = a.find('a', class_='ng-binding ng-scope').get_text()
				except AttributeError:
					continue
				cursor.execute('SELECT * FROM homeworktable')
				table = cursor.fetchall()
				try:
					assert (day, lesson, homework, dayNum, dayMonth, dayYear) in table
				except AssertionError:
					cursor.execute(
							f"INSERT INTO homeworktable VALUES('{day}', '{lesson}', '{homework}', {dayNum}, {dayMonth}, {dayYear})"
					)
					continue
			except AttributeError as e:
				continue
	connection.commit()

	a, true_false = new_old(cursor), []
	for i in a:
		if i > old_list.pop(0):
			true_false.append(True)
		else:
			true_false.append(False)
	return true_false


def select_homework(day=1, new : bool =False) -> list:
	"""
	This function collect homework day(1 - tommorow, 0 - today, -1 - yesterday, 'all_week' - homework on week) 
	"""
	y = YaDisk("866043d9835b4c7cb58c5ee656e7e8bd", "4566d2a405a04be89a4003d9e7b78014", os.getenv("YDISK_TOKEN"))
	def select(day, month, year) -> list:
		cursor.execute(
				'SELECT lesson, homework FROM homeworktable WHERE daynum=%s and daymonth=%s and dayYear=%s;',
				(day, month, year)
			)
		return cursor.fetchall()
	
	if day == 'all_week':
		homework, r, date = {}, '', datetime.now(pytz.timezone('Asia/Yekaterinburg'))

		if date.strftime('%w') == '0':
			date = datetime.now(pytz.timezone('Asia/Yekaterinburg')) + timedelta(days=1)	
		week = date.isocalendar()[1]
		mon, sun = Week(date.year, week).monday(), Week(date.year, week).sunday()
		cursor.execute(
			f'SELECT dayNum, lesson, homework FROM homeworktable WHERE dayNum >={mon.strftime("%d")} AND dayNum <={sun.strftime("%d")} AND dayMonth >= {mon.strftime("%m")} AND dayMonth <= {sun.strftime("%m")} AND dayyear BETWEEN {mon.strftime("%Y")} AND {sun.strftime("%Y")};'
			)
		result = cursor.fetchall()
		cursor.execute(
			f'SELECT day, dayNum FROM homeworktable WHERE dayNum >={mon.strftime("%d")} AND dayNum <={sun.strftime("%d")} AND dayMonth >= {mon.strftime("%m")} AND dayMonth <= {sun.strftime("%m")} AND dayyear BETWEEN {mon.strftime("%Y")} AND {sun.strftime("%Y")};'
			)
		day = cursor.fetchall()
		for i in day:
			h = {}
			for a in result:
				if a[0] == i[1]:
					h.update({a[1]: a[2]})	
			homework.update({i[0]: h})
		for i in homework.keys():
			r = str(r)+f'\n\n<i>{i}</i>я\n' + str('\n'.join(map(lambda x: f'<b>{x[0]}</b>:  {x[1]}', list(homework.get(i).items()))))
		
		return r
	
	if datetime.now(pytz.timezone('Asia/Yekaterinburg')).strftime('%w') == '6':
		date = datetime.now(pytz.timezone('Asia/Yekaterinburg')) + timedelta(days=2)
	else:
		date = datetime.now(pytz.timezone('Asia/Yekaterinburg')) + timedelta(days=int(day))

	for i in summerHolidays:
		if date.strftime('%m') == i:
			return 'Какая домаха, лето жеж'
	for i in holidays:
		if date.strftime('%d.%m.%Y') == i:
			return 'Какая домаха, каникулы жеж'
	
	try:
		homework = select(
			int(date.strftime(' %d').replace(' 0', '')), 
			int(date.strftime(' %m').replace(' 0' '')), 
			date.strftime('%Y')
		)
	except TypeError:
		homework = select(date.strftime('%d'), date.strftime('%m'), date.strftime('%Y'))

	d = date.strftime('%d.%m.%Y')
	if new == False:
		#a = f'Домашнее задание на <i>{d}</i>:\n' + '\n'.join(map(lambda x: f'<b>{x[0]}</b>:  {x[1]}', homework))
		a = 'Домашнее задание теперь здесь: https://t.me/joinchat/nDOBdB92pq1jOGFi'
		return a
	else:
		a = f'Похоже появилась новое д\з на <i>{d}</i>:\n' + '\n'.join(map(lambda x: f'<b>{x[0]}</b>:  {x[1]}', homework))

	
	
	attachment, date = [], datetime.now() + timedelta(days=-7)
	headers = {'Accept': 'application/json', 'Authorization': f'OAuth {os.getenv("YDISK_TOKEN")}'}
	r = requests.get('https://cloud-api.yandex.net/v1/disk/resources?path=%2Fche-zadali_files', headers=headers).json()

	for i in r['_embedded']['items']:
		if i['name'] == d:
			for a in requests.get(f'https://cloud-api.yandex.net/v1/disk/resources?path=%2Fche-zadali_files%2F{i["name"]}', headers=headers).json()['_embedded']['items']:
				attachment.append(y.get_download_link(f'/che-zadali_files/{i["name"]}/{a["name"]}'))
		elif int(i['name'].split('.')[0]) < int(date.strftime('%d')) and int(i['name'].split('.')[1]) < int(date.strftime('%m')):
			y.remove(f'/che-zadali_files/{i["name"]}')
	return [a, attachment]