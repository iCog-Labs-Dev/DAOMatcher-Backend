from src.extensions import db
from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship


class User(db.Model):
    id: Mapped[str] = mapped_column(String(length=50), primary_key=True)
    email: Mapped[str] = mapped_column(String(length=255), unique=True, nullable=False)
    display_name: Mapped[str] = mapped_column(
        String(length=50), unique=True, nullable=False
    )
    verification_token: Mapped[str] = mapped_column(String)
    password_reset_token: Mapped[str] = mapped_column(String)
    password: Mapped[str] = mapped_column(String)
    password_salt: Mapped[str] = mapped_column(String)
    api_key: Mapped[str] = mapped_column(String)

    app_settings = relationship("AppSettings", backref="user")
    usage = relationship("Usage", backref="user")
    search_result = relationship("SearchResult", backref="user")
