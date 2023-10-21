import os
from dotenv import load_dotenv

load_dotenv()

FRONTEND_URL = os.environ.get("FRONTEND_URL")
