from MySQLdb._exceptions import IntegrityError
import bcrypt
from flask import request, jsonify

from src.extensions import db
from src.models import User, UserUsage
from src.utils.token import generate_and_send


def get_user_by_id(user_id: str):
    user: User = db.one_or_404(
        db.select(User).filter_by(id=user_id), description="User not found"
    )
    return jsonify(
        {
            "message": "User Found",
            "data": user.serialize(),
            "error": None,
            "success": False,
            "success": True,
        }
    )


def get_user_by_email(email: str, login: bool = False):
    user: User = db.one_or_404(
        db.select(User).filter_by(email=email), description="User not found"
    )
    return jsonify(
        {
            "message": "User Found",
            "data": user.serialize() if not login else user.login_serialize(),
            "error": None,
            "success": False,
            "success": True,
        }
    )


def add_user():
    try:
        new_user = request.json
        user: User = User(
            display_name=new_user.get("display_name"),
            api_key=new_user.get("api_key"),
            email=new_user.get("email"),
        )
        usage: UserUsage = UserUsage()
        user.user_usage = usage

        password = new_user.get("password").encode("utf-8")
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password, salt)

        user.password = hashed_password
        user.password_salt = salt

        db.session.add(user)
        db.session.commit()

        generate_and_send(user.email)

        return jsonify(
            {
                "message": "User added Successfully",
                "data": user.serialize(),
                "error": None,
                "success": False,
                "success": True,
            }
        )
    except Exception as e:
        error_message = "Something went wrong"
        return (
            jsonify(
                {
                    "message": error_message,
                    "data": None,
                    "error": str(e),
                    "success": False,
                }
            ),
            500,
        )


def update_user(user_id: str):
    try:
        updatedUser = request.json
        user: User = db.one_or_404(
            db.select(User).filter_by(id=user_id), description="User not found"
        )

        user.display_name = updatedUser.get("display_name", user.display_name)
        user.api_key = updatedUser.get("api_key", user.api_key)

        db.session.commit()

        return jsonify(
            {
                "message": "User updated Successfully",
                "data": user.serialize(),
                "error": None,
                "success": False,
                "success": True,
            }
        )

    except Exception as e:
        return (
            jsonify(
                {
                    "message": "Something went wrong",
                    "data": None,
                    "error": str(e),
                    "success": False,
                }
            ),
            500,
        )


def update_user_usage(usage_id):
    try:
        updatedUsage = request.json
        usage: UserUsage = db.one_or_404(
            db.select(UserUsage).filter_by(id=usage_id), description="Usage not found"
        )

        usage.token_count = updatedUsage.get("token_count")
        usage.search_count = updatedUsage.get("search_count")

        db.session.commit()

        return jsonify(
            {
                "message": "Usage updated Successfully",
                "data": usage.serialize(),
                "error": None,
                "success": False,
                "success": True,
            }
        )
    except Exception as e:
        return (
            jsonify(
                {
                    "message": "Something went wrong",
                    "data": None,
                    "error": str(e),
                    "success": False,
                }
            ),
            500,
        )
