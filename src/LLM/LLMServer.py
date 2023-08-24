from flask import Flask, request
from ..LLM.LLMMethods import *

app = Flask(__name__)
llm = init_model()
LOCAL_LLM_PORT = 5001


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


app.run(port=LOCAL_LLM_PORT)
together.Models.stop("togethercomputer/llama-2-70b-chat")
