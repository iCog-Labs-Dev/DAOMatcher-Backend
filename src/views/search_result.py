from flask import Blueprint

from src.controllers.search_result import *

search = Blueprint("search-result", __name__)
base_url = "/api/user/<string:user_id>/search-result"


@search.route(f"{base_url}", methods=["GET", "POST"])
def search_results(user_id):
    if request.method == "GET":
        response = get_search_results(user_id)
        return response, response.get("status")
    elif request.method == "POST":
        response = add_search_result(user_id)
        return response, response.get("status")


@search.route(f"{base_url}/<string:id>", methods=["GET"])
def search_result(user_id, id):
    if request.method == "GET":
        response = get_search_result(id)
        return response, response.get("status")
    elif request.method == "DELETE":
        response = delete_search_result(id)
        return response, response.get("status")
