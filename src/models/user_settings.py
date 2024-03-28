from src.extensions import db
from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship


class UserSettings(db.Model):
    id: Mapped[str] = mapped_column(String(length=50), primary_key=True)
    default_user_count: Mapped[int] = mapped_column(Integer)
    default_depth_count: Mapped[int] = mapped_column(Integer)
    theme: Mapped[str] = mapped_column(String(length=10))
