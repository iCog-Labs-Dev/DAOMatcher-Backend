import requests
from bs4 import BeautifulSoup
from src.Scraping import MASTEDON_BASE_URL


class Mastodon:
    def extractText(self, html):
        soup = BeautifulSoup(html)
        return soup.getText()

    # These function specific to Mastodon Scraping

    def getProfile(self, server, acc):
        # BASE_URL = MASTEDON_BASE_URL.format(server=server)
        BASE_URL = MASTEDON_BASE_URL
        acc = "@".join([acc, server])
        try:
            print(f"{BASE_URL}/lookup?acct=@{acc}")
            response = requests.get(f"{BASE_URL}/lookup?acct=@{acc}")
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"\033[91;1m{e}.\033[0m\n")
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
