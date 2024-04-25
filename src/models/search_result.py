from __future__ import annotations

import uuid
from datetime import datetime
from enum import Enum as PEnum
from typing import TYPE_CHECKING, List
from sqlalchemy import ForeignKey, Column, Enum, Integer, String, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.extensions import db

if TYPE_CHECKING:
    from src.models.user import User


class UsernameType(PEnum):
    SEED = "seed"
    FOUND = "found"


class SocialMedia(PEnum):
    TWITTER = "twitter"
    MASTODON = "mastodon"
    LINKEDIN = "linkedin"


search_usernames = db.Table(
    "search_user_results",
    Column("search_id", ForeignKey("search_result.id"), primary_key=True),
    Column("user_result_id", ForeignKey("user_result.id"), primary_key=True),
    Column("type", Enum(UsernameType)),
)


class SearchResult(db.Model):
    id: Mapped[str] = mapped_column(
        String(length=50), primary_key=True, default=lambda: uuid.uuid4().hex
    )
    time_stamp: Mapped[DateTime] = mapped_column(DateTime, default=datetime.now())
    description: Mapped[str] = mapped_column(String(250))
    user_id: Mapped[str] = mapped_column(String(length=50), ForeignKey("user.id"))

    user_result: Mapped[List["UserResult"]] = relationship(
        secondary=search_usernames, back_populates="search_result"
    )
    user: Mapped["User"] = relationship(back_populates="search_result")

    def serialize(self):
        return {
            "id": self.id,
            "time_stamp": self.time_stamp,
            "description": self.description,
            "user_results": [item.serialize() for item in self.user_result],
        }

    def __get_user_results_by_type(self, username_type: UsernameType):
        return [
            user.serialize()
            for user in self.user_result
            if user.type == username_type.value
        ]

    def get_seed_usernames(self):
        return self.__get_usernames_by_type(UsernameType.SEED)

    def get_found_usernames(self):
        return self.__get_usernames_by_type(UsernameType.FOUND)


class UserResult(db.Model):
    id = mapped_column(
        String(length=50), primary_key=True, default=lambda: uuid.uuid4().hex
    )
    username: Mapped[str] = mapped_column(String(length=256), nullable=False)
    type: Mapped[str] = mapped_column(String(length=20), nullable=False)
    score: Mapped[int] = mapped_column(Integer)
    handle: Mapped[str] = mapped_column(String(length=256))
    social_media: Mapped[str] = mapped_column(String(length=256))
    image_url: Mapped[str] = mapped_column(String(length=256))

    search_result: Mapped[List["SearchResult"]] = relationship(
        secondary=search_usernames, back_populates="user_result"
    )

    def serialize(self):
        return {
            "id": self.id,
            "username": self.username,
            "type": self.ype,
            "score": self.score,
            "handle": self.handle,
            "social_media": self.social_media,
            "image_url": self.image_url,
        }
