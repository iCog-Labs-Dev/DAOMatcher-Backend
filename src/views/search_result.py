from flask import Blueprint

from src.controllers.search_result import *

search = Blueprint("search-result", __name__)


@search.route("/<string:user_id>", methods=["POST"])
def add_search(user_id):
    search_result = add_search_result(user_id)
    return search_result


@search.route("/search-result/<string:id>", methods=["GET"])
def get_search(id):
    if request.method == "GET":
        result = get_search_result(id)
        return result
    elif request.method == "DELETE":
        result = delete_search_result(id)
        return result


@search.route("/search-result", methods=["GET"])
def get_searches():
    user_id = request.json.get("id")
    results = get_search_results(user_id)
    return results
