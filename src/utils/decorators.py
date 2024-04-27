import jwt
from flask import request
from functools import wraps
from flask import current_app

from src.controllers.user import get_user_by_id


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        # print("In token required decorator")
        # print("args", request.args["token"])

        if "Authorization" in request.headers:
            token = request.headers["Authorization"].split(" ")[1]

        elif "token" in request.args:
            token = request.args["token"]

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
            current_user = get_user_by_id(data.get("user_id")).json.get("data")
            if not current_user:
                return {
                    "message": "Invalid Authentication token!",
                    "data": None,
                    "error": "Unauthorized",
                }, 401
        except Exception as e:
            return {
                "message": "Something went wrong",
                "data": None,
                "error": str(e),
            }, 500

        return f(current_user, *args, **kwargs)

    return decorated


def authorize(f):
    @wraps(f)
    def decorated(current_user: dict, *args, **kwargs):
        if "user_id" in kwargs and kwargs["user_id"] != current_user.get("id"):
            return {"message": "Unauthorized access"}, 401

        return f(current_user, *args, **kwargs)

    return decorated
