from src.extensions import db
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column


class FoundUsernames(db.Model):
    id: Mapped[str] = mapped_column(String(length=50), primary_key=True)
