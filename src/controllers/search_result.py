from flask import request, jsonify, abort
from requests import HTTPError
from werkzeug.exceptions import NotFound

from src.extensions import db
from src.models import User, SearchResult
from sqlalchemy import desc

from src.models.search_result import Username, UsernameType


def add_search_result(user_id: str, data: dict = None):
    print("Adding search result")
    try:
        data = request.json if not data else data

        found_usernames_str: list[str] = data.get("found_usernames")
        found_usernames: list[Username] = [
            Username(username=username, type=UsernameType.FOUND.value)
            for username in found_usernames_str
        ]

        seed_usernames_str = data.get("seed_usernames")
        seed_usernames: list[Username] = [
            Username(username=username, type=UsernameType.SEED.value)
            for username in seed_usernames_str
        ]

        search_result = SearchResult()
        search_result.description = data.get("description")
        search_result.username.extend(found_usernames)
        search_result.username.extend(seed_usernames)
        search_result.user_id = user_id

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
                    "message": "Search result found",
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
