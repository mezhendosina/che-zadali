#imports 
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from Homework import extract_homework, find_lessons, select_homework
from datetime import datetime, timedelta
import requests, time, os, pytz

token = os.getenv('TELEGRAM_API_KEY') #Telegram api token
def send_message(message):
	r = requests.post(
		f'https://api.telegram.org/bot{token}/sendMessage', #send message 
		data={
			'chat_id': '-1001561236768', 
			'text': message, 
			'disable_notification': True
			} #data for request
	).json()  #send request to telegram api 
	print(r)
	return r
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

	print(time.time() - start_time)
	extract_homework(a)
	l = find_lessons(a)
	if l == True:
			send_message(
				'Похоже появилось расписание\n'+ open('lessons.txt', 'r', encoding='utf-8').read()
			)

if __name__ == '__main__':
	date = datetime.now(pytz.timezone('Asia/Yekaterinburg')) #now time

	old_sgo()	
	times = ['14:29', '14:30', '14:31', '14:32', '14:33', '14:34'] #variable of times
	for i in times:
		if i == date.strftime('%H:%M'):
			r = send_message(select_homework())
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
			break 
