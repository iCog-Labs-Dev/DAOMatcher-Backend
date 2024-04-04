from flask import Blueprint

from src.controllers.search_result import *

search = Blueprint("search-result", __name__)
base_url = "/api/user/<string:user_id>/search-result"


@search.route(f"{base_url}", methods=["GET", "POST"])
def search_results(user_id):
    page = request.args.get("page")
    size = request.args.get("size")

    page = int(page) if page else 1
    size = int(size) if size else 10

    if request.method == "GET":
        response = get_search_results(user_id, page, size)
        return response
    elif request.method == "POST":
        response = add_search_result(user_id)
        return response


@search.route(f"{base_url}/<string:id>", methods=["GET", "DELETE"])
def search_result(user_id, id):
    if request.method == "GET":
        response = get_search_result(id)
        return response
    elif request.method == "DELETE":
        response = delete_search_result(id)
        return response
