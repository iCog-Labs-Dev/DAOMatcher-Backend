from __future__ import annotations

import uuid
from datetime import datetime
from enum import Enum as PEnum
from typing import TYPE_CHECKING, List
from sqlalchemy import ForeignKey, Column, Enum, String, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.extensions import db

if TYPE_CHECKING:
    from src.models.user import User


class UsernameType(PEnum):
    SEED = "seed"
    FOUND = "found"


search_usernames = db.Table(
    "search_usernames",
    Column("search_id", ForeignKey("search_result.id"), primary_key=True),
    Column("username_id", ForeignKey("username.id"), primary_key=True),
    Column("type", Enum(UsernameType)),
)


class SearchResult(db.Model):
    id: Mapped[str] = mapped_column(
        String(length=50), primary_key=True, default=lambda: uuid.uuid4().hex
    )
    time_stamp: Mapped[DateTime] = mapped_column(DateTime, default=datetime.now())
    description: Mapped[str] = mapped_column(String(250))
    user_id: Mapped[str] = mapped_column(String(length=50), ForeignKey("user.id"))

    username: Mapped[List["Username"]] = relationship(
        secondary=search_usernames, back_populates="search_result"
    )
    user: Mapped["User"] = relationship(back_populates="search_result")

    def serialize(self):
        return {
            "id": self.id,
            "time_stamp": self.time_stamp,
            "description": self.description,
            "usernames": self.usernames.serialize(),
        }

    def __get_usernames_by_type(self, username_type: UsernameType):
        return [
            username.serialize()
            for username in self.usernames
            if username.type == username_type
        ]

    def get_seed_usernames(self):
        return self.__get_usernames_by_type(UsernameType.SEED)

    def get_found_usernames(self):
        return self.__get_usernames_by_type(UsernameType.FOUND)


class Username(db.Model):
    id = mapped_column(
        String(length=50), primary_key=True, default=lambda: uuid.uuid4().hex
    )
    username: Mapped[str] = mapped_column(
        String(length=100), nullable=False, unique=True
    )
    type: Mapped[str] = mapped_column(String(length=10), nullable=False)

    search_result: Mapped[List["SearchResult"]] = relationship(
        secondary=search_usernames, back_populates="username"
    )

    def serialize(self):
        return {
            "id": self.id,
            "username": self.username,
            "type": self.type,
        }
