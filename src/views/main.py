from flask_login import login_required
from src.controllers.main import scoring_user
from flask import Blueprint, jsonify

main = Blueprint("main", __name__)


@main.route("/", methods=["GET", "HEAD"])
def wake_handler():
    return jsonify({"message": "Wake up successfull"})


@main.route("/get_users", methods=["POST", "HEAD", "GET"])
@login_required
def handle_get_users():
    scoring_user()
