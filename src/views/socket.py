from flask import request
from src.controllers.socket import connect, get_users
from src.extensions import socketio
from src.globals import USERS, Sessions


@socketio.on("connect")
def handle_connect():
    connect()


@socketio.on("stop")
def handle_cancel(userId):
    scoreUsers = Sessions.get(userId)
    scoreUsers.cancel = True
    print("Request Canceled: ", scoreUsers.cancel)


@socketio.on("get_users")
def handle_get_users(data):
    get_users(data)


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
