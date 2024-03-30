import os
from decouple import Config
from sqlalchemy.orm import DeclarativeBase

config = Config(os.path.join(os.path.pardir, ".env"))

prod_env = config("PROD_ENV", default=False)


class Base(DeclarativeBase):
    pass
