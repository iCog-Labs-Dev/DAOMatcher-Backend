from flask import Blueprint, jsonify

errors = Blueprint("errors", __name__)


@errors.errorhandler(400)
def bad_request(error):
    return (
        jsonify(
            error="Invalid request. Make sure you are sending a JSON object with keys 'query', 'user_list', and 'user_limit' all set to acceptable values"
        ),
        400,
    )


@errors.errorhandler(401)
def bad_request(error):
    return (
        jsonify(error="Unauthorized"),
        401,
    )
