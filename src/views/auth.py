from flask import Blueprint

from src.controllers.auth import login, confirm_email, refresh_token, resend_token
from src.utils.decorators import token_required

auth = Blueprint("auth", __name__)
base_url = "/api/auth"


@auth.route(f"{base_url}/login", methods=["POST"])
def handle_login():
    response = login()
    return response


@auth.route(f"{base_url}/confirm/<token>", methods=["GET"])
@token_required
def confirm(current_user: dict, token: str):
    response = confirm_email(current_user, token)
    return response


@auth.route(f"{base_url}/confirm/resend", methods=["GET"])
@token_required
def resend_confirmation(current_user: dict):
    response = resend_token(current_user)
    return response


@auth.route(f"{base_url}/refresh", methods=["GET"])
def refresh():
    response = refresh_token()
    return response
