from flask import request
import jwt

from src.extensions import socketio
from src.globals import USERS, Sessions
from src.controllers.socket import connect, get_users
from src.utils.decorators import token_required
from src.utils.utils import emitData, get_user_from_token


@socketio.on("connect")
def handle_connect(token: str):
    try:
        current_user = get_user_from_token(token)
        user_id = current_user.get("id", None)
        connect(user_id)
    except jwt.ExpiredSignatureError:
        emitData(
            socketio,
            "something_went_wrong",
            {
                "message": "Token has expired",
                "status": 401,
                "error": "Unauthorized",
                "success": False,
            },
            room=request.sid,
        )


@socketio.on("stop")
def handle_cancel(userId):
    scoreUsers = Sessions.get(userId)
    scoreUsers.cancel = True
    print(f"\033[94mRequest Canceled: {scoreUsers.cancel}\033[0m")


@socketio.on("search")
def handle_get_users(user_id: str, data):
    get_users(user_id, data)


@socketio.on("disconnect")
def handle_disconnect():
    print("\033[94mUser disconnected\033[0m")


@socketio.on("remove")
def handle_remove(userId):
    try:
        del USERS[userId]
        del Sessions[userId]
        print("\033[94mUser session removed\033[0m")
    except KeyError:
        print(f"\033[94mNo user found with: {userId}\033[0m")


@socketio.on("error")
def handle_error(error):
    print(f"\033[91;1m{error}.\033[0m\n")
    requesterId = request.sid
    emitData(
        socketio,
        "something_went_wrong",
        {"message": str(error), "status": 500},
        room=requesterId,
    )
