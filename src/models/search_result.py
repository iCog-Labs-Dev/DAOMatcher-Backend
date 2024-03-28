from __future__ import annotations
from typing import List
from src.extensions import db
from sqlalchemy import ForeignKey, String, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from sqlalchemy import DateTime

from src.models.search_usernames import search_usernames


class SearchResult(db.Model):
    id: Mapped[str] = mapped_column(String(length=50), primary_key=True)
    time_stamp: Mapped[DateTime] = mapped_column(DateTime, default=datetime)
    description: Mapped[str] = mapped_column(String(250))

    usernames: Mapped[List[Username]] = relationship(
        secondary=search_usernames, back_populates="search_result"
    )


class Username(db.Model):
    id = mapped_column(String(length=50), primary_key=True)
    username: Mapped[str] = mapped_column(String(length=100), nullable=False)
    type: Mapped[str] = mapped_column(String(length=10), nullable=False)

    search_result: Mapped[List[SearchResult]] = relationship(
        secondary=search_usernames, back_populates="username"
    )
