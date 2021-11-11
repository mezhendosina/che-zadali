#imports 
import time, os, datetime, requests
from yadisk import YaDisk, exceptions
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from Homework import extract_homework, months, select_homework

def send_homework(message: list, chat_id: str, notification: bool) -> dict:
	token = os.getenv('TELEGRAM_API_TOKEN')
	r1 = requests.post(
		f'https://api.telegram.org/bot{token}/sendMessage', #send message 
		data={
			'chat_id': chat_id, 
			'text': message[0],
			'parse_mode': 'html',
			'disable_notification': notification
			} #data for request
	).json()  #send request to telegram api 
	if message[1] == None:
		return r1
	r2 = requests.post(
		f'https://api.telegram.org/bot{token}/sendMediaGroup', #send message 
		data={
			'chat_id': chat_id, 
			'media': [{'type': 'document', 'media': a} for a in message[1]]
			} #data for request
	).json()  #send request to telegram api
	return r1, r2

def wait(driver: str, elem: str, find_by: str, click:bool = True, select:bool = False, select_id=False) -> None:
	i = 0
	while True:
		if i > 1404:
			raise TimeoutError('Error when wait element')
		try:
			if click == True:
				driver.find_element(find_by, elem).click()
			elif select == True:
				assert select_id != False
				Select(driver.find_element(find_by, elem)).select_by_value(select_id)
			elif click == False:
				driver.find_element(find_by, elem)
			break
		except NoSuchElementException:
			i = i+1
			continue		
	
def sgo() -> None:
	#gloval var
	y = YaDisk(os.getenv("YDISK_LOGIN"), os.getenv("YDISK_PASSWORD"), os.getenv('YDISK_TOKEN'))
	attachments_path = f'{os.getcwd()}/files/homework_attachment'
	#add chrome options
	chrome_options = webdriver.ChromeOptions()
	chrome_options.add_argument("--headless")
	chrome_options.add_argument('--disable-gpu')
	chrome_options.add_argument("--remote-debugging-port=9222")
	chrome_options.add_argument("google-chrome")
	chrome_options.add_argument("--no-sandbox")	
	chrome_options.add_experimental_option("prefs", {
		"download.default_directory": attachments_path,
		"download.prompt_for_download": False,
		"download.directory_upgrade": True,
		"safebrowsing_for_trusted_sources_enabled": False,
		"safebrowsing.enabled": False
	})
	chrome_options.binary_location = os.getenv('GOOGLE_CHROME_SHIM')
	
	driver = webdriver.Chrome(
		executable_path=os.getenv("CHROMEDRIVER_PATH"), 
		chrome_options=chrome_options
		) #configurate webdriver
	#login
	driver.get("https://sgo.edu-74.ru") #go to sgo.edu-74.ru
	wait(driver, 'schools', By.ID, False, True, "89") #select school

	driver.find_element(By.NAME, 'UN').send_keys(os.getenv('SGO_LOGIN')) #type login
	driver.find_element(By.NAME, 'PW').send_keys(os.getenv('SGO_PASSWORD')) #type password
	driver.find_element(By.XPATH, '//*[@id="message"]/div/div/div[11]/a/span').click() #click to login button

	try:
		wait(driver, '/html/body/div[1]/div/div/div/div/div[4]/div/div/div/div/button[2]', By.XPATH) #complete security check
	finally:
		time.sleep(2)
	
	a = driver.page_source #save page source
	
	#get homework
	homework, i = extract_homework(a), 0
	for i in homework:
		if i == True:
			send_homework(select_homework(0, new=True), '-1001503742992', False)
		i+1
	#send homework
	if datetime.datetime.now().strftime('%w') == '6':
		driver.find_element(By.CLASS_NAME, 'mdi mdi-arrow-right-bold').click()
		time.sleep(2)
		extract_homework(driver.page_source)

	#download attachments
	soup = BeautifulSoup(a, features='lxml')
	schoolJournal = soup.find('div', 'schooljournal_content column')
	dayTable = schoolJournal.find_all('div', class_ = 'day_table')

	def left_right_col(day:str) -> int:
		return {
			'Пн': [2, 1], 'Вт': [2, 2], 'Ср': [2, 3],
			'Чт': [3, 1], 'Пт': [3, 2], 'Сб': [3, 3]
		}[day]
	
	for i in dayTable:
		num, day = 1, i.find('span', 'ng-binding').get_text()
		dayNum = int(day.split(' ')[1])
		dayMonth = months(day.split(' ')[2])
		dayYear = int(day.split(' ')[3])
		col = left_right_col(day.split(",")[0])
		
		if len(str(dayNum)) == 1:
			dayNum = f'0{dayNum}'
		elif len(str(dayMonth)) == 1:
			dayMonth = f'0{dayMonth}' 
		
		for a in i.find_all('tr', class_ = 'ng-scope'):
			try:
				lesson = a.find('a', class_='subject ng-binding ng-scope').get_text()
				num = num + 1
			except AttributeError:
				continue
			
			try:
				driver.find_element(
					By.XPATH,
					f'//*[@id="view"]/div[2]/div/div/div[2]/div[{col[0]}]/div[{col[1]}]/diary-day/div/div/table[2]/tbody/tr[{num}]/td[3]/div[2]/assign-attachments/div/i'
				).click()
				wait(
					driver, 
					f'//*[@id="view"]/div[2]/div/div/div[2]/div[{col[0]}]/div[{col[1]}]/diary-day/div/div/table[2]/tbody/tr[{num}]/td[3]/div[2]/assign-attachments/div/div/a/span/div', 
					By.XPATH)
				soup = BeautifulSoup(driver.page_source, features='lxml')
			except NoSuchElementException:
				continue
			
			name_file = soup.find("div", class_="name_file ng-binding").get_text()
			time.sleep(2)
	
	#rename file and upload to Yandex.Disk		
			try:
				y.upload(f'{attachments_path}/{name_file}', f'/che-zadali_files/{dayNum}.{dayMonth}.{dayYear}/{lesson} на {dayNum}.{dayMonth}.{dayYear}({num-1}).{name_file.split(".")[-1]}')	
			except exceptions.ParentNotFoundError:
				y.mkdir(f'/che-zadali_files/{dayNum}.{dayMonth}.{dayYear}')
				y.upload(f'{attachments_path}/{name_file}', f'/che-zadali_files/{dayNum}.{dayMonth}.{dayYear}/{lesson} на {dayNum}.{dayMonth}.{dayYear}({num-1}).{name_file.split(".")[-1]}')
			except exceptions.PathExistsError:
				None	
			driver.find_element(
					By.XPATH,
					f'//*[@id="view"]/div[2]/div/div/div[2]/div[{col[0]}]/div[{col[1]}]/diary-day/div/div/table[2]/tbody/tr[{num}]/td[3]/div[2]/assign-attachments/div/i'
				).click()
	
	#exit from sgo.edu-74.ru
	driver.find_element(By.XPATH, '/html/body/div[1]/div[1]/ul/li[3]/a').click()
	time.sleep(1)
	soup = BeautifulSoup(driver.page_source, "html.parser")
	driver.find_element(By.ID, soup.find('button', class_='btn btn-primary')['id']).click()
	driver.close() #close driver
if __name__ == '__main__':
	sgo()