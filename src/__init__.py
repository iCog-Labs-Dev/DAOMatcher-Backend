import os
from dotenv import load_dotenv

load_dotenv()

prod_env = bool(os.environ.get("PROD_ENV"))
