import os
from dotenv import load_dotenv

load_dotenv()

# Bot
BOT_TOKEN = os.environ.get("BOT_TOKEN")
API_ID = int(os.environ.get("API_ID"))
API_HASH = os.environ.get("API_HASH")

# Authorisation
AUTH = bool(os.environ.get("AUTH", False))
AUTH_USERS = set(int(x) for x in os.environ.get("AUTH_USERS", "").split())

# Database (MongoDB)
DATABASE_URL = os.environ.get("DATABASE_URL")
DATABASE_NAME = os.environ.get("DATABASE_NAME", "Gemini-Bot")
