import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.environ.get("BOT_TOKEN")
API_ID = int(os.environ.get("API_ID"))
API_HASH = os.environ.get("API_HASH")

AUTH = False
AUTH_USERS = set(int(x) for x in os.environ.get("AUTH_USERS", "").split())

# gemini api key from aistudio.google.com/app/apikey
GEMINI_API = os.environ.get("GEMINI_API", "")
