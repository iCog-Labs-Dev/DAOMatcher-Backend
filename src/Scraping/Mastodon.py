import requests
from bs4 import BeautifulSoup
from src.Scraping import MASTEDON_BASE_URL


class Mastodon:
    def extractText(self, html):
        soup = BeautifulSoup(html)
        return soup.getText()

    # These function specific to Mastodon Scraping

    def getProfile(self, server, acc, webfinger=False, searchServer="mastodon.social"):
        # Change the searching server if webfinger is enabled
        BASE_URL = MASTEDON_BASE_URL.format(
            server=searchServer if webfinger else server
        )
        try:
            # Setting the search param based on the type of search
            # When webfinger is True, mastodon will search for the user's server from the current server itself. If not it will just try to find the user itself from the server
            acc = "@" + "@".join([acc, server]) if webfinger else acc
            print(f"{BASE_URL}/lookup?acct={acc}")
            response = requests.get(f"{BASE_URL}/lookup?acct={acc}")
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as errh:
            print(f"\033[91;1m{errh}.\033[0m\n")
            print(f"\033[94;1mRetrying with a different Server...\033[0m\n")
            if (
                (errh.response != None)
                and (errh.response.status_code == 404)
                and (not webfinger)
            ):
                return self.getProfile(
                    server=server,
                    acc=acc,
                    webfinger=True,
                    searchServer="mastodon.social",
                )
            return False
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
