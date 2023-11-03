from random import choice
from src.globals import USERS, Sessions
from string import ascii_letters, digits


def generate_random_string(length=8):
    characters = ascii_letters + digits
    return "".join(choice(characters) for _ in range(length))


def set_user_session(jsonRequest):
    userId = jsonRequest.get("userId")

    CurrentUser = USERS.get(userId)
    scoreUsers = Sessions.get(userId)

    if not all([userId, CurrentUser, scoreUsers]):
        print(f"\033[91;1mUser session not found.\033[0m\n")
        return False, None

    scoreUsers.user_session = CurrentUser
    print(f"\033[92mSet Current User: {scoreUsers.user_session}\033[0m")
    return userId != None, CurrentUser


def validate_data(jsonRequest):
    query = jsonRequest.get("query")
    user_list = jsonRequest.get("user_list")
    user_limit = jsonRequest.get("user_limit")
    depth = jsonRequest.get("depth")

    return all([query, user_list, user_limit, depth])
