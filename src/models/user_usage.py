from __future__ import annotations

import uuid
from src.extensions import db
from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models.user import User


class UserUsage(db.Model):
    id: Mapped[str] = mapped_column(
        String(length=50), primary_key=True, default=lambda: uuid.uuid4().hex
    )
    token_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    search_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)

    user: Mapped["User"] = relationship(back_populates="user_usage")

    def serialize(self):
        return {
            "id": self.id,
            "token_count": self.token_count,
            "search_count": self.search_count,
        }
