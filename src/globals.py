import os
from src.utils.serverLogic.LLMServer import create_llm_server

FRONTEND_URL = os.environ.get("FRONTEND_URL")

Sessions = {}
USERS = {}
