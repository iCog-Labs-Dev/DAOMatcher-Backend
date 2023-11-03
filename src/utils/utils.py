import requests
from random import choice
from src.extensions import socketio
from src.globals import USERS, Sessions
from string import ascii_letters, digits
from src.utils.serverLogic.ScoreUsers import ScoreUsers


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
    print("Set Current User: ", scoreUsers.user_session)
    print("Recieved data: ", jsonRequest)
    return userId != None, CurrentUser


def validate_data(jsonRequest):
    query = jsonRequest.get("query")
    user_list = jsonRequest.get("user_list")
    user_limit = jsonRequest.get("user_limit")
    depth = jsonRequest.get("depth")

    return all([query, user_list, user_limit, depth])


def process_users(user_list, query, user_limit, depth, userId, CurrentUser):
    try:
        scoreUsers = Sessions.get(userId)
        result = scoreUsers.scour(user_list, query, user_limit, depth)
        users = []
        for r in result:
            score, handle, userInfo = r
            users.append(
                {
                    "id": userInfo["id"],
                    "username": userInfo["username"],
                    "name": userInfo["name"],
                    "score": score,
                    "handle": handle,
                    "image": userInfo["image"],
                }
            )
        print(f"result: {users}")
        data = {"result": users}
        socketio.emit("get_users", data, room=CurrentUser)
        print("No results found: ", result)
        return
    except requests.exceptions.RequestException as e:
        response = e.response
        if response != None:
            error = e.response.json()["error"]
            print("error from RequestException: ", error)
            socketio.emit(
                "something_went_wrong",
                {"message": str(error), "status": 502},
                room=CurrentUser,
            )
        else:
            print("Error from ResponseException but no error reported")
            socketio.emit(
                "something_went_wrong",
                {"message": "The LLM server isn't responding", "status": 503},
                room=CurrentUser,
            )
        return
    except Exception as e:
        print(f"\033[91;1m{e}.\033[0m\n")
        socketio.emit(
            "something_went_wrong",
            {"message": "Internal server error"},
            room=CurrentUser,
        )
        return
