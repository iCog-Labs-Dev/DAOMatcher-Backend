from src.controllers.user import (
    request,
    get_user_by_id,
    update_user,
    add_user,
    update_user_usage,
)
from flask import Blueprint

user = Blueprint("user", __name__)


@user.route("/user/<string:user_id>", methods=["GET"])
def get_by_id(user_id):
    user = get_user_by_id(user_id)

    return user


@user.route("/user", methods=["POST"])
def create():
    user = add_user()
    return user


@user.route("/user/<string:user_id>", methods=["PUT"])
def update(user_id):
    user = update_user(user_id)

    return user


@user.route("/user/<string:user_id>/usage", methods=["PUT"])
def update_usage(user_id):
    updated_usage = update_user_usage(user_id)
    return updated_usage
