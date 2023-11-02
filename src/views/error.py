from flask import Blueprint, jsonify

error = Blueprint("errors", __name__)


@error.errorhandler(400)
def bad_request(error):
    return (
        jsonify(
            error="Invalid request. Make sure you are sending a JSON object with keys 'query', 'user_list', and 'user_limit' all set to acceptable values"
        ),
        400,
    )


@error.errorhandler(401)
def bad_request(error):
    return (
        jsonify(error="Unauthorized"),
        401,
    )
