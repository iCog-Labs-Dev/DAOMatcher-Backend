import requests
from flask import request, jsonify, abort
from src.models import User, UserUsage, SearchResult
from src.extensions import db
from src.models.search_usernames import UsernameType
from src.models.username import Username


def get_user_by_id(user_id: str):
    user: User = db.one_or_404(
        db.select(User).filter_by(id=user_id), description="User not found"
    )
    return jsonify(user.serialize())


def add_user():
    try:
        new_user = request.json
        user = User(
            display_name=new_user.get("display_name"),
            api_key=new_user.get("api_key"),
            email=new_user.get("email"),
        )
        db.session.add(user)
        db.session.commit()
        return jsonify(user.serialize())
    except Exception as e:
        abort(500, str(e))


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
            db.select(UserUsage).filter_by(id=usage_id), description="Usage not found"
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

        found_usernames_str: list[str] = data.get("found_usernames")
        found_usernames: list[Username] = [
            Username(username=username, type=UsernameType.FOUND)
            for username in found_usernames_str
        ]

        seed_usernames_str = data.get("seed_usernames")
        seed_usernames: list[Username] = [
            Username(username=username, type=UsernameType.SEED)
            for username in seed_usernames_str
        ]

        search_result = SearchResult()
        search_result.description = data.get("description")
        search_result.usernames.extend(found_usernames)
        search_result.usernames.extend(seed_usernames)
        search_result.user_id = user_id

        db.session.add(search_result)
        db.session.commit()
    except Exception as e:
        abort(500, str(e))


def get_search_result(result_id):
    search_result: SearchResult = db.one_or_404(
        db.select(SearchResult).filter_by(id=result_id),
        description="Search result not found",
    )

    return jsonify(search_result.serialize())


def delete_search_result(result_id):
    search_result: SearchResult = db.one_or_404(
        db.select(User).filter_by(id=result_id), description="Search result not found"
    )

    db.session.delete(search_result)
    db.session.commit()
    return jsonify(message="Search result deleted")


def get_search_results(user_id):
    search_results: list[SearchResult] = db.get_or_404(
        db.select(SearchResult).filter_by(user_id=user_id),
        description="No search results  found",
    )
    return jsonify([result.serialize() for result in search_results])
