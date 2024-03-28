from flask_cors import CORS
from flask_login import LoginManager
from flask_socketio import SocketIO
from src import Base
from src.globals import FRONTEND_URL
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


origins = [FRONTEND_URL, "http://localhost:5173"]

socketio = SocketIO(cors_allowed_origins=origins)
login_manager = LoginManager()
cors = CORS(supports_credentials=True, origins=origins)
db = SQLAlchemy(model_class=Base)
migrate = Migrate()
