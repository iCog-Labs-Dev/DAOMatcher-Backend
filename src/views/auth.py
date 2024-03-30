from flask import Blueprint, url_for
from src.controllers.auth import login, confirm_email
from src.utils.email import send_email
from src.utils.middlewares import token_required
from src.utils.token import generate_token

auth = Blueprint("auth", __name__)


@auth.route("/login", methods=["POST"])
def handle_login():
    return login()


@auth.route("/confirm/<token>", methods=["GET"])
@token_required
def confirm(current_user: dict, token: str):
    confirm_email(current_user, token)


@auth.route("/confirm/resend", methods=["GET"])
@token_required
def resend_confirmation(current_user: dict):
    pass
