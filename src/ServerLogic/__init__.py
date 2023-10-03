from src.Scraping.LinkedIn import LinkedIn
from src.Scraping.Mastodon import Mastodon
from src.LLM.LLMServer import LLMServer
from flask_socketio import SocketIO

llm_server = LLMServer()
linkedIn = LinkedIn()
mastodon = Mastodon()
socketio = SocketIO()
