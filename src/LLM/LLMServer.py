from pyngrok import ngrok
from flask import Flask, request
from LLM_Methods import *

port_no = 5000

app = Flask(__name__)
ngrok.set_auth_token("2TeUpGO7kAzr6rQYvURgNGIO0qG_25bMqYYu3vAcyUf72tc9i")
public_url = ngrok.connect(port_no).public_url
llm = init_model()


@app.route("/", methods=["GET", "POST"])
def semantic_search_query():
    if request.method == "GET":
        return "Send post request"
    elif request.method == "POST":
        print(request)
        query = request.json["query"]
        content = request.json["content"]
        prompt = generate(query, content, llm)
        print(prompt)
        return prompt


print(f"Public url for the API... {public_url}")

app.run(port=port_no)
together.Models.stop("togethercomputer/llama-2-70b-chat")
