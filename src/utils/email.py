from flask_mail import Message

from decouple import config
from src.extensions import mail


def send_email(to, subject, confirm_url):
    template = f"""
    <p>
        Welcome! Thanks for signing up. Please follow this link to activate your
        account:
    </p>
    <p><a href="{confirm_url}">{confirm_url}</a></p>
    <br />
    <p>Cheers!</p>
    """
    msg = Message(
        subject,
        recipients=[to],
        html=template,
        sender=config("EMAIL_USER"),
    )
    mail.send(msg)
