from src.extensions import db
from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from sqlalchemy import DateTime


class SearchResult(db.Model):
    __tablename__ = "search_results"

    id = mapped_column(String(length=50), primary_key=True)
    found_usernames_id = mapped_column(
        String(length=50), ForeignKey("found_usernames.id")
    )
    seed_usernames_id = mapped_column(
        String(length=50), ForeignKey("seed_usernames.id")
    )
    time_stamp = mapped_column(DateTime, default=datetime)
    description = mapped_column(String)

    found_usernames = relationship("FoundUsernames", backref="search_result")
    seed_usernames = relationship("SeedUsernames", backref="search_result")
