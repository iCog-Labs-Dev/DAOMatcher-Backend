import requests


def getProfile(server, acc):
    try:
        response = requests.get(f"https://{server}/api/v1/accounts/lookup?acct={acc}")
        response.raise_for_status()
        return response.json()
    except:
        return False


def getFollowers(server, id):
    # response = requests.get(f'https://{server}/api/v1/accounts/{id}/followers')
    response2 = requests.get(f"https://{server}/api/v1/accounts/{id}/following")
    # response.raise_for_status()
    response2.raise_for_status()
    # return response.json() + response2.json()
    return response2.json()


def getContent(server, id):
    response = requests.get(
        f"https://{server}/api/v1/accounts/{id}/statuses?exclude_replies=true"
    )
    response.raise_for_status()
    return response.json()


from bs4 import BeautifulSoup


def extractText(html):
    soup = BeautifulSoup(html)
    return soup.getText()


def format_prompt(query, content):
    return """
### query:
{query}

### Posts:
{content}
""".format(
        content=content, query=query
    )


def generate_search(query, content):
    prompt = format_prompt(query, content)
    generated_text = generate(prompt)
    parsed_text = parse_text(generated_text)

    return parsed_text


from collections import *
from heapq import *

user_heap = []


def store_items(item, limit):
    if len(user_heap) == limit:
        heappushpop(user_heap, item)
    else:
        heappush(user_heap, item)


def scour(starting_users, query, user_limit):
    accounts = deque(starting_users)

    visited = set()
    results = []
    count = 0

    while accounts and count < Limit:
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
            store_items(int((generate_search(query, content), account)), user_limit)

            for follower in getFollowers(server, id):
                username = follower["acct"]
                if "@" in username:
                    username = "@" + username
                else:
                    username = "@" + username + "@" + server
                if username not in visited:
                    accounts.append(username)
                    visited.add(username)
            print(count)
            count += 1

    return user_heap
