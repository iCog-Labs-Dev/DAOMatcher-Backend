from flask import Flask, request
from src.ServerLogic.StoringUsers import *

app = Flask(__name__)

LOCAL_APP_PORT = 5000


@app.route("/", methods=["GET", "POST"])
def semantic_search_query():
    if request.method == "GET":
        return "Send post request"
    elif request.method == "POST":
        query = request.json["query"]
        user_list = request.json["user_list"]
        user_limit = request.json["user_limit"]
        return scour(user_list, query, user_limit)


app.run(port=LOCAL_APP_PORT)
