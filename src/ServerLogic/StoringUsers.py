from collections import *
from heapq import *
from ..LLM.LLMMethods import *
from ..ServerLogic.ScrapingMethods import *

user_heap = []

def store_items(item, limit):
    if len(user_heap) == limit:
        heappushpop(user_heap, item)
    else:
        heappush(user_heap, item)


def scour(starting_users, query, user_limit):
    accounts = deque(starting_users)

    visited = set()
    count = 0

    while accounts and count < user_limit:
        account = accounts.popleft()
        _, acc, server = account.split("@")
        profile = getProfile(server, acc)
        if profile:
            id = profile["id"]
            content = []
            # print(id)
            if "note" in profile:
                content.append(extractText(profile["note"]))
                # print(content[-1])
            for c in getContent(server, id):
                if "content" in c and c["content"]:
                    content.append(extractText(c["content"]))
                    # print(content[-1])
            content = "\n\n------------------\n".join(content)
            # print(content)
            score = generate_search(query, content)["response"]
            user = {
                "id": profile["id"],
                "name": profile["display_name"],
                "username": profile["username"],
            }
            store_items(((int(score), account, user)), user_limit)


            for follower in getFollowers(server, id):
                username = follower["acct"]
                if "@" in username:
                    username = "@" + username
                else:
                    username = "@" + username + "@" + server
                if username not in visited:
                    accounts.append(username)
                    visited.add(username)
            # print(count)
            count += 1

    return user_heap
