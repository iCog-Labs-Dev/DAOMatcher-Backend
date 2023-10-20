import os
from flask import Flask, request, jsonify, abort
from src.ServerLogic.ScoreUsers import ScoreUsers

from src.ServerLogic import socketio
import src.ServerLogic as ServerLogic

from flask_cors import CORS
import requests
import secrets
import string


def generate_random_string(length):
    characters = string.ascii_letters + string.digits
    random_string = "".join(secrets.choice(characters) for _ in range(length))
    return random_string


def create_app():
    app = Flask(__name__)
    CORS(app)
    socketio.init_app(app)

    scoreUsers = ScoreUsers()

    @socketio.on("connect")
    def handle_connect():
        print("User connected")

    @socketio.on("stop")
    def handle_cancel(data):
        scoreUsers.cancel = True
        print("Request Canceled: ", scoreUsers.cancel)

    @socketio.on("get_users")
    def handle_get_users(data):
        jsonRequest = data
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
            for user in result:
                score, handle, userInfo = user
                users.append(
                    {
                        "id": userInfo["id"],
                        "username": userInfo["username"],
                        "name": userInfo["name"],
                        "score": score,
                        "handle": handle,
                    }
                )
            print(f"result: {users}")
            data = {"result": users}
            socketio.emit("get_users", data)
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
            socketio.emit("something_went_wrong", {"message": "Internal server error"})
            return

    @socketio.on("disconnect")
    def handle_disconnect():
        print("User disconnected")

    @app.errorhandler(400)
    def bad_request(error):
        return (
            jsonify(
                error="Invalid request. Make sure you are sending a JSON object with keys 'query', 'user_list', and 'user_limit' all set to acceptable values"
            ),
            400,
        )

    # Add your other error handlers here...

    @app.route("/", methods=["POST", "HEAD", "GET"])
    def scoring_user():
        # print(request.json)
        socketio.init_app(app)
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
                result = scoreUsers.scour(user_list, query, user_limit, depth)
                users = []
                for user in result:
                    score, handle, userInfo = user
                    users.append(
                        {
                            "id": userInfo["id"],
                            "username": userInfo["username"],
                            "name": userInfo["name"],
                            "score": score,
                            "handle": handle,
                        }
                    )

                print(f"result: {users}")
                data = {"result": users}
                return jsonify(data)
            except requests.exceptions.RequestException as e:
                response = e.response
                if response != None:
                    error = e.response.json()["error"]
                    print("error from RequestException: ", error)
                    abort(502, description=error)
                else:
                    print("Error from ResponseException but no error reported")
                    abort(503, description="The LLM server isn't responding")
            except Exception as e:
                print(e)
                abort(500)
        else:
            print("Other type of request with method ", request.method)
            return jsonify({"success": True})

    return app
