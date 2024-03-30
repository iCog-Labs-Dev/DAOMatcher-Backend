import os
import bcrypt
from flask import jsonify, request
import jwt

from src.controllers.user import get_user_by_email
from src.extensions import db
from decouple import config

from src.utils.token import confirm_token


def login():
    try:
        data = request.json
        if not data:
            return {
                "message": "Please provide user details",
                "data": None,
                "error": "Bad request",
            }, 400

        is_validated, user = False, None
        error = None

        try:
            is_validated, user = validate_credentials(
                data.get("email"), data.get("password")
            )
        except Exception as e:
            error = str(e)

        if not is_validated:
            return (
                dict(message="Invalid credentials", data=None, error=error),
                401,
            )

        if user:
            try:
                token = jwt.encode(
                    {"user_id": user["_id"]},
                    config("SECRET_KEY"),
                    algorithm="HS256",
                )
                return {
                    "message": "Login successful",
                    "data": {"user": user, "token": token},
                    "success": True,
                }
            except Exception as e:
                return {
                    "error": str(e),
                    "message": "Something went wrong",
                    "success": False,
                }, 500
        return {
            "message": "Unauthorized",
            "data": None,
            "error": "Error fetching auth token!, invalid email or password",
            "success": False,
        }, 401
    except Exception as e:
        return {
            "message": "Something went wrong!",
            "error": str(e),
            "data": None,
            "success": False,
        }, 500


def validate_credentials(email: str, password: str):
    if not email or not password:
        raise Exception("Invalid email or password")

    user = get_user_by_email(email)
    if not user:
        raise Exception("User not found")

    hashed_password = user.password
    salt = user.salt

    hashed_password_with_salt = bcrypt.hashpw(
        password.encode("utf-8"), salt.encode("utf-8")
    )

    valid_credential = hashed_password_with_salt == hashed_password.encode("utf-8")

    return valid_credential, user


def confirm_email(current_user: dict, token: str):
    try:
        if current_user.get("verified", False):
            return jsonify(
                {
                    "message": "Email already verified",
                    "data": None,
                    "error": None,
                    "success": True,
                }
            )

        email = confirm_token(token)
        user = get_user_by_email(current_user.get("email"))

        if user and user.email == email:
            user.verified = True
            db.session.add(user)
            db.session.commit()
            return jsonify(
                {
                    "message": "Email verified",
                    "data": None,
                    "error": None,
                    "success": True,
                }
            )
        else:
            return jsonify(
                {
                    "message": "Invalid token",
                    "data": None,
                    "error": "Unauthorized",
                    "success": False,
                    "status": 401,
                }
            )
    except Exception as e:
        return jsonify(
            {
                "message": "Something went wrong",
                "data": None,
                "error": str(e),
                "success": False,
                "status": 500,
            }
        )
