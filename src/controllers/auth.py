from flask import Blueprint, request, jsonify, session
import os
from flask_login import (
    login_user,
    logout_user,
)

from src.globals import User


def login():
    data = request.get_json()
    user_id = data.get("email")
    user_pass = data.get("password")
    admin_id = os.environ.get("ADMIN_ID")
    admin_pass = os.environ.get("ADMIN_PASS")

    if user_id and user_pass:
        if user_id == admin_id and user_pass == admin_pass:
            user = User(user_id)
            login_user(user)
            session["user_id"] = user_id
            return jsonify({"message": "Logged in successfully", "success": True})
        return (
            jsonify({"message": "Email or password incorrect", "success": False}),
            401,
        )
    else:
        return jsonify({"message": f"Login failed", "success": False}), 401


def logout():
    logout_user()
    return jsonify({"message": "Logged out successfully", "success": True})
