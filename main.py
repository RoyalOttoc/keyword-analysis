import pandas as pd
import requests
import json
import re
import time
from seleniumLogin import browser
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from bs4 import BeautifulSoup
from time import sleep
from save import save_to_file, add_to_file

# it controls numbers of posts to read, I have set it as 1 for the simple test
NUM_SCROLL = 5

def extract_pages(REQUEST_URL):
    '''
    1) go to an URL by the order in an Excel sheet
    2) go to each post and extract all data from the post
    '''
    browser.get(REQUEST_URL)
    time.sleep(3)
    # NUM_SCROLL can control how many posts to be extracted
    for i in range(1, NUM_SCROLL):
        browser.execute_script(
            "window.scrollTo(0, document.body.scrollHeight)")
        time.sleep(3)

    soup = BeautifulSoup(browser.page_source, "html.parser")
    articles = soup.find_all(
        "article", {"class": "_55wo _5rgr _5gh8 async_like"})

    pages = []

    for article in articles:
        """it extracts name, timeline, post, number of likes and comments and url of each post from each article"""
        try:
            href = article.find("a", {"class": "_5msj"}).get('href')
            if "https://m.facebook.com" not in href:
                link = "https://m.facebook.com" + href
            else:
                link = href

            header = article.find("div", {"class": "_4g34"})
            name = header.find("strong").text
            timeline = header.find("abbr").text

            if article.find("div", {"class": "_1g06"}):
                like = int(article.find("div", {"class": "_1g06"}).text)
            else:
                like = 0
            if article.find("span", {"class": "_1j-c"}):
                comment = article.find("span", {"class": "_1j-c"}).text
                comment = int(comment.split()[0])
            else:
                comment = 0

            postPart = article.find("div", {"class": "_5rgt _5nk5 _5msi"})

            if postPart.find("span", {"class": "text_exposed_show"}):
                browser.get(link)
                element = WebDriverWait(browser, 10).until(
                    EC.presence_of_element_located((By.ID, "m_story_permalink_view")))
                soup = BeautifulSoup(browser.page_source, "html.parser")
                story_body = soup.find(
                    "div", {"class": "story_body_container"})
                if story_body.find("div", {"class": "_3w8y"}):
                    post = story_body.find("div", {"class": "_3w8y"}).text
                elif story_body.find("div", {"class": "_5rgt _5nk5"}):
                    post = story_body.find(
                        "div", {"class": "_5rgt _5nk5"}).text
                else:
                    post = ""
            else:
                post = postPart.text

        except Exception as e:
            print(e)

        post_dic = {"name": name, "timeline": timeline,
                    "post": post, "like": like, "comment": comment, "URL": link}
        pages.append(post_dic)

    return pages


df = pd.read_excel('./URLS/urls.xlsx')
for i in range(len(df)):
    """the result is saved as a list having dictionaries, and it is saved as csv file """
    result = extract_pages(df["URL"][i])
    save_to_file(result, df["NAME"][i])

    # It adds new posts and remove duplications
    # add_to_file(result, df["NAME"][i])
