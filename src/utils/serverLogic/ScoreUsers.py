import requests
from heapq import *
from collections import *
from urllib.parse import urlparse
from src.extensions import socketio
from src.utils.serverLogic import mastodon, linkedIn, llm_server


class ScoreUsers:
    def __init__(self) -> None:
        self.cancel = False
        self.user_session = None

    def __store_items(self, item, limit, user_heap):
        if len(user_heap) == limit:
            heappushpop(user_heap, item)
        else:
            heappush(user_heap, item)

    def __is_link(self, string):
        try:
            parsed_url = urlparse(string)
            return parsed_url.scheme in ["http", "https"] and parsed_url.netloc != ""
        except ValueError:
            return False

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
                    text = mastodon.extractText(c["content"])
                    # Added filter to check if content is only link
                    if not self.__is_link(text):
                        content.append(text)
                    # print(content[-1])
            content = "\n\n------------------\n".join(content)
            # print(f"Profile: {profile}")
            user = {
                "id": profile["id"],
                "name": profile["display_name"],
                "username": profile["username"],
                "image": profile["avatar"],
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

    def scour(self, starting_users, query, user_limit, depth):
        user_heap = []

        accounts = deque(starting_users)

        visited = set()
        count = 0
        self.cancel = False
        print("User from scour: ", self.user_session)

        while (not self.cancel) and accounts and (count < depth):
            account = accounts.popleft()

            # Orgnanized logging for debugging purposes
            print(
                "\033[93;1m{:<15} {:<25} {:<8} {:<10}\033[0m".format(
                    "Processing: ", account, " From: ", len(account)
                )
            )
            try:
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

                    # If there is no user found, no point in excuting the rest of the code
                    if not user:
                        continue

                    # Get followers for linkedIn
                    for follower in linkedIn.getConnections(account, 1000):
                        username = follower["publicIdentifier"]
                        if username not in visited:
                            accounts.append(username)
                            visited.add(username)
            except Exception as e:
                print(f"\033[91;1m{e} In scour.\033[0m\n")
                socketio.emit(f"update", {"error": str(e)}, room=self.user_session)

            if user:
                try:
                    if query and content:
                        score = llm_server.generate_search(query, content)["response"]
                        self.__store_items(
                            ((int(score), account, user)), user_limit, user_heap
                        )
                        # print(count)
                        count += 1
                        socketio.emit(
                            f"update",
                            {"progress": count, "curr_user": account},
                            room=self.user_session,
                        )
                        print("Emitting to: ", self.user_session)
                    else:
                        continue

                except requests.exceptions.RequestException as e:
                    socketio.emit(f"update", {"error": str(e)}, room=self.user_session)
                except Exception as e:
                    socketio.emit(f"update", {"error": str(e)}, room=self.user_session)
                    # raise Exception("Error encountered on storing the scores")
        self.user_session = None
        return user_heap
