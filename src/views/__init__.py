from flask_login import UserMixin
from src.views.main import main
from src.views.auth import auth
from src.views.error import error
from src.views.socket_events import socket_events


class User(UserMixin):
    def __init__(self, user_id):
        self.id = user_id
