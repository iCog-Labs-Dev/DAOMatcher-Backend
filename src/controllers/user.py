import bcrypt
from flask import request, jsonify, abort
from src.models import User, UserUsage
from src.extensions import db
from src.utils.token import confirm_token, generate_and_send


def get_user_by_id(user_id: str):
    user: User = db.one_or_404(
        db.select(User).filter_by(id=user_id), description="User not found"
    )
    return jsonify(user.serialize())


def get_user_by_email(email: str):
    user: User = db.one_or_404(
        db.select(User).filter_by(email=email), description="User not found"
    )
    return user


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
        return jsonify(user.serialize())
    except Exception as e:
        print(e)
        return jsonify(
            {
                "message": "Something went wrong",
                "data": None,
                "error": str(e),
                "success": False,
                "status": 500,
            }
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
        return jsonify(user.serialize())

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


def update_user_usage(usage_id):
    try:
        updatedUsage = request.json
        usage: UserUsage = db.one_or_404(
            db.select(UserUsage).filter_by(id=usage_id), description="Usage not found"
        )

        usage.token_count = updatedUsage.get("token_count")
        usage.search_count = updatedUsage.get("search_count")

        db.session.commit()
        return jsonify(usage.serialize())
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
