from flask import request
from src.extensions import socketio
from src.globals import USERS, Sessions
from src.utils.serverLogic.ScoreUsers import ScoreUsers
from src.utils.utils import (
    generate_random_string,
    process_users,
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
    socketio.emit("set_cookie", userId, room=request.sid)


def get_users(data):
    jsonRequest = data
    print("Recieved Data: ", jsonRequest)
    sessionIsSet, CurrentUser = set_user_session(data)
    valid = validate_data(data)
    if (not sessionIsSet) or (not valid):
        socketio.emit(
            "something_went_wrong",
            {
                "message": "Invalid request, make sure you are logged in",
                "status": 400,
            },
        )
        print("error emitted")
        return
    print("CurrentUser: ", CurrentUser)
    query = jsonRequest.get("query")
    user_list = jsonRequest.get("user_list")
    user_limit = jsonRequest.get("user_limit")
    depth = jsonRequest.get("depth")
    userId = jsonRequest.get("userId")
    process_users(user_list, query, user_limit, depth, userId, CurrentUser)
