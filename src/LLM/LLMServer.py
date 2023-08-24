from flask import Flask, request
from src.LLM.LLMMethods import *
from config import LocalLLMPort as LLMPort

app = Flask(__name__)
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


app.run(port=LLMPort)
together.Models.stop("togethercomputer/llama-2-70b-chat")
