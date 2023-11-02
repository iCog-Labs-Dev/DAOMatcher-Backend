import requests
from flask import request
from src.extensions import socketio
from src.globals import USERS, Sessions
from src.utils.serverLogic import ScoreUsers
from src.utils.utils import generate_random_string


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
# @login_required
def handle_cancel(userId):
    scoreUsers = Sessions.get(userId)
    scoreUsers.cancel = True
    print("Request Canceled: ", scoreUsers.cancel)


@socketio.on("get_users")
def handle_get_users(data):
    jsonRequest = data
    userId = jsonRequest.get("userId")
    CurrentUser = USERS.get(userId)
    scoreUsers = Sessions.get(userId)
    scoreUsers.user_session = CurrentUser
    print("Set Current User: ", scoreUsers.user_session)
    print("Recieved data: ", data)
    if not all(
        key in jsonRequest for key in ("query", "user_list", "user_limit", "depth")
    ):
        socketio.emit(
            "something_went_wrong",
            {
                "message": "Invalid request. Make sure you are sending a JSON object with keys 'query', 'user_list', 'depth' and 'user_limit' all set to acceptable values",
                "status": 400,
            },
        )
        print("error emitted")
        return
    query = jsonRequest["query"]
    user_list = jsonRequest["user_list"]
    user_limit = jsonRequest["user_limit"]
    depth = jsonRequest["depth"]
    if not all([query, user_list, user_limit]):
        socketio.emit(
            "something_went_wrong",
            {
                "message": "Invalid request. Make sure you are sending a JSON object with keys 'query', 'user_list', and 'user_limit' all set to acceptable values",
                "status": 400,
            },
        )
        print("error emitted")
        return
    try:
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
                "something_went_wrong", {"message": str(error), "status": 502}
            )
        else:
            print("Error from ResponseException but no error reported")
            socketio.emit(
                "something_went_wrong",
                {"message": "The LLM server isn't responding", "status": 503},
            )
        return
    except Exception as e:
        print(e)
        socketio.emit("something_went_wrong", {"message": "Internal server error"})
        return


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
        print("No user found")
