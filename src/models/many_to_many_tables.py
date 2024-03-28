from sqlalchemy import ForeignKey, Column
from src.extensions import db
from src.models import SearchResult, Usernames

seed_usernames = db.Table(
    "seed_usernames",
    Column("search_id", ForeignKey(SearchResult.id)),
    Column("username_id", ForeignKey(Usernames.id)),
)

found_usernames = db.Table(
    "found_usernames",
    Column("search_id", ForeignKey(SearchResult.id)),
    Column("username_id", ForeignKey(Usernames.id)),
)
