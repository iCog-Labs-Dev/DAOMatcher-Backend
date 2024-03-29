from src import config


class Config:
    DEBUG = False
    TESTING = False
    SECRET_KEY = config("SECRET_KEY", default="This is a secret key")
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_SAMESITE = "None"
    SQLALCHEMY_DATABASE_URI = config("DATABASE_URL")

    # Mail Settings
    MAIL_DEFAULT_SENDER = "noreply@flask.com"
    MAIL_SERVER = "smtp.ethereal.com"
    MAIL_PORT = 587
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True
    MAIL_DEBUG = False
    MAIL_USERNAME = config("EMAIL_USER")
    MAIL_PASSWORD = config("EMAIL_PASSWORD")


class DevelopmentConfig(Config):
    DEBUG = True
    TESTING = True
