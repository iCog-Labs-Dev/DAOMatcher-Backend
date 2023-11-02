import os
from flask import Flask, request, jsonify, abort, session
from src.ServerLogic.ScoreUsers import ScoreUsers

from src.ServerLogic import FRONTEND_URL, socketio, USERS, Sessions

from flask_cors import CORS
from flask_login import (
    LoginManager,
    UserMixin,
    login_user,
    logout_user,
    login_required,
)

import requests
import string
import random


def generate_random_string(length=8):
    characters = string.ascii_letters + string.digits
    return "".join(random.choice(characters) for _ in range(length))


def create_app():
    app = Flask(__name__)
    app.secret_key = "Secret to be replaced with environment"
    app.config["SESSION_COOKIE_SECURE"] = True
    app.config["SESSION_COOKIE_SAMESITE"] = "None"
    origins = [FRONTEND_URL if FRONTEND_URL else "http://localhost:5173"]

    CORS(app, supports_credentials=True, origins=origins)
    login_manager = LoginManager(app)
    socketio.init_app(app)

    class User(UserMixin):
        def __init__(self, user_id):
            self.id = user_id

    @login_manager.user_loader
    def load_user(user_id):
        return User(user_id)

    @app.route("/login", methods=["POST"])
    def login():
        data = request.get_json()
        user_id = data.get("email")
        user_pass = data.get("password")
        admin_id = os.environ.get("ADMIN_ID")
        admin_pass = os.environ.get("ADMIN_PASS")
        # print(
        #     f"userId: {user_id} userPass: {user_pass} adminId: {admin_id} adminPass: {admin_pass}"
        # )
        if user_id and user_pass:
            if user_id == admin_id and user_pass == admin_pass:
                user = User(user_id)
                login_user(user)
                session["user_id"] = user_id
                return jsonify({"message": "Logged in successfully", "success": True})
            return (
                jsonify({"message": "Email or password incorrect", "success": False}),
                401,
            )
        else:
            return jsonify({"message": f"Login failed", "success": False}), 401

    @app.route("/logout", methods=["POST"])
    @login_required
    def logout():
        logout_user()
        return jsonify({"message": "Logged out successfully", "success": True})

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

    @app.errorhandler(400)
    def bad_request(error):
        return (
            jsonify(
                error="Invalid request. Make sure you are sending a JSON object with keys 'query', 'user_list', and 'user_limit' all set to acceptable values"
            ),
            400,
        )

    @app.errorhandler(401)
    def bad_request(error):
        return (
            jsonify(error="Unauthorized"),
            401,
        )

    @app.route("/", methods=["GET", "HEAD"])
    def wake_handler():
        return jsonify({"message": "Wake up successfull"})

    @app.route("/get_users", methods=["POST", "HEAD", "GET"])
    @login_required
    def scoring_user():
        print(request.json)
        if request.method == "POST":
            jsonRequest = request.json

            if not all(
                key in jsonRequest
                for key in ("query", "user_list", "user_limit", "depth")
            ):
                abort(400)

            query = request.json["query"]
            user_list = request.json["user_list"]
            user_limit = request.json["user_limit"]
            depth = request.json["depth"]

            if not all([query, user_list, user_limit]):
                abort(400)
            try:
                scoreUsers = ScoreUsers()
                result = scoreUsers.scour(user_list, query, user_limit, depth)
                users = []
                print("Result: ", result)
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
                return jsonify(data)
            except requests.exceptions.RequestException as e:
                response = e.response
                if response != None:
                    error = e.response.json()["error"]
                    print(f"\033[91;1mError from RequestException: {error}.\033[0m\n")
                    abort(502, description=error)
                else:
                    print(
                        f"\033[91;1mError from ResponseException but no error reported\033[0m\n"
                    )
                    abort(503, description="The LLM server isn't responding")
            except Exception as e:
                print(f"\033[91;1m{e}.\033[0m\n")
                abort(500)
        else:
            print("Other type of request with method ", request.method)
            return jsonify({"success": True})

    return app
