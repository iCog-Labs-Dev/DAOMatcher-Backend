from flask_mail import Message

from src import config
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
        sender=config("MAIL_DEFAULT_SENDER"),
    )
    mail.send(msg)
