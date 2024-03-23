from src.extensions import db
from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship


class SeedUsernames(db.Model):
    id = mapped_column(String(length=50), primary_key=True)
