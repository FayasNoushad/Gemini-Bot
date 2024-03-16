from vars import *
from pyrogram import Client


Bot = Client(
    "Gemini-Bot",
    bot_token=BOT_TOKEN,
    api_id=API_ID,
    api_hash=API_HASH,
    plugins = dict(
        root="bot"
    )
)

Bot.run()
