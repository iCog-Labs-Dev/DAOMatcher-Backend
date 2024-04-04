from random import choice
from string import ascii_letters, digits

from src.globals import USERS, Sessions


def generate_random_string(length=8):
    characters = ascii_letters + digits
    return "".join(choice(characters) for _ in range(length))


def set_user_session(user_id: str, jsonRequest):
    user_session = USERS[user_id]
    scoreUsers = Sessions.get(user_id)

    if not all([user_id, scoreUsers]):
        print(f"\033[91;1mUser session not found.\033[0m\n")
        return False, None

    scoreUsers.user_session = user_session
    print(f"\033[92mSet Current User: {scoreUsers.user_session}\033[0m")
    return user_session != None


def validate_data(jsonRequest):
    query = jsonRequest.get("query")
    user_list = jsonRequest.get("user_list")
    user_limit = jsonRequest.get("user_limit")
    depth = jsonRequest.get("depth")

    return all([query, user_list, user_limit, depth])


def emitData(socket, event, data=None, room=None):
    if room is None:
        print(f"\033[91;1mRoom is not set.\033[0m\n")
        return
    socket.emit(event, data=data, room=room)
