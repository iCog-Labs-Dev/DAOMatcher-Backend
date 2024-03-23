from src.extensions import db
from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship


class UserUsage(db.Model):
    id = mapped_column(String(length=50), primary_key=True)
    token_count = mapped_column(Integer, nullable=False)
    search_count = mapped_column(Integer, nullable=False)

    user_id = mapped_column(String(length=50), ForeignKey("users.id"))
    user = relationship("User", backref="usage")  # Define backref for User model
