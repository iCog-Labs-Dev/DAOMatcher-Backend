from flask_login import login_required
from flask import Blueprint, jsonify

from src.controllers.main import scoring_user
from src.controllers.search_result import add_search_result
from src.utils.decorators import token_required

main = Blueprint("main", __name__)


@main.route("/", methods=["GET", "HEAD"])
def wake_handler():
    return jsonify({"message": "Wake up successful"})


@main.route("/api/search", methods=["POST", "HEAD", "GET"])
@token_required
def handle_get_users(current_user: dict):
    user_id = current_user.get("id")
    result = scoring_user(user_id)
    return result
