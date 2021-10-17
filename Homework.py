"""
This file works with homework recived from https://sgo.edu-74.ru/

"""

from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from isoweek import Week
import psycopg2, pytz, os

#global variables
connection = psycopg2.connect(os.getenv('DATABASE_URL'), sslmode='require')
cursor = connection.cursor()#connect to database
summerHolidays = ['06', '07', '08'] #summer holidays month number  
holidays = [
	'27.10.2021', '28.10.2021', '29.03.2021,', '30.10.2021', '31.10.2021', 
	'01.11.2021', '02.11.2021', '03.11.2021', '29.12.2021', '30.12.2021', 
	'31.12.2021', '01.01.2022', '02.01.2022', '03.01.2022', '04.01.2022', 
	'05.01.2022', '06.01.2022', '07.01.2022', '08.01.2022', '09.01.2022', 
	'10.01.2022', '11.01.2022', '12.01.2022', '22.03.2022', '23.03.2022', 
	'24.03.2022', '25.03.2022', '26.03.2022', '27.03.2022', '28.03.2022', 
	'29.03.2022'
	] #holidays days


def delete_homework(day=False) -> None:
	"""
	This function delete homework by date(dd.mm.yyyy). 
	If variable day is not filled - deletes homework that was asked 7 days ago
	"""
	
	if day == False:
		date = datetime.now(pytz.timezone('Asia/Yekaterinburg')) + timedelta(days=-7)
	else:
		date = datetime(int(day.split('.')[2]), int(day.split('.')[1]), int(day.split('.')[0]))
	try:
		cursor.execute(
			"DELETE FROM homeworktable WHERE daynum=%s and daymonth=%s and dayYear=%s", 
			(int(date.strftime(' %d').replace(' 0', '')), int(date.strftime(' %m').replace(' 0' '')), date.strftime('%Y'))
		)
	except TypeError:
		cursor.execute(
			"DELETE FROM homeworktable WHERE daynum=%s and daymonth=%s and dayYear=%s", 
			(int(date.strftime('%d')), int(date.strftime('%m')), date.strftime('%Y'))
		)

def add_homework(lesson, homework, day=False) -> None:
	"""This function add homework to database. If day = False add homework to next day"""
	
	if day == False:
		date = datetime.now(pytz.timezone('Asia/Yekaterinburg')) + timedelta(days=1)
	else:
		date = datetime(int(day.split('.')[2]), int(day.split('.')[1]), int(day.split('.')[0]))
	cursor.execute(
		f"INSERT INTO homeworktable VALUES('{date}', '{lesson}', '{homework}', %s, %s, %s)  ON CONFLICT DO NOTHING",
		(date.strftime('%d'), date.strftime('%m'), date.strftime('%Y'))
	)
	connection.commit()
def months(month):
	"""This function compare month name with his number"""
	return {
		'дек.': 12,'янв.': 1, 'февр.': 2,
		'мар.': 3,'апр.': 4,'мая': 5,
		'июн.': 6, 'июл.': 7, 'авг.': 8,
		'сент.': 9, 'окт.': 10, 'нояб.': 11
	}[month]
def extract_homework(code) -> bool:
	"""This function parses code in search homework and delete old homework"""
	
	date = datetime.now(pytz.timezone('Asia/Yekaterinburg')) + timedelta(days=1)
	cursor.execute(f"SELECT * FROM homeworktable WHERE daynum={date.strftime('%d')} AND daymonth={date.strftime('%m')} AND dayyear={date.strftime('%Y')};") 
	old = cursor.fetchall()

	soup =  BeautifulSoup(code, features = 'lxml')
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
					print(day, lesson, homework, dayNum, dayMonth, dayYear)
					continue
			except AttributeError as e:
				continue
	connection.commit()
	cursor.execute(f"SELECT * FROM homeworktable WHERE daynum={date.strftime('%d')} AND daymonth={date.strftime('%m')} AND dayyear={date.strftime('%Y')};") 
	new = cursor.fetchall()
	if new > old:
		return True
	else:
		return False

def select_homework(day=1, new=False) -> str:
	"""
	This function collect day(1 - tommorow, 0 - today, -1 - yesterday, 'all_week' - homework on week) or user selected day and return homework for this day
	"""
	
	def select(day, month, year) -> list:
		cursor.execute(
				'SELECT lesson, homework FROM homeworktable WHERE daynum=%s and daymonth=%s and dayYear=%s;',
				(day, month, year)
			)
		return cursor.fetchall()
	if day == 'all_week':
		homework = {}
		r = ''
		date = datetime.now(pytz.timezone('Asia/Yekaterinburg'))
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
			r = str(r)+f'\n\n_{i}_\n' + str('\n'.join(map(lambda x: f'***{x[0]}***:  {x[1]}', list(homework.get(i).items()))))
		return r 
	elif len(str(day)) == 0:
		return 'Чтобы выбрать день, нужно после команды указать дату в формате ```день.месяц.год```'
	elif len(str(day)) > 2:
		try: 
			homework = select(
				day.split('.')[0],
				day.split('.')[1],
				day.split('.')[2]
			)

			date = f"{day.split('.')[0]}.{day.split('.')[1]}.{day.split('.')[2]}"
		except IndexError:
			return 'Неподдерживаемый формат даты. Пример даты:```\n/set день.месяц.год```'
		except psycopg2.Error as e:
			return 'Возможно вы пытаетесь получить слишком раннюю домаху. Бот хранит только последние 7 дней домашки '
	else:
		date = datetime.now(pytz.timezone('Asia/Yekaterinburg')) + timedelta(days=int(day))
		for i in summerHolidays:
			if date.strftime('%m') == i:
				return 'Какая домаха, лето жеж'
		for i in holidays:
			if date.strftime('%d.%m.%Y') == i:
				return 'Какая домаха, каникулы жеж'
		if date.strftime('%w') == 5:
			date1 = datetime.now(pytz.timezone('Asia/Yekaterinburg')) + timedelta(days=2)
			homework = select(
				date.strftime('%d'),
				date.strftime('%m'),
				date.strftime('%Y')
			)
		if date.strftime('%w') == 0:
			date = datetime.now(pytz.timezone('Asia/Yekaterinburg')) + timedelta(days=1) 
		try:
			homework = select(
				int(date.strftime(' %d').replace(' 0', '')), 
				int(date.strftime(' %m').replace(' 0' '')), 
				date.strftime('%Y')
			)
		except TypeError:
			homework = select(date.strftime('%d'), date.strftime('%m'), date.strftime('%Y'))
	if open(
		os.path.join(
			os.path.dirname(os.path.realpath(__file__)),
			'files/truefalse.txt'
			), 
		'r'
		).read() == 'True':
		tf = '\nP.s. в одном из домашних заданий есть вложенные(-ый) файл(-ы)'
	else:
		tf = '\n'

	d = date.strftime('%d.%m.%Y')
	if new == False:
		a = f'Домашнее задание на _{d}_:\n' + '\n'.join(map(lambda x: f'***{x[0]}***:  {x[1]}', homework)) + tf
	else:
		a = a = f'Похоже появилась новое д\з на _{d}_:\n' + '\n'.join(map(lambda x: f'***{x[0]}***:  {x[1]}', homework)) + tf
	return a