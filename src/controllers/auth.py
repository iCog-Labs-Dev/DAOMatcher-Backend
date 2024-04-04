import jwt
import bcrypt

from decouple import config
from flask import jsonify, request

from src.controllers.user import get_user_by_email
from src.extensions import db
from src.utils.token import confirm_token, generate_and_send


def login():
    try:
        data = request.json
        if not data:
            return jsonify(
                {
                    "message": "Please provide user details",
                    "data": None,
                    "error": "Bad request",
                    "status": 400,
                }
            )

        is_validated, user = False, None
        error = None

        try:
            is_validated, user = validate_credentials(
                data.get("email"), data.get("password")
            )
        except Exception as e:
            error = str(e)

        if not is_validated:
            return jsonify(
                {
                    "message": "Invalid credentials",
                    "data": None,
                    "error": "Bad request",
                    "status": 401,
                }
            )

        if user:
            try:
                token = jwt.encode(
                    {"user_id": user["_id"]},
                    config("SECRET_KEY"),
                    algorithm="HS256",
                )
                return jsonify(
                    {
                        "message": "Login successful",
                        "data": {"user": user, "token": token},
                        "error": None,
                        "status": 200,
                    }
                )
            except Exception as e:
                return jsonify(
                    {
                        "message": "Something went wrong",
                        "data": None,
                        "error": str(e),
                        "status": 500,
                    }
                )
        return jsonify(
            {
                "message": "Unauthorized",
                "data": None,
                "error": "Error fetching auth token!, invalid email or password",
                "status": 401,
            }
        )
    except Exception as e:
        return jsonify(
            {
                "message": "Something went wrong!",
                "error": str(e),
                "data": None,
                "status": 500,
            }
        )


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
                    "status": 400,
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
                    "status": 200,
                }
            )
        else:
            return jsonify(
                {
                    "message": "Invalid token",
                    "data": None,
                    "error": "Unauthorized",
                    "status": 401,
                }
            )
    except Exception as e:
        return jsonify(
            {
                "message": "Something went wrong",
                "data": None,
                "error": str(e),
                "status": 500,
            }
        )


def resend_token(current_user: dict):
    if current_user.get("verified", False):
        return jsonify(
            {
                "message": "Email already verified",
                "data": None,
                "error": None,
                "status": 400,
            }
        )

    generate_and_send(current_user.get("email"))
    return jsonify(
        {
            "message": "Confirmation email sent",
            "data": None,
            "error": None,
            "status": 200,
        }
    )
