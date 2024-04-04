import uuid
from typing import List, Optional, TYPE_CHECKING
from sqlalchemy import Boolean, DateTime, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.extensions import db

if TYPE_CHECKING:
    from src.models.user_usage import UserUsage
    from src.models.user_setting import UserSetting
    from src.models.search_result import SearchResult


class User(db.Model):
    id: Mapped[str] = mapped_column(
        String(length=50), primary_key=True, default=lambda: uuid.uuid4().hex
    )
    email: Mapped[str] = mapped_column(String(length=100), unique=True)
    verified: Mapped[bool] = mapped_column(Boolean, default=False)
    display_name: Mapped[str] = mapped_column(String(length=50), unique=True)
    password: Mapped[str] = mapped_column(String(length=100))
    password_salt: Mapped[str] = mapped_column(String(length=100))
    api_key: Mapped[str] = mapped_column(String(length=50), nullable=True)
    user_setting_id: Mapped[Optional[str]] = mapped_column(
        String(length=50), ForeignKey("user_setting.id"), nullable=True
    )
    usage_id: Mapped[Optional[str]] = mapped_column(
        String(length=50), ForeignKey("user_usage.id")
    )

    user_setting: Mapped[Optional["UserSetting"]] = relationship(back_populates="user")
    user_usage: Mapped[Optional["UserUsage"]] = relationship(back_populates="user")
    search_result: Mapped[List["SearchResult"]] = relationship(
        back_populates="user", cascade="all, delete-orphan", single_parent=True
    )

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "display_name": self.display_name,
            "verified": self.verified,
            "setting": self.user_setting.serialize() if self.user_setting else None,
            "usage": self.user_usage.serialize() if self.user_usage else None,
            "api_key": self.api_key if self.api_key else None,
        }

    def login_serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "display_name": self.display_name,
            "verified": self.verified,
            "setting": self.user_setting.serialize() if self.user_setting else None,
            "usage": self.user_usage.serialize() if self.user_usage else None,
            "api_key": self.api_key if self.api_key else None,
            "password": self.password,
            "salt": self.password_salt,
        }
