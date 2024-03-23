import requests
from flask_cors import CORS
from src.utils.llm.LLM import LLM
from src.utils.llm import LLM_URL, LOCAL_LLM_URL
from flask import Flask, request, jsonify, abort


class LLMServer:
    def __init__(self) -> None:
        self.app = Flask(__name__)
        self.llm = LLM()
        CORS(self.app)

    def start(self):
        @self.app.errorhandler(405)
        def method_not_allowed(error):
            return jsonify(error=str(error.description)), 405

        @self.app.errorhandler(400)
        def bad_request(error):
            return (
                jsonify(
                    error=f"Invalid request sent to the server. Make sure the request is sending JSON object with key of 'query' and 'content'. And make sure both of them are set to a value"
                ),
                400,
            )

        @self.app.errorhandler(503)
        def server_not_responding(error):
            return jsonify(error="Connection to deployed LLM server failed"), 404

        @self.app.route("/", methods=["POST"])
        def handle_request():
            if request.method == "POST":
                if "query" in request.json and "content" in request.json:
                    if not (request.json["content"] and request.json["query"]):
                        abort(400)
                    query = request.json["query"]
                    content = request.json["content"]
                    try:
                        response = self.llm.generate(query, content)
                        response = response.strip()

                        data = {"response": response}

                        return jsonify(data)
                    except Exception as e:
                        abort(503)
                else:
                    abort(400)
            else:
                abort(405)

        # self.app.run(port=LOCAL_LLM_PORT, debug=False)
        # self.llm.model.stop()

    def generate_search(self, query, content):
        headers = {"Content-Type": "application/json"}  # Specify JSON content type
        data = {"query": query, "content": content}

        Url = LLM_URL if LLM_URL else LOCAL_LLM_URL

        try:
            response = requests.post(Url, json=data, headers=headers)
            response.raise_for_status()  # Raise an exception for HTTP errors

            # Assuming the server returns JSON data as well
            generated_text = response.json()
            # print("POST request successful")
            # print("Response:", generated_text)
            return generated_text

        except requests.exceptions.RequestException as e:
            print(f"POST request failed: {e}")
            raise e


def create_llm_server():
    llm_server = LLMServer()
    llm_server.start()
    return llm_server.app
