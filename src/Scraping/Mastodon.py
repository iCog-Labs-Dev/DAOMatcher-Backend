import requests
from bs4 import BeautifulSoup
from src.Scraping import MASTEDON_BASE_URL


class Mastodon:
    def extractText(self, html):
        soup = BeautifulSoup(html)
        return soup.getText()

    # These function specific to Mastodon Scraping

    def getProfile(self, server, acc):
        BASE_URL = MASTEDON_BASE_URL.format(server=server)
        try:
            response = requests.get(f"{BASE_URL}/lookup?acct={acc}")
            response.raise_for_status()
            return response.json()
        except:
            return False

    def getFollowers(self, server, id):
        BASE_URL = MASTEDON_BASE_URL.format(server=server)

        response2 = requests.get(f"{BASE_URL}/{id}/following")
        response2.raise_for_status()
        return response2.json()

    def getContent(self, server, id):
        BASE_URL = MASTEDON_BASE_URL.format(server=server)

        response = requests.get(f"{BASE_URL}/{id}/statuses?exclude_replies=true")
        response.raise_for_status()

        return response.json()
