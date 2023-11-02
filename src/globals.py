import os
from flask_login import UserMixin
from src.utils.serverLogic.LLMServer import create_llm_server


class User(UserMixin):
    def __init__(self, user_id):
        self.id = user_id


FRONTEND_URL = os.environ.get("FRONTEND_URL")
llm_app = create_llm_server()

Sessions = {}
USERS = {}
