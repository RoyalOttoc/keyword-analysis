import requests
import json
from bs4 import BeautifulSoup
from time import sleep
from test import PAGE_RESULT


URL = "https://m.facebook.com/groups/113689859394278"


def get_keys():
    facebook_result = requests.get(URL)
    soup = BeautifulSoup(facebook_result.content, "html.parser")
    links = soup.select('div[data-ft*="mf_story_key"]')
    keys = []
    for link in links:
        data = json.loads(link['data-ft'])
        key = data.get("mf_story_key")
        keys.append(int(key))
    return keys


def extract_message(keys):

    pages = []
    for key in keys:
        page_url = (f"{URL}/permalink/{key}")
        result = requests.get(page_url)
        soup = BeautifulSoup(result.content, "html.parser")
        story_view = soup.find("div", {"id": "m_story_permalink_view"})
        story_body = story_view.find("div").find("div").find("div")
        name = story_body.select_one("div:nth-of-type(1)").find("strong").text
        timeline = story_view.find("abbr").text
        post = story_body.select_one("div:nth-of-type(2)").text
        post_dic = {"name": name, "timeline": timeline,
                    "post": post, "URL": page_url}
        pages.append(post_dic)
    print(pages)


getKey = get_keys()
extract_message(getKey)
