from flask import Blueprint
from src.globals import User
from src.extensions import login_manager
from src.controllers.auth import login, logout
from flask_login import (
    login_required,
)

auth = Blueprint("auth", __name__)


@login_manager.user_loader
def load_user(user_id):
    return User(user_id)


@auth.route("/login", methods=["POST"])
def handle_login():
    return login()


@auth.route("/logout", methods=["POST"])
@login_required
def handle_logout():
    return logout()


@auth.route("/confirm/<token>", methods=["GET"])
def confirm_email(token):

    return "Email confirmed"


def confirm_email(token):
    pass
