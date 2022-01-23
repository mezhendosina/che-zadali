from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
import os, time, datetime
from Homework import extract_homework


def sgo_login() -> str:
    chrome_options = webdriver.ChromeOptions()
    chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--no-sandbox")

    driver = webdriver.Chrome(os.getenv("CHROMEDRIVER_PATH"), options=chrome_options)
    driver.get("https://sgo.edu-74.ru/")

    time.sleep(2)
    Select(driver.find_element(By.ID, "schools")).select_by_value("89")
    driver.find_element(By.NAME, "UN").send_keys(os.getenv("SGO_LOGIN"))
    driver.find_element(By.NAME, "PW").send_keys(os.getenv("SGO_PASSWORD"))
    driver.find_element(By.XPATH, '//*[@id="message"]/div/div/div[11]/a/span').click()

    try:
        time.sleep(1)
        driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div[2]/div/div[4]/div/div/div/div/button[2]").click()
    except NoSuchElementException:
        pass

    time.sleep(2)
    if datetime.datetime.now().strftime("%w") == "6":
        driver.find_element(By.XPATH, '//*[@id="view"]/div[2]/div/div/div[2]/div[1]/div[2]/div[3]/i').click()
        time.sleep(2)
    homework = driver.page_source
    driver.close()

    return homework


if __name__ == "__main__":
    extract_homework(sgo_login())
