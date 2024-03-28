from enum import Enum as PEnum
from sqlalchemy import ForeignKey, Column, Enum
from src.extensions import db


class UsernameType(PEnum):
    SEED = "seed"
    FOUND = "found"


search_usernames = db.Table(
    "search_usernames",
    Column("search_id", ForeignKey("search_result.id"), primary_key=True),
    Column("username_id", ForeignKey("username.id"), primary_key=True),
    Column("type", Enum(UsernameType)),
)
