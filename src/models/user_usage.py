from __future__ import annotations
from src.extensions import db
from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models.user import User


class UserUsage(db.Model):
    id: Mapped[str] = mapped_column(String(length=50), primary_key=True)
    token_count: Mapped[int] = mapped_column(Integer, nullable=False)
    search_count: Mapped[int] = mapped_column(Integer, nullable=False)
    user_id: Mapped[str] = mapped_column(String(length=50), ForeignKey("user.id"))

    user: Mapped["User"] = relationship(back_populates="user_usage")

    def serialize(self):
        return {
            "id": self.id,
            "token_count": self.token_count,
            "search_count": self.search_count,
        }
