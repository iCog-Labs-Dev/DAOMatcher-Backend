# These function specific to Mastodon Scraping

import requests
from bs4 import BeautifulSoup


def getProfile(server, acc):
    try:
        response = requests.get(f"https://{server}/api/v1/accounts/lookup?acct={acc}")
        response.raise_for_status()
        return response.json()
    except:
        return False


def getFollowers(server, id):
    response2 = requests.get(f"https://{server}/api/v1/accounts/{id}/following")
    response2.raise_for_status()
    return response2.json()


def getContent(server, id):
    response = requests.get(
        f"https://{server}/api/v1/accounts/{id}/statuses?exclude_replies=true"
    )
    response.raise_for_status()
    return response.json()


def extractText(html):
    soup = BeautifulSoup(html)
    return soup.getText()
