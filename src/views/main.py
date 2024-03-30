from flask_login import login_required
from flask import Blueprint, jsonify

from src.controllers.main import scoring_user

main = Blueprint("main", __name__)


@main.route("/", methods=["GET", "HEAD"])
def wake_handler():
    return jsonify({"message": "Wake up successful"})


@main.route("/get_users", methods=["POST", "HEAD", "GET"])
@login_required
def handle_get_users():
    return scoring_user()
