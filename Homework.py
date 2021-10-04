from bs4 import BeautifulSoup
from datetime import datetime, timedelta
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
	
	cursor.execute('SELECT * FROM homeworktable;') 
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
					homework = None
				cursor.execute(
					f"INSERT INTO homeworktable VALUES('{day}', '{lesson}', '{homework}', {dayNum}, {dayMonth}, {dayYear})  ON CONFLICT DO NOTHING"
				)
			except AttributeError as e:
				continue
	connection.commit()
	cursor.execute('SELECT * FROM homeworktable;') 
	new = cursor.fetchall()
	if new > old:
		return True
	else:
		return False

def select_homework(day=1) -> str:
	"""
	This function collect day(1 - tommorow, 0 - today, -1 - yesterday) or user selected day and return homework for this day
	"""
	
	def select(day, month, year) -> list:
		cursor.execute(
				'SELECT lesson, homework FROM homeworktable WHERE daynum=%s and daymonth=%s and dayYear=%s;',
				(day, month, year)
			)
		return cursor.fetchall()

	if len(str(day)) == 0:
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
			homework = select()
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
			
	d = date.strftime('%d.%m.%Y')
	a = f'Домаха на _{d}_:\n' + '\n'.join(map(lambda x: f'***{x[0]}***:  {x[1]}', homework))
	return a