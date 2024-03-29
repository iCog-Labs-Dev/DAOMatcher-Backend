from src.controllers.user import (
    request,
    get_user_by_id,
    update_user,
    add_user,
    update_user_usage,
)
from flask import Blueprint, jsonify

user = Blueprint("user", __name__)


@user.route("/user/<string:user_id>", methods=["GET", "PUT"])
def get(user_id):

    if request.method == "GET":
        user = get_user_by_id(user_id)
        return user
    elif request.method == "PUT":
        user = update_user(user_id)
        return user


@user.route("/user", methods=["POST"])
def create():
    user = add_user()
    return jsonify({"user": user})


@user.route("/user/<string:user_id>/usage", methods=["PUT"])
def update_usage(user_id):
    updated_usage = update_user_usage(user_id)
    return updated_usage
