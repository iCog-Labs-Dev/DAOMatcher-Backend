import os
from sqlalchemy.orm import DeclarativeBase
from decouple import Config

config = Config(os.path.join(os.path.pardir, ".env"))

prod_env = config("PROD_ENV", default=False)


class Base(DeclarativeBase):
    pass
