from flask import request
import jwt

from src.extensions import socketio
from src.globals import USERS, Sessions
from src.controllers.socket import connect, get_users
from src.utils.decorators import token_required
from src.utils.utils import emitData, get_user_from_token


@socketio.on("connect")
@token_required
def handle_connect(current_user: dict):
    print("\033[94mConnected to socket io\033[0m")
    user_id = current_user.get("id", None)
    connect(user_id)


@socketio.on("stop")
def handle_cancel(userId):
    scoreUsers = Sessions.get(userId)
    if scoreUsers:
        scoreUsers.cancel = True
        print(f"\033[94mRequest Canceled: {scoreUsers.cancel}\033[0m")


@socketio.on("search")
def handle_get_users(data):
    user_id = data.get("userId", None)
    get_users(user_id, data)


@socketio.on("disconnect")
def handle_disconnect():
    print("\033[94mUser disconnected\033[0m")


@socketio.on("remove")
def handle_remove(user_id):
    print("Removing user")
    try:
        del USERS[user_id]
        del Sessions[user_id]
        print("\033[94mUser session removed\033[0m")
    except KeyError:
        print(f"\033[94mNo user found with: {user_id}\033[0m")


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
