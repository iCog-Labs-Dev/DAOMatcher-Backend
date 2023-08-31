from flask import Flask, request, jsonify
from src.ServerLogic.StoringUsers import *
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

LOCAL_APP_PORT = 5000


@app.route("/", methods=["GET", "POST"])
def semantic_search_query():
    print(request.json)
    if request.method == "GET":
        return "Send post request"
    elif request.method == "POST":
        query = request.json["query"]
        user_list = request.json["user_list"]
        user_limit = request.json["user_limit"]
        result = scour(user_list, query, user_limit)
        print(f"result: {users}")
        
        users = []
        for user in result:
            score , handle, userInfo = user
            users.append({
                "id": userInfo["id"],
                "username": userInfo["username"],
                "name": userInfo["name"],
                "score": score,
                "handle": handle
            })
        
        data = {"result": users}
        
        return jsonify(data)


app.run(port=LOCAL_APP_PORT)
