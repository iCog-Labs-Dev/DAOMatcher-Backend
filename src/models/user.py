from src.extensions import db
from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship


class User(db.Model):
    id: Mapped[str] = mapped_column(String(length=50), primary_key=True)
    email: Mapped[str] = mapped_column(String(length=100), unique=True, nullable=False)
    display_name: Mapped[str] = mapped_column(
        String(length=50), unique=True, nullable=False
    )
    verification_token: Mapped[str] = mapped_column(String(length=50))
    password_reset_token: Mapped[str] = mapped_column(String(length=50))
    password: Mapped[str] = mapped_column(String(length=50))
    password_salt: Mapped[str] = mapped_column(String(length=50))
    api_key: Mapped[str] = mapped_column(String(length=50))
