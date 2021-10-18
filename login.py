#imports 
from bs4 import BeautifulSoup
from Homework import extract_homework, select_homework
from telegramBot import send_homework
from selenium.webdriver.support.ui import Select
from selenium import webdriver
import time, os

def sgo() -> None:
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
	time.sleep(3)
	Select(driver.find_element_by_id('schools')).select_by_value("89") #select school

	driver.find_element_by_name('UN').send_keys(os.getenv('SGO_LOGIN')) #type login
	driver.find_element_by_name('PW').send_keys(os.getenv('SGO_PASSWORD')) #type password
	driver.find_element_by_xpath('//*[@id="message"]/div/div/div[11]/a/span').click() #click to login button
	time.sleep(3)

	try:
		driver.find_element_by_xpath(
			'/html/body/div[1]/div/div/div/div/div[4]/div/div/div/div/button[2]'
		).click()#complete security check
		time.sleep(2)
	except:
		time.sleep(2)
	
	
	driver.find_element_by_class_name('icon-off').click()
	time.sleep(1)
	a = driver.page_source #save page source
	soup = BeautifulSoup(a, features='lxml')

	homework = extract_homework(a)
	driver.close() #close driver

	print(time.time() - start_time, homework)
	if homework == True:
		send_homework(select_homework(new=True), '-1001503742992', False)

if __name__ == '__main__':
	sgo()

