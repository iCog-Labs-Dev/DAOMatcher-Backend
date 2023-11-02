import requests
from flask_login import login_required
from src.controllers.main import scoring_user
from src.utils.serverLogic import ScoreUsers
from flask import Blueprint, request, jsonify, abort

main = Blueprint("main", __name__)


@main.route("/", methods=["GET", "HEAD"])
def wake_handler():
    return jsonify({"message": "Wake up successfull"})


@main.route("/get_users", methods=["POST", "HEAD", "GET"])
@login_required
def handle_get_users():
    scoring_user()
