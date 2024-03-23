from src.extensions import db
from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column


class Usernames(db.Model):
    id = mapped_column(String(length=50), primary_key=True)
    table_id = mapped_column(
        String(length=50), ForeignKey("seed_usernames.id, found_usernames.id")
    )
    username: Mapped[str] = mapped_column(String, nullable=False)
