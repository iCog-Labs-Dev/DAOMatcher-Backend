import requests
from flask import request, jsonify, abort
from src.models import User, UserUsage, SearchResult
from src.extensions import db


def get_user_by_id(user_id: str):
    user: User = db.one_or_404(
        db.select(User).filter_by(id=user_id), description="User not found"
    )
    return jsonify(user.serialize())


def update_user(user_id: str):
    try:
        updatedUser = request.json
        user: User = db.one_or_404(
            db.select(User).filter_by(id=user_id), description="User not found"
        )

        user.display_name = updatedUser.get("display_name", user.display_name)
        user.api_key = updatedUser.get("api_key", user.api_key)
        user.email = updatedUser.get("email", user.email)

        db.session.commit()
        return jsonify(user.serialize())

    except Exception as e:
        abort(500, str(e))


def update_user_usage(usage_id):
    try:
        updatedUsage = request.json
        usage: UserUsage = db.one_or_404(
            db.select(User).filter_by(id=usage_id), description="Usage not found"
        )

        usage.token_count = updatedUsage.get("token_count")
        usage.search_count = updatedUsage.get("search_count")

        db.session.commit()
        return jsonify(usage.serialize())
    except Exception as e:
        abort(500, str(e))


def add_search_result(user_id):
    try:
        data = request.json
        search_result = SearchResult()
        search_result.description = data.get("description")
        pass
    except Exception as e:
        pass


def get_search_result(result_id):
    search_result = SearchResult.query.get(result_id)
    if not search_result:
        abort(404, "Search result not found")
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
