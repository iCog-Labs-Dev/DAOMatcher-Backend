from flask import Flask, request, jsonify, abort
from src.ServerLogic.ScoreUsers import ScoreUsers
from flask_cors import CORS
from flask_sse import sse
import requests


def create_app():
    app = Flask(__name__)
    CORS(app)
    app.config[
        "REDIS_URL"
    ] = "redis://red-ck61b3j6fquc73bk1fag:6379"  # Redis server for SSE

    # Initialize the SSE extension
    app.register_blueprint(sse, url_prefix="/stream")

    scoreUsers = ScoreUsers()

    @app.errorhandler(400)
    def bad_request(error):
        return (
            jsonify(
                error="Invalid request. Make sure you are sending a JSON object with keys 'query', 'user_list', and 'user_limit' all set to acceptable values"
            ),
            400,
        )

    # Add your other error handlers here...

    @app.route("/", methods=["POST"])
    def scoring_user():
        print(request.json)
        if request.method == "POST":
            jsonRequest = request.json

            if not all(
                key in jsonRequest for key in ("query", "user_list", "user_limit")
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
                abort(500)
        else:
            print(request.method)
            abort(405)

    return app
