from collections import *
from heapq import *
from ..LLM.LLMMethods import *
from .MastodonScraping import *
from .LinkedInScraping import * 

user_heap = []

def store_items(item, limit):
    if len(user_heap) == limit:
        heappushpop(user_heap, item)
    else:
        heappush(user_heap, item)
#Returns Mastodon user content and user in a dictionary of keys id, name, username
def get_mastodon_user(acc, server):
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
        user = {
                "id": profile["id"],
                "name": profile["display_name"],
                "username": profile["username"],
            }
        # print(content)
        return content, user

#Returns LinkedIn user content and user in a dictionary of keys id, name, username
def get_linkedIn_user(username):
    
    profile = getLinkedInProfile(username)
    
    if profile:
        
        content = []
        
        if "aboutSummaryText" in profile and profile["aboutSummaryText"]:
            content.append(profile["aboutSummaryText"])
        
        for p in getUserPosts(profile):
            if "text" in p and p["text"]:
                content.append(p["text"])
                
        content = "\n\n------------------\n".join(content)
        saleNavId = getSaleNavId(profile["salesNavLink"])
        username  = getUsername(profile["link"])
        
        user ={
            "id": saleNavId,
            "name": profile["name"],
            "username": username
        }
        
        return content, user
        
    
    
    
    
def scour(starting_users, query, user_limit):
    accounts = deque(starting_users)

    visited = set()
    count = 0

    while accounts and count < user_limit:
        account = accounts.popleft()
        if "@" in account: # If it contains @ it is mastodon otherwise it is LinkedIn URL
            _, acc, server = account.split("@")
            content, user = get_mastodon_user(acc, server)
        else:
            pass
        if user:
            score = generate_search(query, content)["response"]
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
