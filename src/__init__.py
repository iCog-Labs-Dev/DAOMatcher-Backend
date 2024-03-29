from sqlalchemy.orm import DeclarativeBase
from decouple import Config

config = Config()

prod_env = config("PROD_ENV", default=False)


class Base(DeclarativeBase):
    pass
