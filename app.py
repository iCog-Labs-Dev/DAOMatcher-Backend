from flask import Flask, request, jsonify, abort
from src.ServerLogic.ScoreUsers import ScoreUsers
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)

LOCAL_APP_PORT = 5000
scoreUsers = ScoreUsers()


@app.errorhandler(405)
def method_not_allowed(error):
    return jsonify(error=str(error.description)), 405


@app.errorhandler(400)
def bad_request(error):
    return (
        jsonify(
            error="Invalid request. Make sure you are sending JSON object with keys 'query', 'user_list' and 'user_limit' all set to acceptable value"
        ),
        400,
    )


@app.errorhandler(502)
def service_not_available(error):
    return (
        jsonify(
            error=str(
                f"LLM server failed with the following error: {error.description}"
            )
        ),
        503,
    )


@app.errorhandler(503)
def service_not_available(error):
    return jsonify(error=error.description), 503


@app.errorhandler(500)
def internal_server_error(error):
    return (
        jsonify(error=str(error.description)),
        500,
    )


@app.route("/", methods=["POST"])
def scoring_user():
    print(request.json)
    if request.method == "POST":
        jsonRequest = request.json

        if not all(key in jsonRequest for key in ("query", "user_list", "user_limit")):
            abort(400)

        query = request.json["query"]
        user_list = request.json["user_list"]
        user_limit = request.json["user_limit"]

        if not all([query, user_list, user_limit]):
            abort(400)

        try:
            result = scoreUsers.scour(user_list, query, user_limit)
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
                abort(502, description=error)
            else:
                abort(503, description="The LLM server isn't responding")
        except Exception as e:
            abort(500)
    else:
        abort(405)


app.run(port=LOCAL_APP_PORT, debug=True)
