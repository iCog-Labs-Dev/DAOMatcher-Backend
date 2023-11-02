import os
from src.Scraping.LinkedIn import LinkedIn
from src.Scraping.Mastodon import Mastodon
from src.LLM.LLMServer import LLMServer
from flask_socketio import SocketIO


llm_server = LLMServer()
linkedIn = LinkedIn()
mastodon = Mastodon()
FRONTEND_URL = os.environ.get("FRONTEND_URL")

socketio = SocketIO(cors_allowed_origins=FRONTEND_URL if FRONTEND_URL else "*")
Sessions = {}
USERS = {}
