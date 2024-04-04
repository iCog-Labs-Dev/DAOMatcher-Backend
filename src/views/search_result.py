from flask import Blueprint

from src.controllers.search_result import *

search = Blueprint("search-result", __name__)


@search.route("/user/<string:user_id>/search-result", methods=["GET", "POST"])
def search_results(user_id):
    if request.method == "GET":
        results = get_search_results(user_id)
        return results
    elif request.method == "POST":
        pass
    search_result = add_search_result(user_id)
    return search_result


@search.route("/user/<string:user_id>/search-result/<string:id>", methods=["GET"])
def search_result(user_id, id):
    if request.method == "GET":
        result = get_search_result(id)
        return result
    elif request.method == "DELETE":
        result = delete_search_result(id)
        return result
