import os

lix_api_key = os.getenv("LIX_API_KEY")
lix_base_url = "https://api.lix-it.com/v1"
linkedIn_payload={}

linkedIn_headers = {
  'Authorization': lix_api_key
}