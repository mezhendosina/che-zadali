#imports 
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from Homework import extract_homework, select_homework
from datetime import datetime, timedelta
import requests, time, os, pytz

token = os.getenv('TELEGRAM_API_KEY') #Telegram api token
def old_sgo():
	start_time = time.time()
	#add chrome options
	chrome_options = webdriver.ChromeOptions()
	chrome_options.add_argument("--headless")
	chrome_options.add_argument('--disable-gpu')
	chrome_options.add_argument("--remote-debugging-port=9222")
	chrome_options.add_argument("google-chrome")
	chrome_options.add_argument("--no-sandbox")
	chrome_options.binary_location = os.getenv('GOOGLE_CHROME_SHIM')
	driver = webdriver.Chrome(
		executable_path=os.getenv("CHROMEDRIVER_PATH"), 
		chrome_options=chrome_options
		) #configurate webdriver

	driver.get("https://sgo.edu-74.ru") #go to sgo.edu-74.ru
	time.sleep(5)
	Select(driver.find_element_by_id('schools')).select_by_value("89") #select school

	driver.find_element_by_name('UN').send_keys(os.getenv('SGO_LOGIN')) #type login
	driver.find_element_by_name('PW').send_keys(os.getenv('SGO_PASSWORD')) #type password
	driver.find_element_by_xpath('//*[@id="message"]/div/div/div[11]/a/span').click() #click to login button
	time.sleep(5)

	try:
		driver.find_element_by_xpath(
			'/html/body/div[1]/div/div/div/div/div[4]/div/div/div/div/button[2]'
		).click()#complete security check
		time.sleep(2)
	except:
		time.sleep(2)
	a = driver.page_source #save page source
	driver.close() #close driver

	extract_homework(a)
	print(time.time() - start_time)
'''
def new_sgo(weekstart, weekend):
	start_time = time.time()
	url = f'https://sgo.edu-74.ru/webapi/student/diary?studentId=472262&vers=1631092270754&weekEnd={weekend}&weekStart={weekstart}&withLaAssigns=true&yearId=21330'
	headers = {
		'Accept': 'application/json, text/plain, */*',
		'Accept-Encoding': 'gzip, deflate, br',
		'Accept-Language': 'en-RU,en;q=0.9,ru-RU;q=0.8,ru;q=0.7,en-GB;q=0.6,en-US;q=0.5',
		'at': os.getenv('at'),
		'Connection': 'keep-alive',
		'Cookie': 'NSSESSIONID=c3e8906c3e374881a21f704f46ec3846; ESRNSec=ESRNSECR9544=fa7fcd929f07eeef70c3e0641efc37b1-116345453t; TTSLogin=SCID=89&PID=-1&CID=2&SID=1&SFT=2&CN=1&BSP=0; UserLanguage=ru; FUNCTIONALITYTYPE=2; securekey=ODUzMDYyNzU5; ASPSESSIONIDACRSRRSC=LJMDKKCAIKAHGJFBBKKAGCJN',
		'Host': 'sgo.edu-74.ru',
		'Referer': 'https://sgo.edu-74.ru/angular/school/studentdiary/',
		'sec-ch-ua': '"Google Chrome";v="93", " Not;A Brand";v="99", "Chromium";v="93"',
		'sec-ch-ua-mobile': '?0',
		'sec-ch-ua-platform': '"Windows"',
		'Sec-Fetch-Dest': 'empty',
		'Sec-Fetch-Mode': 'cors',
		'Sec-Fetch-Site': 'same-origin',
		'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36'    
	}
	data = f'studentId=472262&vers=1631092270754&weekEnd={weekend}&weekStart={weekstart}&withLaAssigns=true&yearId=21330'
	r = requests.get(url, headers=headers, data=data)
	a = new_extract_homework(r.json())
	if a == 'Error':
		r1 = requests.post(
					f'https://api.telegram.org/bot{token}/sendMessage', #send message 
					data={
						'chat_id': '401311369', 
						'text': 'Error', 
						'disable_notification': True
						} #data for request
				).json()  #send request to telegram api 	
	else:
		r1 = requests.post(
					f'https://api.telegram.org/bot{token}/sendMessage', #send message 
					data={
						'chat_id': '401311369', 
						'text': a, 
						'disable_notification': True
						} #data for request
				).json()  #send request to telegram api 	
	print(time.time() - start_time)
'''
if __name__ == '__main__':
	date = datetime.now(pytz.timezone('Asia/Yekaterinburg')) #now time
	'''
	try:
		monday = date.today() - timedelta(days=date.today().isoweekday() % 7 - 1)
		sunday = datetime(int(monday.strftime('%Y')), int(monday.strftime('%m')), int(monday.strftime('%d'))) + timedelta(days=6)
		new_sgo(monday.strftime('%Y-%m-%d'), sunday.strftime('%Y-m-%d'))
	except:
		old_sgo()
	'''
	old_sgo()	
	times = ['14:29', '14:30', '14:31', '14:32', '14:33', '14:34'] #variable of times
	for i in times:
		if i == date.strftime('%H:%M'):
			r = requests.post(
				f'https://api.telegram.org/bot{token}/sendMessage', #send message 
				data={
					'chat_id': '-1001561236768', 
					'text': select_homework(), 
					'disable_notification': True
					} #data for request
			).json()  #send request to telegram api 
			
			r1 = requests.post(
				f'https://api.telegram.org/bot{token}/pinChatMessage',#pin message 
				data={
					'chat_id': '-1001561236768', 
					'message_id': r['result']['message_id']} #data for request
			).json()#send request to telegram api 
			r3 = requests.post(
				f'https://api.telegram.org/bot{token}/sendMessage', #send message 
				data={
					'chat_id': '401311369', 
					'text': 'домашка отправлена', 
					} #data for request
			)
