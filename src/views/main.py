from flask import Blueprint, request, jsonify, abort
from flask_login import login_required
import requests

from src.ServerLogic import ScoreUsers

main = Blueprint("main", __name__)


@main.route("/", methods=["GET", "HEAD"])
def wake_handler():
    return jsonify({"message": "Wake up successfull"})


@main.route("/get_users", methods=["POST", "HEAD", "GET"])
@login_required
def scoring_user():
    print(request.json)
    if request.method == "POST":
        jsonRequest = request.json
        if not all(
            key in jsonRequest for key in ("query", "user_list", "user_limit", "depth")
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
