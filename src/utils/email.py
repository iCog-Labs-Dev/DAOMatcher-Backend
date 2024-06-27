from flask_mail import Message
from decouple import config

from src.extensions import mail


def send_email(to, subject, confirm_url):
    template = f"""
    <p>
        Welcome! Thanks for signing up. Please follow this link to activate your
        account:
    </p>
    <p>Click <a href="{confirm_url}">here </a>to verify.</p>
    <br />
    """
    msg = Message(
        subject,
        recipients=[to],
        html=template,
        sender=config("MAIL_DEFAULT_SENDER"),
        extra_headers={"Reply-To": "no-reply@example.com"},
    )
    mail.send(msg)
