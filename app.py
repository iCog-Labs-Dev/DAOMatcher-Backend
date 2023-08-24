import os
from flask import Flask, request
from pyngrok import ngrok
from dotenv import load_dotenv
from src.ServerLogic.StoringUsers import *

load_dotenv()

port_no = 5000

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def semantic_search_query():
    if request.method == "GET":
        return "Send post request"
    elif request.method == "POST":
        query = request.json["query"]
        user_list = request.json["user_list"]
        user_limit = request.json["user_limit"]
        return scour(user_list, query, user_limit)


app.run(port=port_no)
