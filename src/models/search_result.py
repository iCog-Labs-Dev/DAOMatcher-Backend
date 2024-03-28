from __future__ import annotations
from typing import TYPE_CHECKING, List
from src.extensions import db
from sqlalchemy import ForeignKey, String, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from sqlalchemy import DateTime

from src.models.search_usernames import search_usernames

if TYPE_CHECKING:
    from src.models.username import Username


class SearchResult(db.Model):
    id: Mapped[str] = mapped_column(String(length=50), primary_key=True)
    time_stamp: Mapped[DateTime] = mapped_column(DateTime, default=datetime)
    description: Mapped[str] = mapped_column(String(250))

    usernames: Mapped[List["Username"]] = relationship(
        secondary=search_usernames, back_populates="search_result"
    )
