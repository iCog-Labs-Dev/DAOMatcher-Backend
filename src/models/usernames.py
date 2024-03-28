from src.extensions import db
from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column


class Usernames(db.Model):
    id = mapped_column(String(length=50), primary_key=True)
    username: Mapped[str] = mapped_column(String(length=100), nullable=False)
    type: Mapped[str] = mapped_column(String(length=10), nullable=False)
