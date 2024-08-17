import json
import requests
import urllib.parse
from src.utils.scraping import (
    TWITTER_HEADERS as headers,
    TWITTER_PAYLOAD as payload,
    TWITTER_BASE_URL as base_url,
    TWITTER_API_KEY as api_key,
    TWITTER_API_SECRET as api_secret,
)


class Twitter:
    # Used to get user information displayed on the profile page of the user.
    # Username used here is the username used in twitter.
    auth = (api_key, api_secret)

    # Used to cache user tweets for the get related users
    RELATED_USERS= []
    def getTwitterProfile(self, username):
        url = f"{base_url}/users/by/username/{username}?user.fields=created_at,description,profile_image_url,public_metrics&expansions=pinned_tweet_id,most_recent_tweet_id"
        response = requests.request("GET", url, headers=headers, data=payload)
        # print(headers)
        data = self.__handleException(response)
        userInfo = data.get("data", None)
        return userInfo

    # Get user Followers
    def getRelatedUsers(self, count):

        relatedUsers= Twitter.RELATED_USERS[:count] if len(Twitter.RELATED_USERS) > count else Twitter.RELATED_USERS

        return relatedUsers
    # Given the userInfo returned from user profile,
    # this function can return the posts made by a user
    def getUserPosts(self, id, count=5):
        url = f"{base_url}/users/{id}/tweets?max_results={count}&expansions=referenced_tweets.id.author_id"
        # print(url)

        response = requests.request("GET", url, headers=headers, data=payload)
        userPosts = self.__handleException(response)
        userPosts = response.json().get("data", {})
        Twitter.RELATED_USERS= response.json().get("includes", {}).get("users", [])
        Twitter.RELATED_USERS = [user for user in Twitter.RELATED_USERS if user["id"] != id]

        return userPosts

    def __handleException(self, response: requests.Response):
        if response.ok:
            return response.json()
        else:
            # print(response.text)
            error = response.text
            raise Exception(f"Error: {error}")
