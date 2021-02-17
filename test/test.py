from math import ceil
import requests
import time
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
# username and password needed to login in secrets file
from secrets import USERNAME, PASSWORD

LOGIN_URL = 'https://www.facebook.com/login'

REQUEST_URL = f'https://m.facebook.com/groups/113689859394278'
# it controls numbers of acticles to read
NUM_SCROLL = 1

browser = webdriver.Chrome(ChromeDriverManager().install())
browser.get(LOGIN_URL)
username = browser.find_element_by_id("email")
password = browser.find_element_by_id("pass")
submit = browser.find_element_by_id("loginbutton")
username.send_keys(USERNAME)
password.send_keys(PASSWORD)
submit.click()
time.sleep(3)
browser.get(REQUEST_URL)
time.sleep(3)
for i in range(1, NUM_SCROLL):
    browser.execute_script("window.scrollTo(0, document.body.scrollHeight)")
    time.sleep(3)

PAGE_RESULT = browser.page_source
