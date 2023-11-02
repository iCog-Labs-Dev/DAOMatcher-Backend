from flask_socketio import SocketIO
from src.utils.serverLogic import FRONTEND_URL


socketio = SocketIO(cors_allowed_origins=FRONTEND_URL if FRONTEND_URL else "*")
