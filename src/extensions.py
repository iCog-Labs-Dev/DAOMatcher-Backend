from flask_cors import CORS
from flask_login import LoginManager
from flask_socketio import SocketIO
from src.globals import FRONTEND_URL

origins = [FRONTEND_URL, "http://localhost:5173"]

socketio = SocketIO(cors_allowed_origins=FRONTEND_URL if FRONTEND_URL else "*")
login_manager = LoginManager()
cors = CORS(supports_credentials=True, origins=origins)
