from selenium import webdriver
from selenium.webdriver.support.ui import Select
from extractHomeworkFromHTML import extractHomework, selectHomework
from datetime import datetime
import requests, time, os, pytz

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--headless")
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument("--remote-debugging-port=9222")
chrome_options.add_argument("google-chrome")
chrome_options.add_argument("--no-sandbox")
chrome_options.binary_location = os.getenv('GOOGLE_CHROME_SHIM')
driver = webdriver.Chrome(executable_path=os.getenv("CHROMEDRIVER_PATH"), chrome_options=chrome_options)

driver.get("https://sgo.edu-74.ru")
time.sleep(5)
Select(driver.find_element_by_id('schools')).select_by_value("89")

driver.find_element_by_name('UN').send_keys(os.getenv('SGO_LOGIN'))
driver.find_element_by_name('PW').send_keys(os.getenv('SGO_PASSWORD'))
driver.find_element_by_xpath('//*[@id="message"]/div/div/div[11]/a/span').click()
time.sleep(5)

try:
	driver.find_element_by_xpath('/html/body/div[1]/div/div/div/div/div[4]/div/div/div/div/button[2]').click()
	time.sleep(2)
except:
	time.sleep(2)
a = driver.page_source
driver.close()

extractHomework(a)

times = ['14:29', '14:30', '14:31', '14:32', '14:33', '14:34']
date = datetime.now(pytz.timezone('Asia/Yekaterinburg'))
token = os.getenv('TELEGRAM_API_KEY')
for i in times:
	if times == date.strftime('%H:%M'):
		r = requests.post(
			f'https://api.telegram.org/bot{token}/sendMessage',
			data={'chat_id': '-1001561236768', 'text': selectHomework(), 'disable_notification': True}
		).json()
		
		r1 = requests.post(
			f'https://api.telegram.org/bot{token}/pinChatMessage',
			data={'chat_id': '-1001561236768', 'message_id': r['result']['message_id']}
		).json()

