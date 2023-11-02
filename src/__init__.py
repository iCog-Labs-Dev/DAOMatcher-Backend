import os
from dotenv import load_dotenv

load_dotenv()

prod_env = os.environ.get("PROD_ENV")
