from src.extensions import db
from sqlalchemy import ForeignKey, String, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from sqlalchemy import DateTime


class SearchResult(db.Model):
    __tablename__ = "search_results"

    id: Mapped[str] = mapped_column(String(length=50), primary_key=True)
    time_stamp: Mapped[DateTime] = mapped_column(DateTime, default=datetime)
    description: Mapped[str] = mapped_column(String(250))
