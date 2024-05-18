from datetime import datetime
from flask import request, jsonify, abort
from requests import HTTPError
from werkzeug.exceptions import NotFound

from src.extensions import db
from src.models import User, SearchResult
from sqlalchemy import desc

from src.models.search_result import UserResult, UsernameType


def add_search_result(user_id: str, data: dict = None):
    print("Adding data: ", data.get("found_users"))
    try:
        required_key = ["found_users", "seed_users", "description"]
        if not all(key in data for key in required_key):
            return (
                jsonify(
                    {
                        "message": "Make sure the data has all 'found_users', 'seed_users' and 'description' keys",
                        "data": None,
                        "error": "Bad request",
                        "success": False,
                    }
                ),
                400,
            )

        data = request.json if not data else data

        found_users: list[str] = data.get("found_users")
        found_user_results: list[UserResult] = [
            UserResult(
                username=user.get("username"),
                type=UsernameType.FOUND.value,
                score=user.get("score"),
                handle=user.get("handle"),
                social_media=user.get("social_media"),
                image_url=user.get("image"),
            )
            for user in found_users
        ]

        seed_users = data.get("seed_users")
        seed_user_results: list[UserResult] = [
            UserResult(
                username=username,
                type=UsernameType.FOUND.value,
            )
            for username in seed_users
        ]

        search_result = SearchResult()
        search_result.description = data.get("description")
        search_result.user_result.extend(found_user_results)
        search_result.user_result.extend(seed_user_results)
        search_result.user_id = user_id
        search_result.time_stamp = datetime.now()

        db.session.add(search_result)
        db.session.commit()
        print("Finished adding search results")

        return (
            jsonify(
                {
                    "message": "Search result added Successfully",
                    "data": search_result.serialize(),
                    "error": None,
                    "success": True,
                }
            ),
            201,
        )
    except Exception as e:
        print("Error while adding search result: ", e)
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


def get_search_result(result_id):
    try:
        search_result: SearchResult = db.one_or_404(
            db.select(SearchResult).filter_by(id=result_id),
            description="Search result not found",
        )

        return jsonify(
            {
                "message": "Search result Found",
                "data": search_result.serialize(),
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


def delete_search_result(result_id):
    try:
        search_result: SearchResult = db.one_or_404(
            db.select(SearchResult).filter_by(id=result_id),
            description="Search result not found",
        )

        db.session.delete(search_result)
        db.session.commit()

        return (
            jsonify(
                {
                    "message": "Search result deleted",
                    "data": None,
                    "error": None,
                    "success": True,
                }
            ),
            201,
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


def get_search_results(user_id, page=1, size=10):
    start = (page - 1) * size
    end = start + size

    try:
        search_results: list[SearchResult] = (
            db.session.query(SearchResult)
            .filter_by(user_id=user_id)
            .order_by(desc(SearchResult.time_stamp))
            .slice(start, end)
            .all()
        )

        return (
            jsonify(
                {
                    "message": (
                        "Search result found"
                        if len(search_results) > 0
                        else "No search results found"
                    ),
                    "data": [result.serialize() for result in search_results],
                    "error": None,
                    "success": True,
                }
            ),
            201,
        )
    except Exception as e:
        return (
            jsonify(
                {
                    "message": "Something went wrong",
                    "data": None,
                    "error": str(e),
                    "success": False,
                },
            ),
            500,
        )
