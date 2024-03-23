import os
from dotenv import load_dotenv
from sqlalchemy.orm import DeclarativeBase

load_dotenv()

prod_env = bool(os.environ.get("PROD_ENV"))


class Base(DeclarativeBase):
    pass
