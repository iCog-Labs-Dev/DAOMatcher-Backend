from collections import *
from heapq import *
import requests
from src.ServerLogic import mastodon, linkedIn, llm_server


class StoreUsers:
    def __store_items(self, item, limit, user_heap):
        if len(user_heap) == limit:
            heappushpop(user_heap, item)
        else:
            heappush(user_heap, item)

    # Returns Mastodon user content and user in a dictionary of keys id, name, username
    def __get_mastodon_user(self, acc, server):
        profile = mastodon.getProfile(server, acc)
        if profile:
            content = []
            # print(id)
            if "note" in profile:
                content.append(mastodon.extractText(profile["note"]))
                # print(content[-1])
            for c in mastodon.getContent(server, profile["id"]):
                if "content" in c and c["content"]:
                    content.append(mastodon.extractText(c["content"]))
                    # print(content[-1])
            content = "\n\n------------------\n".join(content)
            user = {
                "id": profile["id"],
                "name": profile["display_name"],
                "username": profile["username"],
            }
            # print(content)
            return content, user
        return None, None

    # Returns LinkedIn user content and user in a dictionary of keys id, name, username
    def __get_linkedIn_user(self, username):
        profile = linkedIn.getLinkedInProfile(username)

        if profile:
            content = []

            if "aboutSummaryText" in profile and profile["aboutSummaryText"]:
                content.append(profile["aboutSummaryText"])

            for p in linkedIn.getUserPosts(profile):
                if "text" in p and p["text"]:
                    content.append(p["text"])

            content = "\n\n------------------\n".join(content)
            saleNavId = linkedIn.getSaleNavId(profile["salesNavLink"])
            username = linkedIn.getUsername(profile["link"])

            user = {"id": saleNavId, "name": profile["name"], "username": username}

            return content, user
        return None, None

    def scour(self, starting_users, query, user_limit):
        user_heap = []

        accounts = deque(starting_users)

        visited = set()
        count = 0

        while accounts and count < user_limit:
            account = accounts.popleft()
            if (
                "@" in account
            ):  # If it contains @ it is mastodon otherwise it is LinkedIn URL
                _, acc, server = account.split("@")
                content, user = self.__get_mastodon_user(acc, server)

                # If there is no user found, no point in excuting the rest of the code
                if not user:
                    continue

                # Get mastodon followers
                for follower in mastodon.getFollowers(server, user["id"]):
                    username = follower["acct"]
                    if "@" in username:
                        username = "@" + username
                    else:
                        username = "@" + username + "@" + server
                    if username not in visited:
                        accounts.append(username)
                        visited.add(username)
            else:
                content, user = self.__get_linkedIn_user(account)

                # Get followers for linkedIn
                for follower in linkedIn.getConnections(account, 1000):
                    username = follower["publicIdentifier"]
                    if username not in visited:
                        accounts.append(username)
                        visited.add(username)

            if user:
                try:
                    score = llm_server.generate_search(query, content)["response"]
                    self.__store_items(
                        ((int(score), account, user)), user_limit, user_heap
                    )
                    # print(count)
                    count += 1
                except requests.exceptions.RequestException as e:
                    raise e
                except Exception as e:
                    raise Exception("Error encountered on storing the scores")

        return user_heap
