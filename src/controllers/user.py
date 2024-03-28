import requests
from flask import request, jsonify, abort
from src.models import User, UserUsage, SearchResult
from src.extensions import db


def get_user_by_id(user_id: str):
    user: User = db.one_or_404(
        db.select(User).filter_by(id=user_id), description="User not found"
    )
    return jsonify(
        {
            "id": user.id,
            "email": user.email,
            "display_name": user.display_name,
            "api_key": user.api_key,
            "setting": user.user_setting,
            "usage": user.usage,
        }
    )


def update_user(user_id: str):
    updatedUser = request.json
    user: User = db.one_or_404(
        db.select(User).filter_by(id=updatedUser.id), description="User not found"
    )

    user.display_name = updatedUser.get("display_name", user.display_name)
    user.api_key = updatedUser.get("api_key", user.api_key)
    user.email = updatedUser.get("email", user.email)

    db.session.commit()
    return jsonify(user.serialize())


def update_user_usage(user_id):
    user = User.query.get(user_id)
    if not user:
        abort(404, "User not found")

    user_usage = UserUsage.query.filter_by(user_id=user_id).first()
    if not user_usage:
        abort(404, "User usage not found")

    # Update user usage attributes based on request data
    user_usage.usage_count = request.json.get("usage_count", user_usage.usage_count)
    user_usage.last_usage_date = request.json.get(
        "last_usage_date", user_usage.last_usage_date
    )
    # Update other attributes as needed

    db.session.commit()
    return jsonify(user_usage.serialize())


def get_search_result(result_id):
    search_result = SearchResult.query.get(result_id)
    if not search_result:
        abort(404, "Search result not found")
    return jsonify(search_result.serialize())


def update_search_result(result_id):
    search_result = SearchResult.query.get(result_id)
    if not search_result:
        abort(404, "Search result not found")

    # Update search result attributes based on request data
    search_result.result_data = request.json.get(
        "result_data", search_result.result_data
    )
    # Update other attributes as needed

    db.session.commit()
    return jsonify(search_result.serialize())


def delete_search_result(result_id):
    search_result = SearchResult.query.get(result_id)
    if not search_result:
        abort(404, "Search result not found")

    db.session.delete(search_result)
    db.session.commit()
    return jsonify(message="Search result deleted")


def get_search_results():
    search_results = SearchResult.query.all()
    return jsonify([result.serialize() for result in search_results])
