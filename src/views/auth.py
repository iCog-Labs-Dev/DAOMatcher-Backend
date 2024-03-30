from flask import Blueprint, url_for
from src.controllers.user import get_user_by_email
from src.globals import User
from src.controllers.auth import login
from src.utils.email import send_email
from src.utils.middlewares import token_required
from src.utils.token import confirm_token, generate_token
from src.extensions import db

auth = Blueprint("auth", __name__)


@auth.route("/login", methods=["POST"])
def handle_login():
    return login()


@auth.route("/confirm/<token>", methods=["GET"])
@token_required
def confirm_email(current_user: dict, token: str):
    if current_user.is_confirmed:
        return {"message": "Email already verified", "data": None, "error": None}, 200
    email = confirm_token(token)
    user = get_user_by_email(current_user.get("email"))
    if user and user.email == email:
        user.verified = True
        db.session.add(user)
        db.session.commit()
        return {"message": "Email verified", "data": None, "error": None}, 200
    else:
        return {"message": "Invalid token", "data": None, "error": None}, 401


@auth.route("/confirm/resend", methods=["GET"])
@token_required
def resend_confirmation(current_user: dict):
    if current_user.get("verified", False):
        return {"message": "Email already verified", "data": None, "error": None}, 200

    token = generate_token(current_user.email)
    confirm_url = url_for("accounts.confirm_email", token=token, _external=True)
    subject = "Please confirm your email"
    send_email(current_user.email, subject, confirm_url)

    return {"message": "Confirmation email sent", "data": None, "error": None}, 200
