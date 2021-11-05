#imports 
from bs4 import BeautifulSoup
import requests
from Homework import extract_homework, months, select_homework
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium import webdriver
import time, os, json, datetime

def send_homework(message: str, chat_id: str, notification: bool) -> dict:
	token = os.getenv('TELEGRAM_API_TOKEN')
	r1 = requests.post(
		f'https://api.telegram.org/bot{token}/sendMessage', #send message 
		data={
			'chat_id': chat_id, 
			'text': message,
			'parse_mode': 'Markdown',
			'disable_notification': notification
			} #data for request
	).json()  #send request to telegram api 
def sgo() -> None:
	attachments_path = f'{os.getcwd()}\\files\\homework_attachment'
	#add chrome options
	chrome_options = webdriver.ChromeOptions()
	chrome_options.add_argument("--headless")
	chrome_options.add_argument('--disable-gpu')
	chrome_options.add_argument("--remote-debugging-port=9222")
	chrome_options.add_argument("google-chrome")
	chrome_options.add_argument("--no-sandbox")	
	chrome_options.add_experimental_option("prefs", {
		"download.default_directory": f"{attachments_path}\\not_parsed",
		"download.prompt_for_download": False,
		"download.directory_upgrade": True,
		"safebrowsing_for_trusted_sources_enabled": False,
		"safebrowsing.enabled": False
	})
	#chrome_options.binary_location = os.getenv('GOOGLE_CHROME_SHIM')
	
	driver = webdriver.Chrome(
		executable_path=os.getenv("CHROMEDRIVER_PATH"), 
		chrome_options=chrome_options
		) #configurate webdriver

	driver.get("https://sgo.edu-74.ru") #go to sgo.edu-74.ru
	time.sleep(3)
	Select(driver.find_element_by_id('schools')).select_by_value("89") #select school

	driver.find_element(By.NAME, 'UN').send_keys(os.getenv('SGO_LOGIN')) #type login
	driver.find_element(By.NAME, 'PW').send_keys(os.getenv('SGO_PASSWORD')) #type password
	driver.find_element(By.XPATH, '//*[@id="message"]/div/div/div[11]/a/span').click() #click to login button
	time.sleep(3)

	try:
		driver.find_element(
			By.XPATH,
			'/html/body/div[1]/div/div/div/div/div[4]/div/div/div/div/button[2]'
		).click()#complete security check
		time.sleep(2)
	except:
		time.sleep(2)
	
	a = driver.page_source #save page source

	homework = extract_homework(a)
	if homework == True:
		send_homework(select_homework(new=True), '-1001503742992', False)
	if datetime.datetime.now().strftime('%w') == '6':
		driver.find_element(By.CLASS_NAME, 'mdi mdi-arrow-right-bold').click()
		time.sleep(2)
		extract_homework(driver.page_source)
	soup = BeautifulSoup(a, features='lxml')
	schoolJournal = soup.find('div', 'schooljournal_content column')
	dayTable = schoolJournal.find_all('div', class_ = 'day_table')
	
	def left_right_col(day):
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
		if len(str(dayMonth)) == 1:
			dayMonth = f'0{dayMonth}' 
		for a in i.find_all('tr', class_ = 'ng-scope'):
			
			try:
				lesson = a.find('a', class_='subject ng-binding ng-scope').get_text()
				num = num + 1
			except AttributeError:
				print("None")
				continue
			
			try:
				driver.find_element(
					By.XPATH,
					f'//*[@id="view"]/div[2]/div/div/div[2]/div[{col[0]}]/div[{col[1]}]/diary-day/div/div/table[2]/tbody/tr[{num}]/td[3]/div[2]/assign-attachments/div/i'
				).click()
				time.sleep(3)
				try:
					driver.find_element(
						By.XPATH,
						f'//*[@id="view"]/div[2]/div/div/div[2]/div[{col[0]}]/div[{col[1]}]/diary-day/div/div/table[2]/tbody/tr[{num}]/td[3]/div[2]/assign-attachments/div/div/a/span/div'
					).click()
				except:
					print('NOne2')
				soup = BeautifulSoup(driver.page_source, features='lxml')
			except:
				print('None1')
				continue
			
			name_file = soup.find("div", class_="name_file ng-binding").get_text()
			new_file_name = f'{attachments_path}\\{lesson} на {dayNum}.{dayMonth}.{dayYear}({num-1}).{name_file.split(".")[-1]}'
			time.sleep(2)
			try:
				os.rename(
					f'{attachments_path}\\not_parsed\\{name_file}',
					new_file_name
				)
				with open(f'{os.getcwd()}\\files\\list_of_files.json', 'r') as f:
					a = json.loads(f.read())
					x = a['attachments_path'].get(f'{dayNum}.{dayMonth}.{dayYear }')
					try:
						x.append(new_file_name)
						a['attachments_path'].update({f'{dayNum}.{dayMonth}.{dayYear }': x})
					except:
						a['attachments_path'].update({f'{dayNum}.{dayMonth}.{dayYear }': [new_file_name]})

				with open(f'{os.getcwd()}\\files\\list_of_files.json', 'w') as f:
					f.write(str(json.dumps(a)))		
			except FileExistsError:
				print('a')
				os.remove(f'{attachments_path}\\not_parsed\\{name_file}')
	
	driver.find_element(By.XPATH, '/html/body/div[1]/div[1]/ul/li[3]/a').click()
	time.sleep(1)
	soup = BeautifulSoup(driver.page_source, "html.parser")
	driver.find_element(By.ID, soup.find('button', class_='btn btn-primary')['id']).click()
	driver.close() #close driver
	for f in os.listdir(attachments_path):
		i += 1
		if i > 10:
			os.remove(os.path.join(attachments_path, f))
if __name__ == '__main__':
	sgo()

