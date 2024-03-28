from __future__ import annotations
from typing import TYPE_CHECKING
import uuid
from src.extensions import db
from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

if TYPE_CHECKING:
    from src.models.user import User


class UserSetting(db.Model):
    id: Mapped[str] = mapped_column(
        String(length=50), primary_key=True, default=lambda: uuid.uuid4().hex
    )
    default_user_count: Mapped[int] = mapped_column(Integer)
    default_depth_count: Mapped[int] = mapped_column(Integer)
    theme: Mapped[str] = mapped_column(String(length=10))
    user_id: Mapped[str] = mapped_column(String(length=50), ForeignKey("user.id"))

    user: Mapped["User"] = relationship(back_populates="user_setting")

    def serialize(self):
        return {
            "id": self.id,
            "default_user_count": self.default_user_count,
            "default_depth_count": self.default_depth_count,
            "theme": self.theme,
        }
