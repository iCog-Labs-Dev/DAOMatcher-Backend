from datetime import datetime, timezone
from flask_socketio import disconnect
import jwt
from flask import request
from functools import wraps
from flask import current_app
from src.extensions import socketio

from src.controllers.user import get_user_by_id
from src.utils.utils import emitData


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        socket = False
        print("In token required decorator")
        print("args", request.args.get("token"))

        if "Authorization" in request.headers:
            token = request.headers["Authorization"].split(" ")[1]

        elif "token" in request.args:
            token = request.args["token"]
            socket = True

        if not token:
            return {
                "message": "Authentication Token is missing!",
                "data": None,
                "error": "Unauthorized",
            }, 401
        try:
            data = jwt.decode(
                token, current_app.config["SECRET_KEY"], algorithms=["HS256"]
            )
            timestamp = data.get("exp")
            invalidTokenErrorResponse = {
                "message": "Invalid Authentication token!",
                "data": None,
                "error": "Unauthorized",
            }
            if not timestamp or datetime.now(timezone.utc) > datetime.fromtimestamp(
                timestamp, timezone.utc
            ):
                if socket:
                    emitData(
                        socketio,
                        "refresh_token",
                        invalidTokenErrorResponse,
                        room=request.sid,
                    )
                return invalidTokenErrorResponse, 401
            current_user = get_user_by_id(data.get("user_id")).json.get("data")
            if not current_user:
                if socket:
                    emitData(
                        socketio,
                        "refresh_token",
                        invalidTokenErrorResponse,
                        room=request.sid,
                    )
                return invalidTokenErrorResponse, 401

        except Exception as e:
            exceptionOccurredMessage = {
                "message": "Something went wrong",
                "data": None,
                "error": str(e),
            }
            if socket:
                emitData(
                    socketio,
                    "refresh_token",
                    exceptionOccurredMessage,
                    room=request.sid,
                )
            return exceptionOccurredMessage, 500

        return f(current_user, *args, **kwargs)

    return decorated


def authorize(f):
    @wraps(f)
    def decorated(current_user: dict, *args, **kwargs):
        if "user_id" in kwargs and kwargs["user_id"] != current_user.get("id"):
            return {"message": "Unauthorized access"}, 401

        return f(current_user, *args, **kwargs)

    return decorated
