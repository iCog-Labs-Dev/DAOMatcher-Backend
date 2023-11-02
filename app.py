import os
from flask import Config, Flask, request, jsonify, abort, session
from src.config import DevelopmentConfig
from src.utils.serverLogic.ScoreUsers import ScoreUsers
from src import prod_env
from src.extensions import login_manager, socketio, cors
from src.utils.serverLogic import FRONTEND_URL, USERS, Sessions
from src.views import auth, main, error, socket_events

from flask_login import (
    login_user,
    logout_user,
    login_required,
)

import requests
from src.utils.utils import generate_random_string

from src.views import User


def create_app():
    app = Flask(__name__)

    app.config.from_object(Config if prod_env else DevelopmentConfig)

    cors.init_app(app)
    login_manager.init_app(app)
    socketio.init_app(app)

    app.register_blueprint(main)
    app.register_blueprint(auth)
    app.register_error_handler(error)

    return app
