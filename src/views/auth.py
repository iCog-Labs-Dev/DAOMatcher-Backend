from flask import Blueprint, request, jsonify, session
from src.controllers.auth import login, logout
from src.globals import User
from src.extensions import login_manager
from flask_login import (
    login_user,
    logout_user,
    login_required,
)

auth = Blueprint("auth", __name__)


@login_manager.user_loader
def load_user(user_id):
    return User(user_id)


@auth.route("/login", methods=["POST"])
def handle_login():
    login()


@auth.route("/logout", methods=["POST"])
@login_required
def handle_logout():
    logout()
