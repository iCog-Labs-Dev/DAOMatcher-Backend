import requests
from flask import request
from src.controllers.socket import on_connect
from src.extensions import socketio
from src.globals import USERS, Sessions
from src.utils.serverLogic.ScoreUsers import ScoreUsers
from src.utils.utils import (
    generate_random_string,
    process_users,
    set_user_session,
    validate_data,
)


@socketio.on("connect")
def handle_connect():
    userId = generate_random_string()
    USERS[userId] = request.sid
    scoreUsers = ScoreUsers()
    print("users: ", USERS)
    Sessions[userId] = scoreUsers
    print("User connected with userId: ", userId)
    socketio.emit("set_cookie", userId, room=request.sid)


@socketio.on("stop")
def handle_cancel(userId):
    scoreUsers = Sessions.get(userId)
    scoreUsers.cancel = True
    print("Request Canceled: ", scoreUsers.cancel)


@socketio.on("get_users")
def handle_get_users(data):
    jsonRequest = data
    sessionIsSet, CurrentUser = set_user_session(data)
    valid = validate_data(data)
    if (not sessionIsSet) or (not valid):
        socketio.emit(
            "something_went_wrong",
            {
                "message": "Invalid request. Make sure you are sending a JSON object with keys 'query', 'user_list', 'depth' and 'user_limit' all set to acceptable values",
                "status": 400,
            },
        )
        print("error emitted")
        return

    query = jsonRequest.get("query")
    user_list = jsonRequest.get("user_list")
    user_limit = jsonRequest.get("user_limit")
    depth = jsonRequest.get("depth")
    process_users(user_list, query, user_limit, depth, CurrentUser)


@socketio.on("disconnect")
def handle_disconnect():
    print("User disconnected")


@socketio.on("remove")
def handle_remove(userId):
    try:
        del USERS[userId]
        del Sessions[userId]
        print("User session removed")
    except KeyError:
        print("No user found with: ", userId)


@socketio.on("error")
def handle_error(error):
    print(f"\033[91;1m{error}.\033[0m\n")
    requesterId = request.sid
    socketio.emit(
        "something_went_wrong", {"message": str(error), "status": 500}, room=requesterId
    )
