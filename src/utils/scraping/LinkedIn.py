import json
import requests
import urllib.parse
from src.utils.scraping import (
    LINKEDIN_HEADERS as headers,
    LINKEDIN_PAYLOAD as payload,
    LIX_BASE_URL as base_url,
)


class LinkedIn:
    # Used to get user information displayed on the profile page of the user.
    # Username used here is the handle LinkedIn uses to identify the user publicly
    # It can be found from the link on the user profile
    # i.e alfie-lambert
    def getLinkedInProfile(self, username):
        url = f"{base_url}/person?profile_link=https://linkedin.com/in/{username}"
        response = requests.request("GET", url, headers=headers, data=payload)
        userInfo = self.__handleException(response)
        return userInfo

    # Get user Connections(Followers)
    def getConnections(self, username, count):
        url = f"{base_url}/connections?count={count}&start=0&viewer_id={username}"

        response = requests.request("GET", url, headers=headers, data=payload)
        userConns = self.__handleException(response)
        if "elements" in userConns:
            userConns = userConns["elements"]
        else:
            userConns = []
        return userConns

    # Supposed to fetch email address but doesn't work as expected
    def getEmail(self, username):
        url = f"{base_url}/contact/email/by-linkedin?url=https://linkedin.com/in/{username}"
        response = requests.request("GET", url, headers=headers, data=payload)
        userEmails = self.__handleException(response)
        return userEmails

    # Given the linked in url of a profile this function returns the public linkedin id
    # i.e from https://www.linkedin.com/in/yeabesera-derese-7a9075224 returns yeabesera-derese-7a9075224
    def getUsername(self, link):
        return link.split("/")[-1]

    def getSaleNavId(self, salesNavLink):
        # Extracting user sales navigation link given the user information json
        salesNavLink = salesNavLink.split("lead")[1]

        # Sales navigation Id is used by linkedIn to identify posts made by a user
        salesNavigationID = salesNavLink.split("/")[-1].split(",")[0]
        return salesNavigationID

    # Given the userInfo returned from user profile,
    # this function can return the posts made by a user
    def getUserPosts(self, userInfo):
        salesNavigationID = self.getSaleNavId(userInfo["salesNavLink"])
        postUrl = f"https://www.linkedin.com/search/results/content/?fromMember={salesNavigationID}&origin=SWITCH_SEARCH_VERTICAL&sid=G;z"
        postUrl = urllib.parse.quote(postUrl, safe="")

        url = f"{base_url}/li/linkedin/search/posts?url={postUrl}"

        # print(postUrl) #Uncomment this for debugging
        # print(url)  # Uncomment this for debugging

        response = requests.request("GET", url, headers=headers, data=payload)
        userPosts = self.__handleException(response)

        if "posts" in userPosts:
            userPosts = userPosts["posts"]
        else:
            userPosts = []

        return userPosts

    def __handleException(self, response: requests.Response):
        if response.ok:
            return json.loads(response.text)
        else:
            print(response.text)
            error = json.loads(response.text)
            raise Exception(f"Lix Error: {error['error']['message']}")
