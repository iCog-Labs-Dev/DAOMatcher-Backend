from flask import Blueprint, jsonify

from src.controllers.user import (
    request,
    get_user_by_id,
    update_user,
    add_user,
    update_user_usage,
)

user = Blueprint("user", __name__)
base_url = "/api/user"


@user.route(f"{base_url}/<string:user_id>", methods=["GET", "PUT"])
def get(user_id):

    if request.method == "GET":
        response = get_user_by_id(user_id)
        return response
    elif request.method == "PUT":
        response = update_user(user_id)
        return response


@user.route(f"{base_url}", methods=["POST"])
def create():
    response = add_user()
    return response


@user.route(f"{base_url}/<string:user_id>/usage/<string:usage_id>", methods=["PUT"])
def update_usage(user_id, usage_id):
    response = update_user_usage(usage_id)
    return response
