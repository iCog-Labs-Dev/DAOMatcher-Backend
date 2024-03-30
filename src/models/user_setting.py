from __future__ import annotations

import uuid

from typing import TYPE_CHECKING
from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.extensions import db

if TYPE_CHECKING:
    from src.models.user import User


class UserSetting(db.Model):
    id: Mapped[str] = mapped_column(
        String(length=50), primary_key=True, default=lambda: uuid.uuid4().hex
    )
    default_user_count: Mapped[int] = mapped_column(Integer)
    default_depth_count: Mapped[int] = mapped_column(Integer)
    theme: Mapped[str] = mapped_column(String(length=10))

    user: Mapped["User"] = relationship(
        back_populates="user_setting", cascade="all, delete-orphan"
    )

    def serialize(self):
        return {
            "id": self.id,
            "default_user_count": self.default_user_count,
            "default_depth_count": self.default_depth_count,
            "theme": self.theme,
        }
