import os
from flask import Flask, request
from pyngrok import ngrok
from dotenv import load_dotenv
from src.ServerLogic.StoringUsers import *

load_dotenv()

port_no = 5000

app = Flask(__name__)
ngrok.set_auth_token(os.environ["NGROK_API_KEY"])
public_url = ngrok.connect(port_no).public_url


@app.route("/", methods=["GET", "POST"])
def semantic_search_query():
    if request.method == "GET":
        return "Send post request"
    elif request.method == "POST":
        query = request.json["query"]
        user_list = request.json["user_list"]
        user_limit = request.json["user_limit"]
        return scour(user_list, query, user_limit)


print(f"Public url for the API... {public_url}")

app.run(port=port_no)
