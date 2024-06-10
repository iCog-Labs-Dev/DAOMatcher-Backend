import requests
from flask import request, jsonify, abort

from src.controllers.search_result import add_search_result
from src.utils.serverLogic.ScoreUsers import ScoreUsers


def scoring_user(user_id: str):
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
                        "social_media": userInfo["social_media"],
                    }
                )
            print(f"result: {users}")
            search_result = {
                "found_users": users,
                "seed_users": user_list,
                "description": query,
            }
            add_search_result(user_id, search_result)
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
