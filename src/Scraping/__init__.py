import os

LIX_API_KEY = os.getenv("LIX_API_KEY")
LIX_BASE_URL = "https://api.lix-it.com/v1"
LINKEDIN_PAYLOAD = {}
LINKEDIN_HEADERS = {"Authorization": LIX_API_KEY}

# MASTEDON_BASE_URL = "https://{server}/api/v1/accounts"
MASTEDON_BASE_URL = "https://mastodon.social/api/v1/accounts"
