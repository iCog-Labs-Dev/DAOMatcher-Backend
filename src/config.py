import os


class Config:
    DEBUG = False
    TESTING = False
    SECRET_KEY = os.environ.get("SECRET_KEY")
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_SAMESITE = "None"


class DevelopmentConfig(Config):
    DEBUG = True
    TESTING = True
