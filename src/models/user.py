from typing import List, Optional, TYPE_CHECKING
import uuid
from src.extensions import db
from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship


if TYPE_CHECKING:
    from src.models.user_usage import UserUsage
    from src.models.user_setting import UserSetting
    from src.models.search_result import SearchResult


class User(db.Model):
    id: Mapped[str] = mapped_column(
        String(length=50), primary_key=True, default=lambda: uuid.uuid4().hex
    )
    email: Mapped[str] = mapped_column(String(length=100), unique=True)
    display_name: Mapped[str] = mapped_column(String(length=50), unique=True)
    verification_token: Mapped[str] = mapped_column(String(length=50), nullable=True)
    password_reset_token: Mapped[str] = mapped_column(String(length=50), nullable=True)
    password: Mapped[str] = mapped_column(String(length=50), nullable=True)
    password_salt: Mapped[str] = mapped_column(String(length=50), nullable=True)
    api_key: Mapped[str] = mapped_column(String(length=50), nullable=True)
    user_setting_id: Mapped[Optional[str]] = mapped_column(
        String(length=50), ForeignKey("user_setting.id"), nullable=True
    )
    usage_id: Mapped[Optional[str]] = mapped_column(
        String(length=50), ForeignKey("user_usage.id"), nullable=True
    )

    user_setting: Mapped[Optional["UserSetting"]] = relationship(back_populates="user")
    user_usage: Mapped[Optional["UserUsage"]] = relationship(back_populates="user")
    search_result: Mapped[List["SearchResult"]] = relationship(back_populates="user")

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "display_name": self.display_name,
            "setting": self.user_setting.serialize(),
            "usage": self.usage.serialize(),
            "api_key": self.api_key,
        }
