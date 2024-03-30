from flask import Blueprint

from src.controllers.search_result import *

search = Blueprint("search-result", __name__)


@search.route("/", methods=["POST"])
def add_search():
    user_id = request.args.get("id")
    search_result = add_search_result(user_id)
    return search_result


@search.route("/", methods=["GET"])
def get_search():
    search_id = request.json.get("id")
    result = get_search_result(search_id)
    return result


@search.route("/", methods=["GET"])
def get_searches():
    user_id = request.json.get("id")
    results = get_search_results(user_id)
    return results


@search.route("/usage", methods=["DELETE"])
def delete_search():
    search_id = request.json.get("id")
    result = delete_search_result(search_id)
    return result
