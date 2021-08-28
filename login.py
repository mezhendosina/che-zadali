from selenium import webdriver
from selenium.webdriver.support.ui import Select
from extractHomeworkFromHTML import extractHomework
import os 
import time

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--no-sandbox")
chrome_options.binary_location = os.environ.get('GOOGLE_CHROME_SHIM', None)
driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH", chrome_options=chrome_options)

driver.get('https://sgo.edu-74.ru')
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

c = extractHomework(a)
'''
if c == 'New': 
	
'''