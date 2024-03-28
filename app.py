from flask import Flask
from src.config import DevelopmentConfig, Config
from src import prod_env
from src.extensions import login_manager, socketio, cors, db, migrate
from src.views import auth, main, error
from src.models import *


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config if prod_env else DevelopmentConfig)

    cors.init_app(app)
    login_manager.init_app(app)
    socketio.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)

    app.register_blueprint(main)
    app.register_blueprint(auth)
    app.register_blueprint(error)

    return app


if __name__ == "__main__":
    app = create_app()
    with app.app_context():
        db.create_all()
    # app.run(debug=True)
