from datetime import datetime, timezone, timedelta
from decouple import config
from random import choice
from string import ascii_letters, digits

import jwt

from src.controllers.user import get_user_by_id
from src.globals import USERS, Sessions
from src.models.user import User


def generate_random_string(length=8):
    characters = ascii_letters + digits
    return "".join(choice(characters) for _ in range(length))


def generate_refresh_token(user: User):
    payload = {
        "sub": user.id,
        "iat": datetime.now(timezone.utc),
        "exp": datetime.now(timezone.utc)
        + timedelta(days=int(config("REFRESH_TOKEN_EXPIRY_IN_DAYS"))),
    }
    return jwt.encode(payload, config("SECRET_KEY"), algorithm="HS256")


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


def get_user_from_token(token):
    data = jwt.decode(token, config("SECRET_KEY"), algorithms=["HS256"])
    current_user = get_user_by_id(data.get("user_id")).json.get("data")
    return current_user
