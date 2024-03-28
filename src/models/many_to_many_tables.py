from enum import Enum as PEnum
from sqlalchemy import ForeignKey, Column, Enum
from src.extensions import db
from src.models import SearchResult, Usernames


class UsernameType(PEnum):
    SEED = "seed"
    FOUND = "found"


search_usernames = db.Table(
    "seed_usernames",
    Column("search_id", ForeignKey(SearchResult.id)),
    Column("username_id", ForeignKey(Usernames.id)),
    Column("type", Enum(UsernameType)),
)
