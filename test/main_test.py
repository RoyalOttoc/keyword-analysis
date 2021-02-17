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
from save import save_to_file

# it controls numbers of posts to read, I have set it as 1 for the simple test
NUM_SCROLL = 1


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
    links = soup.find_all("a", {"class": "_5msj"})
    articles = soup.find_all(
        "article", {"class": "_55wo _5rgr _5gh8 async_like"})
    keys = []
    pages = []
    comments = []

    for article in articles:

        if article.find("span", {"class": "_1j-c"}):
            comment = article.find("span", {"class": "_1j-c"}).text
            comment = comment.split()[0]
        else:
            comment = "0"
        comment_dic = {"comment": comment}
        comments.append(comment_dic)

    for link in links:
        # key is an unique link of each post
        key = link.get('href')
        if re.search("m.facebook.com", key):
            keys.append(key)

    for key in keys:
        page_url = (f"{key}")
        browser.get(page_url)
        element = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.ID, "m_story_permalink_view")))
        soup = BeautifulSoup(browser.page_source, "html.parser")
        # the codes below extract all data such as name, post, timeline.

        story_body = soup.find("div", {"class": "story_body_container"})
        name = story_body.find("header").find("strong").text
        if story_body.find("div", {"class": "_3w8y"}):
            post = story_body.find("div", {"class": "_3w8y"}).text
        elif story_body.find("div", {"class": "_5rgt _5nk5"}):
            post = story_body.find("div", {"class": "_5rgt _5nk5"}).text
        else:
            post = ""
        timeline = story_body.find("abbr").text
        if soup.find("div", {"class": "_1g06"}):
            like = soup.find("div", {"class": "_1g06"}).text
        else:
            like = 0

            # comments = soup.find_all("div", {"class": "_2a_i"})
            # commentNum = len(comments)
            # for comment in comments:
            # if comment.find("span", {"class": "_4ayk"}):
            #     num = comment.find("span", {"class": "_4ayk"}).text.split()[1]
            #     commentNum += int(num)

        post_dic = {"name": name, "timeline": timeline,
                    "post": post, "URL": page_url, "like": like}
        pages.append(post_dic)

    # add comments to the existed dictionary

    print("comments:", len(comments))
    print("pages:", len(pages))
    # for i in range(len(comments)):
    #     post_dic = comments[i]
    #     pages[i].update(post_dic)

    return pages


df = pd.read_excel('./URLS/urls.xlsx')
for i in range(len(df)):
    result = extract_pages(df["URL"][i])
    save_to_file(result, df["NAME"][i])
