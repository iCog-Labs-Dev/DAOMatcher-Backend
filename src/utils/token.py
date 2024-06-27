from flask import url_for
from decouple import config
from itsdangerous import URLSafeTimedSerializer

from src.utils.email import send_email


def generate_token(email):
    serializer = URLSafeTimedSerializer(config("SECRET_KEY"))
    return serializer.dumps(email, salt=config("SECURITY_PASSWORD_SALT"))


def confirm_token(token, expiration=3600):
    serializer = URLSafeTimedSerializer(config("SECRET_KEY"))
    try:
        email = serializer.loads(
            token, salt=config("SECURITY_PASSWORD_SALT"), max_age=expiration
        )
        return email
    except Exception:
        return False


def generate_and_send(email):
    token = generate_token(email)
    base_url = config("CONFIRM_URL")

    confirm_url = base_url + "/" + token
    subject = "Please confirm your email"
    send_email(email, subject, confirm_url)
