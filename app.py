from flask import Flask, request, jsonify, abort
from src.ServerLogic.Users import Users
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)

LOCAL_APP_PORT = 5000
users = Users()


@app.route("/", methods=["GET", "POST"])
def scoring_user():
    print(request.json)
    if request.method == "GET":
        return "Send post request"
    elif request.method == "POST":
        jsonRequest = request.json

        if not all(key in jsonRequest for key in ("query", "user_list", "user_limit")):
            abort(
                400,
                description="Invalid JSON request. Make sure the request has set 'query', 'user_list' and 'user_limit'",
            )

        query = request.json["query"]
        user_list = request.json["user_list"]
        user_limit = request.json["user_limit"]
        try:
            result = users.scour(user_list, query, user_limit)
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
            abort(
                e.response.status_code,
                description=f"Invalid response submitted to the LLM server",
            )
        except Exception as e:
            abort(500, description="Server encountered Unknown error")


app.run(port=LOCAL_APP_PORT, debug=True)
