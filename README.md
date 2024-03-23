# Gemini-Bot
A telegram gemini generative ai bot made with gemini api.

---

## Deploy

```sh
git clone https://github.com/FayasNoushad/Gemini-Bot.git
cd Gemini-Bot
python3 -m venv venv
. ./venv/bin/activate
pip3 install -r requirements.txt
# <Create Variables appropriately>
python3 main.py
```

---

## Variables

### Required

- `API_HASH` Your API Hash from my.telegram.org
- `API_ID` Your API ID from my.telegram.org
- `BOT_TOKEN` Your bot token from @BotFather
- `DATABASE_URL` From Mongo DB

### Not Required

- `DATABASE_NAME` Your database name
- `AUTH` Authorisation (True or False), default is false
- `AUTH_USERS` Authorised users IDs seperated by whitespace
---

## Credits

- [Google AI Studio](https://aistudio.google.com/)
- [Contributors](https://github.com/FayasNoushad/Gemini-Bot/graphs/contributors)
- [Pyrogram](https://github.com/pyrogram/pyrogram)

---
