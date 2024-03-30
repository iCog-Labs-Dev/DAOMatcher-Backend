import requests

from flask import request

from src.extensions import socketio
from src.globals import USERS, Sessions
from src.utils.serverLogic.ScoreUsers import ScoreUsers
from src.utils.utils import (
    emitData,
    generate_random_string,
    set_user_session,
    validate_data,
)


def connect():
    userId = generate_random_string()
    USERS[userId] = request.sid
    # print("users: ", USERS)
    # print("User connected with userId: ", userId)

    scoreUsers = ScoreUsers()
    Sessions[userId] = scoreUsers
    emitData(socketio, "set_cookie", userId, room=request.sid)


def get_users(data):
    jsonRequest = data
    print(f"\033[94mRecieved Data: {jsonRequest}\033[0m")
    sessionIsSet, CurrentUser = set_user_session(data)
    valid = validate_data(data)
    if not sessionIsSet:
        print(f"\033[91merror emitted\033[0m")
        return
    if not valid:
        if CurrentUser:
            emitData(
                socketio,
                "something_went_wrong",
                {
                    "message": "Error data sending",
                    "status": 400,
                },
                room=CurrentUser,
            )
        print(f"\033[91merror emitted\033[0m")
        return

    print(f"\033[94mCurrentUser:  {CurrentUser}\033[0m")
    query = jsonRequest.get("query")
    user_list = jsonRequest.get("user_list")
    user_limit = jsonRequest.get("user_limit")
    depth = jsonRequest.get("depth")
    userId = jsonRequest.get("userId")

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
        print(f"\033[94mTotal results: {len(users)} \033[0m")
        if users:
            data = {"result": users}
            if CurrentUser:
                emitData(socketio, "get_users", data, room=CurrentUser)
                return
            else:
                print(f"\033[91mNo session found: {result}\033[0m")
                return

        print(f"\033[91mNo results found: {result}\033[0m")
        return

    except requests.exceptions.RequestException as e:
        response = e.response
        if response != None:
            error = e.response.json()["error"]
            print(f"\033[91mError from RequestException: {error}\033[0m")
            emitData(
                socketio,
                "something_went_wrong",
                {"message": str(error), "status": 502},
                room=CurrentUser,
            )
        else:
            print(f"\033[91mError from ResponseException but no error reported\033[0m")
            emitData(
                socketio,
                "something_went_wrong",
                {"message": "The LLM server isn't responding", "status": 503},
                room=CurrentUser,
            )
        return

    except Exception as e:
        print(f"\033[91;1m{e}.\033[0m\n")
        emitData(
            socketio,
            "something_went_wrong",
            {"message": "Internal server error"},
            room=CurrentUser,
        )
        return
