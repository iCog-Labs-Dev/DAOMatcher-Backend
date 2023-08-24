import requests
from bs4 import BeautifulSoup

MASTEDON_BASE_URL = """https://{server}/api/v1/accounts"""


def extractText(html):
    soup = BeautifulSoup(html)
    return soup.getText()


# These function specific to Mastodon Scraping


def getProfile(server, acc):
    BASE_URL = MASTEDON_BASE_URL.format(server=server)
    try:
        response = requests.get(f"{BASE_URL}/lookup?acct={acc}")
        response.raise_for_status()
        return response.json()
    except:
        return False


def getFollowers(server, id):
    BASE_URL = MASTEDON_BASE_URL.format(server=server)

    response2 = requests.get(f"{BASE_URL}/{id}/following")
    response2.raise_for_status()
    return response2.json()


def getContent(server, id):
    BASE_URL = MASTEDON_BASE_URL.format(server=server)

    response = requests.get(f"{BASE_URL}/{id}/statuses?exclude_replies=true")
    response.raise_for_status()
    return response.json()
