import os
from decouple import config
from src.utils.serverLogic.LLMServer import create_llm_server


FRONTEND_URL = config("FRONTEND_URL")
llm_app = create_llm_server()

Sessions = {}
USERS = {}
