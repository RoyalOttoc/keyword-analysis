import time
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
# username and password needed to login in secrets file
from secrets import USERNAME, PASSWORD

LOGIN_URL = 'https://www.facebook.com/login'

browser = webdriver.Chrome(ChromeDriverManager().install())
browser.get(LOGIN_URL)
username = browser.find_element_by_id("email")
password = browser.find_element_by_id("pass")
submit = browser.find_element_by_id("loginbutton")
username.send_keys(USERNAME)
password.send_keys(PASSWORD)
submit.click()
time.sleep(3)
