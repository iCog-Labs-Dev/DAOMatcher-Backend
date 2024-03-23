from src.extensions import db
from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship


class UserSettings(db.Model):
    id = mapped_column(String(length=50), primary_key=True)
    default_user_count = mapped_column(Integer)
    default_depth_count = mapped_column(Integer)
    theme = mapped_column(String)

    user_id = mapped_column(String(length=50), ForeignKey("users.id"))
    user = relationship("User", backref="app_settings")
