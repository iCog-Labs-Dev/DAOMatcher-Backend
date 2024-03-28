from src.extensions import db
from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship


class UserUsage(db.Model):
    id: Mapped[str] = mapped_column(String(length=50), primary_key=True)
    token_count: Mapped[int] = mapped_column(Integer, nullable=False)
    search_count: Mapped[int] = mapped_column(Integer, nullable=False)

    user_id: Mapped[str] = mapped_column(String(length=50), ForeignKey("users.id"))
