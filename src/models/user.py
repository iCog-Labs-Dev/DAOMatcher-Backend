from typing import Optional, TYPE_CHECKING
from src.extensions import db
from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

if TYPE_CHECKING:
    from src.models.user_usage import UserUsage
    from src.models.user_setting import UserSetting


class User(db.Model):
    id: Mapped[str] = mapped_column(String(length=50), primary_key=True)
    email: Mapped[str] = mapped_column(String(length=100), unique=True, nullable=False)
    display_name: Mapped[str] = mapped_column(
        String(length=50), unique=True, nullable=False
    )
    verification_token: Mapped[str] = mapped_column(String(length=50))
    password_reset_token: Mapped[str] = mapped_column(String(length=50))
    password: Mapped[str] = mapped_column(String(length=50))
    password_salt: Mapped[str] = mapped_column(String(length=50))
    api_key: Mapped[str] = mapped_column(String(length=50))
    user_setting_id: Mapped[Optional[str]] = mapped_column(
        String(length=50), ForeignKey("user_setting.id")
    )
    usage_id: Mapped[Optional[str]] = mapped_column(
        String(length=50), ForeignKey("user_usage.id")
    )

    user_setting: Mapped[Optional["UserSetting"]] = relationship(back_populates="user")
    usage: Mapped[Optional["UserUsage"]] = relationship(back_populates="user")

    # search_results
