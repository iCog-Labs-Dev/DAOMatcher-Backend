from typing import TYPE_CHECKING, List
from src.extensions import db
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models import search_usernames

if TYPE_CHECKING:
    from src.models.search_result import SearchResult


class Username(db.Model):
    id = mapped_column(String(length=50), primary_key=True)
    username: Mapped[str] = mapped_column(String(length=100), nullable=False)
    type: Mapped[str] = mapped_column(String(length=10), nullable=False)

    search_result: Mapped[List["SearchResult"]] = relationship(
        secondary=search_usernames, back_populates="username"
    )

    def serialize(self):
        return {
            "id": self.id,
            "username": self.username,
            "type": self.type,
        }
